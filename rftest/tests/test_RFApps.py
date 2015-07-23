from test_RF import RFUnitTests

class RFApps(RFUnitTests):

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
        pass

class RFserver(RFApps):

    def __init__(self, logger):
        super().__init__(logger)

    def run_tests(self):
        '''
        basically runs methods inherited with self.tests attribute
        self.evaluate
        self.verify
        self.analyse
        '''
        self.addTestsDefault()
        self.addTest("ps aux | grep rfserver","find","python ./rfserver/rfserver/py")
        self.logger.getlogger("Test_rfserver")
        self.logger.INFO("Test rfserver class Begin")
        self.evaluate()
        self.verify()
        self.analyse()

class RFproxy(RFApps):

    def __init__(self, logger):
        super().__init__(logger)

    #ryu-manager --use-stderr --ofp-tcp-listen-port=$CONTROLLER_PORT ryu-rfproxy/rfproxy.py"
    def setTestsParams(self, cmd, param):
        '''
        Define for example self.containernames, self.mongoport, self.controllerport
        for Container, Mongo, Controller classes respectively
        In this case modify cmd in self.tests
        '''
        return str(cmd) + str(param)

    def setTestsOutputs(self, output1, output2, param):
        '''
        The output to be analysed contains port number as argument.
        To accomodate this change add a method specific to this class.
        :output1, output2: string that is to be tested
        :param: controller port number
        '''
        return str(output1) + str(param) +  str(output2)

    def run_tests(self):
        '''
        basically runs methods inherited with self.tests attribute
        self.evaluate
        self.verify
        self.analyse
        '''
        self.addTestsDefault()
        output = setTestsOutputs('ryu-manager --use-stderr --ofp-tcp-listen-port=',' ryu-rfproxy/rfproxy.py', 6633)
        self.addTest("ps aux | grep rfproxy","find",output)
        output = setTestsOutputs('ryu-manager --use-stderr --ofp-tcp-listen-port=',' ryu-rfproxy/rfproxy.py', 6653)
        self.addTest("ps aux | grep rfproxy","find",output)

        output =  setTestsOutputs('127.0.0.1:', '', 6633)
        cmd = self.setTestsParams("netstat -plant | grep", 6633)
        self.addTest(cmd,"find",output)

        output =  setTestsOutputs('127.0.0.1:', '', 6653)
        cmd = self.setTestsParams("netstat -plant | grep", 6653)
        self.addTest(cmd,"find",output)

        self.logger.getlogger("Test_rfproxy")
        self.logger.INFO("Test rfproxy class Begin")
        self.evaluate()
        self.verify()
        self.analyse()
