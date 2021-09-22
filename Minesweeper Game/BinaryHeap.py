# Class implementing the PRIORITY_QUEUE ADT as a binary heap.

class BinHeap:
    # Constructs a new binary heap with the given capacity and
    # less-than function for type X.
    def __init__(self, capacity, lt):
        self._data = [None]*capacity
        self._size = 0
        self._lt = lt

    def len(self):
        return self._size

    def insert(self, new_element):
        self._data[self.len()] = new_element
        self._size = self.len() + 1
        if self.len() > 1:
            self._bubble_up(self.len()-1)

    def find_min(self):
        if self.len() == 0:
            print("The priority queue is empty")
        else:
            return self._data[0]

    def remove_min(self):
        if self.len() == 0:
            print("The priority queue is empty")
        if self.len() == 1:
            self._size = self.len() - 1
            self._data[0] = None
        elif self.len() > 1:
            self._size = self.len() - 1
            self._data[0] = self._data[self.len()]
            self._data[self.len()] = None
            self._percolate_down(0)
            
    def _swap(self, index_a, index_b):
        at_a = self._data[index_a]
        at_b = self._data[index_b]
        self._data[index_a] = at_b
        self._data[index_b] = at_a
        
    def _find_parent_index(self, elem_index):
        if elem_index == 0:
            print("The 0 element has no parents")
        elif elem_index%2 == 0:
            return (elem_index-1)//2
        else:
            return (elem_index-1)//2
        
    def _bubble_up(self, elem_index):
        #println("Bubble up was called")
        elem_parent_index = self._find_parent_index(elem_index)
        elem_val = self._data[elem_index]
        elem_parent_val = self._data[elem_parent_index]
        while (self._lt(elem_val, elem_parent_val) and elem_index != 0):
            #self.see()
            #println("elem_index: %p, elem_parent_index: %p", elem_index, elem_parent_index)
            self._swap(elem_index, elem_parent_index)
            elem_index = elem_parent_index
            elem_val = self._data[elem_index]
            if elem_index != 0:
                elem_parent_index = self._find_parent_index(elem_index)
                elem_parent_val = self._data[elem_parent_index]
            #self.see()
                
    def _find_left_index(self, elem_index):
        left_index = (elem_index*2 + 1)
        if left_index >= self.len():
            return 
        return left_index
    
    def _find_right_index(self, elem_index):
        right_index = (elem_index*2 + 2)
        if right_index >= self.len():
            return
        return right_index
    
    def _find_min_child_index(self, elem_index):
        left_child_index = self._find_left_index(elem_index)
        right_child_index = self._find_right_index(elem_index)
        #println("left_child index: %p", left_child_index)
        #println("right_child_index: %p", right_child_index)
        if (left_child_index == None) and (right_child_index == None):
            return
        elif right_child_index == None:
            if self._lt(self._data[left_child_index], self._data[elem_index]):
                return left_child_index
        elif self._lt(self._data[left_child_index], self._data[right_child_index]):
            if self._lt(self._data[left_child_index], self._data[elem_index]):
                return left_child_index
        elif self._lt(self._data[right_child_index], self._data[elem_index]):
                return right_child_index
        #else:
        #    return left_child_index
        
    def _percolate_down(self, elem_index):
        #self.see()
        min_child_index = self._find_min_child_index(elem_index)
        #println("min_child_index: %p", min_child_index)
        while min_child_index != None:
            self._swap(elem_index, min_child_index)
            elem_index = min_child_index
            min_child_index = self._find_min_child_index(elem_index)
            
    def see(self):
        println('%p', self._data)

def bin_heap_tests():
    h = BinHeap(10, lambda x, y: x < y)
    h.insert(1)
    assert h.len() == 1
    assert h.find_min() == 1
    h.remove_min()
    assert h.len() == 0
    #assert h.find_min() == None
    h.insert(1)
    h.insert(2)
    assert h.find_min() == 1
    h.insert(0) 
    assert h.find_min() == 0
    h.insert(0)
    assert h.find_min() == 0
    h.insert(100)
    assert h.find_min() == 0
    h.insert(3)
    h.insert(4)
    h.insert(5)
    h.insert(6)
    h.insert(7)
    assert h.len() == 10

# Sorts a vector of Xs, given a less-than function for Xs.
#
# This function performs a heap sort by inserting all of the
# elements of v into a fresh heap, then removing them in
# order and placing them back in v.
def heap_sort(v, lt):
    x = BinHeap(len(v), lt)
    for each_val in v:
        x.insert(each_val)
    for each_index in range(len(v)):
        v[each_index] = x.find_min()
        x.remove_min()

def heap_sort_tests():
    v = [3, 6, 0, 2, 1]
    heap_sort(v, lambda x, y: x > y)
    assert v == [6, 3, 2, 1, 0]
    
    c = [-3, 2, -7, -1, 1, 0]
    heap_sort(c, lambda x, y: (x*x) < (y*y))
    assert c == [0,-1,1,2,-3,-7]
