import logging
import subprocess
from test_RF import RFUnitTests

class Containers(RFUnitTests):

    '''
    TESTS contain association of commands and a dict containing
    the method of evaluation of the command and the expected output
    '''
    TESTS = {}

    def __init__(self, logger):
        super(Containers, self).__init__(logger)

    def addTestsDefault(self):
        self.tests = self.TESTS #tests is initialised in RFUnitTests class and should be filled in here.

    def addTest(self, cmd, method, output):
        '''
        add in self.tests new tests following the TEST structure
        '''
        self.TESTS[str(cmd)] = {'method':str(method),
                                'output':str(output),}

    def setTestsParams(self, cmd, param):
        '''
        Define for example self.containernames, self.mongoport, self.controllerport
        for Container, Mongo, Controller classes respectively
        In this case modify cmd in self.tests
        '''
        return str(cmd) + str(param)

    def evaluate(self):
        for key,value in self.tests.items():
            self.logger.info("running test : %s", key)
            sp = subprocess.Popen(key,stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell = True)
            out,err = sp.communicate()
            if out != '':
                self.logger.info("testcase with command %s PASSED ", key)
                self.logger.info("Status of containers")
                self.logger.info("\n\n %s", out)
            elif err != '':
                self.logger.info("testcase with command %s FAILED ", key)
                self.logger.error("Status of containers could not be found")
                self.logger.error(err)

    def run_tests(self):
        '''
        basically runs methods inherited with self.tests attribute
        self.evaluate
        self.verify
        self.analyse
        '''
        self.addTestsDefault()
        cmd = self.setTestsParams("sudo lxc-list"," -s")
        self.addTest(cmd,"find","state: RUNNING")
        self.logger = logging.getLogger("Test_Containers")
        self.logger.info("\n")
        self.logger.info("=============Test containers class Begin==================")
        self.logger.info("+++ This test case is to list down the currently 'running', 'stopped' and 'Frozen' list of containers +++")
        self.evaluate()
        #self.verify()
        #self.analyse()
