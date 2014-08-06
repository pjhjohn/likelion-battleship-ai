from flask import Flask
import os, sys

# Create Flask Instance (application)
app = Flask('application')

# Import Every function in 'controllers' directory
for base, dirs, names in os.walk(os.path.join('application', 'controllers')):
	for name in filter(lambda s: s.endswith('.py') and s != '__init__.py', names) :
		exec('from application.controllers.' + name[:-3] + ' import *')

# Add application to sys.path
sys.path.append('.')

# Import application config (setting)
import config