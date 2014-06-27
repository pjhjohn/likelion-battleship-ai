from os import path

def importAI(path) :
  modules = map(__import__, path)
  print modules

if __name__ == '__main__' :
  print "module leading test"
  importAI('../scripts/base/
