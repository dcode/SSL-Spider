import Queue, csv
import threading
import time

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.q = q
    def run(self):
        print "Starting " + str(self.threadID)
        process_data(self.threadID, self.q)
        print "Exiting " + str(self.threadID)

def process_data(threadID, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            ##new method
            print "%d processing %s" % (threadID, data)
        else:
            queueLock.release()


urls=[]
with open("input.txt", 'r') as inputfile:     
    records=csv.reader(inputfile)
    for ii in records:
        urls.append(ii[1])

threadList = [i for i in range(20)]
queueLock = threading.Lock()
workQueue = Queue.Queue(len(urls))
threads = []
threadID = 1

# Create new threads
for threadID in threadList:
    thread = myThread(threadID, workQueue)
    thread.start()
    threads.append(thread)

# Fill the queue
queueLock.acquire()

LIMIT=len(urls)

i=0
for url in urls:
    if i<LIMIT:        
        workQueue.put(url)
    i+=1

queueLock.release()

"""
for word in nameList:
    workQueue.put(word)
queueLock.release()
"""
# Wait for queue to empty
while not workQueue.empty():
    pass

# Notify threads it's time to exit
exitFlag = 1

# Wait for all threads to complete
for t in threads:
    t.join()
print "Exiting Main Thread"