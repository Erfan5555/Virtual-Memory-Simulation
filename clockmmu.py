


from mmu import MMU

class Page:
    def __init__(self, page_num):
        self.page_num = page_num
        self.ref_bit = 0
        self.dirty = False

    def __repr__(self):
        return f"Page({self.page_num}, ref_bit={self.ref_bit}, dirty={self.dirty})"



class ClockMMU(MMU):
    def __init__(self, frames_num):
        self.frames= [None]* frames_num
        self.clock_tip = 0
        self.count_diskR= 0
        self.count_diskW=0
        self.page_faults=0
        self.debug_mode=False
        self.total_frames= frames_num

    def set_debug(self):
        self.debug_mode = True

    def reset_debug(self):
        self.debug_mode = False
    
    def handle_empty (self, page_number,write,current):
        # set the ref bit to 1 
        # if its a write op set the dirty bit to treu - Check THIS WITH THE BOOK
        self.frames[self.clock_tip] = Page(page_number)
        self.frames[self.clock_tip].ref_bit = 1  

        if write:
            self.frames[self.clock_tip].dirty = True  
        self.count_diskR += 1  
        if self.debug_mode:
            print(f"load page{current}")
        self.clock_tip = (self.clock_tip + 1) % len(self.frames) 
        return current
    

    def handle_zero (self, page_number,write,current):
        current.ref_bit = 0
        if self.debug_mode:
            print("pass making the ref bit 0 now")
        self.clock_tip = (self.clock_tip + 1) % len(self.frames)  
        return

    def handle_replacment (self, page_number,write,current):
        if current.dirty:

            self.count_diskW += 1
            if self.debug_mode:
                print(f"writing dirty page{current}")

        if self.debug_mode:
            print(f"Evicting {current}")
        self.frames[self.clock_tip] = Page(page_number)
        self.frames[self.clock_tip].ref_bit = 1  
        if write:
            self.frames[self.clock_tip].dirty = True 
        self.count_diskR += 1  
        if self.debug_mode:
            print(f"Loading page{current} ")
        self.clock_tip = (self.clock_tip + 1) % len(self.frames)  
        return


    def clock(self, page_number,write):

        while True:
            current = self.frames[self.clock_tip]
            if current is None:
                self.handle_empty ( page_number,write,current)
                return
            else:
                if current.ref_bit == 1:
                    self.handle_zero(page_number,write,current)

                else:
                    self.handle_replacment (page_number,write,current)
           
                    return



    def read_memory(self, page_number):

        for page in self.frames:
            if page and page.page_num == page_number: 
                    page.ref_bit=1
                    if self.debug_mode:
                        print("Read hit")
                    return
        self.page_faults+=1
        self.clock(page_number,write=False)

    def write_memory(self, page_number):

        for page in self.frames:
            if page and page.page_num == page_number:

                page.ref_bit = 1 

                page.dirty = True
                if self.debug_mode:
                    print(f"Write hit.")
                return

        self.page_faults+=1
        self.clock(page_number,write=True)


    def get_total_disk_reads(self):
        return self.count_diskR

    def get_total_disk_writes(self):
        return self.count_diskW

    def get_total_page_faults(self):
        return self.page_faults

