CC = hipcc
# Auto-detect GPU architecture, fallback to gfx942 if detection fails
GPU_ARCH ?= $(shell if command -v rocminfo >/dev/null 2>&1; then rocminfo 2>/dev/null | grep "Name:" | grep "gfx" | awk 'NR==1' | awk '{print $$2}'; else echo "gfx942"; fi)
# If GPU_ARCH is empty after detection, use default
ifeq ($(GPU_ARCH),)
GPU_ARCH = gfx942
endif

SRCS_ALL = $(shell echo *.cpp)

CFLAGS = -O3 -Wall -fPIC --offload-arch=$(GPU_ARCH) 
SRCS = $(SRCS_ALL)

INCLUDES = -I/. -I$(ROCM_PATH)/include/roctracer -I$(ROCM_PATH)/include/rocprofiler-sdk-roctx
LIBS = -L$(ROCM_PATH)/roctracer/lib -L$(ROCM_PATH)/lib -lroctracer64 -lroctx64 -lrocprofiler-sdk-roctx


OBJS = $(SRCS:.c=.o)
TARGET = libHIPcode.so

.PHONY: clean
    
all:    $(TARGET)
	@echo  Successfully compiled ${TARGET} library with GPU_ARCH=$(GPU_ARCH).

info:
	@echo "Detected GPU_ARCH: $(GPU_ARCH)"
	@echo "To override, use: make GPU_ARCH=<arch>"

$(TARGET): $(OBJS) 
	$(CC) $(CFLAGS) $(INCLUDES) $(LIBS) -shared -o $(TARGET) $(OBJS) 

.c.o:
	$(CC) $(CFLAGS) $(INCLUDES) -cpp $<  -o $@
clean:
	$(RM) *.o ${TARGET}
