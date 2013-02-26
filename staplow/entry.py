"""Staplow!

Usage:
  staplow init [options]
  staplow add (input|output) <port> [options]
  staplow delete [options]
  staplow flush [options]

Options:
  -h --help     Show this screen.
  --version     Show version.
  -i <interface>, --interface <interface> Specify interface.
  -s <source>, --source <source>
  -d <destination>, --destination <destination>
  -f <conf>, --config <conf> [default: conf.yml]

"""
from docopt import docopt
from sh import iptables
from operator import eq
iptables.bake("-t" "mangle")

interfaces = ["eth0",
              "eth1"]

def console():
    args = docopt(__doc__, version='Staplow 0.1')

    print args
    global interfaces
    if args['--interface']:
        interfaces = filter(lambda x: x == args['--interface'], interfaces)
        print interfaces
    if args['init']:
        init(args)
    if args['add']:
        add(args)
    if args['flush']:
        flush(args)
    if args['delete']:
        delete(args)

def init(args):
    for interface in interfaces:
        print iptables("-N", "{0}_{1}_{2}".format("staplow", "in", interface))
        print iptables("-N", "{0}_{1}_{2}".format("staplow", "out", interface))


def delete(args):
    for interface in interfaces:
        iptables("-D", "INPUT", "-i", interface, "-j", "{0}_{1}_{2}".format("staplow", "in", interface))
        iptables("-D", "OUTPUT", "-o", interface, "-j", "{0}_{1}_{2}".format("staplow", "out", interface))


def flush(args):
    for interface in interfaces:
        iptables("-F", "{0}_{1}_{2}".format("staplow", "in", interface))
        iptables("-F", "{0}_{1}_{2}".format("staplow", "out", interface))


def add(args):

    pass
