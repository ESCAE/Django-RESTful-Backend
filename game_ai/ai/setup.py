from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize('tests.pyx')
)

'genetic.pyx', 'tic_tack.pyx', 'test_nerual_network.pyx', 'tests.pyx'