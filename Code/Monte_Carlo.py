import numpy as np
import matplotlib.pyplot as plt
import random

class Q_averages_fitter:

    def __init__(self, Q_averages_histogram, n):
        self.E = 511
        self.n = n
        self.Q_averages_histogram = Q_averages_histogram
        self.E_deposited = self.Simulate_Mu_With_KN_Weight()
        self.E_smeared = self.Smear_Energies_By_Detector(self.E_deposited, 1)

    def Compute_E_prime(self, mu):
        E_prime = self.E / (1 + (self.E / 511)*(1 - mu))
        return E_prime
    
    def Compute_E_deposited(self, mu):
        E_prime = self.Compute_E_prime(mu)
        E_deposited = self.E - E_prime
        return E_deposited
    
    def Compute_Klein_Nishina_Weight(self, mu):
        E_prime = self.Compute_E_prime(mu)
        KN_weight = ((E_prime / self.E)**2) * ((E_prime / self.E) + (self.E / E_prime) + mu**2 - 1) 
        return KN_weight
    
    def Simulate_Mu_With_KN_Weight(self):
        maximum_weight = self.Compute_Klein_Nishina_Weight(1)
        random_mus = np.random.uniform(-1, 1, self.n)
        random_rs = np.random.uniform(0, maximum_weight, self.n)
        mus_weight = [self.Compute_Klein_Nishina_Weight(mu) for mu in random_mus]
        deposited_energies = []
        for i in range(self.n):
            if random_rs[i] < mus_weight[i]:
                deposited_energies.append(self.Compute_E_deposited(random_mus[i]))
        return deposited_energies

    def Smear_Energies_By_Detector(self, deposited_energies, beta):
        sigmas = [beta * np.sqrt(E) for E in deposited_energies]
        smeared_energies = []
        for i in range(len(deposited_energies)):
            smeared_energies.append(random.gauss(deposited_energies[i], sigmas[i]))
        return smeared_energies

    def Compute_Chi_squared(experimental_histogram, simulated_histogram, V):
        errors = []
        for i in range(len(experimental_histogram)):
            errors.append(((V * simulated_histogram[i] - experimental_histogram[i])**2) / (V * simulated_histogram[i] + experimental_histogram[i]))
        return np.sum(errors)
    



    # def Fit_parameters(experimental_histogram, bins_edges, fit_range=(200.0, 380.0),
    #                     n_mc=2_000_000, seed=123,
    #                     x0=(1.0, 1.0, 1.0), bounds=((0.1, 10.0), (0.01, 50.0), (1e-6, None))):
        




    #     hist_exp = np.asarray(hist_exp, dtype=float)
    #     bins_edges = np.asarray(bins_edges, dtype=float)
    #     centers = 0.5 * (bins_edges[1:] + bins_edges[:-1])

    #     # select bins in fit range (like 200-380 keV in the paper)
    #     lo, hi = fit_range
    #     fit_mask = (centers >= lo) & (centers <= hi)

    #     model = KNFitModel(bins_edges=bins_edges, n_mc=n_mc, seed=seed)

    #     def objective(p):
    #         alpha, beta, V = p
    #         hsim = model.Nsim_hist(alpha, beta)
    #         return neyman_chi2(hist_exp[fit_mask], hsim[fit_mask], V)

    #     res = minimize(
    #         objective,
    #         x0=np.array(x0, dtype=float),
    #         bounds=bounds,
    #         method="L-BFGS-B"
    #     )
    #     return res, model





    

x = Q_averages_fitter(1, 100000)
E_dep  = x.E_deposited
E_smear = x.E_smeared

plt.hist(E_dep, bins = 100, alpha = 0.8)
plt.hist(E_smear, bins = 100, alpha = 0.8)
plt.show()