from flask import Flask
import os
from glob import glob


# Create Flask Instance (application)
app = Flask('application')



# Import Every function in 'controllers' directory
for base, dirs, names in os.walk(os.path.join('application', 'controllers')):
	for name in filter(lambda s: s.endswith('.py') and s != '__init__.py', names) :
		exec('from application.controllers.' + name[:-3] + ' import *')

# Import application config (setting)
import config