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
from sh import iptables


def console():
    args = docopt(__doc__, version='Staplow 0.1')

    if args['init']:
        init(args)
    if args['add']:
        add(args)
    

def init(args):
    iptables.bake("-t", "mangle")
    chains_to_add = ("staplow_in", "staplow_out")
    for chains in chains_to_add:
        iptables("-N", chains)


def add(args):
    pass
