class myRange:
    def __init__(self, start, stop=None, stepsize=1):

        #Check for bad stepsize
        if stepsize == 0:
            raise ValueError("Step cannot be zero.")
        
        #Check for special n range.
        if stop == None:
            #In this special case, we want to range 0 through n, therefore:
            start, stop = 0, start
        
        #Calculate effective length
        self._length = max(0, (stop - start + stepsize - 1) // stepsize)

        self._start, self._stepsize = start, stepsize
    
    #Return length of range.
    def __len__(self):
        return self._length
    #Gets an item
    def __getitem__(self, k):
        if(k < 0):
            k += len(self)
        if(0 <= k < self._length):
            return self._start + self._stepsize*k
        raise IndexError("Index out of range")

    #Python automatically generates an iterator



def main():
    for i in myRange(0, 10):
        print(i)

if __name__ == "__main__":
    main()