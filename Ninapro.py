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
        data['stimulus'] = dataset['stimulus'] 
        data['restimulus'] = dataset['restimulus'] 
        data['repetition'] = dataset['repetition']
        data['rerepetition'] = dataset['rerepetition']

        self.DataSet = data        
        return data
    
    def FilterDataset(self, stimulus, repetition, reannotated=False): 
        if reannotated:
            stim = self.DataSet[(self.DataSet.stimulus==stimulus) & (self.DataSet.repetition==repetition) & 
                                (self.DataSet.restimulus>=0) & (self.DataSet.rerepetition>=0)] 
        else:
            
            stim = self.DataSet[(self.DataSet.stimulus==stimulus) & (self.DataSet.repetition==repetition) & 
                                (self.DataSet.restimulus==stimulus) & (self.DataSet.rerepetition==1)] 
             
        stim.pop('stimulus')        
        stim.pop('repetition')
        stim.pop('restimulus')        
        stim.pop('rerepetition') 
        return stim.to_numpy().T 

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
    
    def FilterDataset(self, stim=None, rep=None, filterRe=False, save=False):
        if filterRe==None:
            temp=self.DataSet[(self.DataSet['stimulus']==stim) & (self.DataSet['repetition']==rep)]
        else:
            temp=self.DataSet[(self.DataSet['restimulus']==stim) & (self.DataSet['rerepetition']==rep)]
            
        if save:
            self.DataSet = temp
        return temp
        
        
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
        
    def FilterReStimulus(self, stim, save=False):
        isTrue = self.DataSet['restimulus']==stim
        if save:
            self.DataSet = self.DataSet[isTrue]
        return self.DataSet[isTrue]
    
    def FilterReRepetition(self, rep, save=False):
        isTrue = self.DataSet['rerepetition']==rep
        if save:
            self.DataSet = self.DataSet[isTrue]
        return self.DataSet[isTrue]
    
