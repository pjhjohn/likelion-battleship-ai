class ai(object) : 
  def __init__(self, team_name):
    self.team_name = team_name

  def __repr__(self) :
    return '[ai by : ' + self.team_name + ']'

  def arrangement(self) :
    pass

  def decision(self) :
    pass

if __name__ == '__main__' :
  print "Testing Main Module"
