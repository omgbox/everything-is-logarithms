"""Log-space linear layer."""

import torch
import torch.nn as nn


class LogLinear(nn.Module):
    """
    Log-space linear layer.
    
    Standard: y = Wx + b
    Log-space: log(y) = log(W) + log(x) + log(b)
    
    In practice: y = W @ x + b, but weights are stored in log-space.
    """
    
    def __init__(self, in_features, out_features, bias=True):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        
        # Store weights in log-space
        self.log_weight = nn.Parameter(torch.randn(out_features, in_features) * 0.01)
        
        if bias:
            self.log_bias = nn.Parameter(torch.zeros(out_features))
        else:
            self.register_parameter('log_bias', None)
    
    def forward(self, x):
        # Convert input to log-space if not already
        if x.min() <= 0:
            x_log = torch.log(x + 1e-6)
        else:
            x_log = torch.log(x)
        
        # Log-space linear: log(W @ x) = log(W) + log(x)
        # But we need to handle the matrix multiplication properly
        # So we do: W @ x = exp(log(W)) @ exp(log(x)) = exp(log(W) + log(x))
        
        weight = torch.exp(self.log_weight)
        output = torch.matmul(x_log, weight.t())
        
        if self.log_bias is not None:
            output = output + self.log_bias
        
        return output
    
    def extra_repr(self):
        return f'in_features={self.in_features}, out_features={self.out_features}, bias={self.log_bias is not None}'
