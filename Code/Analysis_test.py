import time
import re
import matplotlib.pyplot as plt
from pypdf import PdfReader, PdfWriter
from Signal import *
from Events_List import *
from Histograms_Saver import *
from Compton_Graph_Saver import *
from Monte_Carlo import *
from Theoretical import *


def Enumerate_files(i, files_path):
    if i < 1:
        return files_path
    if i >= 10000:
        print("File path error!")
        return False
    return f"{files_path}_{i:04d}"


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
    pdf_titles = ["CH0 Amplitudes", "CH1 Amplitudes", "CH0 Charges", "CH1 Charges", "Charge averages", "Time averages", "Time differences", "Compton Edges", "Percentage Compton Edges"]
    writer = PdfWriter()
    for title in pdf_titles:
        with open("../Results/" + title + ".pdf", "wb") as f:
            writer.write(f)
        f.close()


def Data_unpacker(number_of_files):
    measurements_list = []
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
                while current_line:
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
                        try:
                            current_CH0_signal.Compute_All_Variables()
                        except:
                            pass
                    elif Channel_regex(current_line) == "1":
                        current_line.strip()
                        current_line = current_file.readline()
                        current_CH1_waveform = [float(number) for number in current_line.split()]
                        current_CH1_signal = Signal(current_CH1_waveform, current_sampling_time)
                        try:
                            current_CH1_signal.Compute_All_Variables()
                        except:
                            pass
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
        measurements_list.append(events_list)
        events_list = Events_List([])
    return measurements_list


def Analyze_measurement(measurement):
    measurement.Execute_Preliminary_Cuts()
    



def main():
    Erase_pdfs()
    compton_values = []
    
    measurements_list = Data_unpacker(10)

    i = 41
    for measurement in measurements_list:
        Histogram_Dictionary
        measurement.Execute_Preliminary_Cuts()
        histograms_saver = Histograms_Saver(measurement, str(i) + "V")

        compton_value = histograms_saver.Save_Compton_Type_Histograms()
        compton_values.append([i] + compton_value)
        histograms_saver.Charge_averages()
        histograms_saver.Time_averages()
        histograms_saver.Time_differences()
        i = i + 0.5

    compton_graph_saver = Compton_Graph_Saver(compton_values)
    compton_graph_saver.Save_Compton_Graphs()

    os.remove("../Results/new_page.pdf")
    
main()