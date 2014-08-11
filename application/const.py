from application.lib.attrdict import attrdict_const

Key = attrdict_const(
	USER_ID 		= 'user_id',
	USER_LEVEL 		= 'user_level',
	EMAIL 			= 'email',
	PASSWORD 		= 'password',
	SCHOOL_ID 		= 'school_id',
	LEAGUE_ID 		= 'league_id',
	CODE 			= 'code',
	AI_MODULE 		= 'ai_module',
	FLEET_DEPLOYMENT= 'fleet_deployment',
	PLAYER 			= 'player',
	MEMBERS 		= 'members',
	RANKING 		= 'ranking',
	WINNER_ID 		= 'winner_id',
	ENEMY_TYPE 		= 'enemy_type',
	TEST_CODE 		= 'test_code',
	ENEMY_CODE 		= 'enemy_code',
	SINK 			= 'sink'
)
Col = attrdict_const(
	ID = 'ID',
	USER_LEVEL 		= 'user_level',
	UPLOADED_TIME 	= 'uploaded_time',
	FILE_NAME 		= 'file_name',
	SCHOOL_NAME 	= 'school_name',
	SCHOOL_ID 		= 'school_id',
	DEPLOYMENT 		= 'deployment',
)
Level = attrdict_const(
	SCHOOL_ADMIN 	= 2,
	GLOBAL_ADMIN 	= 3
)
Path = attrdict_const(
	Upload = attrdict_const(
		DIR 	= 'uploads',
		PREFIX 	= 'with_header_'
	),
	LOGS = 'application/static/logs',
	TEMP = 'tmp/',
	CODE_HEADER_FILE_NAME = 'tmp/code_header'
)
# Error Message Corresponds to its errorcode
ErrorCode = attrdict_const(
	NotError	 = 0,
	TripleQuote  = 1,
	GuessNotDef  = 2,
	RecursionNA	 = 3,
	InputFuncNA	 = 4,
	ImportNA_SYS = 5,
	ImportNA_OS  = 6,
	RuntimeError = 7,
	TimeoutError = 8,
	ImportError  = 9,
	CompileError = 10,
	Player1LostWithError = 11,
	Player2LostWithError = 12,
	SyntaxError  = 13
)
ErrorMsg = attrdict_const(
	CodeSubmit = [
		'Clean Exit',										# 0
		'EOF While scanning triple-quoted string literal',	# 1
		'Function Not Definded : guess',					# 2
		'Recursion Not Allowed : guess',					# 3
		'Input Functions Not Allowed',						# 4
		'Not Allowed Module : sys',							# 5
		'Not Allowed Module : os',							# 6
		'Runtime Error',									# 7
		'Timeout Error',									# 8
		'Import Error',										# 9	
		'Compile Error',									# 10	
		"Error from Your ( Player1's ) Code",				# 11
		"Error from Player2's Code",						# 12
		'Syntax Error',										# 13
		'Unexpected Error'									# 14
	]
)