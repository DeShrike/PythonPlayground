def Params(oldFunc):
  def inside(*args, **kwargs):
    print("Params: ", args, kwargs)
    return oldFunc(*args, **kwargs)
  return inside

@Params
def Mult(x, y = 10):
  print(f"{x} x {y} = {x*y}")

Mult(4, 4)
Mult(7)
Mult(y = 3, x = 1)
