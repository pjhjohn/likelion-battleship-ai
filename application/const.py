from application.lib.attrdict import attrdict_const

Key = attrdict_const(
	USER_ID = 'user_id',
	USER_LEVEL = 'user_level',
	EMAIL = 'email',
	PASSWORD = 'password',
	SCHOOL_ID = 'school_id',
	LEAGUE_ID = 'league_id',
	CODE = 'code',
	AI_MODULE = 'ai_module',
	FLEET_DEPLOYMENT = 'fleet_deployment',
	PLAYER = 'player',
	MEMBERS = 'members',
	RANKING = 'ranking',
	WINNER_ID = 'winner_id',
	TEST_ENEMY_TYPE = 'enemy_type',
	TEST_CODE = 'code_test',
	ENEMY_CODE = 'code_enemy',
	SINK = 'sink'
)
Col = attrdict_const(
	ID = 'ID',
	USER_LEVEL = 'user_level',
	UPLOADED_TIME = 'uploaded_time',
	FILE_NAME = 'file_name',
	SCHOOL_NAME = 'school_name',
	SCHOOL_ID = 'school_id',
	DEPLOYMENT = 'deployment',
)
Level = attrdict_const(
	SCHOOL_ADMIN = 2,
	GLOBAL_ADMIN = 3
)
Path = attrdict_const(
	Upload = attrdict_const(
		DIR = 'uploads',
		PREFIX = 'with_header_'
	),
	LOGS = 'application/static/logs',
	TEMP = 'tmp/',
	CODE_HEADER_FILE_NAME = 'tmp/code_header'
)