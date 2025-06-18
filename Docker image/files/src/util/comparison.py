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


class Comparison:
    def __init__(self,experimental, computed, maxticks, nbagents, parameters):
        self.experimental = experimental
        self.computed = computed
        self.maxticks = maxticks
        self.type = computed.type
        self.nbagents = nbagents
        self.parameters = parameters
        #print('Starting ' + str(computed.type) + ' model comparison')
        logging.info('Initializing Comparison for ' + str(self.type) + ' model, maxticks = ' + str(self.maxticks) + ', nbagents = ' + str(nbagents))

    def parse_filename(filename):
        if ('SEIRS' in filename):
            return 'SEIRS'
        elif ('SEIR' in filename):
            return 'SEIR'
        elif ('SIRS' in filename):
            return 'SIRS'
        elif ('SIR' in filename):
            return 'SIR'
        elif ('SIS' in filename):
            return 'SIS'
        else:
            return 'SI'

    def compute_aic(self,S0,E0,I0,R0,F0):
        logging.debug('Computing AIC')

        p = 0
        if self.type in [ 'SI', 'SIS' ]:
            p = 2
        elif self.type in [ 'SIR', 'SIRS' ]:
            p = 3
        else:
            p = 4
        
        #calculate for S
        y_actual = self.experimental.Susceptible_avg[0:self.maxticks]
        logging.debug('S_actual = ')
        logging.debug(str(y_actual))
        y_computed = self.computed.get_S(self.maxticks,S0,E0,I0,R0,F0)
        logging.debug('S_computed = ')
        logging.debug(str(y_computed))
        aic_S = aic.aic(y_actual, list(y_computed), p)
        
        #calculate for E
        y_actual = self.experimental.Exposed_avg[0:self.maxticks]
        logging.debug('E_actual = ')
        logging.debug(str(y_actual))
        y_computed = self.computed.get_E(self.maxticks,S0,E0,I0,R0,F0)
        logging.debug('E_computed = ')
        logging.debug(str(y_computed))
        aic_E = aic.aic(y_actual, list(y_computed), p)
        
        #calculate for I
        y_actual = self.experimental.Infected_avg[0:self.maxticks]
        logging.debug('I_actual = ')
        logging.debug(str(y_actual))
        y_computed = self.computed.get_I(self.maxticks,S0,E0,I0,R0,F0)
        logging.debug('I_computed = ')
        logging.debug(str(y_computed))
        aic_I = aic.aic(y_actual, list(y_computed), p)
        
        #calculate for R
        y_actual = self.experimental.Recovered_avg[0:self.maxticks]
        logging.debug('R_actual = ')
        logging.debug(str(y_actual))
        y_computed = self.computed.get_R(self.maxticks,S0,E0,I0,R0,F0)
        logging.debug('R_computed = ')
        logging.debug(str(y_computed))
        aic_R = aic.aic(y_actual, list(y_computed), p)

        retval = [ aic_S , aic_E , aic_I , aic_R ]

        logging.info(str(self.parameters) + ' AIC = ' + str(retval))
        return retval

    def compute_nrmse(self,S0,E0,I0,R0,F0):
        logging.info('Computing NRMSE')
        
        #calculate for S
        y_actual = (self.experimental.Susceptible_avg[0:self.maxticks]) #/ self.nbagents
        logging.info('S_actual = ')
        logging.info(str(y_actual))
        y_computed = self.computed.get_S(self.maxticks,S0,E0,I0,R0,F0)
        logging.info('S_computed = ')
        logging.info(str(y_computed))
        rms_S = math.sqrt(mean_squared_error(y_actual, y_computed, squared=True)) / self.nbagents
        
        #calculate for E
        y_actual = (self.experimental.Exposed_avg[0:self.maxticks]) #/ self.nbagents
        logging.info('E_actual = ') 
        logging.info(str(y_actual))
        y_computed = self.computed.get_E(self.maxticks,S0,E0,I0,R0,F0)
        logging.info('E_computed = ')
        logging.info(str(y_computed))
        rms_E = math.sqrt(mean_squared_error(y_actual, y_computed, squared=True)) / self.nbagents
        
        #calculate for I
        y_actual = (self.experimental.Infected_avg[0:self.maxticks]) #/ self.nbagents
        logging.info('I_actual = ')
        logging.info(str(y_actual))
        y_computed = self.computed.get_I(self.maxticks,S0,E0,I0,R0,F0)
        logging.info('I_computed = ')
        logging.info(str(y_computed))
        rms_I = math.sqrt(mean_squared_error(y_actual, y_computed, squared=True)) / self.nbagents
        
        #calculate for R
        y_actual = (self.experimental.Recovered_avg[0:self.maxticks]) #/ self.nbagents
        logging.info('R_actual = ')
        logging.info(str(y_actual))
        y_computed = self.computed.get_R(self.maxticks,S0,E0,I0,R0,F0)
        logging.info('R_computed = ')
        logging.info(str(y_computed))
        rms_R = math.sqrt(mean_squared_error(y_actual, y_computed, squared=True)) / self.nbagents

        retval = [ rms_S , rms_E , rms_I , rms_R ]
        
        logging.info(str(self.parameters) + ' NRMSE = ' + str(retval))
        return retval
    
    def compute_rsquared(self,S0,E0,I0,R0,F0):
        logging.debug('Computing RSQ')
        #rsq = r2_score(y, p(x)) # coefficient_of_dermination
        
        #calculate for S
        y_actual = self.experimental.Susceptible_avg[0:self.maxticks]
        logging.debug('S_actual = ')
        logging.debug(str(y_actual))
        y_computed = self.computed.get_S(self.maxticks,S0,E0,I0,R0,F0)
        logging.debug('S_computed = ')
        logging.debug(str(y_computed))
        rsq_S = self.rsquared(y_actual, y_computed, self.type)

        #calculate for E
        y_actual = self.experimental.Exposed_avg[0:self.maxticks]
        logging.debug('E_actual = ')
        logging.debug(str(y_actual))
        y_computed = self.computed.get_E(self.maxticks,S0,E0,I0,R0,F0)
        logging.debug('E_computed = ')
        logging.debug(str(y_computed))
        rsq_E = self.rsquared(y_actual, y_computed, self.type)

        #calculate for I
        y_actual = self.experimental.Infected_avg[0:self.maxticks]
        logging.debug('I_actual = ')
        logging.debug(str(y_actual))
        y_computed = self.computed.get_I(self.maxticks,S0,E0,I0,R0,F0)
        logging.debug('I_computed = ')
        logging.debug(str(y_computed))
        rsq_I = self.rsquared(y_actual, y_computed, self.type)

        #calculate for R
        rsq_I = self.rsquared(y_actual, y_computed, self.type)
        logging.debug('R_actual = ')
        logging.debug(str(y_actual))
        y_actual = self.experimental.Recovered_avg[0:self.maxticks]
        logging.debug('R_computed = ')
        logging.debug(str(y_computed))
        y_computed = self.computed.get_R(self.maxticks,S0,E0,I0,R0,F0)
        rsq_R = self.rsquared(y_actual, y_computed, self.type)
        
        retval = [ rsq_S , rsq_E , rsq_I , rsq_R ]
        
        logging.info(str(self.parameters) + ' RSQ = ' + str(retval))
        return retval

    def compute_pearson(self,S0,E0,I0,R0,F0):
        logging.debug('Computing Pearson')

        #calculate for S
        y_actual = self.experimental.Susceptible_avg[0:self.maxticks]
        logging.debug('S_actual = ')
        logging.debug(str(y_actual))
        y_computed = self.computed.get_S(self.maxticks,S0,E0,I0,R0,F0)
        logging.debug('S_computed = ')
        logging.debug(str(y_computed))
        pearson = np.corrcoef([y_actual, y_computed])
        pearson_S = pearson[1][0]

        #calculate for E
        y_actual = self.experimental.Exposed_avg[0:self.maxticks]
        logging.debug('E_actual = ')
        logging.debug(str(y_actual))
        y_computed = self.computed.get_E(self.maxticks,S0,E0,I0,R0,F0)
        logging.debug('E_computed = ')
        logging.debug(str(y_computed))
        pearson = np.corrcoef([y_actual, y_computed])
        pearson_E = pearson[1][0]

        #calculate for I
        y_actual = self.experimental.Infected_avg[0:self.maxticks]
        logging.debug('I_actual = ')
        logging.debug(str(y_actual))
        y_computed = self.computed.get_I(self.maxticks,S0,E0,I0,R0,F0)
        logging.debug('I_computed = ')
        logging.debug(str(y_computed))
        pearson = np.corrcoef([y_actual, y_computed])
        pearson_I = pearson[1][0]

        #calculate for R
        y_actual = self.experimental.Recovered_avg[0:self.maxticks]
        logging.debug('R_actual = ')
        logging.debug(str(y_actual))
        y_computed = self.computed.get_R(self.maxticks,S0,E0,I0,R0,F0)
        logging.debug('R_computed = ')
        logging.debug(str(y_computed))
        pearson = np.corrcoef([y_actual, y_computed])
        pearson_R = pearson[1][0]

        retval = [ pearson_S , pearson_E , pearson_I , pearson_R ]
        logging.info(str(self.parameters) + ' Pearson = ' + str(retval))
        return retval
    
    #SST or TSS
    def SST(self, y_actual):
        retval = 0
        mean = np.mean(y_actual)
        #print('Calculating SST, mean = ' + str(mean))
        for i in range(0,len(y_actual)):
            retval += ( y_actual[i] - mean ) ** 2
        return retval

    #SSR or ESS
    def SSR(self, y_actual, y_predicted):
        retval = 0
        if len(y_actual) != len(y_predicted):
            raise Exception('Error: Array length mismatch')
        else:
            mean = np.mean(y_actual)
            #print('Calculating SSR, mean = ' + str(mean))
            for i in range(0,len(y_predicted)):
                retval += ( y_predicted[i] - mean ) ** 2
        return retval


    #SSE or RSS
    def SSE(self, y_actual, y_predicted):
        retval = 0
        if len(y_actual) != len(y_predicted):
            raise Exception('Error: Array length mismatch')
        else:
            for i in range(0,len(y_predicted)):
                retval += ( y_actual[i] -  y_predicted[i] ) ** 2
        return retval

    #R squared (R^2)
    def rsquared(self, y_actual, y_predicted, model = 'Unknown'):
        retval = 0
        if len(y_actual) != len(y_predicted):
            raise Exception('Error: Array length mismatch')
        else:
            ssr_value = self.SSR(y_actual, y_predicted)
            sse_value = self.SSE(y_actual, y_predicted)
            sst_value = self.SST(y_actual)
            #print("[" + str(model) + "] Calculating R^2. Mean = " + str(np.mean(y_actual)) + ", SSR = " + str(ssr_value) + ", SST = " + str(sst_value))
            #retval =  ssr_value / sst_value
            retval = 1 - ( sse_value / sst_value )
        return retval

