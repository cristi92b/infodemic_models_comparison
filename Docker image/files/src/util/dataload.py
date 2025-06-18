#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Cristian Berceanu
# Copyright 2023 Cristian Berceanu. All rights reserved.

import logging
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


class SEIRS_Data:
    def __init__(self,xlimit=200):
        self.xlimit = xlimit
        self.Total_min = []
        self.Total_avg = []
        self.Total_max = []
        self.Susceptible_min = []
        self.Susceptible_avg = []
        self.Susceptible_max = []
        self.Exposed_min = []
        self.Exposed_avg = []
        self.Exposed_max = []
        self.Infected_min = []
        self.Infected_avg = []
        self.Infected_max = []
        self.Recovered_min = []
        self.Recovered_avg = []
        self.Recovered_max = []
        self.xAxisArray = range(0,xlimit+1)

    def load(self,csvpath,nbruns = 1000):
        all_run_data_found = False
        try:
            with open(csvpath, newline='') as csvfile:
                #print('Opening file: ' + str(csvpath))
                logging.info('Opening experiment file: ' + str(csvpath))
                reader = csv.reader(csvfile, delimiter=',', quotechar='\"')
                for row in reader:
                    if all_run_data_found == False:
                        for cell in row:
                            if cell == '[all run data]':
                                all_run_data_found = True
                    if all_run_data_found == True and row[0] == '':
                        Total = []
                        Susceptible = []
                        Exposed = []
                        Infected = []
                        Recovered = []
                        for i in range(0,nbruns):
                            Total.append(int(row[1+6*i+0]))
                            Susceptible.append(int(row[1+6*i+1]))
                            Exposed.append(int(row[1+6*i+3]))
                            Infected.append(int(row[1+6*i+2]))
                            Recovered.append(int(row[1+6*i+4]))
                        self.Total_min.append(min(Total))
                        self.Total_avg.append(sum(Total)/len(Total))
                        self.Total_max.append(max(Total))
                        self.Susceptible_min.append(min(Susceptible))
                        self.Susceptible_avg.append(sum(Susceptible)/len(Susceptible))
                        self.Susceptible_max.append(max(Susceptible))
                        self.Exposed_min.append(min(Exposed))
                        self.Exposed_avg.append(sum(Exposed)/len(Exposed))
                        self.Exposed_max.append(max(Exposed))
                        self.Infected_min.append(min(Infected))
                        self.Infected_avg.append(sum(Infected)/len(Infected))
                        self.Infected_max.append(max(Infected))
                        self.Recovered_min.append(min(Recovered))
                        self.Recovered_avg.append(sum(Recovered)/len(Recovered))
                        self.Recovered_max.append(max(Recovered))
                #print(self.Total_avg)
                                
        except Exception as e:
            logging.error('Error: ' + str(e))
            print('Error: ' + str(e))

    def plot(self,outputfile='output.pdf'):
        fig, ax = plt.subplots()
        #ax.plot(self.xAxisArray, self.Susceptible_min, label = "Min")
        #ax.plot(self.xAxisArray, self.Susceptible_max, label = "Max")


        ax.plot(self.xAxisArray, self.Susceptible_avg, label = "Susceptible")
        ax.fill_between(self.xAxisArray,self.Susceptible_min,self.Susceptible_max,alpha=0.3)

        ax.plot(self.xAxisArray, self.Infected_avg, label = "Infected")
        ax.fill_between(self.xAxisArray,self.Infected_min,self.Infected_max,alpha=0.3)

        if (self.Exposed_avg.count(0) != len(self.Exposed_avg)):
            ax.plot(self.xAxisArray, self.Exposed_avg, label = "Exposed")
            ax.fill_between(self.xAxisArray,self.Exposed_min,self.Exposed_max,alpha=0.3)

        if (self.Recovered_avg.count(0) != len(self.Recovered_avg)):
            ax.plot(self.xAxisArray, self.Recovered_avg, label = "Recovered")
            ax.fill_between(self.xAxisArray,self.Recovered_min,self.Recovered_max,alpha=0.3)

        ax.plot(self.xAxisArray, self.Total_avg, label = "Total")
        ax.fill_between(self.xAxisArray,self.Total_min,self.Total_max,alpha=0.3)

        #ax.set_aspect(aspect=aspectratio)
        #ax.set(xlabel=xlabel, ylabel=ylabel)
        ax.grid()
        ax.legend()
        #fig.show()


        fig.savefig(outputfile,bbox_inches='tight')

