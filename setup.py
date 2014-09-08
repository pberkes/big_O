from distutils.core import setup

with open('README.rst') as readme_file:
      long_description = readme_file.read()

setup(name='big_O',
      version='0.7',
      description='Empirical estimation of time complexity from execution time',
      author='Pietro Berkes',
      author_email='pietro.berkes@googlemail.com',
      url='https://github.com/pberkes/big_O',
      license='LICENSE.txt',
      long_description=long_description,
      packages=['big_o', 'big_o.test']
      )
