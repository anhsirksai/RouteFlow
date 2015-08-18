from test_RF import RFUnitTests
import subprocess

#class Connectivity(RFUnitTests()):
class Connectivity():

    TESTS = {}

    #def __init__(self, containerNames, logger):
    def __init__(self,containerNames):
        #super(Conncetivity, self).__init__(logger)
        self.containerRoutes = {}
        self.containerInterfaces = {}
        self.containerNames = containerNames #string to be defined by user (e.g., in rftest2 is rfvmA, B, ...
        self.tests = {}

    def getContainerRoutes(self, name):
        #cmd = "lxc-attach -n " + name + " -- /home route -n"
        cmd = "route -n"
        sp =  subprocess.Popen(cmd,stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell = True)
        out,err = sp.communicate()
        return out,err
        #return sp.stdout This is a file pointer. No use in using this method
        #return subprocess.call(cmd)

    def parseContainerRoutes(self, name):
        '''
        for container name parse the result of getContainerRoutes
        and put it as list of strings (one string for each route) inside dict self.containerRoutes[name]
        route format is the destination ip address

        sudo lxc-console -n b2
        ubuntu/ubuntu

        ubuntu@b2:~$ route -n
        Kernel IP routing table
        Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
        0.0.0.0         172.31.2.1      0.0.0.0         UG    100    0        0 eth0
        172.31.2.0      0.0.0.0         255.255.255.0   U     0      0        0 eth0

        '''
        out = getContainerRoutes(name)
        for line in out:
            print line #handle storing of only routes in the self.containerRoutes dictionary.


    def getContainerInterfaces(self, name):
        cmd = "lxc-ps -n " + name + "ifconfig"

        return subprocess.call(cmd)

    def parseContainerInterfaces(self, name):
        '''
        parse the result of getContainerInterfaces storing in self.containerInterfaces
        the result of parse (list of strings) containing all interfaces ip address
        remember to filter 127.0.0.1 interface

        ubuntu@b2:~$ ifconfig
        eth0      Link encap:Ethernet  HWaddr 02:b2:b2:b2:b2:b2
                  inet addr:172.31.2.2  Bcast:172.31.2.255  Mask:255.255.255.0
                  inet6 addr: fe80::b2:b2ff:feb2:b2b2/64 Scope:Link
                  UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
                  RX packets:14 errors:0 dropped:0 overruns:0 frame:0
                  TX packets:20 errors:0 dropped:0 overruns:0 carrier:0
                  collisions:0 txqueuelen:1000
                  RX bytes:1212 (1.2 KB)  TX bytes:1296 (1.2 KB)

        lo        Link encap:Local Loopback
                  inet addr:127.0.0.1  Mask:255.0.0.0
                  inet6 addr: ::1/128 Scope:Host
                  UP LOOPBACK RUNNING  MTU:16436  Metric:1
                  RX packets:2 errors:0 dropped:0 overruns:0 frame:0
                  TX packets:2 errors:0 dropped:0 overruns:0 carrier:0
                  collisions:0 txqueuelen:0
                  RX bytes:176 (176.0 B)  TX bytes:176 (176.0 B)
        '''
        pass

    def addTest(self, cmd, method, output, **kwargs):
        '''
        add in self.tests new tests following the TEST structure
        '''
        #self.tests[str(cmd)] = {'method':str(method),
        #                       'output':str(output), kwargs}
        pass


    def addTestsDefault(self):
        '''
        Break point 1.
        calls getcontainerInterfaces and parseContainerInterfaces for every container in self.containerNames
        calls getContainerRoutes and parseContainerRoutes for every container in self.containerNames
        for containerName in self.containerNames:
            self.containerRoutes[containerName] = parseContainerRoutes(getContainerRoutes(contanername))

        for containerName in self.containerNames:
            cmd = "lxc-ps -n {name} ping -c3 {target}"
            cmd.format(name=containerName, target=containerNameInterface)


        with the results of the calls above we need to addTest for every pair of containers
        the idea is that for each container it is going to ping every interfaces of all the other containers

        example:
        rfvmA ping rfvmB interface 172.31.2.1 then we will have the command

        cmd = "lxc-ps -n {name} ping -c3 {target}"
        cmd.format(name=rfvmA, target=rfvmBInterface)

        method is going to be a find of the % of packet loss, if it is less than 100% then
        we consider True otherwise false

        expected output=True

        method = 'customFind'
        methodFunc = findFunction

        then call addTest(cmd, method, output, name=rfvmA, target="rfvmB,rfvmBInterface", methodFunc = findFunction)

        I think we will need to create/customize a find function to parse the result of the ping command

        I put kwargs in addTest to insert the containers name and target so it can be logged
        in the analyse function
        '''
    def findFunction(self):
        '''
        find packet loss percentage in ping result
        and set true or false if is 100% less or not
        '''

    def run_tests(self):
        '''
        basically runs methods inherited with self.tests attribute
        self.evaluate
        self.verify
        self.analyse
        '''
        self.addTestsDefault()
        #self.logger.getlogger("Test_connectivity")
        self.logger.info("Test connectivity class Begin")
        self.evaluate()
        self.verify()
        self.analyse()




class Topology(Connectivity):


    TESTS = {}

    def __init__(self, containerNames):
        super(Topology, self).__init__(containerNames)

    def addTestsDefault():
        '''
        cmd instead of ping, traceroute and iperf
        '''
