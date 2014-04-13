import requests
import sys
import thread
import threading
import time
import socket
import signal
import sys

def signal_handler(signal, frame):
    print("Received interrupt, waiting for threads to die...")
    sys.exit(0)
	
signal.signal(signal.SIGINT, signal_handler)

#print the banner
print("" +
"  _   _           _               __  __                                        \n" +
" | | | | ___  ___| |_ ___  _ __  |  \\/  | ___  _ __   __ _  ___   ___  ___  ___ \n" +
" | |_| |/ _ \\/ __| __/ _ \\| '__| | |\\/| |/ _ \| '_ \\ / _` |/ _ \\ / _ \\/ __|/ _ \\\n" +
" |  _  |  __/ (__| || (_) | |    | |  | | (_) | | | | (_| | (_) | (_) \\__ \\  __/\n" +
" |_| |_|\\___|\\___|\\__\\___/|_|    |_|  |_|\\___/|_| |_|\\__, |\\___/ \\___/|___/\\___|\n" +
"                                                     |___/                      \n")
print("Mass rDNS Resolver")
print("Written by Hector Mongoose")
print("")

#check for incorrect usage
#TODO: use OptionParser
if len(sys.argv) != 4:
	print("Incorrect usage: python %s <ip list> <threads> <out file>" % (sys.argv[0]))

threads = int(sys.argv[2])

def getHost(target):
	try:
		with open(sys.argv[3], "a") as f:
			f.write("%s:%s\n" % (target, socket.gethostbyaddr(target)[0]))
			f.flush()
	except (KeyboardInterrupt, SystemExit):
		sys.exit(0)
	except Exception:
		with open(sys.argv[3], "a") as f:
			f.write("%s:%s\n" % (target, target))
			f.flush()

#a little output message
print("Running on %s with %s threads to %s" % (sys.argv[1], sys.argv[2], sys.argv[3]))

#begin looping the input
for line in open(sys.argv[1]):
	#wait until we have an available thread
	while threading.activeCount() - 1 >= threads:
		try:
			pass
		except (KeyboardInterrupt, SystemExit):
			sys.exit(0)
	#double check that's right
	if threading.activeCount() - 1 < threads:
		#finally, start the thread
		threading.Thread(target=getHost, args=[line.rstrip(),]).start()
		time.sleep(0.01)

print("Finished creating threads, waiting for them to die...")
		
while True:
	if threading.activeCount() == 1:
		break
	pass
	