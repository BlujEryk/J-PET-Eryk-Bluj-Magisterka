import numpy as np

class Theoretical:

    def __init__(self, energy, number_of_counts):
        self.E = energy
        # self.n_counts = number_of_counts
        self.number_of_counts = 100000
        self.deposited_energies = self.Simulate_Energies_With_KN_Weight()


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
    

    def Simulate_Energies_With_KN_Weight(self):
        maximum_weight = self.Compute_Klein_Nishina_Weight(1)
        random_mus = np.random.uniform(-1, 1, self.number_of_counts)
        random_rs = np.random.uniform(0, maximum_weight, self.number_of_counts)
        mus_weight = [self.Compute_Klein_Nishina_Weight(mu) for mu in random_mus]
        deposited_energies = []
        for i in range(self.number_of_counts):
            if random_rs[i] < mus_weight[i]:
                deposited_energies.append(self.Compute_E_deposited(random_mus[i]))
        return deposited_energies 