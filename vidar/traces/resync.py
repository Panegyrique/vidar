from . import CONVERT

class RESYNC(CONVERT):

    def __init__(self, moving_operator=None, window_size=None, min_peak_dist=None, min_peak_height=None):

        if moving_operator == None:
            print("Find moving operator")

        if window_size == None:
            print("Find window size")

        if min_peak_dist == None:
            print("Find min peak dist")
            
        if min_peak_height == None:
            print("Find min peak height")
        
        self.resync_traces()

    
    def resync_traces(self):
        print("Need to be implemente")