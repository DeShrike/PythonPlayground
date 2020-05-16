def AddTags(*tags):
  def decorator(oldFunc):
    def inside(*args, **kwargs):
      code = oldFunc(*args, **kwargs)
      for tag in reversed(tags):
        code = "<{0}>{1}</{0}>".format(tag, code)
      return code
    return inside
  return decorator

@AddTags("p","i","b")
def MyWebWelcome(name):
  return "Welcome " + name + " to my blog"

print(MyWebWelcome("Bob"))
