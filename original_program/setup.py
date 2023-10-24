from distutils.core import setup, Extension


setup(name = 'CSBICalcModule', version = '1.0.0',
   ext_modules = [Extension('CSBICalcModule', ['CSBICalculationModule.cpp'],
                            extra_compile_args=['-fopenmp'],
                            extra_link_args=['-lgomp'])])
#setup(name = 'CSBICalcModule', version = '1.0.0', 
#   ext_modules = [Extension('CSBICalcModule', ['CSBICalculationModule.cpp'])])