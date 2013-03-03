from sh import iptables, iptables_save
import os
from collections import defaultdict, namedtuple
import glob
from pprint import pprint

interfaces = glob.glob("/sys/class/net/*")

class Chain(object):
    def __init__(self, name):
        self.name = name

class Chain(object):
    def __init__(self, name):
        self.name = name
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class Table(object):

    all_tables = None
    
    _Table = namedtuple("_Table", ('body', 'chains'))

    table_bodies = {}

    def __init__(self, name):
        self.name = name

        Table._find_table(name)

        self.exe = iptables.bake("-t", name)


    def create_chain(self, name):
        self.exe("-N", name)


    def list_chains(self):
        pass

    @staticmethod
    def _get_table_bodies():
        full = iptables_save()
        current_table = []
        table_chains = {}
        current_table_name = None
        for item in full:
            if item.startswith('#'): continue
            if item.strip() == "COMMIT":
                Table.table_bodies[current_table_name] = Table._Table(current_table, table_chains)
                table_chains = {}
                continue
            if item.startswith('*'):
                current_table_name = item[1:].strip()
                current_table = []
                continue

            current_table.append(item.strip())

            if item.startswith(':'):
                current_chain_name = item[1:item.find(' ')].strip()
                current_chain = Chain(current_chain_name)
                table_chains[current_chain_name] = current_chain
                continue

            current_chain.add_rule(item.strip())



    @staticmethod
    def _find_table(name):
        if not Table.all_tables:
            print "Refreshing list"
            Table.all_tables = [x[1:].strip() for x in iptables_save() if x.startswith('*')]
            Table._get_table_bodies()
            pprint(Table.table_bodies)
        else:
            print "Cached"
        if name in Table.all_tables:
            return name
        else:
            print Table.all_tables
            raise Exception("Table not found")
