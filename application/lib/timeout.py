import sys, threading

class TimeoutError(Exception): pass
def timeout_sec(time_in_sec) :
	def wrapper(func) :
		def core(*args, **kwargs) :
			class Timer(threading.Thread) :
				def __init__(self) :
					threading.Thread.__init__(self)
					self.result = None
					self.error = None
					global THREAD_ACTIVE
					THREAD_ACTIVE = False

				def run(self) :
					try :
						global THREAD_ACTIVE
						THREAD_ACTIVE = True
						self.result = func(*args, **kwargs)
					except :
						self.error = sys.exc_info()[0]
			timer = Timer()
			timer.start()
			timer.join(time_in_sec)
			if timer.isAlive() :
				global THREAD_ACTIVE
				THREAD_ACTIVE = False
				raise TimeoutError
			if timer.error :
				raise timer.error
			return timer.result
		return core
	return wrapper