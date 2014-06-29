import os, sys
script_path = os.path.abspath('../script')
sys.path.append(script_path)
scripts = os.listdir(script_path)
scripts.remove('base.py')
scripts.remove('gen.py')

for script in scripts :
  if script.endswith('.py') :
    print script[:-3]
#    exec('import '+script[:-3])
    ai = __import__(script[:-3], globals(), locals(), [], -1)
    print ai.module('Module@'+script)

'''
def my_import(name) :
  mod = __import__(name)
  components = name.split('.')
  for comp in components[1:] :
    mod = getattr(mod, comp)
  return mod
'''
