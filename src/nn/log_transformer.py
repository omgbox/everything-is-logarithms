"""Log-space Transformer architecture."""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math
from .log_attention import LogAttention
from .log_activation import LogLayerNorm, LogReLU


class LogTransformerBlock(nn.Module):
    """A single transformer block in log-space."""
    
    def __init__(self, d_model, n_heads, d_ff, dropout=0.1):
        super().__init__()
        
        # Log-space multi-head attention
        self.attention = LogAttention(d_model, n_heads, dropout)
        
        # Log-space feed-forward network
        self.ff_network = nn.Sequential(
            nn.Linear(d_model, d_ff),
            LogReLU(),
            nn.Linear(d_ff, d_model)
        )
        
        # Log-space layer normalization
        self.norm1 = LogLayerNorm(d_model)
        self.norm2 = LogLayerNorm(d_model)
        
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x, mask=None):
        # Self-attention with residual connection
        attn_output, log_probs = self.attention(x, mask)
        x = self.norm1(x + self.dropout(attn_output))
        
        # Feed-forward with residual connection
        ff_output = self.ff_network(x)
        x = self.norm2(x + self.dropout(ff_output))
        
        return x, log_probs


class LogTransformer(nn.Module):
    """
    Log-space Transformer architecture.
    
    This transformer operates in log-space, where:
    - Attention uses log_softmax
    - Layer normalization is additive (not multiplicative)
    - Residual connections are additive in log-space
    
    Key insight: In log-space, the chain rule becomes additive,
    making backpropagation linear.
    """
    
    def __init__(
        self,
        vocab_size,
        d_model=512,
        n_heads=8,
        n_layers=6,
        d_ff=2048,
        max_seq_len=512,
        dropout=0.1,
        num_classes=None
    ):
        super().__init__()
        
        self.d_model = d_model
        self.n_heads = n_heads
        
        # Token embedding (log-space)
        self.embedding = nn.Embedding(vocab_size, d_model)
        
        # Positional encoding (learnable)
        self.pos_encoding = nn.Embedding(max_seq_len, d_model)
        
        # Transformer blocks
        self.blocks = nn.ModuleList([
            LogTransformerBlock(d_model, n_heads, d_ff, dropout)
            for _ in range(n_layers)
        ])
        
        # Final layer norm
        self.final_norm = LogLayerNorm(d_model)
        
        # Output projection
        if num_classes is not None:
            self.output = nn.Linear(d_model, num_classes)
        else:
            self.output = nn.Linear(d_model, vocab_size)
        
        self.dropout = nn.Dropout(dropout)
        self.scale = math.sqrt(d_model)
    
    def forward(self, x, mask=None):
        batch_size, seq_len = x.size()
        
        # Token embeddings
        embeds = self.embedding(x) * self.scale
        
        # Add positional encoding
        positions = torch.arange(seq_len, device=x.device).unsqueeze(0).expand(batch_size, -1)
        pos_embeds = self.pos_encoding(positions)
        
        # Combine embeddings (additive in log-space)
        x = embeds + pos_embeds
        x = self.dropout(x)
        
        # Apply transformer blocks
        all_log_probs = []
        for block in self.blocks:
            x, log_probs = block(x, mask)
            all_log_probs.append(log_probs)
        
        # Final normalization
        x = self.final_norm(x)
        
        # Output projection
        logits = self.output(x)
        
        return logits, all_log_probs
    
    def generate(self, x, max_len, temperature=1.0):
        """Generate text autoregressively."""
        self.eval()
        with torch.no_grad():
            for _ in range(max_len):
                logits, _ = self.forward(x)
                next_token_logits = logits[:, -1, :] / temperature
                probs = F.softmax(next_token_logits, dim=-1)
                next_token = torch.multinomial(probs, num_samples=1)
                x = torch.cat([x, next_token], dim=1)
        return x
