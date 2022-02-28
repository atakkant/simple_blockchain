import threading
import time
import blockchain

def thread_function(digits,miner,prev_hash,thread_id):
    random_string = blockchain.create_random_string(digits=3,miner='0',prev_hash="")
    print("thread_id: %d - "%thread_id,end="")
    time.sleep(10-thread_id)
    print(random_string)
    



if __name__ == "__main__":
    print("Program is starting")
    for i in range(2,10):
        time.sleep(5)
        x = threading.Thread(target=thread_function,args=(3,'0',"",i),daemon=True)
        x.start()
    print("Main: all done")