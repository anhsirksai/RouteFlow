class Testrfserver():

    logger = logging.getLogger('TestRFServer')

    def test_processrfserverrunning(self,capfd):
        self.logger.info('Test for process rfserver running')
        subprocess.call('ps aux| grep rfserver', shell = True)
        out,err = capfd.readouterr()
        str2 = 'python ./rfserver/rfserver/py'
        with open("testout.txt","a") as txtfile:
             txtfile.write("\n ==== Test for process rfserver running ==== \n ")
             txtfile.write(out)
        with open("testerr.txt","a") as txtfile:
             txtfile.write("\n ==== Test for process rfserver running ==== \n ")
             txtfile.write(err)
        assert out.find(str2) != -1

class Testrfproxy():

    logger = logging.getLogger('TestRFProxy')

    def test_processrfproxy(self,capfd):
        self.logger.info('Test for process rfproxy running')
        subprocess.call('ps aux| grep rfproxy', shell = True)
        out,err = capfd.readouterr()
        str2 = 'ryu-manager --use-stderr --ofp-tcp-listen-port=$CONTROLLER_PORT ryu-rfproxy/rfproxy.py'
        with open("testout.txt","a") as txtfile:
             txtfile.write("\n ==== Test for process rfproxy running ==== \n ")
             txtfile.write(out)
        with open("testerr.txt","a") as txtfile:
             txtfile.write("\n ==== Test for process rfproxy running ==== \n ")
             txtfile.write(err)
        assert out.find(str2) != -1
