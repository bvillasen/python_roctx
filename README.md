# python_roctx

Example: Using roctx calls within a Python program


Step 1: Compile the hip_code library
```
module load rocm
make
```
This will create `libHIPcode.so` which is used in the python code downstream.


Step 2: Run the script to make sure it works

**Host example:**
```
python3 roctx_example.py
```

**PyTorch GPU example:**
```
python3 roctx_example_gpu.py
```

Step 3: Get the roctx trace using rocprof

**Host example:**
```
rocprofv3 --marker-trace --output-format pftrace -- python3 roctx_example.py
```

**PyTorch GPU example:**
```
rocprofv3 --kernel-trace --marker-trace --output-format pftrace -d ex1 -o ex1 -- python3 roctx_example_gpu.py
```

Step 4: Copy the **pftrace** file to your system and visualize in [Perfetto](https://ui.perfetto.dev/)
