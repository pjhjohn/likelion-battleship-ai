import sys, threading

class TimeoutError(Exception): pass
def timeout_sec(time_in_sec) :
	def wrapper(func) :
		def core(*args, **kwargs) :
			class Timer(threading.Thread) :
				def __init__(self) :
					threading.Thread.__init__(self)
					self.result = None
					self.error  = None
				def run(self) :
					try    : self.result = func(*args, **kwargs)
					except : self.error = sys.exc_info()[0:2]
			timer = Timer()
			timer.start()
			timer.join(time_in_sec)
			if timer.isAlive() :
				raise TimeoutError(func.__name__)
			if timer.error :
				raise timer.error[0](timer.error[1])
			return timer.result
		return core
	return wrapper
