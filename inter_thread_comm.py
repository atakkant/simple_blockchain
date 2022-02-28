import threading
import time
import queue
import concurrent.futures
import blockchain

max_size = 10

def message_creator(queue,event):
    count = 0
    while not event.is_set() and count <10:
        message = blockchain.create_random_string(digits=5,miner='0',prev_hash="")
        print("message is created and putting in queue: %s"%message)
        queue.put(message)
        count += 1
    print("Message creator recieved exit event. Exiting")

def consumer(queue,event):
    while not event.is_set() or not queue.empty():
        message = queue.get()
        print("Consumer storing message: %s size=%s"%(message,queue.qsize()))
    print("consumer recieved EXit event. Exiting")


if __name__ == "__main__":
    pipeline = queue.Queue(maxsize=max_size)
    event = threading.Event()
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(message_creator,pipeline,event)
        executor.submit(consumer,pipeline,event)
        time.sleep(0.1)
        print("main: about to set event")
        event.set()
    
