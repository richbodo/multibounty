# block.io test

from block_io import BlockIo


def print_recurse_dicts(topdict):
    i = 0
    for k in topdict:
        i = i + 1
        v = topdict[k]
        print "key " + str(i) + " is " + str(k)
        print "val " + str(i) + " is " + str(v)
        if isinstance(v, dict):
            print "Val " + str(v) + " is a subdict"
            for seq in print_recurse_dicts(v):
                print "subdict: " + str(seq)
                #yield seq
        else:
            print "Val " + str(v) + " is not a subdict"


block_io = BlockIo("620d-887e-8171-7db1", '18726354', 2)

# print the account balance
balance = block_io.get_balance()
print_recurse_dicts(balance)

print "why didn't that run?"

# block_io.get_current_price()


#for value in mystery_stucture:
#	if 

# print all addresses on this account
#print block_io.get_my_addresses()

# get a new address
# print block_io.get_new_address(label='addy_one')

#print block_io.get_address_balance(labels='addy_one')

# print the response of a withdrawal request
# print block_io.withdraw(from_labels='default', to_label='', amount='50.0')