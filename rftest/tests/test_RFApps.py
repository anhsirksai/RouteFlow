import logging
from test_RF import RFUnitTests

class RFApps(RFUnitTests):

    '''
    TESTS contain association of commands and a dict containing
    the method of evaluation of the command and the expected output
    '''
    TESTS = {}

    def __init__(self, logger):
        super(RFApps, self).__init__(logger)

    def addTestsDefault(self):
        self.tests = self.TESTS #tests is initialised in RFUnitTests class and should be filled in here.

    def addTest(self, cmd, method, output):
        '''
        add in self.tests new tests following the TEST structure
        '''
        self.TESTS[str(cmd)] = {'method':str(method),
                                'output':str(output),}

    #def setTestsParams(self, cmd, param):
    def setTestsParams(self, param):
        '''
        Define for example self.containernames, self.mongoport, self.controllerport
        for Container, Mongo, Controller classes respectively
        In this case modify cmd in self.tests
        '''
        #return str(cmd) + str(param)
        #self.port = param
        pass

    def run_tests(self):
        '''
        basically runs methods inherited with self.tests attribute
        self.evaluate
        self.verify
        self.analyse
        '''
        pass

class RFServer(RFApps):

    def __init__(self, logger):
        super(RFServer, self).__init__(logger)

    def run_tests(self):
        '''
        basically runs methods inherited with self.tests attribute
        self.evaluate
        self.verify
        self.analyse
        '''
        self.addTestsDefault()
        self.addTest("ps aux | grep rfserver","find","python ./rfserver/rfserver/py")
        self.logger = logging.getLogger("Test_RFServer")
        self.logger.info("\n =============Test rfserver class Begin================")
        self.evaluate()
        self.verify()
        self.analyse()

class RFProxy(RFApps):

    def __init__(self, logger):
        super(RFProxy, self).__init__(logger)
        self.port = 6653
        #super(RFproxy, self).__init__(logger, port=6653)
        #self.port = port

    #ryu-manager --use-stderr --ofp-tcp-listen-port=$CONTROLLER_PORT ryu-rfproxy/rfproxy.py"
    def setTestsParams(self, param):
        '''
        Define for example self.containernames, self.mongoport, self.controllerport
        for Container, Mongo, Controller classes respectively
        In this case modify cmd in self.tests
        '''
        #return str(cmd) + str(param)
        self.port = param

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
        output = self.setTestsOutputs('ryu-manager --use-stderr --ofp-tcp-listen-port=',' ryu-rfproxy/rfproxy.py', self.port)
        self.addTest("ps aux | grep rfproxy","find",output)

        output =  self.setTestsOutputs('127.0.0.1:', '', self.port)
        cmd = self.setTestsParams("netstat -plant | grep", self.port)
        self.addTest(cmd,"find",output)

        self.logger = logging.getLogger("Test_RFProxy")
        self.logger.info("\n ================Test rfproxy class Begin==================")
        self.evaluate()
        self.verify()
        self.analyse()
