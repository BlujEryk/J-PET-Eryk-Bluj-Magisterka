import numpy as np
import scipy as sp
from Monte_Carlo import *

class Histogram:

    def __init__(self, values_list, number_of_bins):
        self.values_list = values_list
        self.number_of_bins = number_of_bins
        self.counts, self.bin_edges, self.bin_centers = self.Compute_Histogram()
        self.mmp_counts = self.Compute_Moving_Mean_Counts(3)
        self.derivative = self.Compute_Histogram_Derivative()
        self.mmp_derivative = self.Compute_MMP_Histogram_Derivative()


    def Compute_Histogram(self):
        counts, bin_edges = np.histogram(self.values_list, bins = self.number_of_bins)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        return [counts, bin_edges, bin_centers]


    def Compute_Moving_Mean_Counts(self, order):
        if order == 3:
            mmp_counts = [self.counts[0]] + [(self.counts[i-1] + self.counts[i] + self.counts[i+1])/3 for i in range(1, len(self.counts) - 1)] + [self.counts[-1]]
        elif order == 5:
            mmp_counts = [self.counts[0]] + [(self.counts[0] + self.counts[1] + self.counts[2])/3] + [(self.counts[i-2] + 2*self.counts[i-1] + 3*self.counts[i] + 2*self.counts[i+1] + self.counts[i+2])/9 for i in range(2, len(self.counts) - 2)] + [(self.counts[-3] + self.counts[-2] + self.counts[-1])/3] + [self.counts[-1]]
        return mmp_counts
    

    def Compute_Histogram_Derivative(self):
        derivative = np.gradient(self.counts, self.bin_centers)
        return derivative


    def Compute_MMP_Histogram_Derivative(self):
        mmp_derivative = np.gradient(self.mmp_counts, self.bin_centers)
        return mmp_derivative
    


class Compton_Histogram(Histogram):

    def __init__(self, values_list, number_of_bins):
        super().__init__(values_list, number_of_bins)
        self.border, self.minimum, self.minimum_index = self.Compute_Minimum()


    @staticmethod
    def Parabolic_Fit(x, a, p, q):
        return a*(x - p)**2 + q
    

    def Compute_Minimum(self):
        border = int(len(self.mmp_derivative)*18/100)
        minimum = np.min(self.mmp_derivative[border:])
        minimum_index = np.argmin(self.mmp_derivative[border:]) + border
        return border, minimum, minimum_index
    

    def Compute_Compton_Edge_And_Parabolic_Fit(self):
        x_fit = self.bin_centers[self.minimum_index - 2 : self.minimum_index + 3]
        y_fit = self.mmp_derivative[self.minimum_index - 2 : self.minimum_index + 3]
        popt, pcov = sp.optimize.curve_fit(self.Parabolic_Fit, x_fit, y_fit, p0=self.p0, bounds=self.bounds)
        perr = np.sqrt(np.diag(pcov))
        a, p, q = popt
        sigma_a, sigma_p, sigma_q = perr
        return [a, p, q, sigma_a, sigma_p, sigma_q]
    


class Time_Histogram(Histogram):

    @staticmethod
    def Gaussian_Fit(x, A, mu, sigma):
        return A * np.exp(-0.5 * ((x - mu) / sigma) ** 2)
    


class Amplitude_Histogram(Compton_Histogram):

    def __init__(self, values_list, number_of_bins):
        super().__init__(values_list, number_of_bins)
        self.p0 = (1e9, self.bin_centers[self.minimum_index], self.minimum)
        self.bounds = ((1e6, self.bin_centers[self.minimum_index - 2], -3*np.absolute(self.minimum)), (1e12, self.bin_centers[self.minimum_index + 2], +3*np.absolute(self.minimum)))
        self.a, self.p, self.q, self.sigma_a, self.sigma_p, self.sigma_q = self.Compute_Compton_Edge_And_Parabolic_Fit()



class Charge_Histogram(Compton_Histogram):

    def __init__(self, values_list, number_of_bins):
        super().__init__(values_list, number_of_bins)
        self.p0 = (1e6, self.bin_centers[self.minimum_index], self.minimum)
        self.bounds = ((1, self.bin_centers[self.minimum_index - 2], -3*np.absolute(self.minimum)), (1e9, self.bin_centers[self.minimum_index + 2], +3*np.absolute(self.minimum)))
        self.a, self.p, self.q, self.sigma_a, self.sigma_p, self.sigma_q = self.Compute_Compton_Edge_And_Parabolic_Fit()



class Charge_Average_Histogram(Charge_Histogram):

    def __init__(self, values_list, number_of_bins):
        super().__init__(values_list, number_of_bins)


    def Compute_Energy_Boundries(self):
        self.bound_200 = (200 / 340.66)*self.p
        self.bound_380 = (380 / 340.66)*self.p
        return [self.bound_200, self.bound_380]


    def Compute_Monte_Carlo_Fit_Parameters(self):
        self.monte_carlo = Monte_Carlo(self.counts, self.bin_edges)
        alpha, beta, V = self.monte_carlo.Fit_Histogram().x
        # print(alpha, beta, V)
        fit_counts, fit_bin_edges = self.monte_carlo.Simulate_Histogram((alpha, beta, V))
        return [alpha, beta, V, fit_counts, fit_bin_edges]
        
        

class Time_Histogram(Histogram):

    @staticmethod
    def Gaussian_Fit(x, A, mu, sigma):
        return A * np.exp(-0.5 * ((x - mu) / sigma) ** 2)