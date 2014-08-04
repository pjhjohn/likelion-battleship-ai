from application import app

# Application Config
app.config.update(dict(
    DEBUG = True,
    SECRET_KEY = 'development key',
    SALT = 'afew25fg'
))
