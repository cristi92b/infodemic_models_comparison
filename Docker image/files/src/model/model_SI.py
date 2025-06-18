#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Cristian Berceanu
# Copyright 2023 Cristian Berceanu. All rights reserved.

import numpy
import matplotlib.pyplot as plt
import math 
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import numpy as np
import csv
import fnmatch
import os
import statistics
from scipy.stats import skewnorm
from scipy.stats import skew
from scipy.stats import kurtosis
from scipy.stats import gennorm
from scipy.stats import exponnorm
from scipy.stats import linregress
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
from scipy.integrate import solve_ivp 

class SI_Model:
    def __init__(self,beta,mu,nu,rho,tau,theta):
        self.beta = beta     #infectios rate
        self.mu = mu         #birth rate
        self.nu = nu         #death rate (natural causes)
        self.rho = rho       #information engagement rate
        self.tau = tau       #info consumption rate
        self.theta = theta   #grass regrowth rate
        self.P = 1089        #total number of patches
        self.type = 'SI'

    def printparams(self):
        print('SI model params')

    def get_S(self,maxtick,S0,E0,I0,R0,F0):
        result = self.compute_discrete(maxtick,S0,I0,F0)
        return result[1]

    def get_E(self,maxtick,S0,E0,I0,R0,F0):
        return range(maxtick)

    def get_I(self,maxtick,S0,E0,I0,R0,F0):
        result = self.compute_discrete(maxtick,S0,I0,F0)
        return result[2]

    def get_R(self,maxtick,S0,E0,I0,R0,F0):
        return range(maxtick)

    def plot(self,maxtick,S0,I0,F0):
        result = self.compute(maxtick=maxtick,S0=S0,I0=I0,F0=F0)
        results_ivp = self.compute_ivp(maxtick=maxtick,S0=S0,I0=I0,F0=F0)
        results_discrete = self.compute_discrete(maxtick=maxtick,S0=S0,I0=I0,F0=F0)
        #print(result)
        fig = plt.figure()
        plt.plot(result[0],result[1],'b--',label='Susceptible')
        plt.plot(result[0],result[2],'r--',label='Infected')
        plt.plot(result[0],result[3],'k--',label='Total')
        plt.plot(results_ivp[0],results_ivp[1],'b')
        plt.plot(results_ivp[0],results_ivp[2],'r')
        plt.plot(results_ivp[0],results_ivp[3],'k')
        plt.plot(results_discrete[0],results_discrete[1],'b*')
        plt.plot(results_discrete[0],results_discrete[2],'ro')
        plt.plot(results_discrete[0],results_discrete[3],'k+')
        plt.ylabel('Total population')
        plt.legend()
        plt.grid()
        plt.show()

    def compute(self,maxtick,S0,I0,F0):
        S = S0
        I = I0
        N = S0 + I0
        F = F0
        S_array = [ S ]
        I_array = [ I ]
        N_array = [ (S+I) ]
        F_array = [ F ]
        P = self.P
        for t in range(maxtick-1):
            S_k = S
            I_k = I
            N_k = N
            F_k = F
            try:
                S = S_k + self.mu * N_k - self.beta * S_k * I_k / N_k - self.nu * S_k - self.rho * S_k / F_k 
                I = I_k + self.beta * S_k * I_k / N_k - self.nu * I_k - self.rho * I_k / F_k 
                #F = F_k - self.theta * F_k * 3  + self.tau * N_k * 2.15 / P #* 300 #* N_k * 2.15
                #F = F_k - self.tau * N_k  +  self.theta * P / F_k
                #F = F_k - self.tau * N_k   +  self.theta * P / F_k
                #F = F_k -  0.1 * N_k  +  0.03 * (P - N_k)
                #F = F_k + 10*P - self.rho * F_k
                F = F_k + 3*P - self.rho * F_k
                #100 * P
                N = S + I
                S_array.append(S)
                I_array.append(I)
                N_array.append(N)
                F_array.append(F)
            except Exception as e:
                print("Exception: " + str(e))
        return [range(maxtick),S_array,I_array,N_array,F_array]
    
    def compute_rhs(self, t, v):
        S,I,F = v
        N = S + I
        dS = self.mu * N - self.beta * S * I / N - self.nu * S - self.rho * S / F
        dI = self.beta * S * I / N - self.nu * I - self.rho * I / F 
        dF = 3 * self.P - self.rho * F
        return [ dS , dI , dF ]
    
    def compute_ivp(self,maxtick,S0,I0,F0):
        result = solve_ivp(self.compute_rhs, (0, maxtick),[S0,I0,F0])
        return [ result.t , result.y[0,:], result.y[1,:] , np.sum(result.y[0:2],axis=0) , result.y[2,:] ]

    def compute_discrete(self,maxtick,S0,I0,F0):
        result = solve_ivp(self.compute_rhs, (0, maxtick),[S0,I0,F0])
        time = [ 0 ]
        S = [ S0 ]
        I = [ I0 ]
        F = [ F0 ]
        for t in range(0,maxtick):
            if t != 0:
                S.append(np.interp(t, result.t, result.y[0,:]))
                I.append(np.interp(t, result.t, result.y[1,:]))
                F.append(np.interp(t, result.t, result.y[2,:]))
                time.append(t)
        N = np.sum([ S , I ],axis=0)
        return [ time , S , I , N , F ]

if __name__ == '__main__':
    print('Generating example...')
    example = SI_Model(beta=0.5,mu=0.0,nu=0.0,rho=0.0,tau=0.0,theta=0.0)
    example.plot(maxtick=50,S0=900,I0=450,F0=50000)