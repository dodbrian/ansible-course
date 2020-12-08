#!/usr/bin/env python

'''
Sample custom dynamic inventory script for Ansible, in Python
'''

import os
import sys
import argparse

try:
    import json
except ImportError:
    import simpleJson as json


class ExampleInventory(object):

    def __init__(self):
        self.inventory = {}
        self.read_cli_args()

        # Called with '--list'
        if self.args.list:
            self.inventory = self.example_inventory()

        # Called with '--host [hostname]'
        elif self.args.host:

            # Not implemented, since we return _meta info '--list'
            self.inventory = self.empty_inventory()

        # If no groups or vars are present, return an empty inventory
        else:
            self.inventory = self.empty_inventory()

        print(json.dumps(self.inventory))

    # Example inventory for testing
    def example_inventory(self):
        return {
            "group": {
                "hosts": [
                    "23.253.22.21",
                    "23.253.22.100",
                    "23.253.22.125",
                    "23.253.22.82"
                ],
                "vars": {
                    "example_variable": "value"
                }
            },
            "_meta": {
                "hostvars": {
                    "23.253.22.21": {
                        "host_specific_var": "web01"
                    },
                    "23.253.22.100": {
                        "host_specific_var": "web02"
                    },
                    "23.253.22.125": {
                        "host_specific_var": "db01"
                    },
                    "23.253.22.82": {
                        "host_specific_var": "db02"
                    }
                }
            }
        }

    # Empty inventory for testing
    def empty_inventory(self):
        return {'_meta': {'hostvars': {}}}

    # Read the command line args passed to the script
    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action='store_true')
        parser.add_argument('--host', action='store')
        self.args = parser.parse_args()


# Get the inventory
ExampleInventory()
