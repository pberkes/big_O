from distutils.core import setup

setup(name='big_O',
      version='0.7',
      description='Empirical estimation of time complexity from execution time',
      author='Pietro Berkes',
      author_email='pietro.berkes@googlemail.com',
      url='https://github.com/pberkes/big_O',
      license='LICENSE.txt',
      long_description=open('README.rst').read(),
      packages=['big_o', 'big_o.test']
      )
