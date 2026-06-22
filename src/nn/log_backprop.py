"""Log-space backpropagation utilities."""

import torch
import torch.nn as nn


class LogSpaceOptimizer:
    """
    Optimizer that works in log-space.
    
    In standard space: w_{t+1} = w_t - eta * grad
    In log-space: log(w_{t+1}) = log(w_t) - eta * log_grad
    
    Key insight: The gradient in log-space is additive, not multiplicative.
    """
    
    def __init__(self, model, lr=0.001, betas=(0.9, 0.999), eps=1e-8):
        self.model = model
        self.lr = lr
        self.beta1, self.beta2 = betas
        self.eps = eps
        
        # Store log-parameters
        self.log_params = {}
        self.m = {}  # First moment
        self.v = {}  # Second moment
        self.t = 0
        
        # Initialize log-parameters
        for name, param in model.named_parameters():
            if param.requires_grad:
                self.log_params[name] = torch.log(param.abs() + self.eps)
                self.m[name] = torch.zeros_like(param)
                self.v[name] = torch.zeros_like(param)
    
    def step(self):
        """Perform a single optimization step in log-space."""
        self.t += 1
        
        for name, param in self.model.named_parameters():
            if param.requires_grad and param.grad is not None:
                grad = param.grad
                
                # Convert gradient to log-space
                log_grad = torch.log(grad.abs() + self.eps) * grad.sign()
                
                # Update moments
                self.m[name] = self.beta1 * self.m[name] + (1 - self.beta1) * log_grad
                self.v[name] = self.beta2 * self.v[name] + (1 - self.beta2) * log_grad ** 2
                
                # Bias correction
                m_hat = self.m[name] / (1 - self.beta1 ** self.t)
                v_hat = self.v[name] / (1 - self.beta2 ** self.t)
                
                # Update in log-space: log(w) = log(w) - lr * m_hat / (sqrt(v_hat) + eps)
                self.log_params[name] = self.log_params[name] - self.lr * m_hat / (torch.sqrt(v_hat) + self.eps)
                
                # Convert back to standard space
                param.data = torch.exp(self.log_params[name]) * param.sign()
    
    def zero_grad(self):
        """Zero all gradients."""
        self.model.zero_grad()


class LogSpaceLoss:
    """
    Loss function designed for log-space training.
    
    Standard cross-entropy: H(p, q) = -sum p(x) * log(q(x))
    Log-space: This IS the natural loss function
    """
    
    def __init__(self, reduction='mean'):
        self.reduction = reduction
    
    def __call__(self, logits, targets):
        """
        Compute cross-entropy loss.
        
        In log-space, this is:
        loss = -sum targets * logits
        where logits are already in log-space (log_softmax)
        """
        # If logits are not in log-space, apply log_softmax
        if logits.min() > -10:  # Heuristic to detect non-log-space
            log_probs = torch.log_softmax(logits, dim=-1)
        else:
            log_probs = logits
        
        # Cross-entropy in log-space
        loss = -torch.sum(targets * log_probs, dim=-1)
        
        if self.reduction == 'mean':
            return loss.mean()
        elif self.reduction == 'sum':
            return loss.sum()
        else:
            return loss
