
import blockchain
import sys

arguments = sys.argv
if len(arguments) > 1:
    print("Start searching for argument: ",end="")
    try:
        miner = int(arguments[1])
    except:
        print("input not converted to int",end="")
        print(arguments[1])
else:
    print("no arguments")


max_char = 100
miner = '0'
chain_size = 5

first_block = blockchain.mineTheNextBlock(max_char,miner,prev_hash="")

print("genesis block: ",end="")
print(first_block)

last_hash = first_block['hash_for_next_block']
del first_block['hash_for_next_block']
blocklist = [first_block]

for i in range(1,chain_size+1):
    block_i = blockchain.mineTheNextBlock(max_char,miner,last_hash)
    block_i["Hash_%d"%(i-1)] = last_hash
    print(block_i)
    last_hash = block_i['hash_for_next_block']
    del block_i['hash_for_next_block']
    blocklist.append(block_i)

print("blocklist: ")
print(blocklist)