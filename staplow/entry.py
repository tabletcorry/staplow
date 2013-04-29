"""Staplow!

Usage:
  staplow init [options]
  staplow add (input|output) <port> [options]
  staplow delete [options]
  staplow flush [options]
  staplow add [options]

Options:
  -h --help     Show this screen.
  --version     Show version.
  -i <interface>, --interface <interface> Specify interface.
  -s <source>, --source <source>
  -d <destination>, --destination <destination>
  -f <conf>, --config <conf> [default: conf.yml]

"""
from docopt import docopt
from iptables import Table
from sh import iptables
from operator import eq
import os
from glob import glob

interfaces = glob("/sys/class/net/*")
interfaces = map(os.path.basename, interfaces)

ipt_mangle = iptables.bake("-t", "mangle")

def console():
    args = docopt(__doc__, version='Staplow 0.1')

    print args
    global interfaces
    if args['--interface']:
        interfaces = filter(lambda x: x == args['--interface'], interfaces)
    if args['init']:
        init(args)
    if args['add']:
        add(args)
    if args['flush']:
        flush(args)
    if args['delete']:
        delete(args)

def init(args):
    mangle = Table("mangle")
    for interface in interfaces:
        mangle.create_chain("{0}_{1}_{2}".format("staplow", "in", interface))
        mangle.create_chain("{0}_{1}_{2}".format("staplow", "out", interface))

        ipt_mangle("-N", "{0}_{1}_{2}".format("staplow", "in", interface))
        ipt_mangle("-N", "{0}_{1}_{2}".format("staplow", "out", interface))
        ipt_mangle("-A", "INPUT", "-i", interface, "-j", "{0}_{1}_{2}".format("staplow", "in", interface))
        ipt_mangle("-A", "OUTPUT", "-o", interface, "-j", "{0}_{1}_{2}".format("staplow", "out", interface))



def delete(args):
    for interface in interfaces:
        ipt_mangle("-D", "INPUT", "-i", interface, "-j", "{0}_{1}_{2}".format("staplow", "in", interface))
        ipt_mangle("-D", "OUTPUT", "-o", interface, "-j", "{0}_{1}_{2}".format("staplow", "out", interface))
        ipt_mangle("-X", "{0}_{1}_{2}".format("staplow", "in", interface))
        ipt_mangle("-X", "{0}_{1}_{2}".format("staplow", "out", interface))


def flush(args):
    for interface in interfaces:
        ipt_mangle("-F", "{0}_{1}_{2}".format("staplow", "in", interface))
        ipt_mangle("-F", "{0}_{1}_{2}".format("staplow", "out", interface))


def add(args):
    for interface in interfaces:
        ipt_mangle("-A", "{0}_{1}_{2}".format("staplow", "in", interface), "-p", "tcp", "-m", "comment", "--comment", "tcp")
        ipt_mangle("-A", "{0}_{1}_{2}".format("staplow", "out", interface), "-p", "tcp", "-m", "comment", "--comment", "tcp")
