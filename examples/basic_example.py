from pathlib import Path
from vidar import CPA, LEAKAGE_MODEL, TARGET, CONVERT, DASH_CPA


def main():
    plaintexts = Path(__file__).parent / 'dataset/example-2/textins.npy'
    traces = Path(__file__).parent / 'dataset/example-2/traces.npy'

    cpa_attack = CPA(
        plaintexts, 
        traces, 
        LEAKAGE_MODEL.HAMMING_WEIGHT, 
        TARGET.AES.FIRST_ROUND,
        number_step=1,
    )
    
    dashboard = DASH_CPA(cpa_attack)
    dashboard.run(debug=False)
    

if __name__ == "__main__":
    # my_traces = TRACES(Path(__file__).parent / 'traces/dataset/stagegate1.ets')
    # my_traces.show_traces(10)
    main()
