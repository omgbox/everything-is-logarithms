"""Log-space attention mechanism."""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math


class LogAttention(nn.Module):
    """
    Log-space attention mechanism.
    
    Standard: attention(Q, K, V) = softmax(QK^T / sqrt(d)) @ V
    Log-space: log(attention) = log_softmax(QK^T / sqrt(d)) + log(V)
    
    Key insight: softmax in log-space is log_softmax, which is just:
    log_softmax(x)_i = x_i - log(sum(exp(x_j)))
    """
    
    def __init__(self, d_model, n_heads, dropout=0.1):
        super().__init__()
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_k = d_model // n_heads
        
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
        
        self.dropout = nn.Dropout(dropout)
        self.scale = math.sqrt(self.d_k)
    
    def forward(self, x, mask=None):
        batch_size, seq_len, _ = x.size()
        
        # Linear projections
        Q = self.W_q(x).view(batch_size, seq_len, self.n_heads, self.d_k).transpose(1, 2)
        K = self.W_k(x).view(batch_size, seq_len, self.n_heads, self.d_k).transpose(1, 2)
        V = self.W_v(x).view(batch_size, seq_len, self.n_heads, self.d_k).transpose(1, 2)
        
        # Log-space attention scores
        # QK^T / sqrt(d) in log-space
        scores = torch.matmul(Q, K.transpose(-2, -1)) / self.scale
        
        # Apply mask if provided (set masked positions to -inf)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float('-inf'))
        
        # Log-space softmax: log_softmax(scores)
        # This is just: scores - log(sum(exp(scores)))
        log_probs = F.log_softmax(scores, dim=-1)
        
        # Apply dropout in log-space
        log_probs = self.dropout(log_probs)
        
        # Apply attention to values
        # In log-space: attention @ V = sum(log_probs * V)
        # But we need to handle this carefully
        # Standard: output = softmax(scores) @ V
        # Log-space: output = exp(log_softmax(scores)) @ V
        
        probs = torch.exp(log_probs)
        output = torch.matmul(probs, V)
        
        # Reshape and project
        output = output.transpose(1, 2).contiguous().view(batch_size, seq_len, self.d_model)
        output = self.W_o(output)
        
        return output, log_probs
