# block.io test

from block_io import BlockIo
import block_io_sanity_checks
import ConfigParser
import os
import pdb
import datetime
from decimal import *
import json
import six # for python2 back-compatibility in printing messages using print as a function
import random
import sys

# Secret data from a restricted file
#
class Secrets:
    def __init__(self):
        self.bio_doge_api_key=0 # DogeCoin Test Net for example
        self.bio_auth_spin=0 # All BTC test net for now
        self.bio_auth_key=0
        self.bio_plat_key=0
        self.bio_plat_spin=0
    def __str__(self):
        return ("Block IO Author API Key: " + str(self.bio_auth_key) + "\n"
                "Block IO Author Secret Pin: " + str(self.bio_auth_spin) + "\n"
                "Block IO Platform API Key: " + str(self.bio_plat_key) + "\n"
                "Block IO Platform Secret Pin: " + str(self.bio_plat_spin)
        )

# Transaction data for both bounty and award transactions
#
class Transaction:
    def __init__(self):
        self.amount=0
        self.editor_rcv_address=0
        self.script_hash=0
        self.expected_fee=0
    def __str__(self):
        return ("Transaction amountq Amount: " + str(self.amount) + "\n"
                "Editor Receive Address: " + str(self.editor_rcv_address) + "\n"
                "Script Hash: " + str(self.script_hash)  + "\n"
                "Expected Transaction Fee: " + str(self.expected_fee) + "\n"
                )

#
# Create a transaction awarding coin from AUTHOR to a SCRIPT(must be signed by author and platform)
# BUG - Need public keys of author and platform - which I don't know how to find.  Not sure why random keys work in the example.
# Maybe it's o.k. to just make up passphrases and generate private keys from those, then public keys, which is what it looks like is going on here.
# Instead of doing this, probably what we need to do is:
#
# 1) Generate AUTHOR private and public keys
# 2) Generate PLATFORM private and public keys
# 3) Generate the multisig address
# 4) Generate the BOUNTY transaction
#
# Probably in separate functions
#
# So need to rewrite this whole thing
#
#
#
def create_bounty(auth_key, auth_spin, bounty_amount):

    version = 2 # API version

    # using bitcoin testnet
    block_io_author = BlockIo(auth_key, auth_spin, version)
    getcontext().prec = 8 # coins are 8 decimal places at most

    # create a new address with a random label
    address_label = 'dtrust'+str(int(random.random()*10000))

    print "The dtrust address label is: " + address_label

    # create the key objects for each private key
    keys = [ BlockIo.Key.from_passphrase('alpha3alpha4alpha1alpha2'), BlockIo.Key.from_passphrase('alpha4alpha1alpha2alpha3') ]

    pubkeys = []

    for key in keys:
        pubkeys.insert(len(pubkeys), key.pubkey_hex())
        six.print_(key.pubkey_hex())

    # create a dTrust address that requires 2 out of 2 keys.
    # Block.io automatically adds +1 to specified required signatures because of its own key

    print "* Creating a new 2 of 2 MultiSig address for BTCTEST"
    six.print_(','.join(str(x) for x in pubkeys))
    response = block_io_author.get_new_dtrust_address(label=address_label,public_keys=','.join(str(x) for x in pubkeys),required_signatures=2)

    # if you want this to be a green address (instant coin usage), add make_green=1 to the above call's parameters
    # if choosing a green address, you will not receive a redeem_script in the response
    # this is because Block.io must guarantee against double spends for green addresses

    # what's our new address?
    new_dtrust_address = response['data']['address']
    six.print_(">> New dTrust Address on Network=", response['data']['network'], "is", new_dtrust_address)

    # save this redeem script so you can use this address without depending on Block.io
    six.print_(">> Redeem Script:", response['data']['redeem_script'])

    # let's deposit some coins into this dTrust address of ours
    print "* Sending {}".format(bounty_amount) + " to {}".format(new_dtrust_address)
    response = block_io_author.withdraw_from_labels(from_labels='default', to_addresses=new_dtrust_address, amounts=bounty_amount)
    six.print_(">> Transaction ID:", response['data']['txid']) # you can check this on SoChain or any other blockchain explorer immediately


# Award the bounty
#
# Create a transaction awarding coin from SCRIPT to the EDITOR
#
# BUG - AUTHOR and PLATFORM both need to unlock the script with their private keys.
# It looks like the dtrust example just makes up passphrases, private keys and public keys, so I haven't figured out why that works.
#
def award_bounty(plat_key, plat_spin, bounty_script_address, editor_rcv_address, bounty_amount):

    block_io_platform = BlockIo(plat_key, plat_spin, version)
    getcontext().prec = 8 # coins are 8 decimal places at most

    # create the key objects for each private key
    keys = [ BlockIo.Key.from_passphrase('alpha3alpha4alpha1alpha2'), BlockIo.Key.from_passphrase('alpha4alpha1alpha2alpha3') ]

    pubkeys = []

    for key in keys:
        pubkeys.insert(len(pubkeys), key.pubkey_hex())
        six.print_(key.pubkey_hex())

    # create the withdrawal request
    six.print_("* Creating withdrawal request")

    response = block_io_platform.withdraw_from_dtrust_addresses(
        from_addresses=bounty_script_address,to_addresses=editor_rcv_address,amounts=("%0.8f" % bounty_amount))

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
        block_io_platform.sign_transaction(signature_data=json.dumps(response['data']))
        six.print_(">> Signatures relayed to Block.io for Public Key=", key.pubkey_hex())

    # finalize the transaction now that's it been signed by all our keys
    six.print_("* Finalizing transaction")
    response = block_io_platform.finalize_transaction(reference_id=response['data']['reference_id'])
    six.print_(">> Transaction ID:", response['data']['txid'])
    six.print_(">> Network Fee Incurred:", response['data']['network_fee'], response['data']['network'])

# Grab the secrets out of an ini file so we don't have to check them into git!
#
def get_secrets(secrets):
    """

    :rtype : integer - zero for success
    """
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

    secrets = Secrets()
    bounty_tx = Transaction()
    award_tx = Transaction()

    get_secrets(secrets)

    # Sanity Checks
    #
    #test_block_io(mb_secrets.bio_api_key,mb_secrets.bio_spin)
    #block_io_dtrust_example(mb_secrets.bio_doge_api_key, mb_secrets.bio_spin)

    bounty_tx.amount = .0001
    bounty_tx.expected_fee = .00001
    award_tx.expected_fee = .00001
    award_tx.editor_rcv_address = '2MzhYahdyuyH6Dv4MuKXxbX61rTgxBNFM4R'

    # Step 1 - Bounty Transaction
    # Funds are being taken from AUTHOR - using author_bitcoin_api_key
    # We need the public keys of the author and the platform to create the script, though...
    create_bounty(secrets.bio_api_key, secrets.bio_spin, bounty_tx.amount)

    # Step 2 - Decision (skipped for now - just decide to award total to one editor)
    award_tx.award_amount = ( bounty_tx.amount - bounty_tx.expected_fee - award_tx.expected_fee)

    # Step 3 - Award Transaction
    # Here we need both the author and the platform to sign the output, and their private keys are locked up in block.io, so...
    award_bounty(secrets.bio_plat_key, secrets.bio_plat_spin,
                 secrets.bio_auth_key, secrets.bio_auth_spin,
                 secrets.script_hash, award_tx.editor_rcv_address, award_tx.award_amount)

if __name__ == '__main__':
    main()

