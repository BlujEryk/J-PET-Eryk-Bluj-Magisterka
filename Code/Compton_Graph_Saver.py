import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib.backends.backend_pdf import PdfPages
from pypdf import PdfReader, PdfWriter
import numpy as np
import os

class Compton_Graph_Saver:
    

    def __init__(self, compton_list):
        self.compton_list = compton_list


    @staticmethod
    def Linear_Fit(x, a, b):
        return a*x + b 


    def Get_Compton_Lists(self):
        self.CH0_amplitude_compton_values = []
        self.CH0_amplitude_compton_sigmas = []
        self.CH1_amplitude_compton_values = []
        self.CH1_amplitude_compton_sigmas = []
        self.CH0_charge_compton_values = []
        self.CH0_charge_compton_sigmas = []
        self.CH1_charge_compton_values = []
        self.CH1_charge_compton_sigmas = []
        self.compton_voltages = []
        for compton_params in self.compton_list:
            self.compton_voltages.append(compton_params[0])
            self.CH0_amplitude_compton_values.append(compton_params[1][0])
            self.CH0_amplitude_compton_sigmas.append(compton_params[1][1])
            self.CH1_amplitude_compton_values.append(compton_params[2][0])
            self.CH1_amplitude_compton_sigmas.append(compton_params[2][1])
            self.CH0_charge_compton_values.append(compton_params[3][0])
            self.CH0_charge_compton_sigmas.append(compton_params[3][1])
            self.CH1_charge_compton_values.append(compton_params[4][0])
            self.CH1_charge_compton_sigmas.append(compton_params[4][1])


    def Save_Compton_Graph(self, x_values, y_values, y_sigmas, title, unit):
        p0 = (1, 0)
        bounds = ((-np.inf, -np.inf), (np.inf, np.inf))
        popt, pcov = curve_fit(self.Linear_Fit, x_values, y_values, p0=p0, bounds=bounds)
        perr = np.sqrt(np.diag(pcov))
        a, b = popt
        a_sigma, b_sigma = perr
        x_range = x_values[-1] - x_values[0]

        x_fit = np.linspace(x_values[0] - x_range/10 , x_values[-1] + x_range/10, 200)
        y_fit = np.array([self.Linear_Fit(x, a, b) for x in x_fit])

        plt.figure()
        plt.errorbar(x_values, y_values, yerr = y_sigmas, capsize = 4, label = title, fmt = 'o')
        plt.plot(x_fit, y_fit, linewidth = 1, label = "Linear Fit")
        plt.title(title + " vs Voltage")
        plt.xlabel("Voltage (V)")
        plt.ylabel(title + " ("  + unit + ")")
        plt.legend()

        plt.savefig("../Results/new_page.pdf")
        plt.close()
        writer = PdfWriter()
        reader_existing = PdfReader("../Results/Compton Edges.pdf")
        reader_new = PdfReader("../Results/new_page.pdf")
        for page in reader_existing.pages:
            writer.add_page(page)
        writer.add_page(reader_new.pages[0])
        with open("../Results/result.pdf", "wb") as f:
            writer.write(f)
        os.replace("../Results/result.pdf", "../Results/Compton Edges.pdf")


    def Save_Divided_Compton_Graph(self, x_values, y_values, y_sigmas, title):
        p0 = (1, 0)
        bounds = ((-np.inf, -np.inf), (np.inf, np.inf))
        y_values_divided = [100*y_value / y_values[0] for y_value in y_values]
        y_sigmas_divided = [np.sqrt((y_sigma/y_sigmas[0])**2 + (y_sigma*y_sigmas[0]/(y_sigmas[0]**2))**2) for y_sigma in y_sigmas]
        popt, pcov = curve_fit(self.Linear_Fit, x_values, y_values_divided, p0=p0, bounds=bounds)
        perr = np.sqrt(np.diag(pcov))
        a, b = popt
        sigma_a, sigma_b = perr
        x_range = x_values[-1] - x_values[0]

        x_fit = np.linspace(x_values[0] - x_range/10 , x_values[-1] + x_range/10, 200)
        y_fit = np.array([self.Linear_Fit(x, a, b) for x in x_fit])

        plt.figure()
        plt.errorbar(x_values, y_values_divided, yerr = y_sigmas_divided, capsize = 4, label = title, fmt = 'o')
        plt.plot(x_fit, y_fit, linewidth = 1, label = f"Linear Fit\n a = ({a:.5f} +- {sigma_a:.5f})[%/V]")
        plt.title("Percentage " + title + " vs Voltage")
        plt.xlabel("Voltage (V)")
        plt.ylabel("Percentage " + title + " (%)")
        plt.legend()

        plt.savefig("../Results/new_page.pdf")
        plt.close()
        writer = PdfWriter()
        reader_existing = PdfReader("../Results/Percentage Compton Edges.pdf")
        reader_new = PdfReader("../Results/new_page.pdf")
        for page in reader_existing.pages:
            writer.add_page(page)
        writer.add_page(reader_new.pages[0])
        with open("../Results/result.pdf", "wb") as f:
            writer.write(f)
        os.replace("../Results/result.pdf", "../Results/Percentage Compton Edges.pdf")
    

    def Save_Compton_Graphs(self):
        self.Get_Compton_Lists()
        self.Save_Compton_Graph(self.compton_voltages, self.CH0_amplitude_compton_values, self.CH0_amplitude_compton_sigmas, "CH0 Amplitude", "V")
        self.Save_Compton_Graph(self.compton_voltages, self.CH1_amplitude_compton_values, self.CH1_amplitude_compton_sigmas, "CH1 Amplitude", "V")
        self.Save_Compton_Graph(self.compton_voltages, self.CH0_charge_compton_values, self.CH0_charge_compton_sigmas, "CH0 Charge", "V * ns")
        self.Save_Compton_Graph(self.compton_voltages, self.CH1_charge_compton_values, self.CH1_charge_compton_sigmas, "CH1 Charge", "V * ns")

        self.Save_Divided_Compton_Graph(self.compton_voltages, self.CH0_amplitude_compton_values, self.CH0_amplitude_compton_sigmas, "CH0 Amplitude")
        self.Save_Divided_Compton_Graph(self.compton_voltages, self.CH1_amplitude_compton_values, self.CH1_amplitude_compton_sigmas, "CH1 Amplitude")
        self.Save_Divided_Compton_Graph(self.compton_voltages, self.CH0_charge_compton_values, self.CH0_charge_compton_sigmas, "CH0 Charge")
        self.Save_Divided_Compton_Graph(self.compton_voltages, self.CH1_charge_compton_values, self.CH1_charge_compton_sigmas, "CH1 Charge")
