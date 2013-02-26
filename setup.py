import os
import re
import shutil
import sys

from setuptools import setup
setup_params = {
    'entry_points': {
        'console_scripts': [
            'staplow=staplow.entry:console',
        ],
    },
    'zip_safe': False,
}

here = os.path.dirname(os.path.abspath(__file__))



# Hack to prevent stupid TypeError: 'NoneType' object is not callable error on
# exit of python setup.py test # in multiprocessing/util.py _exit_function when
# running python setup.py test (see
# http://www.eby-sarna.com/pipermail/peak/2010-May/003357.html)
try:
    import multiprocessing
except ImportError:
    pass

setup(
    name='staplow',
    # If you change the version here, change it in virtualenv.py and
    # docs/conf.py as well
    version=0.1,
    description="",
    long_description="",
    author='Corry Haines',
    author_email='tabletcorry@gmail.com',
    license='MIT',
    packages=['staplow'],
    **setup_params)
