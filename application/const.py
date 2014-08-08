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
	RuntimeError = 5,
	TimeoutError = 6,
	ImportError  = 7,
	CompileError = 8,
	Player1LostWithError = 9,
	Player2LostWithError = 10,
	SyntaxError  = 11	
)
ErrorMsg = attrdict_const(
	CodeSubmit = [
		'Clean Exit',										# 0
		'EOF While scanning triple-quoted string literal',	# 1
		'Function Not Definded : guess',					# 2
		'Recursion Not Allowed : guess',					# 3
		'Input Functions Not Allowed',						# 4
		'Runtime Error',									# 5
		'Timeout Error',									# 6
		'Import Error',										# 7	
		'Compile Error',									# 8	
		"Error from Your ( Player1's ) Code",				# 9
		"Error from Player2's Code",						# 10
		'Syntax Error',										# 11
		'Unexpected Error'									# 12
	]
)