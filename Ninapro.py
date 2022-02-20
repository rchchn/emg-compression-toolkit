import numpy as np
import pandas as pd

from scipy.io import loadmat

class Database:
    def __init__(self):
        self.database_root = ("./")
        

    def LoadDataset(self, path):
        '''
        Ingests a .mat matlab dataset from the Ninapro database.  Removes
        extraneous data keys (like the matlab header, version, etc.) and
        returns the data as a pandas dataframe
        '''
        dataset = loadmat(path)
        header = dataset.pop("__header__")
        version = dataset.pop("__version__")
        globs = dataset.pop("__globals__")
        return pd.DataFrame(dataset.items())

    
    def LoadEMGDataset(self, path):
        dataset = loadmat(path)
        data = pd.DataFrame(dataset['emg'])
        data['stimulus'] = dataset['restimulus'] 
        data['repetition'] = dataset['repetition']

        self.DataSet = data        
        return data

    def SetCurrentDataset(self, dataset):
        self.DataSet = dataset
        
    def GetCurrentDataset(self):
        return self.DataSet

class Dataset:
    def __init__(self, dataset):
        self.DataSet = dataset

    def SetCurrentDataset(self, dataset):
        self.DataSet = dataset
        
    def GetCurrentDataset(self):
        return self.DataSet
        
    def FilterStimulus(self, stim, save=False):
        isTrue = self.DataSet['stimulus']==stim
        if save:
            self.DataSet = self.DataSet[isTrue]
        return self.DataSet[isTrue]
    
    def FilterRepetition(self, rep, save=False):
        isTrue = self.DataSet['repetition']==rep
        if save:
            self.DataSet = self.DataSet[isTrue]
        return self.DataSet[isTrue]
    
