# $Source: /home/scrobotics/src/cscore_images_from_queues/RCS/queue_demo.py,v $
# $Revision: 1.2 $
# $Date: 2026/01/23 18:11:52 $
"""
This demo shows a number of things about using queues and threads.
"""
from collections import deque
import threading
from time import sleep
from pprint import pprint
#
# Declare the queue(s) that will be shared by the main program and the threaded
# process(es).
#
Q1 = deque(maxlen=1)
Q2 = deque(maxlen=1)

#
# Define the funcion(s) that will be run as theads. The "qname" argument will
# be one of the queues declared above.
#
def load_queue1(qname):
    while True:
        sleep (5)
        qname.append('TADA!')

def load_queue2(qname):
    while True:
        sleep (3)
        qname.append('Howdy!!')

#
# These are just plain ol' functions
#
def get1():
    try:
        val1 = Q1.pop()   # This syntax removes the item from the queue.
        #val1 = Q1[0]     # This syntax leaves the item in the queue.
        return True, val1
    except:
        return False, None

def get2():
    try:
        val2 = Q2.pop()   # This syntax removes the item from the queue.
        #val2 = Q2[0]     # This syntax leaves the item in the queue.
        return True, val2
    except:
        return False, None

#
# Declare the thread(s) you'll be runnung. The thread target is the load_queue1(2)
# function defined above, "args" is the arguments you're passing to the function.
# Note the trailing "," in the argument list. It's required.
#
t1 = threading.Thread(target=load_queue1, args=(Q1,))
t2 = threading.Thread(target=load_queue2, args=(Q2,))

#
# Start the thread(s) running.
#
t1.start()
t2.start()

while True:
    sleep (1)
    success1, value1 = get1()
    success2, value2 = get2()
    print (success1, success2)
    print (value1, value2)
    print()
