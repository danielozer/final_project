"""
---------------------------------------------------------------
Author          :   Daniel Ozer
Date            :   XXXX
Version         :   1.0
Description     :   all the function the have connection with security and encryptions
---------------------------------------------------------------
"""

#imports

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
import cPickle as pickle
import hashlib
from Crypto import Random
import base64
import os

#imports

BUFFER=2048

BLOCK_SIZE = 16

# the character used for padding--with a block cipher such as AES, the value
# you encrypt must be a multiple of BLOCK_SIZE in length.  This character is
# used to ensure that your value is always a multiple of BLOCK_SIZE
PADDING = '{'

pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)

def cut_for_blocks(data):
    """
    this func recv the string and cut it to blocks sort by size
    recv: string
    return:array of string
    """


    data_len=len(data)


    chunks, chunk_size = data_len, 100
    blocks=[ data[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]
    print blocks
    return blocks



def create_AES_key():
    """
    this func create an aes key
    recv: none
    return:aes key
    """
    # generate a random secret key
    secret = os.urandom(BLOCK_SIZE)

    # create a cipher object using the random secret
    cipher = AES.new(secret)

    return cipher


def public_key_nxt_client(p_k):
    """
    this func recv a public key which is not ready for encrpt and made it ready for encrypt
    recv: public key
    return: public key
    """

    pu_key = RSA.importKey(p_k)
    return pu_key
def get_public_key_from_other_side(recv_data):
    """
    this func recv  data string and transport it to public key
    recv: strind data
    return: public key
    """


    pu_key = RSA.importKey(pickle.loads(recv_data))

    print("***GOT PUBLIC KEY***"),pu_key.exportKey()

    pu_key = RSA.importKey(pu_key.exportKey())

    return pu_key

def create_key():
    """
    this func create privtae key(RSA)
    recv: none
    return:private key
    """
    random_generator = Random.new().read#get new random key
    key = RSA.generate(1024, random_generator)#larger is more secure!

    return key

def Public_Key(key):
    """
    the function create a new public key and return it

    input: ket
    output:  the public key
    """


    print "The public Key IS self:\n ", key.publickey().exportKey()



    return pickle.dumps(key.publickey().exportKey())

def DecryptMesg(enc_data,key):

    """

    this func recv mesg then it decrypt the mesg using RSA (public key)
    input: string (mesg ),key
    output:string mesg

    """
    binPrivKey = key.exportKey()
   # print "the private: "+ binPrivKey
    #enc_data=pickle.loads(enc_data)
    privKeyObj = RSA.importKey(binPrivKey)
    return privKeyObj.decrypt(enc_data)

def EncryptMesg(data,pu_key):

    """

    this func recv mesg then it encrypt the mesg using RSA (public key)
    input: string (mesg ),key
    output: string mesg encrpyt

    """

    data_encrypt = pu_key.encrypt(data, 32)#32 is random parameter used by RSA
    print data
    print "The Encrypted Data: " , data_encrypt
    print "*************    " ,type(data_encrypt)
    return data_encrypt




def EncryptDB(key, stringMesg):
    """
    this func recv mesg then it encrypt the mesg using AES
    input: string (mesg ),key
    output: string mesg encrpyt
    """

    return EncodeAES(key, stringMesg)


def DecryptDB(key,stringMesg):
    """

    this func recv mesg then it decrypt the mesg using AES
    input: string (mesg ),key
    output :string mesg

    """

    return DecodeAES(key, stringMesg)

def checksum_md5_text(text):

    """

    this func recv text and then hash it in md5 function
    input: string text
    output :string (md5)

    """
    return hashlib.md5(text).hexdigest()

def checksum_md5_file(file):

    """

    this func recv file and then hash it in md5 function to get the check sum
    input: string text
    output :string (md5)

    """
    return hashlib.md5(open(file,'rb').read()).hexdigest()

