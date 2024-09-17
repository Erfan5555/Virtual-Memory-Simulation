from clockmmu import ClockMMU
from lrummu import LruMMU
from randmmu import RandMMU
from mmu import MMU
import matplotlib.pyplot as plt
import numpy as np

import sys


def set_up(file):
    PAGE_OFFSET = 12
    page_nums = set()
    with open(file, 'r') as trace_file:
        for trace_line in trace_file:
            trace_cmd = trace_line.strip().split(" ")
            logical_address = int(trace_cmd[0], 16)
            page_number = logical_address >>  PAGE_OFFSET
            page_nums.add(page_number)
    total_frames = len(page_nums)
    print(total_frames)
    frames = []
    for x in range(10,100,10):
        num = round(total_frames * (x / 100))
        frames.append(num)
    return frames


def test_mmu(mode,frames,file):
    PAGE_OFFSET = 12
    no_events = 0

    total_diskw = []
    total_diskr = []
    total_event = []
    page_fault = []





    for x in frames:
        if mode == "rand":
            mmu = RandMMU(x)
        elif mode == "lru":
            mmu = LruMMU(x)
        elif mode == "clock":
            mmu = ClockMMU(x)
        with open(file, 'r') as trace_file:
            for trace_line in trace_file:
                trace_cmd = trace_line.strip().split(" ")
                logical_address = int(trace_cmd[0], 16)
                page_number = logical_address >>  PAGE_OFFSET


                # Process read or write
                if trace_cmd[1] == "R":
                    mmu.read_memory(page_number)
                elif trace_cmd[1] == "W":
                    mmu.write_memory(page_number)
                else:
                    print(f"Badly formatted file. Error on line {no_events + 1}")
                    return

                no_events += 1
        total_diskr.append(mmu.get_total_disk_reads())
        total_diskw.append(mmu.get_total_disk_writes())
        total_event.append(no_events)
        page_fault.append(mmu.get_total_page_faults() / no_events)
        print(f"total memory frames: {x}")
        print(f"events in trace: {no_events}")
        print(f"total disk reads: {mmu.get_total_disk_reads()}")
        print(f"total disk writes: {mmu.get_total_disk_writes()}")
        print("page fault rate: ", end="")
        print("{0:.4f}".format(mmu.get_total_page_faults() / no_events))
        
    return total_diskr,total_diskw,total_event,page_fault



def main():
    PAGE_OFFSET = 12  # page is 2^12 = 4KB

    ############################
    # Check input parameters   #
    ############################

    # if (len(sys.argv) < 5):
    #     print("Usage: python memsim.py inputfile numberframes replacementmode debugmode")
    #     return

    input_file = sys.argv[1]

    try:
        with open(input_file, 'r') as file:
            # Read the trace file contents
            trace_contents = file.readlines()
    except FileNotFoundError:
        print(f"Input '{input_file}' could not be found")
        print("Usage: python memsim.py inputfile numberframes replacementmode debugmode")
        return


    ############################################################
    # Main Loop: Process the addresses from the trace file     #
    ############################################################

    no_events = 0
 
    page_arr = set_up(input_file)
    print(page_arr)
    lru_diskr, lru_diskw,lru_events, lru_page =test_mmu("lru",page_arr,input_file)
    rand_diskr, rand_diskw, rand_events, rand_page = test_mmu("rand",page_arr,input_file)
    clock_diskr, clock_diskw, clock_events, clock_page = test_mmu("clock",page_arr,input_file)

    #Plotting graph for page fault 
    plt.plot(page_arr,lru_page, label = "LRU",linestyle="-")
    plt.plot(page_arr,rand_page, label = "RAND",linestyle="--")
    plt.plot(page_arr,clock_page, label = "CLOCK",linestyle="dotted")
    plt.xlabel("Page Fault Rate")
    plt.xlabel("Memory Frames")
    plt.title("Page fault rate comparison across the three different algorithms for swim.trace")
    plt.legend()
    plt.show()

    #Plotting graph for Disk Reads
    plt.plot(page_arr,lru_diskr, label = "LRU",linestyle="-")
    plt.plot(page_arr,rand_diskr, label = "RAND",linestyle="--")
    plt.plot(page_arr,clock_diskr, label = "CLOCK",linestyle="dotted")
    plt.xlabel("Disk Reads")
    plt.xlabel("Memory Frames")
    plt.title("Disk Reads rate comparison across the three different algorithms for swim.trace")
    plt.legend()
    plt.show()
    
    #Plotting graph for Disk Writes

    plt.plot(page_arr,lru_diskw, label = "LRU",linestyle="-")
    plt.plot(page_arr,rand_diskw, label = "RAND",linestyle="--")
    plt.plot(page_arr,clock_diskw, label = "CLOCK",linestyle="dotted")
    plt.xlabel("Disk Writes")
    plt.xlabel("Memory Frames")
    plt.title("Disk Writes comparison across the three different algorithms for swim.trace")
    plt.legend()
    plt.show()

    # with open(input_file, 'r') as trace_file:
    #     for trace_line in trace_file:
    #         trace_cmd = trace_line.strip().split(" ")
    #         logical_address = int(trace_cmd[0], 16)
    #         page_number = logical_address >>  PAGE_OFFSET
         

    #         # Process read or write
    #         if trace_cmd[1] == "R":
    #             mmu.read_memory(page_number)
    #         elif trace_cmd[1] == "W":
    #             mmu.write_memory(page_number)
    #         else:
    #             print(f"Badly formatted file. Error on line {no_events + 1}")
    #             return

    #         no_events += 1

    # TODO: Print results
    # print(f"total memory frames: {frames}")
    # print(f"events in trace: {no_events}")
    # print(f"total disk reads: {mmu.get_total_disk_reads()}")
    # print(f"total disk writes: {mmu.get_total_disk_writes()}")
    # print("page fault rate: ", end="")
    # print("{0:.4f}".format(mmu.get_total_page_faults() / no_events))


if __name__ == "__main__":
    main()
                    
