# make sure you've got the following packages installed
import scipy as sp
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.optimize as spopt
import scipy.fftpack as spfft
import scipy.ndimage as spimg
import cvxpy as cvx
import pywt #PyWavelets
from skimage.filters import gabor_kernel #gabor kernels


class CompressedSensing:
    def __init__(self, dataset, basis="DCT"):
        self.DataSet = dataset
        self.BasisFunct = basis

        self.GenerateBasis()
        

    def SetCurrentDataset(self, dataset):
        self.DataSet = dataset
        
    def GetCurrentDataset(self):
        return self.DataSet

    def dct2(self):
        return scipy.fftpack.dct(scipy.fftpack.dct(self.DataSet.T, norm='ortho', axis=0).T, norm='ortho', axis=0)

    def idct2(self):
        return scipy.fftpack.idct(scipy.fftpack.idct(self.DataSet.T, norm='ortho', axis=0).T, norm='ortho', axis=0)

    def GenerateBasis(self):
        if self.BasisFunct.upper() == "DCT":
            self.Basis = spfft.idct(np.identity(self.DataSet.size), norm='ortho', axis=0)
        elif self.BasisFunct[0:2].upper() == "DB": 
            self.Basis = pywt.dwt(np.identity(self.DataSet.size), self.BasisFunct.lower())
        elif self.BasisFunct.upper() == "GABOR":
            self.Basis=np.real(gabor_kernel(frequency=0.1, theta=np.pi/4, sigma_x=3.0, sigma_y=5.0, offset=np.pi/5, n_stds=5))
            
        else:
            raise("Uh oh! you didn't give me the right basis.")

    def GaborBasis(self, n, w, phase, sigma, step=0.1):
        '''n = window size, w = frequency (omega), phase = angle, sigma = standard deviation or spread of gabor window, step sets the point resolution'''
        gab = []
        for i in np.arange(0,n,step):
            gab.append((1./(np.sqrt(2*np.pi)*sigma))*np.exp(-((i-(n/2))**2)/sigma**2)*np.cos(w*i+phase))
            
        gab = np.asarray(gab)
        self.Basis = gab
            

    def Resample(self, percentage):
        num_samples = round(float(self.DataSet.size)*percentage)
        print("Selected "+str(num_samples)+" out of "+str(self.DataSet.size)+" ("+str(percentage*100.0)+"%)")
        random_index = np.random.choice(self.DataSet.size, num_samples, replace=False)

        self.DataSetResampled = self.DataSet[random_index]
        self.BasisResampled = self.Basis[random_index]

    def L1Optimization(self):
        vx = cvx.Variable(self.DataSet.size)
        objective = cvx.Minimize(cvx.norm(vx, 1))
        #constraints = [A*vx == y2]
        constraints = [self.BasisResampled*vx == self.DataSetResampled]
        prob = cvx.Problem(objective, constraints)
        result = prob.solve(verbose=True)
        self.vx = vx
        self.SparseMatrix = vx.value

    def ReconstructSignal(self):                
        x = np.array(self.SparseMatrix)
        x = np.squeeze(x)
        return spfft.idct(x, norm='ortho', axis=0)

        
