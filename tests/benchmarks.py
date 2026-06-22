"""Benchmark suite for logarithmic neural networks."""

import torch
import torch.nn as nn
import torch.nn.functional as F
import time
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class StandardTransformer(nn.Module):
    """Standard transformer for comparison."""
    
    def __init__(self, vocab_size, d_model=128, n_heads=4, n_layers=2, num_classes=10):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
        encoder_layer = nn.TransformerEncoderLayer(d_model, n_heads, dim_feedforward=d_model*4, batch_first=True)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=n_layers)
        self.output = nn.Linear(d_model, num_classes)
    
    def forward(self, x):
        x = self.embedding(x)
        x = self.transformer(x)
        x = x.mean(dim=1)  # Global average pooling
        return self.output(x)


class SimpleMLP(nn.Module):
    """Simple MLP for comparison."""
    
    def __init__(self, input_size, hidden_size, num_classes):
        super().__init__()
        self.embedding = nn.Embedding(1000, input_size)
        self.layers = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, num_classes)
        )
    
    def forward(self, x):
        x = self.embedding(x).mean(dim=1)
        return self.layers(x)


def benchmark_training(model, dataloader, optimizer, criterion, n_epochs=5):
    """Benchmark training time and accuracy."""
    device = next(model.parameters()).device
    model.train()
    
    start_time = time.time()
    for epoch in range(n_epochs):
        total_loss = 0
        correct = 0
        total = 0
        
        for batch_idx, (data, target) in enumerate(dataloader):
            data, target = data.to(device), target.to(device)
            
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            _, predicted = output.max(1)
            correct += predicted.eq(target).sum().item()
            total += target.size(0)
            
            if batch_idx >= 10:  # Limit batches for speed
                break
        
        avg_loss = total_loss / min(batch_idx + 1, len(dataloader))
        accuracy = 100. * correct / total
        
    elapsed = time.time() - start_time
    
    return {
        'time': elapsed,
        'loss': avg_loss,
        'accuracy': accuracy,
        'epochs': n_epochs
    }


def benchmark_memory(model, input_shape):
    """Benchmark memory usage."""
    device = next(model.parameters()).device
    
    # Forward pass
    x = torch.randint(0, 1000, input_shape).to(device)
    output = model(x)
    
    # Count parameters
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    
    return {
        'total_params': total_params,
        'trainable_params': trainable_params
    }


def run_benchmarks():
    """Run all benchmarks."""
    print("=" * 70)
    print("LOGARITHMIC NEURAL NETWORKS: Benchmark Suite")
    print("=" * 70)
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}")
    
    # Create synthetic dataset
    vocab_size = 1000
    seq_len = 32
    n_samples = 1000
    num_classes = 10
    
    X = torch.randint(0, vocab_size, (n_samples, seq_len))
    y = torch.randint(0, num_classes, (n_samples,))
    dataset = torch.utils.data.TensorDataset(X, y)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True)
    
    results = {}
    
    # 1. Standard Transformer
    print("\n[1/4] Standard Transformer...")
    model_std = StandardTransformer(vocab_size).to(device)
    optimizer = torch.optim.Adam(model_std.parameters(), lr=0.001)
    criterion = nn.CrossEntropyLoss()
    results['standard'] = benchmark_training(model_std, dataloader, optimizer, criterion)
    results['standard'].update(benchmark_memory(model_std, (32, seq_len)))
    
    # 2. Log-Transformer
    print("[2/4] Log-Transformer...")
    try:
        from src.nn import LogTransformer
        class LogTransformerWrapper(nn.Module):
            def __init__(self, vocab_size, num_classes):
                super().__init__()
                self.model = LogTransformer(vocab_size, d_model=128, n_heads=4, n_layers=2, num_classes=num_classes)
            def forward(self, x):
                logits, _ = self.model(x)
                return logits.mean(dim=1)
        model_log = LogTransformerWrapper(vocab_size, num_classes).to(device)
        optimizer = torch.optim.Adam(model_log.parameters(), lr=0.001)
        results['log'] = benchmark_training(model_log, dataloader, optimizer, criterion)
        results['log'].update(benchmark_memory(model_log, (32, seq_len)))
    except Exception as e:
        print(f"  Log-Transformer failed: {e}")
        results['log'] = {'time': 0, 'loss': 0, 'accuracy': 0, 'total_params': 0}
    
    # 3. Simple MLP
    print("[3/4] Simple MLP...")
    model_mlp = SimpleMLP(seq_len, 256, num_classes).to(device)
    optimizer = torch.optim.Adam(model_mlp.parameters(), lr=0.001)
    results['mlp'] = benchmark_training(model_mlp, dataloader, optimizer, criterion)
    results['mlp'].update(benchmark_memory(model_mlp, (32, seq_len)))
    
    # 4. Log-Linear Layer (simple test)
    print("[4/4] Log-Linear Layer...")
    try:
        from src.nn import LogLinear
        model_loglinear = nn.Sequential(
            LogLinear(seq_len * vocab_size, 256),
            nn.ReLU(),
            nn.Linear(256, num_classes)
        ).to(device)
        optimizer = torch.optim.Adam(model_loglinear.parameters(), lr=0.001)
        results['loglinear'] = benchmark_training(model_loglinear, dataloader, optimizer, criterion)
        results['loglinear'].update(benchmark_memory(model_loglinear, (32, seq_len)))
    except Exception as e:
        print(f"  Log-Linear failed: {e}")
        results['loglinear'] = {'time': 0, 'loss': 0, 'accuracy': 0, 'total_params': 0}
    
    # Print results
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    
    print(f"\n{'Model':<20} {'Time (s)':<12} {'Loss':<10} {'Accuracy':<10} {'Params':<12}")
    print("-" * 64)
    
    for name, r in results.items():
        print(f"{name:<20} {r['time']:<12.2f} {r['loss']:<10.4f} {r['accuracy']:<10.2f} {r['total_params']:<12,}")
    
    # Calculate speedup
    if results['log']['time'] > 0 and results['standard']['time'] > 0:
        speedup = results['standard']['time'] / results['log']['time']
        print(f"\nLog-Transformer speedup: {speedup:.2f}x")
    
    return results


if __name__ == '__main__':
    results = run_benchmarks()
