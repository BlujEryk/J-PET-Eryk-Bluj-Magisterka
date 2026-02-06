import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

class Histograms_Saver:
    
    def __init__(self, events_list, pdf_file_path):
        self.events_list = events_list
        self.pdf_file_path = pdf_file_path

    def Save_All_Histograms(self):
        with PdfPages(self.pdf_file_path) as pdf:

            plt.figure()
            CH0_amplitudes_list = [event[0].amplitude_value for event in self.events_list.events_list]
            plt.hist(CH0_amplitudes_list, bins = 100)
            plt.title("CH0 amplitude (mV)")
            pdf.savefig()
            plt.close()

            plt.figure()
            CH1_amplitudes_list = [event[1].amplitude_value for event in self.events_list.events_list]
            plt.hist(CH1_amplitudes_list, bins = 100)
            plt.title("CH1 amplitude (mV)")
            pdf.savefig()
            plt.close()

            plt.figure()
            CH0_charges_list = [event[0].charge_value for event in self.events_list.events_list]
            plt.hist(CH0_charges_list, bins = 100)
            plt.title("CH0 charge (mV * ps)")
            pdf.savefig()
            plt.close()

            plt.figure()
            CH1_charges_list = [event[1].charge_value for event in self.events_list.events_list]
            plt.hist(CH1_charges_list, bins = 100)
            plt.title("CH0 charge (mV * ps)")
            pdf.savefig()
            plt.close()