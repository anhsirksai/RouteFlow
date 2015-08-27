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
        self.TESTS.clear()
        self.tests = self.TESTS

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

class RFServer(RFApps):

    def __init__(self, logger):
        super(RFServer, self).__init__(logger)

    def setTestsParams(self, param):
        '''
        Define for example self.containernames, self.mongoport, self.controllerport
        for Container, Mongo, Controller classes respectively
        '''
        pass

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
        self.logger.info("\n")
        self.logger.info("=============Test rfserver class Begin================")

        self.evaluate()
        self.verify()
        self.analyse()

class RFProxy(RFApps):

    def __init__(self, logger):
        super(RFProxy, self).__init__(logger)
        self.port = 6653

    #ryu-manager --use-stderr --ofp-tcp-listen-port=$CONTROLLER_PORT ryu-rfproxy/rfproxy.py"
    def setTestsParams(self, param):
        '''
        Define for example self.containernames, self.mongoport, self.controllerport
        for Container, Mongo, Controller classes respectively
        In this case modify port number, which is passed as an argument while running testcase.
        '''
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
        cmd = "netstat -plant | grep " +  str(self.port)
        self.addTest(cmd,"find",output)

        self.logger = logging.getLogger("Test_RFProxy")
        self.logger.info("\n")
        self.logger.info("================Test rfproxy class Begin==================")

        self.evaluate()
        self.verify()
        self.analyse()

class RFClient(RFApps):

    def __init__(self,logger):
        super(RFClient, self).__init__(logger)


    def setTestsParams(self, param):
        '''
        Define for example self.containernames, self.mongoport, self.controllerport
        for Container, Mongo, Controller classes respectively

        In this case modify cmd in self.tests by adding list of tests with vm names
        '''
        self.port = param

    def run_tests(self):
        '''
        basically runs methods inherited with self.tests attribute
        self.evaluate
        self.verify
        self.analyse
        '''
        self.addTestsDefault()

        cmd = "sudo lxc-attach -n rfvm1 -- /bin/ps aux|grep rfclient"
        self.addTest(cmd,"find","rfclient")

        cmd = "sudo lxc-attach -n b1 -- /bin/ps aux|grep rfclient"
        self.addTest(cmd,"find","")

        cmd = "sudo lxc-attach -n b2 -- /bin/ps aux|grep rfclient"
        self.addTest(cmd,"find","")

        self.logger = logging.getLogger("Test_RFClient")
        self.logger.info("\n")
        self.logger.info("================Test rfclient class Begin==================")

        self.evaluate()
        self.verify()
        self.analyse()


