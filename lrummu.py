from mmu import MMU
from collections import OrderedDict
class LruMMU(MMU):
    def __init__(self, frames):
        # TODO: Constructor logic for LruMMU
        self.frames = frames
        self.memory = OrderedDict()  #tracks pages in memory and their order of access
        self.total_disk_reads = 0
        self.total_disk_writes = 0
        self.total_page_faults = 0
        self.debug = False
        pass

    def set_debug(self):
        # TODO: Implement the method to set debug mode
        self.debug = True
        pass

    def reset_debug(self):
        # TODO: Implement the method to reset debug mode
        self.debug = False
        pass

    def read_memory(self, page_number):
        # TODO: Implement the method to read memory
        self.acess_mem(page_number, is_write=False)
        pass

    def write_memory(self, page_number):
        # TODO: Implement the method to write memory
        self.acess_mem(page_number, is_write=True)
        pass

    def acess_mem(self, page_number, is_write):
        if page_number in self.memory:
            #page found
            self.memory.move_to_end(page_number)
            if self.debug:
                print(f"page {page_number} tickled: moved to bottom.")
            if is_write:
                self.memory[page_number] = True
        else:
            #page fault
            self.total_page_faults += 1
            self.total_disk_reads += 1
            if self.debug:
                print(f"page {page_number} fault:put into memory.")

            if len(self.memory) >= self.frames:
                #no free frames, remove LRU page
                lru_page, modified = self.memory.popitem(last=False)
                if self.debug:
                    print(f"remove and replace LRU page {lru_page} with page {page_number}.")
                if modified:
                    self.total_disk_writes += 1  #write back if the page was modified

            # Load the new page into memory
            self.memory[page_number] = is_write  #track if the page is modified
    
    def get_total_disk_reads(self):
        # TODO: Implement the method to get total disk reads
        return self.total_disk_reads

    def get_total_disk_writes(self):
        # TODO: Implement the method to get total disk writes
        return self.total_disk_writes

    def get_total_page_faults(self):
        # TODO: Implement the method to get total page faults
        return self.total_page_faults
