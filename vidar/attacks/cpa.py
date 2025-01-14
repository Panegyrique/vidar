from . import AES, LEAKAGE_MODEL, TARGET

import numpy as np
from tqdm import trange


class CPA():

    def __init__(self, plaintexts, traces, leakage_model, target, number_step=1):
        self._CheckDataIntegrity(plaintexts, traces, leakage_model, target, number_step)
        self.plaintexts = np.load(plaintexts)
        self.traces = np.load(traces)

        if leakage_model == LEAKAGE_MODEL.HAMMING_WEIGHT:
            self.hamming_weight = [self._HammingWeight(n) for n in range (0x00, 0xff + 1)] # pre-compute
        elif leakage_model == LEAKAGE_MODEL.HAMMING_DISTANCE:
            print("UNDER DEVELOPMENT")

        if target in TARGET.AES:
            temp = AES()
            self.sbox = temp.sbox

        self.number_step = number_step
        self._Attack()

    def _CheckDataIntegrity(self, plaintexts, traces, leakage_model, target, number_step):
        print("UNDER DEVELOPMENT")

    def _HammingWeight(self, x):
        return bin(x).count('1')
    
    def _TheoricalPowerLeakage(self, byte_subkey, plaintext):
        if self.hamming_weight:
            return self.hamming_weight[
                        self.sbox [
                            byte_subkey ^ plaintext
                        ]
                    ]
        else:
            print("UNDER DEVELOPMENT")
    
    def _Attack(self):

        number_traces, number_points = np.shape(self.traces)
        
        def OptimizedPearsonCorrelation(X, Y):
            X = np.asarray(X, dtype=np.float64)
            Y = np.asarray(Y, dtype=np.float64)
            if X.shape != Y.shape:
                raise ValueError("Arrays must have equal length")
            X_centered = X - np.mean(X)
            Y_centered = Y - np.mean(Y)
            numerator = np.sum(X_centered * Y_centered)
            denominator = np.sqrt(np.sum(X_centered ** 2) * np.sum(Y_centered ** 2))
            if denominator == 0:
                return 0.0
            return numerator / denominator
        
        recover_subkey = np.zeros(16)
        step_size = number_traces // self.number_step
        guesses_correlation_evolution = np.zeros((16, 256, self.number_step))

        for byte_index in trange(16, desc="Recover key"):
            for byte_subkey in trange(0x00, 0xff + 1, desc=f"Subkey byte {byte_index}"):

                theorical_power = np.zeros(number_traces)
                for trace_index in range(0, number_traces):
                    theorical_power[trace_index] = self._TheoricalPowerLeakage(byte_subkey, self.plaintexts[trace_index][byte_index])

                for i in range(self.number_step):
                    num_traces_to_use = (i+1) * step_size

                    point_correlation = np.zeros(number_points)
                    for point_index in range(number_points):
                        point_correlation[point_index] = OptimizedPearsonCorrelation(
                            theorical_power[:num_traces_to_use],
                            self.traces[:num_traces_to_use, point_index]
                        )
                        
                    guesses_correlation_evolution[byte_index, byte_subkey, i] = np.max(np.abs(point_correlation))
            
            final_correlations = guesses_correlation_evolution[byte_index, :, -1]
            recover_subkey[byte_index] = np.argmax(final_correlations)

        self.guesses_correlation_evolution = guesses_correlation_evolution
        self.recover_subkey = recover_subkey

        hex_values = [f"0x{int(val):02X}" for val in recover_subkey]
        print(f"\nRecovered Key : {hex_values}")
