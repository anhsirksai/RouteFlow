from test_RF import RFUnitTests
#from test_RF import logger

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
