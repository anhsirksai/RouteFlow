import logging
from test_RF import RFUnitTests

class Mongo(RFUnitTests):

    '''
    TESTS contain association of commands and a dict containing
    the method of evaluation of the command and the expected output
    '''
    TESTS = {
            'ps aux | grep mongo':{'method':'find', 'output':'mongod'},
    }

    def __init__(self, logger):
        super(Mongo, self).__init__(logger)
        self.port = 27017

    def addTestsDefault(self):
        self.tests = self.TESTS #tests is initialised in RFUnitTests class and should be filled in here.

    def addTest(self, cmd, method, output):
        '''
        add in self.tests new tests following the TEST structure
        '''
        self.TESTS[str(cmd)] = {'method':str(method),
                                'output':str(output),}

    def setTestsParams(self, param):
        '''
        Define for example self.containernames, self.mongoport, self.controllerport
        for Container, Mongo, Controller classes respectively
        In this case modify cmd in self.tests
        netstat -plant | grep $mongoport
        '''
        print "fuck you mongo"
        self.port = param

    def run_tests(self):
        '''
        basically runs methods inherited with self.tests attribute
        self.evaluate
        self.verify
        self.analyse
        '''
        self.addTestsDefault()
        cmd = "sudo netstat -plant | grep " + str(self.port)
        self.addTest(cmd,"find","mongod")
        self.logger = logging.getLogger("Test_Mongo")
        self.logger.info("\n")
        self.logger.info("=========Test Mongod class Begin==============")
        self.evaluate()
        self.verify()
        self.analyse()
