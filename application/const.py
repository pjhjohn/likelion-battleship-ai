from application.lib.attrdict import attrdict_const

Key = attrdict_const(
	USER_ID = 'userid',
	USER_LEVEL = 'userlevel',
	EMAIL = 'email',
	PASSWORD = 'password',
	CODE = 'code',
	SCHOOL_ID = 'schoolid',
	LEAGUE_ID = 'leagueId',
	AI_MODULE = 'aiModule',
	SHIP_PLACEMENT = 'shipPlacement',
	PLAYER = 'player',
	MEMBERS = 'members',
	RANKING = 'ranking',
	WINNER_ID = 'winnerId',
	TEST_ENEMY_TYPE = 'enemy-type',
	TEST_CODE = 'code-test',
	ENEMY_CODE = 'code-enemy',
	SINK = 'sink'
)
Col = attrdict_const(
	ID = 'ID',
	USER_LEVEL = 'userLevel',
	UPLOADED_TIME = 'uploadedTime',
	FILE_NAME = 'file_name',
	SCHOOL_NAME = 'schoolName',
	SCHOOL_ID = 'schoolId',
	PLACEMENT = 'placement',
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
# TODO POTENTIAL MISMATCH BTW CONST AND DB VARIABLE