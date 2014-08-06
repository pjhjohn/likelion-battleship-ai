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

# RAISE SyntaxError OR return code
def static_analysis(pystr) :
	# Try removing comments
	try :
		pystr = remove_comments_from(pystr)
	except SyntaxError :
		raise
	match = re.search('def[ \t]+guess[ \t]*\([ \t]*record[ \t]*\)[ \t]*:.*\n', pystr)
	# Detect [def guess(record) :]
	if not bool(match) :
		raise SyntaxError('Function Not Defined : guess')
	# Detect Recursion on guess
	if bool(re.search('guess[ \t]*\(.*\)', pystr[match.end(0):])) :
		raise SyntaxError('Recursion Not Allowed : guess')
	# Detect Unexpected function call <- input
	unexpected_functions = ['input', 'raw_input']
	if bool(re.search('('+'|'.join(unexpected_functions)+')[ \t]*\(.*\)', pystr)) :
		raise SyntaxError('Input Functions Not Allowed')
	# return code
	begin, end = match.start(0), match.end(0)
	indent = '\t' if pystr[end:end+1]=='\t' else '    '
	code = pystr[:begin] + '@timeout_sec(3)\n' + pystr[begin:end] + indent + 'global THREAD_ACTIVE\n' + pystr[end:]
	code = re.sub(r'while', 'while THREAD_ACTIVE and', code)
	return code

if __name__ == '__main__' :
	with file('ai_1.py','r') as code :
		result = static_analysis(code.read())
		print '======================================='
		print result
		print '======================================='