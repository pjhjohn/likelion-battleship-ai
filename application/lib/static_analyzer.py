from application.const import *
import re

# Does static-analysis for written ai-code and return code & status
def remove_comments_from(pystr) :
	comment_type_of = { "'''" : 'single', '"""' : 'double', '#' : 'line' }
	comment_token = {
		'single' : { 'start' : "'''", 'stop' : "'''" },
		'double' : { 'start' : '"""', 'stop' : '"""' },
		'line'   : { 'start' : '#'  , 'stop' : '\n'  }
	}
	dieted_pystr = ''
	safe_exit, commenting, comment_type = False, False, None
	matcher = '(' + '|'.join([comment_token[key]['start'] for key in comment_token]) + ')'
	while True :
		if commenting :
			match = re.search(comment_token[comment_type]['stop'], pystr)
			if not bool(match) :
				safe_exit = False
				break
			commenting, comment_type = False, None
			pystr = pystr[match.end(0):]
		else :
			match = re.search(matcher, pystr)
			if not bool(match) :
				safe_exit = True
				break
			commenting = True
			begin, end = match.start(0), match.end(0)
			comment_type = comment_type_of[pystr[begin:end]]
			dieted_pystr += pystr[:begin]
			pystr = pystr[end:]
	if safe_exit :
		return dieted_pystr + pystr	
	else :
		raise SyntaxError('EOF while scanning triple-quoted string literal')

# {'code' : modified_code(pystr), 'errorcode' : error_code}
def static_analysis(pystr) :
	# Try removing comments
	try : 				 pystr = remove_comments_from(pystr)
	except SyntaxError : return {'code' : '', 'errorcode' : ErrorCode.TripleQuote }
	
	# Detect [def guess(record) :]
	match = re.search('def[ \t]+guess[ \t]*\([ \t]*record[ \t]*\)[ \t]*:.*\n', pystr)
	if not bool(match) : 
		return {'code' : '', 'errorcode' : ErrorCode.GuessNotDef }
		
	# Detect Recursion on guess
	if bool(re.search('[ \t]+guess[ \t]*\(.*\)', pystr[match.end(0):])) :
		return {'code' : '', 'errorcode' : ErrorCode.RecursionNA }

	# Detect Unexpected function call <- input
	unexpected_functions = ['input', 'raw_input']
	if bool(re.search('('+'|'.join(unexpected_functions)+')[ \t]*\(.*\)', pystr)) :
		return {'code' : '', 'errorcode' : ErrorCode.InputFuncNA }

	# return code
	begin, end, = match.start(0), match.end(0)
	code = pystr[:begin] + '@timeout_sec(4)\n' + pystr[begin:]#end] + '    global THREAD_ACTIVE\n' + pystr[end:]
	# code = re.sub(r'while', 'while THREAD_ACTIVE and', code)

	# return code
	return {'code' : code, 'errorcode' : ErrorCode.NotError }