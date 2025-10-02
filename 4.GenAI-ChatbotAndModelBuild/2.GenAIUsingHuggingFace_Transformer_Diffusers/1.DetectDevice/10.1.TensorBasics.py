

import torch

x = torch.tensor([[1., 2.], [3., 4.]])
print(x.shape)
print(x.dtype)
print(x.device)
# operations
y = x * 2 + 1

x = torch.tensor([2.0], requires_grad=True)
y = x**2 + 3*x
z = y.sum()
z.backward()
print(x.grad) # dy/dx = 2*x + 3 -> at x=2 -> 7