import time
import re
import matplotlib.pyplot as plt
from pypdf import PdfReader, PdfWriter
from Signal import *
from Events_List import *
from Histograms_Saver import *


def Enumerate_files(i, files_path):
    if i < 1:
        current_path = files_path
    elif i < 10:
        current_path = files_path + "_000" + str(i)
    elif i < 100:
        current_path = files_path + "_00" + str(i)
    elif i < 1000:
        current_path = files_path + "_0" + str(i)
    elif i < 10000:
        current_path = files_path + "_" + str(i)
    else:
        print("File path error!")
        return False
    return current_path 


def Sampling_time_regex(line):
    match = re.search(r"Sampling Period:\s*([\d.]+)\s*ps", line)
    if match:
        return float(match.group(1))
    else:
        return False


def Channel_regex(line):
    match = re.search(r"===\s*CH:\s*(\d+)", line)
    if match:
        return str(match.group(1))
    else:
        return False


def Event_regex(line):
    match = re.search(r"===\s*EVENT\s+(\d+)\s*===", line)
    if match:
        return match.group(1)
    else:
        return False

def Erase_pdfs():
    writer = PdfWriter()
    with open("../Results/Amplitudes_CH0.pdf", "wb") as f:
        writer.write(f)
    f.close()
    with open("../Results/Amplitudes_CH1.pdf", "wb") as f:
        writer.write(f)
    f.close()
    with open("../Results/Charges_CH0.pdf", "wb") as f:
        writer.write(f)
    f.close()
    with open("../Results/Charges_CH1.pdf", "wb") as f:
        writer.write(f)
    f.close()


def main():
    measurements_list = []
    number_of_files = 50
    for i in range(82, 91, 1):
        events_list = Events_List([])
        files_path = "../Data/"+str(i/2)+"V/wavecatcher_run1/wavecatcher_run1_Ascii.dat"
        for j in range(number_of_files):
            print("[" + str(i-81) + "/9, " + str(j+1) + "/100]")
            current_path = Enumerate_files(j, files_path)

            with open(current_path, "r", encoding = "utf-8") as current_file:
                current_sampling_time = 0
                current_CH0_waveform = []
                current_CH1_waveform = []
                current_line = current_file.readline()
                while 1:
                    current_sampling_time = Sampling_time_regex(current_line)
                    if  current_sampling_time:
                        break
                    else:
                        pass
                        current_line.strip()
                        current_line = current_file.readline()

                current_line = current_file.readline()
                while current_line:

                    if Channel_regex(current_line) == "0":
                        current_line.strip()
                        current_line = current_file.readline()
                        current_CH0_waveform = [float(number) for number in current_line.split()]
                        current_CH0_signal = Signal(current_CH0_waveform, current_sampling_time)
                        current_CH0_signal.Compute_All_Variables()
                    elif Channel_regex(current_line) == "1":
                        current_line.strip()
                        current_line = current_file.readline()
                        current_CH1_waveform = [float(number) for number in current_line.split()]
                        current_CH1_signal = Signal(current_CH1_waveform, current_sampling_time)
                        current_CH1_signal.Compute_All_Variables()
                    else:
                        pass

                    if Event_regex(current_line):
                        if (current_CH0_waveform != [] and current_CH1_waveform != []):
                            events_list.events_list.append([current_CH0_signal, current_CH1_signal])
                        current_CH0_waveform = []
                        current_CH1_waveform = []

                    current_line.strip()
                    current_line = current_file.readline()
                current_sampling_time = 0

        events_list.Execute_All_Cuts()
        measurements_list.append(events_list)
        events_list = Events_List([])


    Erase_pdfs()
    i = 41
    for measurement in measurements_list:
        histograms_saver = Histograms_Saver(measurement, str(i) + "V")
        histograms_saver.Amplitudes_CH0()
        histograms_saver.Amplitudes_CH1()
        histograms_saver.Charges_CH0()
        histograms_saver.Charges_CH1()
        i = i + 0.5
    os.remove("../Results/new_page.pdf")
    
main()