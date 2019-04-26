import weka.core.jvm as jvm
from weka.classifiers import Classifier
from weka.core.converters import Loader
from weka.classifiers import Classifier, SingleClassifierEnhancer, MultipleClassifiersCombiner, FilteredClassifier, \
    PredictionOutput, Kernel, KernelClassifier
from weka.classifiers import Evaluation
from weka.filters import Filter
from weka.core.classes import Random, from_commandline
import weka.plot.classifiers as plot_cls
import weka.plot.graph as plot_graph
import weka.core.typeconv as typeconv
import os, sys, json, traceback

# given currency symbol, get the history file & train the model 
def train(option, sym, num):
    # load dataset given the symbol
    path = os.path.join('HistSet', 'histSet_%s.arff' % sym)
    loader = Loader("weka.core.converters.ArffLoader")
    dataset = loader.load_file(path)
    dataset.class_is_last()                 # set the last attribute as class attribute

    # load testset
    # testset = loader.load_file(os.path.join('HistSet', 'testSet_LTC.arff'))
    # testset.class_is_last()

    # define classifier
    cmd = {'DecisionTable': 'weka.classifiers.rules.DecisionTable -X 1 -S "weka.attributeSelection.BestFirst -D 1 -N 5"',
            'SMOreg': 'weka.classifiers.functions.SMOreg -C 1.0 -N 0 -I "weka.classifiers.functions.supportVector.RegSMOImproved -L 0.001 -W 1 -P 1.0E-12 -T 0.001 -V" -K "weka.classifiers.functions.supportVector.PolyKernel -C 250007 -E 1.0"',
            'LinearRegression': 'weka.classifiers.functions.LinearRegression -S 0 -R 1.0E-8',
            'GaussianProcesses': 'weka.classifiers.functions.GaussianProcesses -L 1.0 -N 0 -K "weka.classifiers.functions.supportVector.RBFKernel -C 250007 -G 1.0"',
            }
    
    cls = from_commandline(cmd[option], classname='weka.classifiers.Classifier')
    cls.build_classifier(dataset)

    # begin evaluating
    evaluation = Evaluation(dataset)

    # evaluation.evaluate_train_test_split(cls, dataset, 90, Random(1))   # evaluate by splitting train/test set
    evl = evaluation.test_model(cls, dataset)       # evaluate on test set
    print('predictions (' + str(len(evl)) + '): ')
    for i in range(num):
        print(evl[i - num], end=' ')
    # print(evaluation.summary())
    return evl[-num:]

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Usage: python %s [coin symbol] [days to predict]' % sys.argv[0])
        exit(1)
    sym = sys.argv[1]
    num = int(sys.argv[2])
    try:
        jvm.start(system_cp=True, packages=True, max_heap_size='512m')   
        train('GaussianProcesses', sym, num)
    except Exception as e:
        print(traceback.format_exc())
    finally:
        jvm.stop()
    