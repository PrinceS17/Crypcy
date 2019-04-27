import os, sys, json, traceback, inspect, numpy
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from tools import load_data, get_data_from_cache, get_tid, get_ts
from preprocessing import *

from test_weka import *
from hist_processing import *


'''
    Advance Function 2:
        Using price, volume to generate dataset from daily historical data of the coin, 
        we try to choose suitable regression model to give a basic prediction of the future price
        of the currency. We get 5-day predictions and define utility as the average value
        of them. 
        Though trivial to fit the price curve, the function is advance because of the online 
        learning potential and flexibility in model selection.
'''
def main():
    # get data from cache
    d1 = get_data_from_cache()
    num = 5

    try: os.mkdir('HistSet')
    except OSError: pass
    else: pass
    
    try: os.mkdir('Predict')
    except OSError: pass
    else: pass

    for r in d1:
        sym = r['symbol']    

        # generate dataset from history and training
        path = os.path.join('HistSet', 'histSet_%s.arff' % sym)
        flag = dataset_from_history(path, sym, num)
        if flag < 0: continue                           # no history data
        preds = train('GaussianProcesses', sym, num)
        utility = numpy.average([value for _, value in enumerate(preds)])

        # output to file
        data = {'id':r['id'], 'symbol': sym, 'name':r['name'], 'utility':utility,}
        data['prediction'] = {}
        for i, a in enumerate(preds):
            data['prediction'][i] = a
        pred_path = os.path.join('Predict', 'pred_%s.txt' % sym)
        f = open(pred_path, 'w')
        f.write(json.dumps(data, indent=4))
        f.close()

if __name__ == "__main__":
    
    try:
        jvm.start(system_cp=True, packages=True, max_heap_size='512m')   
        main()
    except Exception as e:
        print(traceback.format_exc())
    finally:
        jvm.stop()
