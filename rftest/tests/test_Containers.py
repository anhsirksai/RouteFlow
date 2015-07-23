from test_RF import RFUnitTests

class Containers(RFUnitTests):

    '''
    TESTS contain association of commands and a dict containing
    the method of evaluation of the command and the expected output
    '''
    TESTS = {}

    def __init__(self, logger):
        super().__init__(logger)

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


    def run_tests(self):
        '''
        basically runs methods inherited with self.tests attribute
        self.evaluate
        self.verify
        self.analyse
        '''
        self.addTestsDefault()
        cmd = self.setTestsParams("lxc-info -n","rfvmA")
        self.addTest(cmd,"find","state: RUNNING")
        self.logger.getlogger("Test_containers")
        self.logger.INFO("Test containers class Begin")
        self.evaluate()
        self.verify()
        self.analyse()
