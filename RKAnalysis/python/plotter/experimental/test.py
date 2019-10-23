class SomeClass:
    def __init__(self):
        print "gay"
        self.arr = [] 
        #All SomeClass objects will have an array arr by default
    
    def insert_to_arr(self, value):
        self.arr.append(value)
gay = SomeClass()
