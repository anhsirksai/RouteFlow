import sys
import time
import argparse
#import unittest
import os
import pytest
import logging
import subprocess

#from utils import DumpToFile

#logging.basicConfig(
#    filename = 'RFtest.log',
#    level=logging.INFO,
#    format='%(asctime)s %(name)-15s %(levelname)-8s %(message)s',
#    datefmt='%b %d %H:%M:%S'
#    )

class Tests:
    CATALOGUE = {
                'ovs':'OVS',
                'containers':'Containers',
                'rfapps':'RFApps',
    }
    LOGLEVEL = {
               10 : 'DEBUG',
               20 : 'INFO',
               30 : 'WARNING',
               40 : 'ERROR',
               50 : 'CRITICAL',
    }

    def __init__(self):
        mongoport = 27017
        containers = ['rfvmA','rfvmB']
        self.testsToRun = {'ovs':True, 'containers':False, 'rfapps':True}
        self.testsParams = {'mongo':mongoport, 'containers':containers, 'rfapps':['rfproxy','rfserver']}
        self.outputFormat = {'txt':False, 'terminal':False}
        self.outputModes = {'json':False, 'raw':False}
        self.use_pytest = False


    #def setTestsToRun(self, *args, **kwargs):
    def setTestsToRun(self, *args):
        '''
        fill self.testsToRun with proper arguments
        like lxc, ovs, rfserver, rfproxy,.... true or false

        define if tests will use pytest or not (self.use_pytest = False)
        '''
        pass


    def configureTests(self, **kwargs):
        '''
        fill self.testsParams with arguments
        '''
        pass

    def setTestsOutput(self, *args, **kwargs):
        '''
        check if tests results must be saved
        in txt file or sent to terminal
        in json or raw formats
        (first let`s save in raw format)
        '''
        pass

    def setup(self,name,output_dir):
        '''
        takes self.testsToRun, self.outputFormat, self.outputModes
        and prepare environment to runtests
        ex: creates loggers, open files/terminal outputs.

        for loggers: define a self.logger and instatiate it to save in file or terminal
        In this case let`s not use open text files, instead let`s create a logger for each Test class
        according to self.testsToRun and outputFormat. you can create a function for that too
        And create a dict like CATALOGUE that will contain testsToRun:logger
        this dict will be used to call RF_tests
        example: https://aykutakin.wordpress.com/2013/08/06/logging-to-console-and-file-in-python/

        for testsToRun create a function that reads self.testsToRun and do the following:
            - look for test_ files in dir and subdir (ex: test_ovs) and load it importing
            its class (ex  from test_ovs import OVS - class name associated with ovs in CATALOGUE)
            - returns a dict (ex: self.setupTests) with teststorun:classes objects
            following self.testParams
        this dict will be used to be used in runTests function
        '''
        logger = setLoggers(name,output_dir)

    def setLoggers(name,output_dir):
        '''
        :name: used to print the class name in the get logger.
        :output_dir: directory to store logs
        '''
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        #INFO handler
        handler = logging.FileHandler(os.path.join(output_dir, "Output.log"),"w", encoding=None, delay="true")
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s %(name)-15s %(levelname)-8s %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        #ERROR handler
        handler = logging.FileHandler(os.path.join(output_dir, "Error.log"),"w", encoding=None, delay="true")
        handler.setLevel(logging.ERROR)
        formatter = logging.Formatter("%(asctime)s %(name)-15s %(levelname)-8s %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger

    def runTests(self):
        '''
        Two approaches here depending on self.use_pytest = True or False:
            - first call pytest.main() https://pytest.org/latest/usage.html
            ex: pytest.main("-qq", plugins=[MyPlugin()])
            I will explain you how to run using pytest! ASK ME

            Second run the tests by ourselves. How?
            Using dict returned by setup (ex: self.setupTests)
            call run_tests for each object
        '''
        # call setup with the name argument. This name will be used by logger.
        # The name is an itervalue from self.testsToRun dictionary. Pass each key as an argument, if the corresponding value is true.
        pass


class RFUnitTests(object):

    def __init__(self, logger):
        self.logger = logger
        self.tests = {}


    def evaluate(self, capfd):
        '''
        for each process in self.tests run it using capfd
        This function only execute the commands, get the output/err,
        return them as {command: {'out':output,'err':err} )
        '''
        pass

    def verify(self, tests_out):
        '''
        receives dict {command: {'out':output,'err':err} )
        run comparisons of responses (output/err) and
        expected_result of TESTS using command as key
        and looking for the method and expected_output
        if using method expected_output == output
        associate dict {command: {'assert':True, 'result':output}}
        else
        associate dict {command: {'assert':False, 'result':err}}
        returns dict with commands:assertions,results
        No need to write assertion
        '''
        pass

    def analyse(self, verify_out):
        '''
        receives dict of verify_processes
        check assertion values and write results to logger
        example:
        self.logger.info("OUTPUT\n %s", out)
        self.logger.info("ERROR\n %s", err)
        No need to write assertion
        '''
        pass


    def run_tests():
        '''
        just pass, the classes inheriting RFUnitTests will
        overwrite this function
        '''
        pass


class OVS(RFUnitTests):

    '''
    TESTS contain association of commands and a dict containing
    the method of evaluation of the command and the expected output
    '''
    TESTS = {
            'ovs-vsctl show | grep dp0':{'method':'find', 'output':'dp0'},
            'ovs-dpctl show | grep dp0':{'method':'find', 'output':'dp0'},
    }

    def __init__(self, logger):
        super().__init__(logger)


    def addTestsDefault(self):
        self.tests = TESTS

    def addTest(self, cmd, method, output):
        '''
        add in self.tests new tests following the TEST structure
        '''
        pass

    def setTestsParams(self, cmd, param):
        '''
        Define for example self.containernames, self.mongoport, self.controllerport
        for Container, Mongo, Controller classes respectively
        In this case modify cmd in self.tests
        '''
        pass

    def run_tests(self):
        '''
        basically runs methods inherited with self.tests attribute
        self.evaluate
        self.verify
        self.analyse
        '''
        pass


    def test_netwokvsctl(self, logger, capfd):
        logger.info('TestOVS Network ovs-vsctl')
        subprocess.call('ovs-vsctl show | grep dp0', shell = True)
        out,err = capfd.readouterr()
        logger.info("\n ==== TestOVS Network ovs-vsctl ==== \n ")
        logger.info("OUTPUT\n %s", out)
        logger.info("ERROR\n %s", err)
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
    #run pytest(y/n)
    parser.add_argument('-p', '--pytest', default=False, type = bool,
                        help='Run tests with pytest(True/False)')
    #accept a list of test modules to be run.
    parser.add_argument('-tc', '--testcases', choices =['ovs','rfapps','mongo','containers'],
                        help='Testcases to be run.choose form the list specified')

    #list of containers : either user gives his own container names(option:l) or chooses from the list(option:ln)
    parser.add_argument('-l', '--lxc', nargs='*',
                        help='Lxc container name, should be given to verify, default not supported, zero or more container names accepted')
    parser.add_argument('-ln', '--lxcnames', choices =['rfvm1','b1','b2','rfvmA','rfvmB'],
                        help='Lxc container name, should be given to verify, default not supported,to be choosen from the list')

    #accept the mongodb port. default 27017
    parser.add_argument('-m', '--mongoport', default=27017, type = int,
                        help='port number to verify running of mongodb')

    #accept controller ports. defaults specified.
    parser.add_argument('-c', '--controllerport1', default=6533, type = int,
                        help='rfproxy controller port1')

    parser.add_argument('-cc', '--controllerport2', default=6653, type = int,
                        help='rfproxy controller port2')

    args = parser.parse_args()
    testsobj = Tests()
    testsobj.setTestsToRun(args.pytest,args.testcases)
    testsobj.configureTests(mongo = args.mongoport, containers = args.lxcnames)
    testsobj.runTests()
