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
import random
import string
from pprint import pprint
import bio_sanity_checks

class Secrets:
# Secret data from a restricted file
#
    def __init__(self):
        self.bio_doge_api_key = 0 # DogeCoin Test Net for example
        self.bio_spin = 0 # All BTC test net for now
        self.bio_key = 0

    def __str__(self):
        return ("BlockIO API Key: " + str(self.bio_key) + "\n"
                "BlockIO Secret Pin: " + str(self.bio_spin) + "\n"
        )

class Transaction:
# Transaction data for both bounty and award transactions
    def __init__(self):
        self.input_amount = 0
        self.rcv_address = 0
        self.script_hash = 0
        self.expected_fee = 0
    def __str__(self):
        return ("Total BTC to use: " + str(self.amount) + "\n"
                "Receive Address to send to: " + str(self.editor_rcv_address) + "\n"
                "Script Hash: " + str(self.script_hash)  + "\n"
                "Expected Transaction Fee: " + str(self.expected_fee) + "\n"
                )

class Keys:
# Bitcoin private and matching public key pair
    def __init__(self):
        self.private_key = 0  # This is actually a block_io "key" object that contains a private key and some other stuff
        self.public_key = 0  # This I'm using to store an actual public key generated from that private key
    def __str__(self):
        return ("Private Key: " + str(self.private_key) + "\n"
                "Public Key: " + str(self.public_key) + "\n"
                )

def create_bounty(author_secrets, author_keys, platform_keys, bounty_tx):
#
# Create a transaction awarding coin from an AUTHOR to a SCRIPT.
# Script is multisig must be signed by author and platform
    # Block IO Settings
    bio_version = 2 # Block.IO API version
    getcontext().prec = 8 # coins are 8 decimal places at most

    author_api_object = BlockIo(author_secrets.bio_key, author_secrets.bio_spin, bio_version)

    # create a dTrust address that requires 2 out of 2 keys.
    # Block.io automatically adds +1 to specified required signatures because of its own key
    # create a new address with a random label

    address_label = 'dtrust'+str(int(random.random()*10000))

    print "The dtrust address label is: " + address_label
    print "* Creating a new 2 of 2 MultiSig address for BTCTEST"

    pubkeys = []
    pubkeys.insert(len(pubkeys), author_keys.public_key)
    pubkeys.insert(len(pubkeys), platform_keys.public_key)
    public_keys_for_multisig = ','.join(pubkeys)
    print "No idea why block.io does not like these keys: " + str(pubkeys)

    # Required signatures is 3: one for author, one for platform, and one for block.io, I think
    # Yet, the example shows one less than that.
    response = author_api_object.get_new_dtrust_address(label=address_label,public_keys=public_keys_for_multisig, required_signatures=2)

    # what's our new address?
    new_dtrust_address = response['data']['address']
    six.print_(">> New dTrust Address on Network=", response['data']['network'], "is", new_dtrust_address)

    # save this redeem script so you can use this address without depending on Block.io
    six.print_(">> Redeem Script:", response['data']['redeem_script'])

    # let's deposit some coins into this dTrust address of ours
    print "* Sending {}".format(bounty_tx.input_amount) + " to {}".format(new_dtrust_address)
    response = author_api_object.withdraw_from_labels(from_labels='default', to_addresses=new_dtrust_address, amounts=bounty_tx.input_amount)
    six.print_(">> Transaction ID:", response['data']['txid']) # you can check this on SoChain or any other blockchain explorer immediately

def award_bounty(auth_keys, plat_keys, bounty_tx, award_tx):
# Award the bounty
#
# Create a transaction awarding coin from SCRIPT to the EDITOR
#
# BUG - AUTHOR and PLATFORM both need to unlock the script with their private keys.
# It looks like the dtrust example just makes up passphrases, private keys and public keys, so I haven't figured out why that works.
#
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

def get_secrets(author_secrets, platform_secrets, editor_fixtures):
# Grab the secrets out of an ini file so we don't have to check them into git!
#
    status = 0
    homedir = os.path.expanduser('~')
    config_file = homedir + '/.multibounty/secrets.json'

    if (os.path.isfile(config_file) != True):
        print "I quit. Expected your block_io secrets in a json file here: " + config_file
        exit()

    config_handle = open(config_file, 'r')
    data = json.load(config_handle)
    #pprint(data)
    config_handle.close()

    author_secrets.bio_spin = data["author"]["spin"]
    author_secrets.bio_key = data["author"]["bitcoin_testnet_api_key"]
    platform_secrets.bio_key = data["platform"]["spin"]
    platform_secrets.bio_spin = data["platform"]["bitcoin_testnet_api_key"]
    editor_fixtures.rcv_address = data["editor"]["rcv_addy"]

def generate_btc_keys(secrets, keys_to_return):
    # Block IO Settings
    bio_version = 2 # Block.IO API version
    getcontext().prec = 8 # coins are 8 decimal places at most

    # create the key objects for each private key
    random_text = "".join( [random.choice(string.ascii_letters) for i in xrange(15)] )

    keys_to_return.private_key = BlockIo.Key.from_passphrase(random_text)  # This is a complex Block IO key object
    keys_to_return.public_key = keys_to_return.private_key.pubkey_hex()  # While this is just text

    return

def main():

    author_secrets = Secrets()
    author_keys = Keys()

    platform_secrets = Secrets()
    platform_keys = Keys()

    bounty_tx = Transaction()
    award_tx = Transaction()
    editor_fixtures = Transaction()

    get_secrets(author_secrets, platform_secrets, editor_fixtures)

    # Generate AUTHOR private and public keys
    generate_btc_keys(author_secrets, author_keys)
    print "Author Pubkey:" + str(author_keys.public_key)

    # Generate PLATFORM private and public keys
    generate_btc_keys(platform_secrets, platform_keys)
    print "Platform Pubkey:" + str(platform_keys.public_key)

    # Step 1 - Bounty Transaction
    # Funds are being taken from AUTHOR - using author_bitcoin_api_key
    # We need the public keys of the author and the platform to create the script
    bounty_tx.input_amount = .0001
    bounty_tx.expected_fee = .00001
    create_bounty(author_secrets, author_keys, platform_keys, bounty_tx)

    # Sanity Check
    # bio_sanity_checks.block_io_dtrust_example(author_secrets.bio_key, author_secrets.bio_spin)

    # Step 2 - Decision (skipped for now - just decide to award total to one editor)
    award_tx.input_amount = ( bounty_tx.input_amount - bounty_tx.expected_fee )

    # Step 3 - Award Transaction
    # Here we need both the author and the platform to sign the output.
    award_tx.expected_fee = .00001
    award_bounty(author_keys, platform_keys, bounty_tx, award_tx, editor_fixtures.rcv_address)

if __name__ == '__main__':
    main()

