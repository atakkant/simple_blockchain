import hashlib
import string
import random


alphanumeric_chars = list(string.ascii_lowercase + string.ascii_uppercase + string.digits)

def create_hash(sample):
    encoded = sample.encode()
    hashed = hashlib.sha256(encoded)
    return hashed.hexdigest()

def verifyChain(hash,number_of_zeros='0000'):
    return hash.startswith(number_of_zeros)

def create_random_string(digits,miner,prev_hash=""):
    final_digits = digits - len(prev_hash) - len(miner)
    global alphanumeric_chars
    alpha_length = len(alphanumeric_chars)
    random_string = random.choices(alphanumeric_chars,k=digits)

    return prev_hash + str(miner).join(random_string)
    

max_char = 35
alpha_length = len(alphanumeric_chars)


def mineTheNextBlock(maxchar,miner,prev_hash):
    confirmation = False
    count = 0    
    while not confirmation:
        nonce_to_test = create_random_string(maxchar,miner,prev_hash)
        #print(nonce_to_test)
        hashed = create_hash(nonce_to_test)
        result = verifyChain(hashed)
        count += 1
        if result:
            print("nonce confirmed")
            confirmation = True
            print(nonce_to_test)
            print(hashed)

    print("confirmation finished")
    print("last rand_string: ",nonce_to_test)
    print("last hash: ",hashed)
    print("loop completed. Number of count: %d"%count)

    return {'miner':str(miner),'nonce':nonce_to_test,'hash_for_next_block':hashed}



