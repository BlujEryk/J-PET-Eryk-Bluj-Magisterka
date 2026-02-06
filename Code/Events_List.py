import numpy as np

class Events_List:
    
    def __init__(self, events_list):
        self.events_list = events_list

    def Cut_Low_Amplitudes(self):
        self.events_list = [event for event in self.events_list if (np.absolute(event[0].amplitude_value) > 3*event[0].standard_deviation and np.absolute(event[1].amplitude_value) > 3*event[1].standard_deviation)]

    def Cut_Too_Long_Signals(self):
        self.events_list = [event for event in self.events_list if (np.absolute(event[0].waveform[-1]) < event[0].standard_deviation and np.absolute(event[1].waveform[-1]) < event[1].standard_deviation)]

    def Cut_Non_Coincidences(self):
        self.events_list = [event for event in self.events_list if ((event[1].signal_detection_time - event[0].signal_detection_time > 3000) and (event[1].signal_detection_time - event[0].signal_detection_time < 7000))]
        # prawy i lewy prog do pozmieniania (ps)

    def Execute_All_Cuts(self):
        self.Cut_Low_Amplitudes()
        self.Cut_Too_Long_Signals()
        self.Cut_Non_Coincidences()