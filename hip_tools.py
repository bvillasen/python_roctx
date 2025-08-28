
encode = lambda s : s.encode('utf-8')

# Needed so that we do not call start when already corresponding id is started
roctx_ids_start = set()
roctx_ids_stop = set()

class HIP_tools:    
  
  """
  @param {string} hip_lib_path: path to compiled libHIPcode.so
  @param {bool} stop_on_it prevents starting of rocprof on initialization. Useful for profiling ML workloads

  """
  def __init__(self,  hip_lib_path, stop_on_init = True):


    from ctypes import cdll, c_int, c_char_p        
    print(f'Loading library: {hip_lib_path}')
    libhip = cdll.LoadLibrary( hip_lib_path )
    
    self._set_device = libhip.set_device
    self._set_device.argtypes = [ c_int ]
    self._set_device.resypes = c_int
    self._get_tid = libhip.get_roctx_tid
    self._start_roctracer = libhip.start_roctracer
    self._stop_roctracer = libhip.stop_roctracer
    self._roctxr_push = libhip.roctxr_push
    self._roctxr_pop = libhip.roctxr_pop    
    self._roctxr_push.argtypes = [c_char_p]
    self._roctxr_start = libhip.roctxr_start
    self._roctxr_stop  = libhip.roctxr_stop
    self._roctxr_start.argtypes = [ c_char_p ]
    self._roctxr_start.resypes = c_int 
    self._roctxr_stop.argtypes = [ c_int ]
    if stop_on_init:
        self.stop_roctracer()
  

  def set_device(self, device_id ):
    self._set_device(device_id)

  def start_roctracer(self):
    tid = self._get_tid()
    if(tid not in roctx_ids_start):
      self._start_roctracer()
      roctx_ids_start.add(tid)
      roctx_ids_stop.discard(tid)

  def stop_roctracer(self):
    tid = self._get_tid()
    if(tid not in roctx_ids_stop):
      self._stop_roctracer()
      roctx_ids_stop.add(tid)
      roctx_ids_start.discard(tid)
         

  def start_marker( self, marker_name ):
    marker_id = self._roctxr_start( encode(marker_name) )
    return marker_id
  
  def stop_marker( self, marker_id, sync_device=False, device=None ):
    # if sync_device: torch.cuda.synchronize(device=device)
    self._roctxr_stop( marker_id )
