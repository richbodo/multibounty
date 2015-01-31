# block.io test

from block_io import BlockIo
import ConfigParser
import os
import pdb
import datetime
from decimal import *
import json
import six # for python2 back-compatibility in printing messages using print as a function
import random
import sys


class Secrets:
    def __init__(self):
        self.bio_spin=0
        self.bio_api_key=0
        self.bio_doge_api_key=0
    def __str__(self):
        return ("Block IO Secret Pin: " + str(self.bio_spin) + "\n"
                "Block IO Bitcoin API Key: " + str(self.bio_api_key) + "\n"
                "Block IO Doge API Key: " + str(self.bio_doge_api_key) )

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

#
# Block IO sanity check 
#
def test_block_io(bio_api_key, bio_spin):
    block_io = BlockIo(bio_api_key, bio_spin, 2)
    print_flat(block_io.get_my_addresses())
#
# Straight up copy of the block.io dtrust.py example
#
def block_io_dtrust_example(bio_api_key, bio_spin):
    version = 2 # API version

    # use a testnet api key here, say, dogecoin
    block_io = BlockIo(bio_api_key, bio_spin, version)
    getcontext().prec = 8 # coins are 8 decimal places at most

    # create a new address with a random label
    address_label = 'dtrust'+str(int(random.random()*10000))

    # create the key objects for each private key
    keys = [ BlockIo.Key.from_passphrase('alpha1alpha2alpha3alpha4'), BlockIo.Key.from_passphrase('alpha2alpha3alpha4alpha1'), BlockIo.Key.from_passphrase('alpha3alpha4alpha1alpha2'), BlockIo.Key.from_passphrase('alpha4alpha1alpha2alpha3') ]

    pubkeys = []

    for key in keys:
        pubkeys.insert(len(pubkeys), key.pubkey_hex())
        six.print_(key.pubkey_hex())

    # create a dTrust address that requires 4 out of 5 keys (4 of ours, 1 at Block.io).
    # Block.io automatically adds +1 to specified required signatures because of its own key

    print "* Creating a new 4 of 5 MultiSig address for DOGETEST"
    six.print_(','.join(str(x) for x in pubkeys))
    response = block_io.get_new_dtrust_address(label=address_label,public_keys=','.join(str(x) for x in pubkeys),required_signatures=3)

    # if you want this to be a green address (instant coin usage), add make_green=1 to the above call's parameters
    # if choosing a green address, you will not receive a redeem_script in the response
    # this is because Block.io must guarantee against double spends for green addresses

    # what's our new address?
    new_dtrust_address = response['data']['address']
    six.print_(">> New dTrust Address on Network=", response['data']['network'], "is", new_dtrust_address)

    # save this redeem script so you can use this address without depending on Block.io
    six.print_(">> Redeem Script:", response['data']['redeem_script'])

    # let's deposit some coins into this dTrust address of ours
    six.print_("* Sending 50 DOGETEST to", new_dtrust_address)
    response = block_io.withdraw_from_labels(from_labels='default', to_addresses=new_dtrust_address, amounts='50')
    six.print_(">> Transaction ID:", response['data']['txid']) # you can check this on SoChain or any other blockchain explorer immediately

    # since the above coins are coming from a Block.io green address (label=default, 2 of 2, visible on dashboard at Block.io),
    # they are spendable instantly
    # let's do that: spend coins from our dTrust address
    six.print_("* Getting address balance for", new_dtrust_address)
    response = block_io.get_dtrust_address_balance(address=new_dtrust_address)
    available_balance = response['data']['available_balance']
    six.print_(response)

    six.print_(">> Available Balance in", new_dtrust_address, "is", available_balance, response['data']['network'])

    # let's send coins back to the default address we withdraw from just now
    # use high precision decimals when dealing with money (8 decimal places)
    amount_to_send = Decimal(available_balance) - Decimal('1.0') # the amount minus the network fee needed to transact it

    six.print_("* Sending", "%0.8f" % amount_to_send, "back to 'default' address")

    # detour: what was our default address for the Dogecoin Testnet?
    default_address = block_io.get_address_by_label(label='default')['data']['address']
    six.print_(">> 'default' address:", default_address)

    # create the withdrawal request
    six.print_("* Creating withdrawal request")

    response = block_io.withdraw_from_dtrust_addresses(from_addresses=new_dtrust_address,to_addresses=default_address,amounts=("%0.8f" % amount_to_send))

    # the response contains data to sign and all the public_keys that need to sign it
    # you can distribute this response to all of your machines the contain your private keys
    # and have them inform block.io after signing the data
    # from anywhere, you can then finalize the transaction

    # below, we take this response, extract the data to sign, sign it and inform Block.io of the signatures right after we make them
    # for one key at a time
    six.print_(">> Withdrawal Reference ID:", response['data']['reference_id'])

    # sign the withdrawal request, one signature at a time

    for key in keys:

        for input in response['data']['inputs']:

            data_to_sign = input['data_to_sign']

            # find the object to put our signature in
            for signer in input['signers']:

                if signer['signer_public_key'] == key.pubkey_hex():
                    # found it, let's add the signature to this object
                    signer['signed_data'] = key.sign_hex(data_to_sign)

                    six.print_("* Data Signed By:", key.pubkey_hex())

        # let's have Block.io record this signature we just created
        block_io.sign_transaction(signature_data=json.dumps(response['data']))
        six.print_(">> Signatures relayed to Block.io for Public Key=", key.pubkey_hex())

    # finalize the transaction now that's it been signed by all our keys
    six.print_("* Finalizing transaction")
    response = block_io.finalize_transaction(reference_id=response['data']['reference_id'])
    six.print_(">> Transaction ID:", response['data']['txid'])
    six.print_(">> Network Fee Incurred:", response['data']['network_fee'], response['data']['network'])


#
# Create the award transaction
#
# Create a transaction awarding coin to a multisig script
# basically the first half of the dtrust example - using btctest
# Input:
# Return:
#
def create_award_transaction(bio_api_key, bio_spin):
    version = 2 # API version

    # using bitcoin testnet
    block_io = BlockIo(bio_api_key, bio_spin, version)
    getcontext().prec = 8 # coins are 8 decimal places at most

    # create a new address with a random label
    address_label = 'dtrust'+str(int(random.random()*10000))

    print "The dtrust address label is: " + address_label

    # create the key objects for each private key
    keys = [ BlockIo.Key.from_passphrase('alpha1alpha2alpha3alpha4'), BlockIo.Key.from_passphrase('alpha2alpha3alpha4alpha1'), BlockIo.Key.from_passphrase('alpha3alpha4alpha1alpha2'), BlockIo.Key.from_passphrase('alpha4alpha1alpha2alpha3') ]

    pubkeys = []

    for key in keys:
        pubkeys.insert(len(pubkeys), key.pubkey_hex())
        six.print_(key.pubkey_hex())

    # create a dTrust address that requires 4 out of 5 keys (4 of ours, 1 at Block.io).
    # Block.io automatically adds +1 to specified required signatures because of its own key

    print "* Creating a new 4 of 5 MultiSig address for BTCTEST"
    six.print_(','.join(str(x) for x in pubkeys))
    response = block_io.get_new_dtrust_address(label=address_label,public_keys=','.join(str(x) for x in pubkeys),required_signatures=3)

    # if you want this to be a green address (instant coin usage), add make_green=1 to the above call's parameters
    # if choosing a green address, you will not receive a redeem_script in the response
    # this is because Block.io must guarantee against double spends for green addresses

    # what's our new address?
    new_dtrust_address = response['data']['address']
    six.print_(">> New dTrust Address on Network=", response['data']['network'], "is", new_dtrust_address)

    # save this redeem script so you can use this address without depending on Block.io
    six.print_(">> Redeem Script:", response['data']['redeem_script'])

    # let's deposit some coins into this dTrust address of ours
    six.print_("* Sending .008 BTCTEST to", new_dtrust_address)
    response = block_io.withdraw_from_labels(from_labels='default', to_addresses=new_dtrust_address, amounts='.008')
    six.print_(">> Transaction ID:", response['data']['txid']) # you can check this on SoChain or any other blockchain explorer immediately


#
# Create the bounty transaction
#
# Create a transaction awarding coin to the editor
# Basically the second half of the dtrust example
#
# Input: editor_rcv_addy
# Returns:
#
def create_bounty_transaction(editor_rcv_address):
    # create the withdrawal request
    six.print_("* Creating withdrawal request")

    response = block_io.withdraw_from_dtrust_addresses(from_addresses=new_dtrust_address,to_addresses=default_address,amounts=("%0.8f" % amount_to_send))

    # the response contains data to sign and all the public_keys that need to sign it
    # you can distribute this response to all of your machines the contain your private keys
    # and have them inform block.io after signing the data
    # from anywhere, you can then finalize the transaction

    # below, we take this response, extract the data to sign, sign it and inform Block.io of the signatures right after we make them
    # for one key at a time
    six.print_(">> Withdrawal Reference ID:", response['data']['reference_id'])

    # sign the withdrawal request, one signature at a time

    for key in keys:

        for input in response['data']['inputs']:

            data_to_sign = input['data_to_sign']

            # find the object to put our signature in
            for signer in input['signers']:

                if signer['signer_public_key'] == key.pubkey_hex():
                    # found it, let's add the signature to this object
                    signer['signed_data'] = key.sign_hex(data_to_sign)

                    six.print_("* Data Signed By:", key.pubkey_hex())

        # let's have Block.io record this signature we just created
        block_io.sign_transaction(signature_data=json.dumps(response['data']))
        six.print_(">> Signatures relayed to Block.io for Public Key=", key.pubkey_hex())

    # finalize the transaction now that's it been signed by all our keys
    six.print_("* Finalizing transaction")
    response = block_io.finalize_transaction(reference_id=response['data']['reference_id'])
    six.print_(">> Transaction ID:", response['data']['txid'])
    six.print_(">> Network Fee Incurred:", response['data']['network_fee'], response['data']['network'])

#
# Grab the secrets out of an ini file so we don't have to check them into git!
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
        secrets.bio_api_key = parser.get('blockio', 'author_bitcoin_api_key', 0)
        secrets.bio_doge_api_key = parser.get('blockio', 'author_doge_api_key', 0)
    except:
        print "Config file present but messed up."
        status = 2

    config_handle.close()
    return status

def main():

    mb_secrets = Secrets()
    get_secrets(mb_secrets)

    #test_block_io(mb_secrets.bio_api_key,mb_secrets.bio_spin)

    #block_io_dtrust_example(mb_secrets.bio_doge_api_key, mb_secrets.bio_spin)

    create_award_transaction(mb_secrets.bio_api_key, mb_secrets.bio_spin)

if __name__ == '__main__':
    main()

