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


    @staticmethod
    def Gaussian_Fit(x, A, mu, sigma):
        return A * np.exp(-0.5 * ((x - mu) / sigma) ** 2)


    @staticmethod
    def Parabolic_Fit(x, a, p, q):
        return a*(x - p)**2 + q


    def Compute_Histogram(self, values_list, number_of_bins):
        counts, bin_edges = np.histogram(values_list, bins = number_of_bins)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        return [bin_centers, counts]


    def Compute_Moving_Averaged_Counts(self, counts, order):
        if order == 3:
            moving_averaged_counts = [counts[0]] + [(counts[i-1] + counts[i] + counts[i+1])/3 for i in range(1, len(counts) - 1)] + [counts[-1]]
        elif order == 5:
            moving_averaged_counts = [counts[0]] + [(counts[0] + counts[1] + counts[2])/3] + [(counts[i-2] + 2*counts[i-1] + 3*counts[i] + 2*counts[i+1] + counts[i+2])/9 for i in range(2, len(counts) - 2)] + [(counts[-3] + counts[-2] + counts[-1])/3] + [counts[-1]]
        return moving_averaged_counts


    def Compute_Histogram_Derivative(self, bin_centers, counts):
        derivative = np.gradient(counts, bin_centers)
        return derivative


    def Compute_Compton_Edge_And_Parabolic_Fit(self, bin_centers, derivative, title):
        border = int(len(derivative)*18/100)
        minimum = np.min(derivative[border:])
        minimum_index = np.argmin(derivative[border:]) + border

        if (title == "CH0 Amplitude") or (title == "CH1 Amplitude"):
            p0 = (1e9, bin_centers[minimum_index], minimum)
            bounds = ((1e6, bin_centers[minimum_index - 2], -3*np.absolute(minimum)), (1e12, bin_centers[minimum_index + 2], +3*np.absolute(minimum)))
        elif (title == "CH0 Charge") or (title == "CH1 Charge"):
            p0 = (1e6, bin_centers[minimum_index], minimum)
            bounds = ((1, bin_centers[minimum_index - 2], -3*np.absolute(minimum)), (1e9, bin_centers[minimum_index + 2], +3*np.absolute(minimum)))
        else:
            print("Wrong Title -- Fit Broken")
            return False

        x_fit = bin_centers[minimum_index - 2 : minimum_index + 3]
        y_fit = derivative[minimum_index - 2 : minimum_index + 3]
        popt, pcov = curve_fit(self.Parabolic_Fit, x_fit, y_fit, p0=p0, bounds=bounds)
        perr = np.sqrt(np.diag(pcov))
        a, p, q = popt
        sigma_a, sigma_p, sigma_q = perr
        return [a, p, q, sigma_a, sigma_p, sigma_q, minimum_index]


    def Save_Compton_Type_Histogram(self, bins, values_list, title, unit):
        bin_centers, counts = self.Compute_Histogram(values_list, bins)
        moving_averaged_counts = self.Compute_Moving_Averaged_Counts(counts, 3)
        derivative = self.Compute_Histogram_Derivative(bin_centers, moving_averaged_counts)
        a, p, q, sigma_a, sigma_p, sigma_q, min_index = self.Compute_Compton_Edge_And_Parabolic_Fit(bin_centers, derivative, title)
        bin_lenght = bin_centers[1] - bin_centers[0]
        x_parabola = np.linspace(p - 5*bin_lenght, p + 5*bin_lenght, 200)
        y_parabola = np.array([self.Parabolic_Fit(x, a, p, q) for x in x_parabola])
        scale = np.max(moving_averaged_counts) / (4*np.max(np.abs(derivative)))

        plt.figure()
        plt.hist(values_list, bins = bins)
        plt.title(title + " histogram for " + self.label)
        plt.xlabel(title + " " + " (" + unit + ")")
        plt.ylabel("Counts")

        plt.plot(bin_centers, counts, linewidth = 1, label = "Orginal histogram")
        plt.plot(bin_centers, moving_averaged_counts, linewidth = 1, label = "MMP Histogram")
        plt.plot(bin_centers, derivative * scale, linewidth = 1, label = "MMP Histogram derivative")
        plt.plot(x_parabola, y_parabola * scale, linewidth = 1, label = "Parabolic Fit")
        plt.axvline(x = p, color='black', linestyle='--', linewidth = 1, label = f"Compton Edge = ({p:.5f} +- {sigma_p:.5f})" + " [" + unit + "]")
        plt.legend()

        plt.savefig("../Results/new_page.pdf")
        plt.close()
        writer = PdfWriter()
        reader_existing = PdfReader("../Results/" + title + "s.pdf")
        reader_new = PdfReader("../Results/new_page.pdf")
        for page in reader_existing.pages:
            writer.add_page(page)
        writer.add_page(reader_new.pages[0])
        with open("../Results/result.pdf", "wb") as f:
            writer.write(f)
        os.replace("../Results/result.pdf", "../Results/" + title + "s.pdf")

        return [p, sigma_p]

    
    def Save_Compton_Type_Histograms(self):
        CH0_amplitudes_list = [-event[0].amplitude_value for event in self.events_list.events_list]
        CH1_amplitudes_list = [-event[1].amplitude_value for event in self.events_list.events_list]
        CH0_charges_list = [-event[0].charge_value/1000 for event in self.events_list.events_list]
        CH1_charges_list = [-event[1].charge_value/1000 for event in self.events_list.events_list]
        Charge_averages_list = [-(event[0].charge_value + event[1].charge_value)/2 for event in self.events_list.events_list]
        CH0_amplitudes_compton = self.Save_Compton_Type_Histogram(100, CH0_amplitudes_list, "CH0 Amplitude", "V")
        CH1_amplitudes_compton = self.Save_Compton_Type_Histogram(100, CH1_amplitudes_list, "CH1 Amplitude", "V")
        CH0_charges_compton = self.Save_Compton_Type_Histogram(100, CH0_charges_list, "CH0 Charge", "V * ns")
        CH1_charges_compton = self.Save_Compton_Type_Histogram(100, CH1_charges_list, "CH1 Charge", "V * ns")
        return [CH0_amplitudes_compton, CH1_amplitudes_compton, CH0_charges_compton, CH1_charges_compton]


    def Charge_averages(self):
        Charge_averages_list = [-(event[0].charge_value + event[1].charge_value)/2 for event in self.events_list.events_list]
        plt.figure()
        plt.hist(Charge_averages_list, bins = 100)
        plt.title("(Q1 + Q2)/2 histogram for" + self.label)
        plt.xlabel("(Q1 + Q2)/2 (V * ns)")
        plt.ylabel("Counts")
        plt.savefig("../Results/new_page.pdf")
        plt.close()
        writer = PdfWriter()
        reader_existing = PdfReader("../Results/Charge averages.pdf")
        reader_new = PdfReader("../Results/new_page.pdf")
        for page in reader_existing.pages:
            writer.add_page(page)
        writer.add_page(reader_new.pages[0])
        with open("../Results/result.pdf", "wb") as f:
            writer.write(f)
        os.replace("../Results/result.pdf", "../Results/Charge averages.pdf")


    def Time_averages(self):
        Time_averages_list = [((event[0].detection_time + event[1].detection_time)/2)/1000 for event in self.events_list.events_list]
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
        plt.xlabel("(T1 + T2)/2 (ns)")
        plt.ylabel("Counts")

        bin_width = bins[1] - bins[0]
        x = np.linspace(bins[0], bins[-1], 1000)
        y = norm.pdf(x, mu, sigma) * len(data) * bin_width

        plt.savefig("../Results/new_page.pdf")
        plt.close()
        writer = PdfWriter()
        reader_existing = PdfReader("../Results/Time averages.pdf")
        reader_new = PdfReader("../Results/new_page.pdf")
        for page in reader_existing.pages:
            writer.add_page(page)
        writer.add_page(reader_new.pages[0])
        with open("../Results/result.pdf", "wb") as f:
            writer.write(f)
        os.replace("../Results/result.pdf", "../Results/Time averages.pdf")


    def Time_differences(self):
        Time_differences_list = [(event[0].detection_time - event[1].detection_time)/1000 for event in self.events_list.events_list]
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
        plt.xlabel("T1 - T2 (ns)")
        plt.ylabel("Counts")

        bin_width = bins[1] - bins[0]
        x = np.linspace(bins[0], bins[-1], 1000)
        y = norm.pdf(x, mu, sigma) * len(data) * bin_width


        plt.savefig("../Results/new_page.pdf")
        plt.close()
        writer = PdfWriter()
        reader_existing = PdfReader("../Results/Time differences.pdf")
        reader_new = PdfReader("../Results/new_page.pdf")
        for page in reader_existing.pages:
            writer.add_page(page)
        writer.add_page(reader_new.pages[0])
        with open("../Results/result.pdf", "wb") as f:
            writer.write(f)
        os.replace("../Results/result.pdf", "../Results/Time differences.pdf")