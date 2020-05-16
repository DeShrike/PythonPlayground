from distutils.core import setup, Extension

module = Extension("myModule", sources = ["myModule.c"])
setup(name="PackageName",
      version="1.0",
      description="This is a package for MyModule",
      ext_modules = [module])



# to setup run:
# python3 setup.py build
# or
# python3 setup.py install

