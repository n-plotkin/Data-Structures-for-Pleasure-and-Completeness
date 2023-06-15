import numpy as np
import ctypes
import sys

class Vector:
    def __init__(self):
        self._size = 0
        self._capacity = 1
        self._arr = self.makearray(1)    

    def __getitem__(self, i):
        if(0 <= i < self._size):
            return self._arr[i]
        else:
            raise Exception("Out of bounds.")
    
    def _checknumber(self, num):
        if not (isinstance(num, float) or isinstance(num, int)):
            raise Exception("This vector implementation only supports numeric data")

    def _resize(self, newcapacity):
        #create dummy with new capacity
        newarr = self.makearray(newcapacity)
        #loop through size and transfer over to dummy
        for i in range(self._size):
            newarr[i] = self._arr[i]
        #set arr to newarr
        self._capacity = newcapacity
        self._arr = newarr

    def _sizedowncheck(self):
        if self._size < self._capacity // 4:
            self._resize(self._capacity // 2)

    def _sizeupcheck(self):
        if self._size == self._capacity:
            self._resize(self._capacity * 2)

       
    def push(self, val):
        self._checknumber(val)
        #Set last index the val
        self._arr[self._size] = val
        self._size += 1
        #check for resize
        self._sizeupcheck()
    
    def pop(self):
        if self._size > 0:
            r = self._arr[self._size-1]
            self._arr[self._size-1] = 0
            self._size -= 1
            self._sizedowncheck()
            return r
        return None

        
    def insert(self, index, val):
        self._checknumber(val)

        if index < 0:
            raise Exception("Out of bounds.")

        #if index is end of list, greater than size, just push
        if index >= self._size:
            self.push(val)
            return
        
        # Determine necessary size of dummyarray
        if self._size+1 == self._capacity:
            self._capacity = self._capacity*2
            newarr = self.makearray(self._capacity)  
        else:
            newarr = self.makearray(self._capacity)
        
        #meat of transfer
        if index > 0:
            for i in range(0, index-1):
                newarr[i] = self._arr[i]
        newarr[index] = val
        for i in range(index, self._size):
            newarr[i+1] = self._arr[i]
        
        self._size += 1
        self._arr = newarr


    def delete(self, index):

        if index < 0:
            raise Exception("Out of bounds.")

        #if index is end of list, just pop
        if index == self._size-1:
            return self.pop()
        
        if self.isEmpty():
            return None
        
        newarr = self.makearray(self._capacity)
        
        #meat of transfer
        if index > 0:
            for i in range(0, index):
                newarr[i] = self._arr[i]
        for i in range(index, self._size-1):
            newarr[i] = self._arr[i+1]
        
        self._size -= 1
        self._arr = newarr

        self._sizedowncheck()


    def isEmpty(self):
        if self._size == 0:
            return True
        return False

    
    def __len__(self):
        return self._size

    def __str__(self):
        string = "{"
        for i in range(self._size):
            string += " \"" + str(self._arr[i]) + "\","
        string += " }"

        return string

    def __iter__(self):
        self._iterator = -1
        return self
    
    def __next__(self):
        if self._iterator+1 == self._size:
            raise StopIteration
        self._iterator += 1
        return self._arr[self._iterator]

    def copy(self):
        copy = Vector()
        for i in self:
            copy.push(i)
        return copy
            
    
    def __add__(self, item):
        if isinstance(item, int) or isinstance(item, float):
            newarr = self.copy()
            newarr.push(item)
            return newarr
        if isinstance(item, Vector):
            newarr = self.copy()
            for i in range(0, len(item)):
                newarr.push(item[i])
            return newarr
        if isinstance(item, list) or isinstance(item, tuple):
            #check if it's numeric
            try:
                listnumeric = tuple(map(float, item))
            except TypeError:
                raise TypeError("Your list must be numeric.")

            #if so newarr, push all of the second list to the end
            newarr = self
            for i in range(0, len(item)):
                newarr.push(item[i])
            
            #return newarr
            return newarr
        raise TypeError("Your item must be numeric.")
    
    def makearray(self, capacity):
        return ((capacity*ctypes.py_object)())

            



            
def main():
    test = Vector()
    test1 = []

    for i in range (1, 10):
        test.insert(0, i)
        test1.insert(0, i)
        print(f"CTYPE: Items {test._size}, Length {len(test._arr)}, Capacity {test._capacity}, datasize: {sys.getsizeof(test._arr)}")


if __name__ == "__main__":
    main()



