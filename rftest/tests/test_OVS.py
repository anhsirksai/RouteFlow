from test_RF import RFUnitTests

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
        super(OVS, self).__init__(logger)

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
        pass


    def run_tests(self):
        '''
        basically runs methods inherited with self.tests attribute
        self.evaluate
        self.verify
        self.analyse
        '''
        print "sai OVS runtests"
        self.addTestsDefault()
        self.addTest("ps aux | grep dp0","find","ovsdb-server")
        self.addTest("ps aux | grep dp0","find","ovs-vswitchd")
        #self.logger = logging.getlogger("Test_OVS")
        self.logger.info("Test OVS class Begin")
        self.evaluate()
        self.verify()
        self.analyse()
