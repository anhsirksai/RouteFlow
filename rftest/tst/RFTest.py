import sys
import logging
import time
import argparse
import unittest
import os

from execanddump import DumpToFile

class RFTest(unittest.TestCase):

    """
    defnition to check status of openVswitch process.
    :test_OVS_Status: calls the function execute and passes 
        1. command
        2. path
        3. log file name
        4. log file type
    """
    def test_OVS_Status(self):
        ins = DumpToFile()
        ins.execute(['ps', 'aux', '|', 'grep', 'ovs'], os.getcwd() , "ovsStatus","txt")
        ins.execute(['ps', 'aux'], os.getcwd() , "allStatus", "txt")


# def execute(self,command,filepath,filename):
