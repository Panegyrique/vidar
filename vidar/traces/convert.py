from pathlib import Path
import scared
import numpy as np
import pandas as pd
import plotly.express as px


class CONVERT():

    def __init__(self, path, focus_window=(None, None), nb_traces=10):
        assert isinstance(path, Path), "Input variables should be a Path from pathlib."
        self._traces = {
            "ciphertext": None,
            "key": None,
            "plaintext": None,
            "samples": None
        }

        try:
            if path.suffix.lower() == ".npy":
                return
            elif path.suffix.lower() == ".ets":
                self.ets_to_numpy(path)
            elif path.suffix.lower() == ".bin":
                self.bin_to_numpy(path)
            else:
                print("File format not supported.")
        except Exception as e:
            print(f"An error has occurred : {e}.")

        if focus_window[0] == None or focus_window[1] == None:
            self.show_traces(nb_traces)
            self.choose_area_of_interest()
        else:
            self._traces["samples"] = self._traces["samples"][:, focus_window[0]:focus_window[1]]

    
    def ets_to_numpy(self, path): # Can be updated case not that name
        ths = scared.traces.read_ths_from_ets_file(path)
        self._traces["ciphertext"] = np.array(ths.metadatas['ciphertext'])
        self._traces["key"] = np.array(ths.metadatas['key'])
        self._traces["plaintext"] = np.array(ths.metadatas['plaintext'])
        self._traces["samples"] = np.array(ths.samples)


    def bin_to_numpy(self, path):
        print("Need to be implement")
    

    def show_traces(self, nb_traces):
        assert self._traces["samples"] is not None, "No trace data available to show"
        df = pd.DataFrame(self._traces["samples"][:nb_traces].T)
        df = df.reset_index().melt(id_vars='index', var_name='Trace', value_name='Amplitude') 
        fig = px.line(df, x='index', y='Amplitude', color='Trace', title='Trace Visualization')
        fig.update_layout(
            xaxis_title="Time samples",
            yaxis_title="Amplitude",
            dragmode="select"
        )
        fig.show()

    
    def choose_area_of_interest(self):
        while(True):
            print('Enter the area of interest (x1, x2) : ')
            window = input()
            try:
                x1, x2 = map(int, window.split(','))
                if x1 < 0 or x2 > self._traces["samples"].shape[1] or x1 >= x2:
                    print("Invalid range. Please ensure x1 and x2 are within bounds and x1 < x2.")
                else:
                    break
            except ValueError:
                print("Invalid input. Please enter two integers separated by a comma (e.g., 450,650).")
        self._traces["samples"] = self._traces["samples"][:, x1:x2]
        