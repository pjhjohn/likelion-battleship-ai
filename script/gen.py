with open('module_no1.py') as a :
  script = a.read()
  frag = script.split('@')
  for n in range(2, 51) :
    writer = open('module_no'+str(n)+'.py', 'w')
    writer.write(frag[0] + '@' + str(n) + "'")
    writer.close()
  if not a.closed :
    a.close()
