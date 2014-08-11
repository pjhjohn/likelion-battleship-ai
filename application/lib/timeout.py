import sys, threading, traceback

class TimeoutError(Exception): pass
def timeout_sec(time_in_sec) :
	def wrapper(func) :
		def core(*args, **kwargs) :
			class Timer(threading.Thread) :
				def __init__(self) :
					threading.Thread.__init__(self)
					self.result = None
					self.error  = None
					self.trace  = None
				def run(self) :
					try    :						
						self.result = func(*args, **kwargs)
						# BAD BAD BUT NECESSARY
						self.result = tuple([int(x) for x in self.result])
						# BAD BAD BUT NECESSARY
					except : 
						self.trace  = traceback.format_exc()
						self.error  = sys.exc_info()
			timer = Timer()
			timer.start()
			timer.join(time_in_sec)
			if timer.isAlive() :
				raise TimeoutError({'msg' : func.__name__, 'traceback' : 'Timeout (Potential Intinite loop)'})
			if timer.error :
				raise timer.error[0]({'msg' : timer.error[1], 'traceback' : timer.trace })
			return timer.result
		return core
	return wrapper
