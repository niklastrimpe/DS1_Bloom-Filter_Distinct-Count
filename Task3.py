import pandas as pd
import numpy as np
import hashlib
from collections import Counter

"""
Hashfunctions used for the implementation of bloom filter and Flajolet-Martin algorithm
"""
def hash_MD5(i):
    return int(hashlib.md5(repr(i).encode()).hexdigest(), 16)

def hash_SHA1(i):
    return int(hashlib.sha1(repr(i).encode()).hexdigest(), 16)

def hash_SHA224(i):
    return int(hashlib.sha224(repr(i).encode()).hexdigest(), 16)

def hash_SHA256(i):
    return int(hashlib.sha256(repr(i).encode()).hexdigest(), 16)

def hash_SHA384(i):
    return int(hashlib.sha384(repr(i).encode()).hexdigest(), 16)

def hash_SHA512(i):
    return int(hashlib.sha512(repr(i).encode()).hexdigest(), 16)

def hash_BLAKE2B(i):
    return int(hashlib.blake2b(repr(i).encode()).hexdigest(), 16)

def hash_BLAKE2S(i):
    return int(hashlib.blake2s(repr(i).encode()).hexdigest(), 16)


class BloomFilter:
    """
    Simple implementation of a bloom filter

    :param n: lenght of bloom filter
    :param k: number of hashfunctions to be used
    :param data: stream of keys to be inserter in den bloom filter
    """

    def __init__(self, n, k, data):
        self.n = n
        self.k = k
        self.data = data
        self.bitmap = np.array([0] * n)
        self.hashfunctions = [hash_MD5, hash_SHA1, hash_SHA256, hash_SHA224, 
                                hash_SHA384, hash_SHA512, hash_BLAKE2B, hash_BLAKE2S]

        for i in self.data:
            for hashfunction in self.hashfunctions[:k]:
                self.bitmap[hashfunction(i) % self.n] = 1
    
    def queryKey(self, key):
        """
        Query the bloom filter for a specific key

        :param key: key to be searched in the bloom filter
        :return: boolean if key is a match in the bloom filter or a miss
        """
        indicies = []
        result = True
        for hashfunction in self.hashfunctions[:self.k]:
            indicies.append(hashfunction(key) % self.n)
        for i in indicies:
            if self.bitmap[i] == 0:
                result = False
        return result

def realQuery(data, key):
    result = False
    for i in data:
        if i == int(key):
            result = True
    return result

def Flajolet_Martin(data):
    """
    Implementation of the Flajolet_Martin algorithm for an approximative distinct count

    :param data: stream of data to perform distinct count on
    """
    bitmap = 0

    def least1(x, L):
        if x == 0:
            return 2**L
        return x & -x

    for i in data:
        h = hash_MD5(i)
        bitmap |= least1(h, 24)

    return least1(~bitmap, 24) / 0.77351

def realCount(data):
    """
    Implementation of a real distinct count

    :param data: stream of data to perform distinct count on
    """
    return(len(Counter(data)))


"""
Test
  
bloomfilter = BloomFilter(40000, 5, pd.read_csv('data/codon_usage.csv')["SpeciesID"])
bloomfilter.queryKey("100220")
bloomfilter.queryKey("100219")
print("FM: ", Flajolet_Martin(pd.read_csv('data/codon_usage.csv')["Kingdom"]))
print("Real Count: ", realCount(pd.read_csv('data/codon_usage.csv')["Kingdom"]))

"""
