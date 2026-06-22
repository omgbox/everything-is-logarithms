"""Log-space activation functions."""

import torch
import torch.nn as nn
import torch.nn.functional as F


class LogReLU(nn.Module):
    """
    Log-space ReLU activation.
    
    Standard: relu(x) = max(0, x)
    Log-space: log(relu(exp(x))) = max(-inf, x) = x for x > 0, -inf for x <= 0
    """
    
    def __init__(self, eps=1e-6):
        super().__init__()
        self.eps = eps
    
    def forward(self, x):
        # In log-space, ReLU becomes: keep positive, mask negative
        return torch.where(x > 0, x, torch.tensor(float('-inf'), device=x.device))


class LogSoftmax(nn.Module):
    """
    Log-space softmax.
    
    Standard: softmax(x)_i = exp(x_i) / sum(exp(x_j))
    Log-space: log(softmax(x))_i = x_i - log(sum(exp(x_j)))
    """
    
    def __init__(self, dim=-1):
        super().__init__()
        self.dim = dim
    
    def forward(self, x):
        # Log-sum-exp trick for numerical stability
        x_max = torch.max(x, dim=self.dim, keepdim=True).values
        log_sum_exp = torch.log(torch.sum(torch.exp(x - x_max), dim=self.dim, keepdim=True)) + x_max
        return x - log_sum_exp


class LogLayerNorm(nn.Module):
    """
    Log-space layer normalization.
    
    Standard: layernorm(x) = (x - mean(x)) / std(x)
    Log-space: log(layernorm(exp(x))) = log(x) - log(mean(exp(x)))
    """
    
    def __init__(self, normalized_shape, eps=1e-5, elementwise_affine=True):
        super().__init__()
        self.eps = eps
        if elementwise_affine:
            self.weight = nn.Parameter(torch.ones(normalized_shape))
            self.bias = nn.Parameter(torch.zeros(normalized_shape))
        else:
            self.weight = None
            self.bias = None
    
    def forward(self, x):
        # Compute in log-space
        # mean(exp(x)) approx exp(mean(x)) for small variance
        x_exp = torch.exp(x)
        mean_exp = torch.mean(x_exp, dim=-1, keepdim=True)
        log_mean = torch.log(mean_exp + self.eps)
        
        # Normalize: x - log(mean(exp(x)))
        x_norm = x - log_mean
        
        # Apply affine transformation if present
        if self.weight is not None:
            x_norm = x_norm * self.weight + self.bias
        
        return x_norm
