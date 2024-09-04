from mmu import MMU

class page:
    def __init__(self,page_num):
        self.page_num = page_num
        self.ref_bit =0
        self.dirty= False

    def __repr__(self):
        return f"Page({self.page_number}, ref_bit={self.reference_bit}, dirty={self.dirty})"


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
    

    def clock_first_pass(self,page_number):

            current = self.frames[self.clock_tip]
            if current is None:
                self.frames[self.clock_tip] = current.page_num
                self.frames[self.clock_tip].ref_bit=1
                self.count_diskR+=1
                if self.debug_mode:
                    print("loading page")
                self.clock_tip=(self.clock_tip+1)% self.num_frames
                return -1
            else :
                if current.ref_bit==0 and current.dirty== False:
                    self.frames[self.clock_hand] = Page(page_number)
                    self.frames[self.clock_hand].reference_bit = 1
                    self.disk_reads += 1
                    self.clock_hand = (self.clock_hand + 1) % self.num_frames
                    return -1
                else:
                    current.reference_bit = 0
                    self.clock_hand = (self.clock_hand + 1) % self.num_frames
                    return +1
    
    def sec_clock_pass(self,page_number):
        
    
    
    def clock(self,page_number):
        
        while True:
            a= self.clock_first_pass(self,page_number)
            if a== -1:
                return
            else:
                a= self.sec_clock_pass(self,page_number)

            







    def read_memory(self, page_number):

        for page in self.frames:
            if page and page.page_num == page_number: 
                    page.ref_bit==1
                    if self.debug_mode:
                        print("Read hit")
                    return
        self.page_faults+=1
        self.clock(page_number)

    def write_memory(self, page_number):

        for page in self.frames:
            if page and page.page_num == page_number:

                page.ref_bit = 1 

                page.dirty = True
                if self.debug_mode:
                    print(f"Write hit.")
                return

        self.page_faults+=1
        self.clock(page_number)



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