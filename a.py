#-*- coding:utf-8 -*-
print "\n".join(["a"%(a,) for a in range(2,10)])

print "\n".join(["%d * %d = %d"%(a,b,a*b) for a in range(2,10) for b in range(1,10)])