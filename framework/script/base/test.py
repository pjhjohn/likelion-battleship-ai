from base_ai_1 import Base_AI_Module1

base = Base_AI_Module1()
base.foo()

module = map(__import__, base_ai_1)
print module
