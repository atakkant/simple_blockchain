import threading
import time
from collections import deque
import concurrent.futures
import blockchain
import timeout_decorator
import hashlib
import string
import random
import stopit



alphanumeric_chars = list(string.ascii_lowercase + string.ascii_uppercase + string.digits)


class Blockchain:
    def __init__(self,id):
        self.chain = deque()
        self.id = id
        

    def create_hash(self,sample):
        encoded = sample.encode()
        hashed = hashlib.sha256(encoded)
        return hashed.hexdigest()

    def verifyChain(self,hash):
        return hash.startswith('0')

    def create_random_string(self,miner,prev_hash):
        global alphanumeric_chars
        final_digits = 90 - len(prev_hash) - len(str(miner))
        global alphanumeric_chars
        alpha_length = len(alphanumeric_chars)
        random_string = random.choices(alphanumeric_chars,k=final_digits)

        return prev_hash + str(miner).join(random_string)
    
    @stopit.threading_timeoutable(default='not finished')
    def mineTheNextBlock(self,prev_hash,queue):
        try:
            confirmation = False
            count = 0
            miner = self.id
            while not confirmation and len(queue)<=len(self.chain):
                nonce_to_test = self.create_random_string(miner,prev_hash)
                
                hashed = self.create_hash(nonce_to_test)
                result = self.verifyChain(hashed)
                count += 1
                if result:
                    print("nonce confirmed by %s"%str(self.id))
                    confirmation = True
                    print(nonce_to_test)
                    print(hashed)
                    time.sleep(4)
                    return {'miner':self.id,'nonce':nonce_to_test,'hash_for_next_block':hashed}
            return None
        except Exception as e:
            print("time completed")
            print(e)
            return None

    def recieve_block(self,queue):
        while len(self.chain)<len(queue):
                indice = len(queue) - len(self.chain)
                new_block = queue[-1*indice]
                if self.verifyChain(new_block.get('hash_for_next_block')):
                    self.chain.append(new_block)
                    print("Node storing the new block: %s size=%s"%(new_block.get('hash_for_next_block'),len(queue)))
                else:
                    print("Node - %d block not confirmed"%self.id)
                    print(new_block)


    def run(self):
        global queue
        print("Mining id: %s"%str(self.id))
        print("number of blocks: %d"%len(queue))
        while len(self.chain)<10:
            self.recieve_block(queue)
            prev_hash = self.chain[-1].get('hash_for_next_block') if self.chain else ""
            new_block = self.mineTheNextBlock(prev_hash=prev_hash,queue=queue,timeout=100000)
            if new_block:
                print("new block found by %d"%self.id)
                queue.append(new_block)
        
        print(queue)


if __name__ == "__main__":
    print("Program is starting")
    queue = deque()
    for i in range(1,4):
        node = Blockchain(i)
        x = threading.Thread(target=node.run)
        x.start()
    
    print("Main: all done")
