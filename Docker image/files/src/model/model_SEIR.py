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

class SEIR_Model:
    def __init__(self,beta,gamma,sigma,mu,nu,rho,tau,theta):
        self.beta = beta     #infectios rate
        self.gamma = gamma   #recovery rate
        self.sigma = sigma   #incubation rate
        self.mu = mu         #birth rate
        self.nu = nu         #death rate (natural causes)
        self.rho = rho       #information engagement rate
        self.tau = tau       #info consumption rate
        self.theta = theta   #grass regrowth rate
        self.P = 1089        #total number of patches
        self.type = 'SEIR'

    def printparams(self):
        print('SEIR model params')

    def get_S(self,maxtick,S0,E0,I0,R0,F0):
        result = self.compute_discrete(maxtick,S0,E0,I0,R0,F0)
        return result[1]

    def get_E(self,maxtick,S0,E0,I0,R0,F0):
        result = self.compute_discrete(maxtick,S0,E0,I0,R0,F0)
        return result[2]

    def get_I(self,maxtick,S0,E0,I0,R0,F0):
        result = self.compute_discrete(maxtick,S0,E0,I0,R0,F0)
        return result[3]

    def get_R(self,maxtick,S0,E0,I0,R0,F0):
        result = self.compute_discrete(maxtick,S0,E0,I0,R0,F0)
        return result[5]

    def plot(self,maxtick,S0,E0,I0,R0,F0):
        result = self.compute(maxtick=maxtick,S0=S0,E0=E0,I0=I0,R0=R0,F0=F0)
        results_ivp = self.compute_ivp(maxtick=maxtick,S0=S0,E0=E0,I0=I0,R0=R0,F0=F0)
        results_discrete = self.compute_discrete(maxtick=maxtick,S0=S0,E0=E0,I0=I0,R0=R0,F0=F0)
        #print(result)
        fig = plt.figure()
        plt.plot(result[0],result[1],'b--',label='Susceptible')
        plt.plot(result[0],result[3],'r--',label='Infected')
        plt.plot(result[0],result[2],'m--',label='Exposed')
        plt.plot(result[0],result[5],'c--',label='Recovered')
        #plt.plot(result[0],result[4],'k--',label='Total')
        plt.plot(results_ivp[0],results_ivp[1],'b')
        plt.plot(results_ivp[0],results_ivp[3],'r')
        plt.plot(results_ivp[0],results_ivp[2],'m')
        plt.plot(results_ivp[0],results_ivp[5],'c')
        plt.plot(results_ivp[0],results_ivp[4],'k')
        plt.plot(results_discrete[0],results_discrete[1],'b*')
        plt.plot(results_discrete[0],results_discrete[3],'ro')
        plt.plot(results_discrete[0],results_discrete[2],'ms')
        plt.plot(results_discrete[0],results_discrete[5],'cp')
        plt.plot(results_discrete[0],results_discrete[4],'k+')
        plt.ylabel('Total population')
        plt.legend()
        plt.grid()
        plt.show()

    def compute(self,maxtick,S0,E0,I0,R0,F0):
        S = S0
        E = E0
        I = I0
        N = S0 + I0 + R0 + E0
        R = R0
        F = F0
        S_array = [ S ]
        E_array = [ E ]
        I_array = [ I ]
        N_array = [ (S+I+R+E) ]
        R_array = [ R ]
        F_array = [ F ]
        P = self.P
        for t in range(maxtick-1):
            S_k = S
            E_k = E
            I_k = I
            N_k = N
            R_k = R
            F_k = F
            try:
                S = S_k + self.mu * N_k - self.beta * S_k * I_k / N_k - self.nu * S_k - self.rho * S_k / F_k
                E = E_k + self.beta * S_k * I_k / N_k - self.sigma * E_k - self.nu * E_k - self.rho * E_k / F_k
                I = I_k - self.gamma * I_k  + self.sigma * E_k - self.nu * I_k - self.rho * I_k / F_k
                R = R_k + self.gamma * I_k - self.nu * R_k - self.rho * R_k / F_k
                F = F_k - self.tau * N_k + self.theta * P
                N = S + I + R + E
                S_array.append(S)
                E_array.append(E)
                I_array.append(I)
                N_array.append(N)
                R_array.append(R)
                F_array.append(F)
            except Exception as e:
                print("Exception: " + str(e))
        return [range(maxtick),S_array,E_array,I_array,N_array,R_array,F_array]

    def compute_rhs(self, t, v):
        S,E,I,R,F = v
        N = S + E + I + R
        dS = self.mu * N - self.beta * S * I / N - self.nu * S - self.rho * S / F
        dE = self.beta * S * I / N - self.sigma * E - self.nu * E - self.rho * E / F
        dI = - self.gamma * I  + self.sigma * E - self.nu * I - self.rho * I / F
        dR = self.gamma * I - self.nu * R - self.rho * R / F
        dF = - self.tau * N + self.theta * self.P
        return [ dS , dE , dI , dR , dF ]
    
    def compute_ivp(self,maxtick,S0,E0,I0,R0,F0):
        result = solve_ivp(self.compute_rhs, (0, maxtick),[S0,E0,I0,R0,F0])
        return [ result.t , result.y[0,:], result.y[1,:] , result.y[2,:] , np.sum(result.y[0:4],axis=0) , result.y[3,:] , result.y[4,:] ]
    
    def compute_discrete(self,maxtick,S0,E0,I0,R0,F0):
        result = solve_ivp(self.compute_rhs, (0, maxtick),[S0,E0,I0,R0,F0])
        time = [ 0 ]
        S = [ S0 ]
        E = [ E0 ]
        I = [ I0 ]
        R = [ R0 ]
        F = [ F0 ]
        for t in range(0,maxtick):
            if t != 0:
                S.append(np.interp(t, result.t, result.y[0,:]))
                E.append(np.interp(t, result.t, result.y[1,:]))
                I.append(np.interp(t, result.t, result.y[2,:]))
                R.append(np.interp(t, result.t, result.y[3,:]))
                F.append(np.interp(t, result.t, result.y[4,:]))
                time.append(t)
        N = np.sum([ S , E , I , R ],axis=0)
        return [ time , S , E , I , N , R , F ]
    
if __name__ == '__main__':
    print('Generating example...')
    example = SEIR_Model(beta=0.5,gamma=1.0,sigma=0.1,mu=0.0,nu=0.0,rho=0.0,tau=0.0,theta=0.0)
    example.plot(maxtick=50,S0=900,E0=0,I0=450,R0=0,F0=50000)