# python_roctx

Example: Using roctx calls within a Python program


Step 1: Compile the hip_code library
```
module load rocm
make
```
This will create `libHIPcode.so` which is used in the python code downstream.


Step 2: Run the script to make sure it works
```
python3 roctx_example.py
```

Step 3: Get the roctx trace using rocprof
```
 rocprofv3 --marker-trace --output-format pftrace -- python roctx_example.py
```

Step 4: Copy the **pftrace** file to your system and visualize in [Perfetto](https://ui.perfetto.dev/)