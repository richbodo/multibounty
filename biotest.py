# block.io test

from block_io import BlockIo
import ConfigParser
import os
import pdb
import datetime

class Secrets:
    def __init__(self):
        self.bio_spin=0
        self.bio_api_key=0
    def __str__(self):
        return ("Block IO Secret Pin: " + str(self.bio_spin) + "\n"
                "Block IO Account: " + str(self.bio_api_key) )

#
# Recurse through the dicts and arrays that are nested in return values and print all the keys, values, and items flat
#
def print_flat(topthing):
    if isinstance(topthing, dict):
        for k in topthing:
            v = topthing[k]
            print str(k) + " : "
            print_flat(v)
    elif isinstance(topthing, list):
        for k in topthing:
            print_flat(k)
    else:
         print topthing

def test_print_flat():
    sample = {}
    sample.update(
        {u'status': u'success', u'data': {u'network': u'BTCTEST', u'addresses': [{u'pending_received_balance': u'0.00000000', u'available_balance': u'0.01000000', u'label': u'default', u'user_id': 0, u'address': u'2NAKxGtGEjwH2nyHovVjYKhyK7uDEGttMxf'}, {u'pending_received_balance': u'0.00000000', u'available_balance': u'0.00000000', u'label': u'addy_one', u'user_id': 1, u'address': u'2MxKK5PNE4wuB3VBrrNCZinykVijPfAxQfG'}, {u'pending_received_balance': u'0.00000000', u'available_balance': u'0.00000000', u'label': u'shibe1', u'user_id': 2, u'address': u'2N6DNQ4f4mQCvmRhZrKtPqW88hZPhMxp7jq'}, {u'pending_received_balance': u'0.00000000', u'available_balance': u'0.00000000', u'label': u'shibe2', u'user_id': 3, u'address': u'2N9JDPRF21kdUvgmzyioiUGpYPnuJ9orTmh'}, {u'pending_received_balance': u'0.00000000', u'available_balance': u'0.00000000', u'label': u'shibe3', u'user_id': 4, u'address': u'2MvcKnCQ83NdM1ZrBYTjjUdJyKJewHZGWv7'}]}}
        )
    print_flat(sample)

def test_block_io(bio_api_key, bio_spin):
    block_io = BlockIo(bio_api_key, bio_spin, 2)
    print_flat(block_io.get_my_addresses())

#
# Create the award transaction
#
# def create_award_transaction():
#     print "tbd create_award_xact"
#
# Test the award transaction
#
# def test_create_award_transaction():
#     print "tbd create_award_xact"
#

#
# Create the bounty transaction
#
# def create_bounty_transaction():
#     print "tbd create_bounty_xact"
#
# Test the bounty transaction
#
# def create_bounty_transaction():
#     print "tbd create_bounty_xact"
#

def get_secrets(secrets):
    status = 0
    homedir = os.path.expanduser('~')
    config_file = homedir + '/.multibounty/secrets.ini'
    if (os.path.isfile(config_file) != True):
        print "I quit. Expected your block_io secrets in an ini file here: " + config_file
        exit()
    config_handle = open(config_file, 'r')

    parser = ConfigParser.SafeConfigParser()
    try:
        parser.read(config_file)
    except ConfigParser.ParsingError, err:
        print "Can't read from config file at all."
        status = 1
    try:
        secrets.bio_spin = parser.get('blockio', 'author_spin', 0)
        secrets.bio_api_key = parser.get('blockio', 'author_api_key', 0)
    except:
        print "Config file present but messed up."
        status = 2

    config_handle.close()
    return status

def main():
    multibounty_secrets = Secrets()
    get_secrets(multibounty_secrets)
    print str(multibounty_secrets)
    test_block_io(multibounty_secrets.bio_api_key,multibounty_secrets.bio_spin)

if __name__ == '__main__':
    main()

