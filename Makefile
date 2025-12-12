CC = hipcc
GPU_ARCH=gfx942

SRCS_ALL = $(shell echo *.cpp)

CFLAGS = -O3 -Wall -fPIC --offload-arch=$(GPU_ARCH) 
SRCS = $(SRCS_ALL)

INCLUDES = -I/. -I$(ROCM_PATH)/include/roctracer -I$(ROCM_PATH)/include/rocprofiler-sdk-roctx
LIBS = -L$(ROCM_PATH)/roctracer/lib -L$(ROCM_PATH)/lib -lroctracer64 -lroctx64 -lrocprofiler-sdk-roctx


OBJS = $(SRCS:.c=.o)
TARGET = libHIPcode.so

.PHONY: clean
    
all:    $(TARGET)
	@echo  Successfully compiled ${TARGET} library.

$(TARGET): $(OBJS) 
	$(CC) $(CFLAGS) $(INCLUDES) $(LIBS) -shared -o $(TARGET) $(OBJS) 

.c.o:
	$(CC) $(CFLAGS) $(INCLUDES) -cpp $<  -o $@
clean:
	$(RM) *.o ${TARGET}
