import numpy as np

class Signal:
    
    def __init__(self, raw_waveform, sampling_time):
        self.raw_waveform = raw_waveform
        self.sampling_time = sampling_time

    def Compute_Baseline(self):
        self.baseline = np.sum(self.raw_waveform[:200])/200

    def Compute_Corrected_Waveform(self):
        waveform = []
        for i in range(len(self.raw_waveform)):
            waveform.append(self.raw_waveform[i] - self.baseline)
        self.waveform = waveform

    def Compute_Standard_Deviation(self):
        self.standard_deviation = np.std(self.waveform[:200])

    def Compute_Amplitude(self):
        self.amplitude_value = np.min(self.waveform)
        self.amplitude_index = np.argmin(self.waveform)
        self.amplitude_time = self.amplitude_index*self.sampling_time

    def Compute_Edges(self):
        i = 0
        for value in self.waveform[self.amplitude_index:]:
            if value > 0.9*self.amplitude_value:
                self.falling_09_value = value
                self.falling_09_index = self.amplitude_index + i
                self.falling_09_time = self.falling_09_index*self.sampling_time
                break
            i = i + 1

        i = 0
        for value in self.waveform[self.amplitude_index:]:
            if value > 0.1*self.amplitude_value:
                self.falling_01_value = value
                self.falling_01_index = self.amplitude_index + i
                self.falling_01_time = self.falling_01_index*self.sampling_time
                break
            i = i + 1

        i = 0
        for value in self.waveform[self.amplitude_index::-1]:
            if value > 0.9*self.amplitude_value:
                self.rising_09_value = value
                self.rising_09_index = self.amplitude_index - i
                self.rising_09_time = self.rising_09_index*self.sampling_time
                break
            i = i + 1

        i = 0
        for value in self.waveform[self.amplitude_index::-1]:
            if value > 0.1*self.amplitude_value:
                self.rising_01_value = value
                self.rising_01_index = self.amplitude_index - i
                self.rising_01_time = self.rising_01_index*self.sampling_time
                break
            i = i + 1

        self.signal_detection_time = self.rising_01_time

    def Compute_Edges_Lenghts(self):
        self.rising_lenght = self.rising_09_time - self.rising_01_time
        self.falling_lenght = self.falling_01_time - self.falling_09_time

    def Compute_Time_Over_Threshold(self):
        self.time_over_threshold = self.falling_01_time - self.rising_01_time 

    def Compute_Charge(self):
        self.charge_value = np.sum(self.waveform[self.rising_01_index : self.falling_01_index])*self.sampling_time

    def Compute_All_Variables(self):
        self.Compute_Baseline()
        self.Compute_Corrected_Waveform()
        self.Compute_Standard_Deviation()
        self.Compute_Amplitude()
        self.Compute_Edges()
        self.Compute_Edges_Lenghts()
        self.Compute_Time_Over_Threshold()
        self.Compute_Charge()