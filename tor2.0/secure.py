__author__ = "daniel ozer"

                        
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto import Random
import cPickle as pickle
import hashlib
import socket



BUFFER=2048



def get_public_key_from_other_side(recv_data):


    pu_key = RSA.importKey(pickle.loads(recv_data))

    print("***GOT PUBLIC KEY***"),pu_key.exportKey()

    pu_key = RSA.importKey(pu_key.exportKey())

    return pu_key



def create_key():
    random_generator = Random.new().read#get new random key
    key = RSA.generate(1024, random_generator)#larger is more secure!

    return key

def Publik_Key(key):
    """
    the function create a new public key and return it

    input: addr
    output:  the public key
    """


    print "The public Key IS:\n ", key.publickey().exportKey()
    print type(key)


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
    print "The Encrypted Data: " , data_encrypt
    print "*************    " ,type(data_encrypt)
    return data_encrypt




def EncryptDB(stringMesg,key):
    """
    this func recv mesg then it encrypt the mesg using AES
    input: string (mesg ),key
    output: string mesg encrpyt
    """

    encryption_suite = AES.new(key, AES.MODE_CBC, 'This is an IV456')
    cipher_text = encryption_suite.encrypt(stringMesg)
    return cipher_text


def decryptDB(stringMesg,key):
    """

    this func recv mesg then it decrypt the mesg using AES
    input: string (mesg ),key
    output :string mesg

    """

    decryption_suite = AES.new(key, AES.MODE_CBC, 'This is an IV456')
    plain_text = decryption_suite.decrypt(stringMesg)

    return  plain_text



def checksum_md5_text(text):

    """

    this func recv text and then hash it in md5 function
    input: string text
    output :string (md5)

    """
    return hashlib.md5("filename.exe").hexdigest()

def checksum_md5_file(file):

    """

    this func recv file and then hash it in md5 function to get the check sum
    input: string text
    output :string (md5)

    """
    return hashlib.md5(open(file,'rb').read()).hexdigest()



