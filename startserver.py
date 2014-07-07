import os
import subprocess
import threading
import time

AVCONVCMD = ["avconv", "-re"]
TIMETOWAITFORABORT = 0.5

#class for controlling the running and shutting down of raspivid
class AvconvController(threading.Thread):
    def __init__(self, filePath, otherOptions=None):
        threading.Thread.__init__(self)

        #setup the raspivid cmd
        self.avconvcmd = AVCONVCMD

        #add file path, timeout and preview to options
        self.avconvcmd.append("-i")
        self.avconvcmd.append(filePath)

        #if there are other options, add them
        if otherOptions != None:
            self.avconvcmd = self.avconvcmd + otherOptions

        #set state to not running
        self.running = False

    def run(self):
        # run avconv
        avconv = subprocess.Popen(self.avconvcmd)

        # loop until its set to stopped or it stops
        self.running = True
        while(self.running and avconv.poll() is None):
            time.sleep(TIMETOWAITFORABORT)
        self.running = False

        # kill avconv if still running
        if avconv.poll() == True: avconv.kill()

    def stopController(self):
        self.running = False

# test program
if __name__ == '__main__':

    # create avconv controller
    vidcontrol = AvconvController("/shared/test.avi", ["-vcodec", "copy", "-an", "-f", "avi", "udp://239.0.1.23:1234"])

    try:
        print("Starting raspivid controller")
        #start up avconv controller
        vidcontrol.start()
        #wait for it to finish
        while(vidcontrol.isAlive()):
            time.sleep(0.5)

    #Ctrl C
    except KeyboardInterrupt:
        print "Cancelled"

    #Error
    except:
        print "Unexpected error:", sys.exc_info()[0]

        raise

    #if it finishes or Ctrl C, shut it down
    finally:
        print "Stopping avconv controller"
        #stop the controller
        vidcontrol.stopController()
        #wait for the tread to finish if it hasn't already
        vidcontrol.join()

    print "Done"
