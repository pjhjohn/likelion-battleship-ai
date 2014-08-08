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
	NotError	= 0,
	TripleQuote = 1,
	GuessNotDef = 2,
	RecursionNA	= 3,
	InputFuncNA	= 4,
	Runtime 	= 5,
	Timeout 	= 6,
	Compile		= 7
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
		'Compile Error'										# 7	
	]
)