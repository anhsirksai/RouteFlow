import sys
import time
import argparse
import os
import logging
import subprocess
import json
import fnmatch
import logging.handlers

from subprocess import Popen, PIPE

logging.basicConfig(
    filename = 'RFtest.log',
    level=logging.DEBUG,
    format='%(asctime)s %(name)-15s %(levelname)-8s %(message)s',
    datefmt='%b %d %H:%M:%S',
    mode = 'w'
    )

class Tests:
    CATALOGUE = {
                'test_OVS':'OVS',
                'test_Mongo':'Mongo',
                'test_Containers':'Containers',
                'test_RFApps':['RFServer','RFProxy','RFClient'],
                'test_Connectivity' : 'Connectivity'
    }
    LOGLEVEL = {
               10 : 'DEBUG',
               20 : 'INFO',
               30 : 'WARNING',
               40 : 'ERROR',
               50 : 'CRITICAL',
    }

    def __init__(self):
        self.testsToRun = {'OVS':True, 'Containers':False, 'RFApps':False}
        self.testsParams = {'Mongo':27017, 'Containers':['rfvmA','rfvmB'], 'Connectivity': ['rfvm1','b1','b2']}#, 'RFApps':['rfproxy','rfserver']}
        self.outputFormat = {'txt':False, 'terminal':False}
        self.outputModes = {'json':False, 'raw':False}
        self.use_pytest = False
        self.setUpTests = {}
        self.logger = None

    def setTestsToRun(self, **kwargs):
        '''
        fill self.testsToRun with proper arguments
        like lxc, ovs, rfserver, rfproxy,.... true or false

        define if tests will use pytest or not (self.use_pytest = False)
        '''

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
        in json or raw formats
        (first let`s save in raw format)
        '''
        self.outputModes.clear()
        if kwargs:
            for key,modes in kwargs.items():
                self.outputModes[key] = modes

    def setup(self,output_dir):
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

        :output_dir: directory to store logs
        '''

        self.logger = logging.getLogger(__name__)
        #self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s %(name)-15s %(levelname)-8s %(message)s")

        #INFO handler
        #handler = logging.handlers.RotatingFileHandler(os.path.join(output_dir, "Output.log"),"a", encoding=None, delay="true", maxBytes=20, backupCount=5)
        handler = logging.handlers.RotatingFileHandler(os.path.join(output_dir, "Output.log"),"a")
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        #DEBUG handler
        handler = logging.handlers.RotatingFileHandler(os.path.join(output_dir, "Debug.log"),"a", encoding=None, delay="true", maxBytes=20, backupCount=5)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        #ERROR handler
        handler = logging.handlers.RotatingFileHandler(os.path.join(output_dir, "Error.log"),"a", encoding=None, delay="true", maxBytes=20, backupCount=5)
        handler.setLevel(logging.ERROR)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def findTests(self):
        '''
        for testsToRun create a function that reads self.testsToRun and do the following:
                - look for test_ files in dir and subdir (ex: test_ovs) and load it importing
                its class (ex  from test_ovs import OVS - class name associated with ovs in CATALOGUE)
                - returns a dict (ex: self.setupTests) with teststorun:classes objects
                following self.testParams
            this dict will be used to be used in runTests function
        '''

        # Find all the files starting with test_* and store output to 'matches' list.
        path = os.getcwd()# This should be pointing to /RouteFlow/rftest/tests
        matches = []
        for root, dirnames, filenames in os.walk(path):
           for filename in fnmatch.filter(filenames, 'test_*'):
               if os.path.join(os.path.splitext(filename)[1]) == ".py":
                   matches.append(os.path.join(os.path.splitext(filename)[0]))

        # Check if class is marked to run tests
        # If so, Create an object for the corresponding class, by referring to CATALOGUE
        for testName,toRun in self.testsToRun.items():
            if toRun == True:
                for i in Tests.CATALOGUE.keys():
                    if i.find(testName) != -1:
                        for obj in matches:
                            if obj.find(testName) != -1:
                                if type(Tests.CATALOGUE[obj]) is list:
                                    for classes_ in Tests.CATALOGUE[obj]: #For each file, instantiate an object for the classes in it.
                                        module = __import__(obj)
                                        class_ = getattr(module, classes_)
                                        self.setUpTests[classes_] = class_(self.logger)
                                else:
                                    module = __import__(obj)
                                    #getattr(li, "pop") is the same as calling li.pop
                                    class_ = getattr(module, Tests.CATALOGUE[obj])
                                    self.setUpTests[obj] = class_(self.logger)
                                    for confkey,confvalues in self.testsParams.items():
                                        if testName == confkey:
                                            self.setUpTests[obj].setTestsParams(confvalues)

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

        for test in self.setUpTests.keys():
            self.setUpTests[test].run_tests()


#class Dictlist(dict):
#    '''
#    class to accept dictionary of lists.
#    Required to handle the outputDictionary in RFUnitTests.
#    The commands that are to be executed are not unique within testcases.
#    Hence this class is required.
#    '''
#    def __setitem__(self, key, value):
#        try:
#            self[key]
#        except KeyError:
#            super(Dictlist, self).__setitem__(key, [])
#        self[key].append(value)

class RFUnitTests(object):

    def __init__(self, logger):
        self.logger = logger
        self.evaluateDictionary = {}
        self.verifyDictionary = {}

    def findFunction(self, output):
        '''
        find packet loss percentage in ping result
        and set true or false if is 100% less or not

        ubuntu@b1:~$ ping -c 3 172.31.2.2

        PING 172.31.2.2 (172.31.2.2) 56(84) bytes of data.
        64 bytes from 172.31.2.2: icmp_req=1 ttl=63 time=3.78 ms
        64 bytes from 172.31.2.2: icmp_req=2 ttl=63 time=3.60 ms
        64 bytes from 172.31.2.2: icmp_req=3 ttl=63 time=3.07 ms

        --- 172.31.2.2 ping statistics ---
        3 packets transmitted, 3 received, 0% packet loss, time 2016ms
        rtt min/avg/max/mdev = 3.072/3.486/3.781/0.305 ms

        ping -c 3 8.8.8.8
        PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
        From 10.0.2.2 icmp_seq=1 Destination Net Unreachable
        From 10.0.2.2 icmp_seq=2 Destination Net Unreachable
        From 10.0.2.2 icmp_seq=3 Destination Net Unreachable

        --- 8.8.8.8 ping statistics ---
        3 packets transmitted, 0 received, +3 errors, 100% packet loss, time 2012ms
        '''
        #cmd = "sudo lxc-attach -n b1 -- /bin/ping -c 3 172.31.2.2"
        #output = subprocess.Popen(cmd,stdout = subprocess.PIPE).communicate()[0]
        #sp = subprocess.Popen(cmd,stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell = True)
        #output,error = sp.communicate()

        if ('unreachable' in output):
            return False
        # The packet loss when connected will usually be 0%,
        # To make sure, any thing below 100% is also counted as connected.
        elif('0% packet loss' in out) or ('100% packet loss' not in out):
            return True

    def evaluate(self):
        '''
        for each process in self.tests run it using capfd
        This function only execute the commands, get the output/err,
        return them as {command: {'out':output,'err':err} )
        '''
        self.tests
        #This approach is fine as long as we follow the non-threading approach. are we planning to use threads?? not in near future.
        if self.evaluateDictionary:
            self.evaluateDictionary.clear()
        self.logger.info("\n")
        for key,value in self.tests.items():
            self.logger.info("running test : %s", key)
            sp = subprocess.Popen(key,stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell = True)
            out,err = sp.communicate()
            self.evaluateDictionary[key] = {'out' : str(out),
                                            'err' : str(err), }

    def verify(self):
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

        Verify if the command is a list or not. define behaviour accordingly.

        sample evaluateDictionary.
        {'ovs-vsctl show | grep dp0': {'err': 'krishna sai klfhahsd dp01',
           'out': 'sai krishnaalskdfkaskj dp0'},}
        '''

        #key of self.evaluateDictionary is always equal to key of self.tests dictionary.
        #This is how data structure is built.Hence tests[inputs] will work.

        self.logger.info("\n")
        for cmdInput,outErrDict in self.evaluateDictionary.items():
            self.logger.info("verifying test : %s", cmdInput)
            for keys,values in outErrDict.items():
                # Logic: If err value exists, do not check for out
                # If out exists, run method and validate tests['output'] with 'out' of outErrDict.
                # Fill in assert:True if 'output'.method = 'out'
                # else, assert:False.
                if keys == 'err':
                    self.verifyDictionary[cmdInput] = {'assert':False, 'result':values}
                elif keys == 'out' :
                    if values == '':
                        self.verifyDictionary[cmdInput] = {'assert':False, 'result':values}
                    else:
                        if self.tests[cmdInput]['method'] == 'find':
                            if values.find(self.tests[cmdInput]['output']) != -1:
                                self.verifyDictionary[cmdInput] = {'assert':True, 'result':values}
                        elif self.tests[cmdInput]['method'] == 'findfp':
                            #TODO : The findfp should be handled as a closure.
                            if self.findFunction(values) == True:
                                self.verifyDictionary[cmdInput] = {'assert':True, 'result':values}
                            else :
                                self.verifyDictionary[cmdInput] = {'assert':False, 'result':values}

    def analyse(self):
        '''
        receives dict of verify_processes
        check assertion values and write results to logger
        example:
        self.logger.info("OUTPUT\n %s", out)
        self.logger.info("ERROR\n %s", err)
        No need to write assertion
        '''
        self.logger.info("\n")
        for keys,values in self.verifyDictionary.items():
            self.logger.info("analysing test : %s", keys)
            if values['assert'] == True:
                self.logger.info("testcase with command %s PASSED ", keys)
            elif values['assert'] == False:
                self.logger.info("testcase with command %s FAILED ", keys)

    def run_tests(self):
        '''
        just pass, the classes inheriting RFUnitTests will
        overwrite this function
        '''
        #pass

if __name__ == '__main__':
    '''
    RFTest suite, to run the tests and determine the state of system
    Report bugs to: https://github.com/routeflow/RouteFlow/issues
    '''

    testsobj = Tests()

    args_fp = open('arguments.json', 'r')
    cmdArgs= json.load(args_fp)
    #print cmdArgs

    #kwargs = {'OVS':True,'Containers':True, 'Mongo':True, 'RFApps':True, 'Connectivity':True}
    testsobj.setTestsToRun(**cmdArgs['testsToRun']) #args.testcases will be a dictionary that is passed.

    # testsobj.configureTests(Mongo = 5056, Containers = 'rfvmA', Connectivity = 'rfvm1', RFApps = ['RFServer','RFClient','RFProxy'])
    testsobj.configureTests(**cmdArgs['configureTests'])

    testsobj.setTestsOutputFormat()
    testsobj.setTestsOutputModes() #dictionary : {'json':False, 'txt':True}

    testsobj.setup(os.path.dirname(os.path.realpath(__file__)))

    testsobj.findTests()
    testsobj.runTests()
