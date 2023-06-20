import ctypes
import random

class HashBase:
    def __init__(self, m):
        #array used as our back end.
        self._arr = (m*ctypes.py_object)()
        #get our prime
        self._p = self._getprime(m)
        #set our m
        self._m = m
        #get a, b
        self._a, self._b = random.randrange(self._p), random.randrange(self._p)
        self._index = 0



    def insert(self, key, value):
        #hash the key
        hash = self._hash(key)
        #probe
        probed = self._probe(hash, key)
        #add key to table
        
        self._arr[probed[0]] = (key, value)
        if probed[1] == -1:
            return False
        return True

    def delete(self, key):
        #hash the key
        hash = self._hash(key)
        #probe
        probed = self._searchprobe(hash, key)
        #delete
        if probed[1] == -1:
            #if the key wasn't found:
            return False
        self._arr[probed[0]] = None
        return True

    def search(self, key):
        #hash
        hash = self._hash(key)
        
        #probe
        probed = self._searchprobe(hash, key)

        #check if not found, OR check if what we ended up on is our key
        if probed[1] == -1 or self._arr[probed[0]][0] != key:
            return -1
        
        #If not, return the VALUE from the array at the probed hash index
        return self._arr[probed[0]][1]



    def _isprime(self, num):
        if num < 2:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True

    def _getprime(self, m):
        for i in range(m, m*2):
            if self._isprime(i):
                return i            

    def _hash(self, hashable):
        #We'll use universal hashing
        hashed = (((hashable * self._a + self._b) % self._p) % self._m )            

        return hashed


    def _probe(self, hash, key):

        try:
            self._arr[hash][0]
        except ValueError:
            return (hash, -1)
        except TypeError:
            if self._arr[hash] == None:
                return (hash, -1)
        while self._arr[hash][0] != key:
            #probe linearly
            hash += 1
            #wrap around
            if hash == len(self._arr):
                hash = 0
            #check empty
            try:
                self._arr[hash][0]
            except ValueError:
                return (hash, -1)
            except TypeError:
                if self._arr[hash] == None:
                    return (hash, -1)
                                    
        return (hash, key)
    
    def _searchprobe(self, hash, key):
        ohash = hash

        while True:
            try:
                self._arr[hash][0]
            except ValueError:
                return (hash, -1)
            except IndexError:
                if hash >= len(self._arr):
                    hash = 0
                hash += 1
                continue
            except TypeError:
                if self._arr[hash] == None:
                    if hash >= len(self._arr):
                        hash = 0
                    hash += 1
                    continue

            if self._arr[hash][0] == key:
                return (hash, key)
            
            hash += 1


            if ohash == hash:
                break

        return (hash, -1)


    
    
    def __iter__(self):
        return self

    def __next__(self):
        #find next occupied index

        #set empty
        empty = True
        while empty == True:
            #Check if index is last index
            if self._index == len(self._arr):
                raise StopIteration
            #Try to check the arr at that index
            try:
                #if non-empty, iterate and break loop
                val = self._arr[self._index]
                self._index += 1
                if val != None:
                    return val
            except ValueError:
                #if empty, iterate till next non-empty
                self._index += 1    

class HashTable:
    def __init__(self):
        #default m
        self._m = 2
        #make hashbase
        self._hb = HashBase(self._m)
        #no elements
        self._size = 0

    def insert(self, key, value):
        if self._hb.insert(key, value) == False:
            self._size += 1
            self._checksize()

    def delete(self, key):
        if self._hb.delete(key) == True:
            self._size -= 1
            self._checksize()

    def search(self, key):
        return self._hb.search(key)

    def _checksize(self):
        if self._size > self._m // 2:
            self._resize(self._m*2)
        if self._size < (self._m / 4):
            self._resize(self._m // 2)

    def _resize(self, m1):
        hb1 = HashBase(m1)
        for i in self._hb:
            hb1.insert(i[0], i[1])
        self._hb = hb1
        self._m = m1
            
#old tests
def main():
    ht = HashTable()
    for i in range(1, 400):
        ht.insert(i, i*11)

    for i in range(1, 400):
        print(ht.search(i))

    for i in ht._hb:
        print(i)

    for i in range(1, 400):
        ht.delete(i)

    for i in range(1, 400):
        print(ht.search(i))

    for i in ht._hb:
        print(i)


if __name__ == "__main__":
    main()
