import base

class module(base.ai) :
  def __init__(self, name) :
    super(module, self).__init__(name)

  def __repr__(self) :
    return super(module, self).__repr__() + '@1'

if __name__ == '__main__' :
  instance = module('test name')
  print instance
