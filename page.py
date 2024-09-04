

class PAGE:
    def __init__(self,pagenumber):
        self.pagenumber = pagenumber
        self.dirtybit = 0
        pass
    def set_bit(self,bit):
        self.dirtybit = bit
        pass