import os, sys
import numpy as np
from hip_tools import HIP_tools

use_torch = False
if use_torch:  import torch


# Get the path to the hip code library
work_dir = os.getcwd()
hip_lib_path = f'{work_dir}/libHIPcode.so'

# Initialize the roctracer tools
hip_tools = HIP_tools( hip_lib_path,True )

if use_torch:
  if not torch.cuda.is_available():
    print('Warning GPU not found')
    device = torch.device('cpu')
  else:  
    print('Setting torch device cuda')
    device = torch.device('cuda')
else:
  # Set the device: Needed since nothing else initialize the device 
  print('Setting hip device 0')
  hip_tools.set_device(0)  

hip_tools.start_roctracer()
# Do some fun stuff
id_init = hip_tools.start_marker('init')

nx, ny = 1024, 1024
A = np.random.rand( nx, ny )
B = np.random.rand( nx, ny )


n_iterations = 20
for i in range(n_iterations):
  
  #Only profiling even number
  if(i%2 == 0):
    hip_tools.start_roctracer()
  
  id_iter = hip_tools.start_marker(f'iter_{i}')
  print( f'iteration: {i}')
  C = np.matmul(A, B)

  hip_tools.stop_marker(id_iter)

  if(i%2 == 0):
    hip_tools.stop_roctracer()

print('Finished successfully')
