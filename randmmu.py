from mmu import MMU
import random
from page import PAGE



class RandMMU(MMU):
    def __init__(self, frames):
        # TODO: Constructor logic for RandMMU
        self.frames = frames
        self.total_read = 0
        self.total_write = 0
        self.total_pagefault = 0
        self.pagetable = []

        pass

    def set_debug(self):
        # TODO: Implement the method to set debug mode
        pass

    def reset_debug(self):
        # TODO: Implement the method to reset debug mode
        pass

    def read_memory(self, page_number):
        # TODO: Implement the method to read memory
        # print(page_number)
        for i in self.pagetable:
            # print(i.pagenumber)
            if (i.pagenumber == page_number):
                return
        self.load_page(page_number)
        pass

    def write_memory(self, page_number):
        # TODO: Implement the method to write memory
        print("yes")
        for i in self.pagetable:
            if (i.pagenumber == page_number):
                print("yes")
                i.set_bit(1)
                return
        self.load_page(page_number) 
        
        


        pass

    def get_total_disk_reads(self):
        # TODO: Implement the method to get total disk reads
        return self.total_read

    def get_total_disk_writes(self):
        # TODO: Implement the method to get total disk writes
        return self.total_write
    
    def get_total_page_faults(self):
        # TODO: Implement the method to get total page faults
        return self.total_pagefault

    def load_page(self,page_number):
        self.total_pagefault += 1
        if(len(self.pagetable) < self.frames):
            self.pagetable.append(PAGE(page_number))
            self.total_read += 1
        else:
            num = random.randint(0,self.frames-1)
            if (self.pagetable[num].dirtybit == 1):
                self.total_write += 1
            self.pagetable[num] = PAGE(page_number)
            self.total_read += 1




        
             

