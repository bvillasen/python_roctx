import os, sys
import torch
from hip_tools import HIP_tools


# Get the path to the hip code library
work_dir = os.getcwd()
hip_lib_path = f'{work_dir}/libHIPcode.so'

# Initialize the roctracer tools
hip_tools = HIP_tools( hip_lib_path, True )

# Check if CUDA/ROCm is available
if not torch.cuda.is_available():
    print('Warning: GPU not found, using CPU')
    device = torch.device('cpu')
else:  
    print('Setting torch device cuda')
    device = torch.device('cuda')
    # Set the device: Needed since nothing else initialize the device 
    hip_tools.set_device(0)

hip_tools.start_roctracer()
# Do some fun stuff
id_init = hip_tools.start_marker('init')

nx, ny = 128, 128
A = torch.randn(nx, ny, device=device)
B = torch.randn(nx, ny, device=device)

hip_tools.stop_marker(id_init)

n_iterations = 5
for i in range(n_iterations):
  
  #Only profiling even number
  if(i%2 == 0):
    hip_tools.start_roctracer()
  
  id_iter = hip_tools.start_marker(f'iter_{i}')
  print(f'iteration: {i}')
  C = torch.matmul(A, B)
  
  # Synchronize to ensure GPU operation completes
  if device.type == 'cuda':
    torch.cuda.synchronize(device=device)
  
  hip_tools.stop_marker(id_iter)

  if(i%2 == 0):
    hip_tools.stop_roctracer()

print('Finished successfully')

