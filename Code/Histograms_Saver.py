import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pypdf import PdfReader, PdfWriter
import numpy as np
import os

class Histograms_Saver:
    
    def __init__(self, events_list, label):
        self.events_list = events_list
        self.label = label


    def Amplitudes_CH0(self):
        CH0_amplitudes_list = [-event[0].amplitude_value for event in self.events_list.events_list]
        plt.figure()
        plt.hist(CH0_amplitudes_list, bins = 100)
        plt.title("CH0 Amplitude histogram for " + self.label)
        plt.xlabel("CH0 amplitude (V)")
        plt.ylabel("Counts")
        plt.savefig("../Results/new_page.pdf")
        plt.close()    
        writer = PdfWriter()
        reader_existing = PdfReader("../Results/Amplitudes_CH0.pdf")
        reader_new = PdfReader("../Results/new_page.pdf")
        for page in reader_existing.pages:
            writer.add_page(page)
        writer.add_page(reader_new.pages[0])
        with open("../Results/result.pdf", "wb") as f:
            writer.write(f)
        os.replace("../Results/result.pdf", "../Results/Amplitudes_CH0.pdf")


    def Amplitudes_CH1(self):
        CH1_amplitudes_list = [-event[1].amplitude_value for event in self.events_list.events_list]
        plt.figure()
        plt.hist(CH1_amplitudes_list, bins = 100)
        plt.title("CH0 Amplitude histogram for " + self.label)
        plt.xlabel("CH0 amplitude (V)")
        plt.ylabel("Counts")
        plt.savefig("../Results/new_page.pdf")
        plt.close()    
        writer = PdfWriter()
        reader_existing = PdfReader("../Results/Amplitudes_CH1.pdf")
        reader_new = PdfReader("../Results/new_page.pdf")
        for page in reader_existing.pages:
            writer.add_page(page)
        writer.add_page(reader_new.pages[0])
        with open("../Results/result.pdf", "wb") as f:
            writer.write(f)
        os.replace("../Results/result.pdf", "../Results/Amplitudes_CH1.pdf")


    def Charges_CH0(self):
        CH0_charges_list = [-event[0].charge_value for event in self.events_list.events_list]
        plt.figure()
        plt.hist(CH0_charges_list, bins = 100)
        plt.title("CH0 Charge histogram for " + self.label)
        plt.xlabel("CH0 charge(V * ps)")
        plt.ylabel("Counts")
        plt.savefig("../Results/new_page.pdf")
        plt.close()
        writer = PdfWriter()
        reader_existing = PdfReader("../Results/Charges_CH0.pdf")
        reader_new = PdfReader("../Results/new_page.pdf")
        for page in reader_existing.pages:
            writer.add_page(page)
        writer.add_page(reader_new.pages[0])
        with open("../Results/result.pdf", "wb") as f:
            writer.write(f)
        os.replace("../Results/result.pdf", "../Results/Charges_CH0.pdf")


    def Charges_CH1(self):
        CH1_charges_list = [-event[1].charge_value for event in self.events_list.events_list]
        plt.figure()
        plt.hist(CH1_charges_list, bins = 100)
        plt.title("CH1 Charge histogram for " + self.label)
        plt.xlabel("CH1 charge(V * ps)")
        plt.ylabel("Counts")
        plt.savefig("../Results/new_page.pdf")
        plt.close()
        writer = PdfWriter()
        reader_existing = PdfReader("../Results/Charges_CH1.pdf")
        reader_new = PdfReader("../Results/new_page.pdf")
        for page in reader_existing.pages:
            writer.add_page(page)
        writer.add_page(reader_new.pages[0])
        with open("../Results/result.pdf", "wb") as f:
            writer.write(f)
        os.replace("../Results/result.pdf", "../Results/Charges_CH1.pdf")