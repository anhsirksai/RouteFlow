import subprocess
import os
import json
from subprocess import call

class DumpToFile(object):

    def __init__(self):
        self.tangerine = "And now a thousand years between"

    """
    Command to execute the os commands required. Runs the commands in background and
    capture the output.
    command : Command to run.
    filepath : location to store output file. should not be appended by "/" at the end.
    filename : name of the output file to store.
	filetype : to store output in the file format specified.

    """
    #def execute(self,command,filepath,filename,filetype):
    def execute(self,command):
        subprocess.call(command, shell = True) #Popen(command, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        #popen = subprocess.Popen(command, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        #lines_iterator = iter(popen.stdout.readline, b"")
        #lines_iterator_error = iter(popen.stderr.readline, c"")

       # if filetype == "json":
       #     dumpfile = filepath+"/output/" + filename + ".output" + ".json"
       #     try:
       #         os.remove(dumpfile)
       #     except OSError:
       #         pass
       #     with open(dumpfile, "a") as jsonfile:
       #         for line in lines_iterator:
       #             json.dump(line,jsonfile)
       # elif filetype == "txt":
       #     dumpfile = filepath+"/output/" + filename + ".output" + ".txt"
       #     try:
       #         os.remove(dumpfile)
       #     except OSError:
       #         pass
       #     with open(dumpfile, "a") as txtfile:
       #         for line in lines_iterator:
       #             txtfile.write(line)


       ## dumpfile1 = filepath+"/" + filename + ".error"
       ## try:
       ##     os.remove(dumpfile1)
       # except OSError:
       #     pass
       # with open(dumpfile1, "a") as jsonfile:
       #     for line in lines_iterator_error:
       #         json.dump(line,jsonfile)
