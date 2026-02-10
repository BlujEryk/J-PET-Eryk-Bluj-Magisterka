import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.stats import norm
from scipy.optimize import curve_fit
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


    def Charge_averages(self):
        Charge_averages_list = [-(event[0].charge_value + event[1].charge_value)/2 for event in self.events_list.events_list]
        plt.figure()
        plt.hist(Charge_averages_list, bins = 100)
        plt.title("(Q1 + Q2)/2 histogram for" + self.label)
        plt.xlabel("(Q1 + Q2)/2 (V * ps)")
        plt.ylabel("Counts")
        plt.savefig("../Results/new_page.pdf")
        plt.close()
        writer = PdfWriter()
        reader_existing = PdfReader("../Results/Charge_averages.pdf")
        reader_new = PdfReader("../Results/new_page.pdf")
        for page in reader_existing.pages:
            writer.add_page(page)
        writer.add_page(reader_new.pages[0])
        with open("../Results/result.pdf", "wb") as f:
            writer.write(f)
        os.replace("../Results/result.pdf", "../Results/Charge_averages.pdf")


    @staticmethod
    def Gaussian_Fit(x, A, mu, sigma):
        return A * np.exp(-0.5 * ((x - mu) / sigma) ** 2)


    def Time_averages(self):
        Time_averages_list = [(event[0].detection_time + event[1].detection_time)/2 for event in self.events_list.events_list]
        data = np.array(Time_averages_list)
        
        plt.figure()
        counts, bins, patches = plt.hist(Time_averages_list, bins = 100)
        centers = 0.5 * (bins[:-1] + bins[1:])

        mask = counts > 0
        x_fit = centers[mask]
        y_fit = counts[mask]

        A0 = np.max(counts)
        mu0 = (bins[0] + bins[-1])/2
        sigma0 = (bins[-1] - bins[0])/10
        p0 = (A0, mu0, sigma0)

        bounds = ((-np.inf, bins[0], 1e-12), (np.inf, bins[-1], np.inf))

        popt, pcov = curve_fit(self.Gaussian_Fit, x_fit, y_fit, p0=p0, bounds=bounds)
        A, mu, sigma = popt

        x = np.linspace(bins[0], bins[-1], 1000)
        y = self.Gaussian_Fit(x, A, mu, sigma)

        plt.plot(x, y, 'r', linewidth=2, label=f"Fit: A={A:.1f}, μ={mu:.3f}, σ={sigma:.3f}")
        plt.legend()

        plt.title("(T1 + T2)/2 histogram for" + self.label)
        plt.xlabel("(T1 + T2)/2 (ps)")
        plt.ylabel("Counts")

        bin_width = bins[1] - bins[0]
        x = np.linspace(bins[0], bins[-1], 1000)
        y = norm.pdf(x, mu, sigma) * len(data) * bin_width

        plt.savefig("../Results/new_page.pdf")
        plt.close()
        writer = PdfWriter()
        reader_existing = PdfReader("../Results/Time_averages.pdf")
        reader_new = PdfReader("../Results/new_page.pdf")
        for page in reader_existing.pages:
            writer.add_page(page)
        writer.add_page(reader_new.pages[0])
        with open("../Results/result.pdf", "wb") as f:
            writer.write(f)
        os.replace("../Results/result.pdf", "../Results/Time_averages.pdf")


    def Time_differences(self):
        Time_differences_list = [event[0].detection_time - event[1].detection_time for event in self.events_list.events_list]
        data = np.array(Time_differences_list)
        
        plt.figure()
        counts, bins, patches = plt.hist(Time_differences_list, bins = 100)
        centers = 0.5 * (bins[:-1] + bins[1:])

        mask = counts > 0
        x_fit = centers[mask]
        y_fit = counts[mask]

        A0 = np.max(counts)
        mu0 = (bins[0] + bins[-1])/2
        sigma0 = (bins[-1] - bins[0])/10
        p0 = (A0, mu0, sigma0)

        bounds = ((-np.inf, bins[0], 1e-12), (np.inf, bins[-1], np.inf))

        popt, pcov = curve_fit(self.Gaussian_Fit, x_fit, y_fit, p0=p0, bounds=bounds)
        A, mu, sigma = popt

        x = np.linspace(bins[0], bins[-1], 1000)
        y = self.Gaussian_Fit(x, A, mu, sigma)

        plt.plot(x, y, 'r', linewidth=2, label=f"Fit: A={A:.1f}, μ={mu:.3f}, σ={sigma:.3f}")
        plt.legend()

        plt.title("T1 - T2 histogram for" + self.label)
        plt.xlabel("T1 - T2 (ps)")
        plt.ylabel("Counts")

        bin_width = bins[1] - bins[0]
        x = np.linspace(bins[0], bins[-1], 1000)
        y = norm.pdf(x, mu, sigma) * len(data) * bin_width


        plt.savefig("../Results/new_page.pdf")
        plt.close()
        writer = PdfWriter()
        reader_existing = PdfReader("../Results/Time_differences.pdf")
        reader_new = PdfReader("../Results/new_page.pdf")
        for page in reader_existing.pages:
            writer.add_page(page)
        writer.add_page(reader_new.pages[0])
        with open("../Results/result.pdf", "wb") as f:
            writer.write(f)
        os.replace("../Results/result.pdf", "../Results/Time_differences.pdf")