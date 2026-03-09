import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import random
from Theoretical import *


class Monte_Carlo:
    
    def __init__(self, counts, bins_edges, seed=123):
        random.seed(seed)
        np.random.seed(seed)
        self.experimental_counts = counts
        self.experimental_bin_edges = bins_edges
        self.number_of_experimental_bins = len(bins_edges) - 1
        self.number_of_experimental_counts = sum(counts)
        self.experimental_bin_centers = [(self.experimental_bin_edges[i] + self.experimental_bin_edges[i + 1])/2 for i in range(self.number_of_experimental_bins)]
        self.theoretical = Theoretical(511, self.number_of_experimental_counts)
        self.theoretical_counts, self.theoretical_bin_edges = np.histogram(self.theoretical.deposited_energies, bins=self.number_of_experimental_bins)


    def Smear_Energies_By_Beta(self, beta):
        sigmas = [beta * np.sqrt(E) for E in self.theoretical.deposited_energies]
        smeared_energies = []
        for i in range(len(self.theoretical.deposited_energies)):
            smeared_energy = random.gauss(self.theoretical.deposited_energies[i], sigmas[i])
            if smeared_energy >= 0:
                smeared_energies.append(smeared_energy)
            else:
                smeared_energies.append(0)
        return smeared_energies
    
    
    def Rescale_Counts_By_V(self, counts, V):
        rescaled_counts = [count * V for count in counts]
        return rescaled_counts
    
    
    def Rescale_Bins_By_Alpha(self, bin_edges, alpha):
        rescaled_bin_edges = [bin_edge * alpha for bin_edge in bin_edges]
        return rescaled_bin_edges
    

    def Compute_Errors(self, x_experimental, x_simulated):
        try:
            errors = []
            for i in range(len(x_experimental)):
                errors.append(((x_simulated[i] - x_experimental[i])**2) / (x_simulated[i] + x_experimental[i]))
        except:
            errors = []
            for i in range(len(x_simulated)):
                errors.append(((x_simulated[i] - x_experimental[i])**2) / (x_simulated[i] + x_experimental[i]))
        return sum(errors)
    

    def Simulate_Histogram(self, parameters):
        alpha, beta, V = parameters
        smeared_energies = self.Smear_Energies_By_Beta(beta)
        smeared_counts, smeared_bin_edges = np.histogram(smeared_energies, bins = self.number_of_experimental_bins)
        rescaled_smeared_counts = self.Rescale_Counts_By_V(smeared_counts, V)
        rescaled_smeared_bin_edges = self.Rescale_Bins_By_Alpha(smeared_bin_edges, alpha)
        return [rescaled_smeared_counts, rescaled_smeared_bin_edges]


    def Compute_Chi_Squared(self, parameters):
        rescaled_smeared_counts, rescaled_smeared_bin_edges = self.Simulate_Histogram(parameters)
        counts_error = self.Compute_Errors(self.experimental_counts, rescaled_smeared_counts)
        bin_edges_error = self.Compute_Errors(self.experimental_bin_edges, rescaled_smeared_bin_edges)
        return counts_error + bin_edges_error
    
    
    # def Fit_Histogram(self):
    #     initial_guess = (0.2*self.experimental_bin_edges[-1], 0.8, max(self.experimental_counts) / max(self.theoretical_counts))
    #     bounds = ((10e-9, 10e9), (10e-9, 10e9), (10e-9, 10e9))
    #     method = "L-BFGS-B"
    #     # method = "Powell"
    #     result = sp.optimize.minimize(self.Compute_Chi_Squared, x0=initial_guess, bounds=bounds, method=method)
    #     return result
    

    def Fit_Histogram(self):
        bounds = ((10e-9, 10e9), (10e-9, 2), (10e-9, 10e9))
        result = sp.optimize.differential_evolution(self.Compute_Chi_Squared, bounds=bounds, popsize=8)
        return result