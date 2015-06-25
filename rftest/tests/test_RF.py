import sys
import time
import argparse
#import unittest
import os
import pytest
import logging
import subprocess

#from utils import DumpToFile

logging.basicConfig(
    filename = 'RFtest.log',
    level=logging.INFO,
    format='%(asctime)s %(name)-15s %(levelname)-8s %(message)s',
    datefmt='%b %d %H:%M:%S'
    )



class RF_Tests(object):

    def __init__(self, mongoPort, controllerOne, controllerTwo, lxc, testsToRun):
        logger = logging.getLogger('RFtest')
        self.logger.info("test case execution start")
        self.mongoPort  = mongoPort
        self.controllerOne = controllerOne
        self.controllerTwo = controllerTwo
        self.lxc = lxc
        self.testsToRun = testsToRun

    def create_parser(self):
        logger.info("create Parser base function")
        pass

    def run_tests():
        pass

    def verify_tests():
        pass


class TestOVS():

    logger = logging.getLogger('TestOVS')

    def test_netwokvsctl(self,capfd):
        self.logger.info('TestOVS Network ovs-vsctl')
        subprocess.call('ovs-vsctl show | grep dp0', shell = True)
        out,err = capfd.readouterr()
        with open("testout.txt","a") as txtfile:
             txtfile.write("\n ==== TestOVS Network ovs-vsctl ==== \n ")
             txtfile.write(out)
        with open("testerr.txt","a") as txtfile:
             txtfile.write("\n ==== TestOVS Network ovs-vsctl ==== \n ")
             txtfile.write(err)
        assert out.find("dp0") != -1

    def test_netwokdpctl(self,capfd):
        self.logger.info('TestOVS Network ovs-dpctl')
        subprocess.call('ovs-dpctl show | grep dp0', shell = True)
        out,err = capfd.readouterr()
        with open("testout.txt","a") as txtfile:
             txtfile.write("\n ==== TestOVS Network ovs-dpctl ==== \n ")
             txtfile.write(out)
        with open("testerr.txt","a") as txtfile:
             txtfile.write("\n ==== TestOVS Network ovs-dpctl ==== \n ")
             txtfile.write(err)
        assert out.find("dp0") != -1


    def test_processdbserver(self,capfd):
        self.logger.info('TestOVS Process ovsdb server')
        subprocess.call('ps aux | grep ovs', shell = True)
        out,err = capfd.readouterr()
        with open("testout.txt","a") as txtfile:
             txtfile.write("\n ==== TestOVS Process ovsdb server === \n ")
             txtfile.write(out)
        with open("testerr.txt","a") as txtfile:
             txtfile.write("\n ==== TestOVS Process ovsdb server === \n ")
             txtfile.write(err)
        assert out.find("ovsdb-server") != -1

    def test_processswitchd(self,capfd):
        self.logger.info('TestOVS Process ovs-vswitchd')
        subprocess.call('ps aux | grep ovs', shell = True)
        out,err = capfd.readouterr()
        with open("testout.txt","a") as txtfile:
             txtfile.write("\n ==== TestOVS Process ovs-vswitchd === \n ")
             txtfile.write(out)
        with open("testerr.txt","a") as txtfile:
             txtfile.write("\n ==== TestOVS Process ovs-vswitchd === \n ")
             txtfile.write(err)
        assert out.find("ovs-vswitchd") != -1

    def test_specific(self,capfd):
        self.logger.info('TestOVS Specific')
        #pass

    def run_tests():
        self.logger.info('TestOVS testcases start execution')
        #self.test_netwok()
        #self.test_process()
        #self.test_specific()

    def verify_tests():
        pass

class Testrfserver():

    logger = logging.getLogger('TestRFServer')

    def test_processrfserverrunning(self,capfd):
        self.logger.info('Test for process rfserver running')
        subprocess.call('ps aux| grep rfserver', shell = True)
        out,err = capfd.readouterr()
        str2 = 'python ./rfserver/rfserver/py'
        with open("testout.txt","a") as txtfile:
             txtfile.write("\n ==== Test for process rfserver running ==== \n ")
             txtfile.write(out)
        with open("testerr.txt","a") as txtfile:
             txtfile.write("\n ==== Test for process rfserver running ==== \n ")
             txtfile.write(err)
        assert out.find(str2) != -1

class Testrfproxy():

    logger = logging.getLogger('TestRFProxy')

    def test_processrfproxy(self,capfd):
        self.logger.info('Test for process rfproxy running')
        subprocess.call('ps aux| grep rfproxy', shell = True)
        out,err = capfd.readouterr()
        str2 = 'ryu-manager --use-stderr --ofp-tcp-listen-port=$CONTROLLER_PORT ryu-rfproxy/rfproxy.py'
        with open("testout.txt","a") as txtfile:
             txtfile.write("\n ==== Test for process rfproxy running ==== \n ")
             txtfile.write(out)
        with open("testerr.txt","a") as txtfile:
             txtfile.write("\n ==== Test for process rfproxy running ==== \n ")
             txtfile.write(err)
        assert out.find(str2) != -1


if __name__ == '__main__':
    description = 'RFTest suite, to run the tests and determine the state of system'
    epilog = 'Report bugs to: https://github.com/routeflow/RouteFlow/issues'

    #config = os.path.dirname(os.path.realpath(__file__)) + "/config.csv"
    #islconf = os.path.dirname(os.path.realpath(__file__)) + "/islconf.csv"

    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    parser.add_argument('-m', '--mongoport', default=27017, type = int,
                        help='port number to verify running of mongodb')
    parser.add_argument('-c', '--controllerport1', default=6533, type = int,
                        help='rfproxy controller port1')
    parser.add_argument('-cc', '--controllerport2', default=6653, type = int,
                        help='rfproxy controller port2')
    parser.add_argument('-l', '--lxcname', default='',
                        help='Lxc container name, should be given to verify, default not supported')

    args = parser.parse_args()
    tests = ['lxc','ovs']
    server = RF_Tests(args.mongoport, args.controllerport1, args.controllerport2, args.lxcname,tests)

