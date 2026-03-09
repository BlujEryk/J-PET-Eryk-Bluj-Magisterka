import numpy as np
from Histograms_Saver import *

class Events_List:
    

    def __init__(self, events_list):
        self.events_list = events_list


    def Cut_When_Not_All_Variables_Were_Computed(self):
        self.events_list = [event for event in self.events_list if (event[0].all_variables_computed and event[1].all_variables_computed)]    


    def Cut_Low_Amplitudes(self):
        self.events_list = [event for event in self.events_list if (np.absolute(event[0].amplitude_value) > 3*event[0].standard_deviation and np.absolute(event[1].amplitude_value) > 3*event[1].standard_deviation)]


    def Cut_Too_Long_Signals(self):
        self.events_list = [event for event in self.events_list if (np.absolute(event[0].waveform[-1]) < event[0].standard_deviation and np.absolute(event[1].waveform[-1]) < event[1].standard_deviation)]


    def Cut_Non_Coincidences(self):
        self.events_list = [event for event in self.events_list if ((event[1].detection_time - event[0].detection_time > 3000) and (event[1].detection_time - event[0].detection_time < 7000))]
        # prawy i lewy prog do pozmieniania (ps)


    def Cut_Charges_In_Range_200_380(self, bound_200, bound_380):
        self.events_list = [event for event in self.events_list if ((event[0].charge_value >= bound_200) and (event[1].charge_value >= bound_200) and (bound_380 >= event[0].charge_value) and (bound_380 >= event[1].charge_value))]
        # self.events_list_200_380 = [event for event in self.events_list if ((event[0].charge_value >= bound_200) and (event[1].charge_value >= bound_200) and (bound_380 >= event[0].charge_value) and (bound_380 >= event[1].charge_value))]
        # return self.events_list_200_380


    def Execute_Preliminary_Cuts(self):
        self.Cut_When_Not_All_Variables_Were_Computed()
        self.Cut_Low_Amplitudes()
        self.Cut_Too_Long_Signals()
        self.Cut_Non_Coincidences()