from mmu import MMU

class page:
    def __init__(self,page_num):
        self.page_num = page_num
        self.ref_bit =0

    def __repr__(self):
        return f"Page({self.page_number}, ref_bit={self.reference_bit})"


class ClockMMU(MMU):
    def __init__(self, frames):
        self.frames= [None]* frames
        self.clock_tip = 0
        self.count_diskR= 0
        self.count_diskW=0
        self.count_page_faults=0
        self.debug_mode=False
        self.total_frames= frames

    def set_debug(self):
        self.debug_mode = True

    def reset_debug(self):
        self.debug_mode = False
    
    def clock (self,page_number):
        pass

    def read_memory(self, page_number):

        for page in self.frames:
            if page and page.page_num == page_number: 
                    page.ref_bit==1
                    if self.debug_mode:
                        print("Read hit")
                    return
            
        self.clock(page_number)


    def write_memory(self, page_number):
        # TODO: Implement the method to write memory
        pass



    def get_total_disk_reads(self):
        # TODO: Implement the method to get total disk reads
        return -1

    def get_total_disk_writes(self):
        # TODO: Implement the method to get total disk writes
        return -1

    def get_total_page_faults(self):
        # TODO: Implement the method to get total page faults
        return -1


# approx least recently used  initilaly set all the refernces to 1 then 
# if the refenrce bit is 0, the page is chosen for replacemnt 
# if the ref bit is 1, the bit is cleared and the clock hand moves to the next page

# disk reads loading a page from disk 
# disk writes saving a modified page back to disk before replacing it 