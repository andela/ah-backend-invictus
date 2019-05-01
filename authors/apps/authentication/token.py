import os
import binascii
import random


def generate_token():
    """ generates a random code """

    min_length = 10
    max_length = 50
    length = random.randint(min_length, max_length)

    # generate the token
    return binascii.hexlify(
        os.urandom(max_length)
    ).decode()[0:length]
