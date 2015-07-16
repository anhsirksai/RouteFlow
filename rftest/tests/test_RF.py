import sys
import time
import argparse
#import unittest
import os
import pytest
import logging
import subprocess
import json
import fnmatch

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
        self.testsToRun = {'ovs':True, 'containers':False, 'rfapps':True}
        self.testsParams = {'mongo':27017, 'containers':['rfvmA','rfvmB'], 'rfapp':['rfproxy','rfserver']}

        #This can be a single dictionary. txt terminal json and raw.
        self.outputFormat = {'txt':False, 'terminal':False}
        self.outputModes = {'json':False, 'raw':False}
        self.use_pytest = False


    #def setTestsToRun(self, *args, **kwargs):
    def setTestsToRun(self, isPytest,**kwargs):
        '''
        fill self.testsToRun with proper arguments
        like lxc, ovs, rfserver, rfproxy,.... true or false

        define if tests will use pytest or not (self.use_pytest = False)
        '''
        self.use_pytest = isPytest

        #If kwargs is empty leave the testsToRun dictionary with default arguments.
        if kwargs:
            self.testsToRun.clear()
            for key,tests  in kwargs.items():
                self.testsToRun[key] = tests


    def configureTests(self, **kwargs):
        '''
        fill self.testsParams with arguments
        '''
        if kwargs:
            self.testsParams.clear()
            for key,param in kwargs.items():
                self.testsParams[key] = param

    #def setTestsOutput(self, *args, **kwargs):
    def setTestsOutputFormat(self, **kwargs):
        '''
        check if tests results must be saved
        in txt file or sent to terminal
        in json or raw formats
        (first let`s save in raw format)
        '''
        self.outputFormat.clear()
        if kwargs:
            for key,formats in kwargs.items():
                self.outputFormat[key] = formats

    def setTestsOutputModes(self, **kwargs):
        '''
        check if tests results must be saved
        in txt file or sent to terminal
        in json or raw formats
        (first let`s save in raw format)
        '''
        self.outputModes.clear()
        if kwargs:
            for key,modes in kwargs.items():
                self.outputModes[key] = modes
        del self.outputModes['raw']
        self.outputModes['raw'] = True

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

    def findTests(self):
        '''
        for testsToRun create a function that reads self.testsToRun and do the following:
                - look for test_ files in dir and subdir (ex: test_ovs) and load it importing
                its class (ex  from test_ovs import OVS - class name associated with ovs in CATALOGUE)
                - returns a dict (ex: self.setupTests) with teststorun:classes objects
                following self.testParams
            this dict will be used to be used in runTests function
        '''
        path = os.getcwd()# This should be pointing to /RouteFlow/rftest/tests
        matches = []
        for root, dirnames, filenames in os.walk(path):
           for filename in fnmatch.filter(filenames, 'test_*'):
               matches.append(os.path.join(filename)) #filename will only return the filename for files even in subdirectory.

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
        self.setTestsOutputModes() #This line is temporary. remove it if it is visible in vandervecken.
        for key,tests in self.testsToRun.items():
            if tests == True:
               logger =  setup(str(key),os.getcwd()) #pass this logger as an argument while calling tests.


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
        #logger.info('TestOVS Network ovs-vsctl')
        #subprocess.call('ovs-vsctl show | grep dp0', shell = True)
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
    #parser.add_argument('-tc', '--testcases', choices =['ovs','rfapps','mongo','containers'],
    #                   help='Testcases to be run.choose form the list specified')

    parser.add_argument('-tc', '--testcases', type=json.loads,
                        help="Testcases to be run.enter on a dict format like :{'ovs':True, 'containers':False, 'rfapps':True}")

    #list of containers : either user gives his own container names(option:l) or chooses from the list(option:ln)
    parser.add_argument('-l', '--lxc', nargs='*',
                        help='Lxc container name, should be given to verify, default not supported, zero or more container names accepted')
    parser.add_argument('-ln', '--lxcnames', choices =['rfvm1','b1','b2','rfvmA','rfvmB'],
                        help='Lxc container name, should be given to verify, default not supported,to be choosen from the list')

    #list of rfapps
    parser.add_argument('-rf', '--rfapps', choices = ['rfserver', 'rfproxy', 'rfclient'],
                        help='list of rfapps to be tested. select from the choice')

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
    mydict = {}
    #mydict = args.testcases
    #testsobj.setTestsToRun(args.pytest, **mydict) #args.testcases will be a dictionary that is passed.
    testsobj.setTestsToRun(True, args.testcases) #args.testcases will be a dictionary that is passed.
    testsobj.configureTests(mongo = args.mongoport, containers = args.lxc, rfapp = args.rfapps )
    testsobj.runTests()
