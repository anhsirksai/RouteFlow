rftest/tests
===========

RouteFlow's Unified testing framework supports two functionalities:
* To run the test and get to know the health of routeflow components.
* Extend the testcases with ease to tests the new features.

Dependencies
-----------

* RouteFlow
* ryu-rfproxy
* 3.5 or 3.8 Generic kernal.(For Connectivity and Topology tests to run)

Building
--------

The testing framework requires RouteFlow and rftest to run. The usual way to install RouteFlow and
all of its dependencies is as follows:

* Requirements system Ubuntu 12.04 updated and git installed. 
    + ```apt-get update & apt-get upgrade & apt-get install git```

* Clone RouteFlow
    + ```git clone https://github.com/raphaelvrosa/RouteFlow```

* Build all the required components of RouteFlow

    + ``` cd RouteFlow ```
    + ``` git checkout vandervecken ```
    + ``` ./build.sh -c -z -n -i ryu ```

Running
-------

RouteFlow usually supplies a script to run all of the components in the
correct order. If you want to run rftests, start rftest1 or rftest2 first followed by 
running test cases. Below are the commands for the same.

* Prior to running the tests, OpenVswitch service should be running. Run the following 
script to bring up the service:

    + ``` cd RouteFlow/```  
    + ```./ovs-init.sh```

* Run the test, either rftest1 or rftest2:

    + ```cd rftest```
    + ```sudo ./rftest1 -z --ryu```
(or)
    + ```sudo ./rftest2 ```
    + ``` sudo mn --custom topo-4sw-4host.py --topo rftest2 --controller=remote,ip=127.0.0.1,port=6633 --switch=ovsk,protocols=OpenFlow13 --pre ipconf ```

* Now open a new terminal and run the testcases:

    + ```cd RouteFlow/rftest/tests/```
    + ```python test_RF.py```

* This will run all the three type of testcases.
    + Basic tests
    + Connectivity tests
    + Topology tests.

Checking the output of testcases:
--------------------------------

* The output of the testing framework will be updated and saved specific to each run of the command
    + ``` python test_RF.py``` The output is stored to file : ```RouteFlow/rftest/tests/Output.log```

* Logs will persistantly be stored in the file : ```RouteFlow/rftest/tests/RFtest.log```

Extend testcases/Implement New testcases
----------------------------------------


FAQ
---

Q. When I run "sudo ./rftest1 -z --ryu" followed by "python test_RF.py", 
I get messages about lxc-attach faled
```lxc-attach: No such file or directory - failed to open '/proc/19731/ns/pid'
lxc-attach: failed to enter the namespace```

A. lxc-attach requires features that are not present in the native 12.04 kernel (3.5). 
You need at least 3.8 which IIRC is available in the backport. The fix is tested on 3.8,
Hence it is suggested you upgrade to 3.8

To fix this issue, I ran the following command to get 3.8:
```sudo apt-get install linux-image-generic-lts-raring linux-headers-generic-lts-raring```

or you can run the following command to get 3.5
```sudo apt-get install linux-image-generic-lts-quantal linux-headers-generic-lts-quantal```

License
-------

This project uses the Apache License version 2.0. See LICENSE for more details.
