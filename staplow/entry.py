"""Staplow!

Usage:
  staplow init
  staplow add (input|output) <port>

Options:
  -h --help     Show this screen.
  --version     Show version.
  -i <interface>, --interface <interface> Specify interface
  -s <source>, --source <source>
  -d <destination>, --destination <destination>

"""
from docopt import docopt

def console():
    arguments = docopt(__doc__, version='Staplow 0.1')
    print(arguments)
