#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Cristian Berceanu
# Copyright 2023 Cristian Berceanu. All rights reserved.

import logging
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
#from mpl_toolkits.mplot3d.axes3d import Axes3D
import matplotlib as mpl
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import time
import itertools
import matplotlib
from enum import Enum
import math

#matplotlib.use('agg')

class PlotMode(Enum):
    DEFAULT = 1
    ALTERNATE = 2
    PEARSON = 3
    RSQUARED = 4

class ResultPlot:

    def __init__(self,exp,model,outdir,resultpath,usetex = True):
        self.exp = exp
        self.model = model
        self.outdir = outdir
        self.resultpath = resultpath
        self.rmse_label = 'NRMSE '
        if usetex:
            matplotlib.rc('text', usetex=True)
            self.usetex = True
            self.rsq_label = 'Coeff. Det. $R^2$ '
            self.pearson_label = 'Pearson Coeff. $\\rho$ '
        else:
            self.usetex = False
            self.rsq_label = 'Coeff. Det. '
            self.pearson_label = 'Pearson Coeff. '
        df = pd.read_csv(resultpath)
        self.dat = df.sort_values(['beta', 'gamma', 'sigma', 'xi'], ascending=True)

    def tex_alt(self,iftex,ifalt):
        if self.usetex:
            return iftex
        else:
            return ifalt

    def default_plot_name(self,fixedcol1=None,fixedval1=None,fixedcol2=None,fixedval2=None):
        retval = str(self.exp) + '_' + str(self.model)
        if fixedcol1 != None and fixedval1 != None:
            retval += '_' + str(fixedcol1) + '_' + str(fixedval1)
        if fixedcol2 != None and fixedval2 != None:
            retval += '_' + str(fixedcol2) + '_' + str(fixedval2)
        retval += '.png'
        return retval

    def combinations(self):
        #assert(self.model in [ 'SIRS', 'SEIR' , 'SEIRS' ])
        columns = { 'beta' , 'gamma' , 'sigma' , 'xi' }
        retval = []
        if self.model == 'SIRS':
            columns.remove('sigma')
            logging.info('Generating parameter combinations for SIRS model')
            retval = list(itertools.combinations(columns, 1))
        elif self.model == 'SEIR':
            columns.remove('xi')
            logging.info('Generating parameter combinations for SEIR model')
            retval = list(itertools.combinations(columns, 1))
        elif self.model == 'SEIRS':
            logging.info('Generating parameter combinations for SEIRS model')
            retval = list(itertools.combinations(columns, 2))
        else:
            logging.warning('ResultPlot.combinations(): Invalid model: ' + str(self.model))
        return retval
        

    def plot_all(self, plot_mode = PlotMode.DEFAULT):
        logging.info('Starting plot_all() for ' + str(self.exp) + ' ' + str(self.model))
        if not(os.path.exists(self.outdir)):
            os.makedirs(self.outdir)
        if self.model == 'SI':
            if plot_mode == PlotMode.DEFAULT:
                self.plotSI()
            elif plot_mode == PlotMode.ALTERNATE:
                self.plotSI_alt()
            elif plot_mode == PlotMode.PEARSON:
                self.plotSI_Pearson()
            elif plot_mode == PlotMode.RSQUARED:
                self.plotSI()
            else:
                logging.waring('plot_all(): Unknown plot mode: ' + str(plot_mode))
        elif self.model == 'SIS':
            if plot_mode == PlotMode.DEFAULT:
                self.plotSIS()
            elif plot_mode == PlotMode.ALTERNATE:
                self.plotSIS_alt4()
            elif plot_mode == PlotMode.PEARSON:
                self.plotSIS_Pearson()
            elif plot_mode == PlotMode.RSQUARED:
                self.plotSIS()
            else:
                logging.waring('plot_all(): Unknown plot mode: ' + str(plot_mode))
        elif self.model == 'SIR':
            if plot_mode == PlotMode.DEFAULT:
                self.plotSIR()
            elif plot_mode == PlotMode.ALTERNATE:
                self.plotSIR()
            elif plot_mode == PlotMode.PEARSON:
                self.plotSIR_Pearson()
            elif plot_mode == PlotMode.RSQUARED:
                self.plotSIR()
            else:
                logging.waring('plot_all(): Unknown plot mode: ' + str(plot_mode))
        elif self.model == 'SIRS':
            comb = self.combinations()
            for column in comb:
                column_name = column[0]
                cloumn_set = self.extract_set(column_name)
                for val in cloumn_set:
                    try:
                        if plot_mode == PlotMode.DEFAULT:
                            self.plotSIRS(column_name, val)
                        elif plot_mode == PlotMode.ALTERNATE:
                            self.plotSIRS(column_name, val)
                        elif plot_mode == PlotMode.PEARSON:
                            self.plotSIRS_Pearson(column_name, val)
                        elif plot_mode == PlotMode.RSQUARED:
                            self.plotSIRS(column_name, val)
                        else:
                            logging.waring('plot_all(): Unknown plot mode: ' + str(plot_mode))
                    except Exception as e:
                        logging.warning('Exception occurred while trying to plot SIRS model: ' + str(e))
        elif self.model == 'SEIR':
            comb = self.combinations()
            for column in comb:
                column_name = column[0]
                cloumn_set = self.extract_set(column_name)
                for val in cloumn_set:
                    try:
                        if plot_mode == PlotMode.DEFAULT:
                            self.plotSEIR(column_name, val)
                        elif plot_mode == PlotMode.ALTERNATE:
                            self.plotSEIR(column_name, val)
                        elif plot_mode == PlotMode.PEARSON:
                            self.plotSEIR_Pearson(column_name, val)
                        elif plot_mode == PlotMode.RSQUARED:
                            self.plotSEIR(column_name, val)
                        else:
                            logging.waring('plot_all(): Unknown plot mode: ' + str(plot_mode))
                    except Exception as e:
                        logging.warning('Exception occurred while trying to plot SEIR model: ' + str(e))
        elif self.model == 'SEIRS':
            comb = self.combinations()
            for columns in comb:
                column_1 = columns[0]
                column_2 = columns[1]
                column_1_set = self.extract_set(column_1)
                column_2_set = self.extract_set(column_2)
                for val_1 in column_1_set:
                    for val_2 in column_2_set:
                        try:
                            if plot_mode == PlotMode.DEFAULT:
                                self.plotSEIRS(fixedcol1 = column_1, fixedval1 = val_1, fixedcol2 = column_2, fixedval2 = val_2)
                            elif plot_mode == PlotMode.ALTERNATE:
                                self.plotSEIRS(fixedcol1 = column_1, fixedval1 = val_1, fixedcol2 = column_2, fixedval2 = val_2)
                            elif plot_mode == PlotMode.PEARSON:
                                self.plotSEIRS_Pearson(fixedcol1 = column_1, fixedval1 = val_1, fixedcol2 = column_2, fixedval2 = val_2)
                            elif plot_mode == PlotMode.RSQUARED:
                                self.plotSEIRS(fixedcol1 = column_1, fixedval1 = val_1, fixedcol2 = column_2, fixedval2 = val_2)
                            else:
                                logging.waring('plot_all(): Unknown plot mode: ' + str(plot_mode))
                        except Exception as e:
                            logging.warning('Exception occurred while trying to plot SEIRS model: ' + str(e))
        else:
            logging.warning('ResultPlot.plot_all(): Invalid model: ' + str(self.model))

    def extract_set(self,column):
        retval = set()
        df = self.dat.reset_index()
        for index, row in df.iterrows():
            retval.add(row[column])
        return sorted(retval)
        
    def build_matrix(self,xcol,ycol,zcol,filter1col = None, filter1val = 0.0, filter2col = None, filter2val = 0.0):
        xset = self.extract_set(xcol)
        yset = self.extract_set(ycol)
        xlen = len(xset)
        ylen = len(yset)
        matrix = np.zeros((xlen,ylen))
        df = self.dat
        for i in range(xlen):
            for j in range(ylen):
                if filter1col is None and filter2col is None:
                    found = df.loc[(df[xcol] == xset[i]) & (df[ycol] == yset[j])]
                elif filter1col is not None and filter2col is None:
                    found = df.loc[(df[xcol] == xset[i]) & (df[ycol] == yset[j]) & (df[filter1col] == filter1val)]
                else:
                    found = df.loc[(df[xcol] == xset[i]) & (df[ycol] == yset[j]) & (df[filter1col] == filter1val) & (df[filter2col] == filter2val)]
                firstrow = found.iloc[0]
                matrix[i][j] = firstrow[zcol]
        return matrix

    def get_beta_for_fixed_gamma(self,gamma,column):
        beta_array = list(self.extract_set('beta'))
        retval = []
        df = self.dat
        for beta_val in beta_array:
            #query_val = df.query('gamma==' + str(gamma) + ' & beta==' + str(beta_val))
            #print(type(query_val))
            #print(query_val)
            #print('gamma = ' + str(gamma) + ', beta = ' + str(beta_val))
            column_value = df.loc[(df['gamma'].eq(gamma)) & (df['beta'].eq(beta_val))] #df[(df['gamma'] == str(gamma)) & (df['beta'] == str(beta_val))][column]
            found_val = column_value[column].to_numpy()
            retval.append(found_val[0])
        return retval

    def get_beta_for_fixed_gamma2(self,gamma,column):
        beta_array = list(self.extract_set('beta'))
        retval = []
        df = self.dat
        for beta_val in beta_array:
            print('beta = ' + str(beta_val) + ' , gamma = ' + str(gamma))
            #row_df = df[(df['gamma'] == str(gamma))]
            row_df = df.query("gamma == " + str(gamma) + " and beta == " + str(beta_val))
            val_arr = row_df[column].to_numpy()
            retval.append(val_arr[0])
        return retval

    def plotSI(self):
        fig, axs = plt.subplots(2, 2, figsize=(8, 8), layout='constrained')
        axs[0][0].plot(self.dat['beta'],self.dat['NRMSE_S'])
        axs[0][1].plot(self.dat['beta'],self.dat['NRMSE_I'])
        axs[1][0].plot(self.dat['beta'],self.dat['Pearson_S'])
        axs[1][1].plot(self.dat['beta'],self.dat['Pearson_I'])
        axs[0][0].set_ylabel(self.rmse_label + '[S]')
        axs[0][1].set_ylabel(self.rmse_label + '[I]')
        axs[1][0].set_ylabel(self.pearson_label + '[S]')
        axs[1][1].set_ylabel(self.pearson_label + '[I]')
        for i in range(0,2):
            for j in range(0,2):
                axs[i][j].set_xlabel(self.tex_alt(r'$\beta$','beta'))
                axs[i][j].grid()
        #fig.suptitle('SI Model', fontsize=16)
        plt.savefig(os.path.join(self.outdir,self.default_plot_name()))
        plt.cla()
        plt.clf()
        plt.close()

    def plotSI_alt(self):
        fig, axs = plt.subplots(1, 4, figsize=(16, 4), layout='constrained')
        axs[0].plot(self.dat['beta'],self.dat['NRMSE_S'])
        axs[1].plot(self.dat['beta'],self.dat['NRMSE_I'])
        axs[2].plot(self.dat['beta'],self.dat['Pearson_S'])
        axs[3].plot(self.dat['beta'],self.dat['Pearson_I'])
        axs[0].set_ylabel(self.rmse_label + '[S]')
        axs[1].set_ylabel(self.rmse_label + '[I]')
        axs[2].set_ylabel(self.pearson_label + '[S]')
        axs[3].set_ylabel(self.pearson_label + '[I]')
        for j in range(0,4):
            axs[j].set_xlabel(self.tex_alt(r'$\beta$','beta'))
            axs[j].grid()
        #fig.suptitle('SI Model', fontsize=16)
        plt.savefig(os.path.join(self.outdir,self.default_plot_name()))
        plt.cla()
        plt.clf()
        plt.close()

    def plotSIS(self):
        beta = self.extract_set('beta')
        gamma = self.extract_set('gamma')
        left   = 0.0 #min(gamma) #0.0
        right  = 1.0 #max(gamma) #1.0
        bottom = 0.0 #min(beta) #0.0
        top    = 1.0 #max(beta) #1.0
        extent = [left, right, bottom, top]
        cmap_white = cmap = ListedColormap(["white"], name='WhiteMap')
        top = cmap_white.resampled(128)
        middle = mpl.colormaps['RdYlGn'].resampled(1280)
        bottom = cmap_white.resampled(128)
        newcolors = np.vstack((top(np.linspace(0, 1, 128)),
                       middle(np.linspace(0, 1, 1280)),
                       bottom(np.linspace(0, 1, 128))))
        newcmp = ListedColormap(newcolors, name='OrangeBlue')
        im = [None for x in range(4)]
        fig, axs = plt.subplots(2, 2, figsize=(8, 8), layout='constrained')
        NRMSE_S = self.build_matrix('beta','gamma','NRMSE_S')
        NRMSE_I = self.build_matrix('beta','gamma','NRMSE_I')
        Pearson_S = self.build_matrix('beta','gamma','Pearson_S')
        Pearson_I = self.build_matrix('beta','gamma','Pearson_I')

        Pearson_S = self.alter_pearson(Pearson_S,NRMSE_S)
        Pearson_I = self.alter_pearson(Pearson_I,NRMSE_I)
        
        im[0] = axs[0][0].imshow(NRMSE_S, cmap='RdYlGn_r', origin='lower', vmin=0, vmax=1, extent=extent)
        im[1] = axs[0][1].imshow(NRMSE_I, cmap='RdYlGn_r', origin='lower', vmin=0, vmax=1, extent=extent)
        im[2] = axs[1][0].imshow(Pearson_S, cmap='RdYlGn', origin='lower', vmin=-1, vmax=1, extent=extent)
        im[3] = axs[1][1].imshow(Pearson_I, cmap='RdYlGn', origin='lower', vmin=-1, vmax=1, extent=extent)
        for item in im:
            fig.colorbar(item, fraction=0.046, pad=0.04)
        axs[0][0].title.set_text(self.rmse_label + '[S]')
        axs[0][1].title.set_text(self.rmse_label + '[I]')
        axs[1][0].title.set_text(self.pearson_label + '[S]')
        axs[1][1].title.set_text(self.pearson_label + '[I]')
        for i in range(0,2):
            for j in range(0,2):
                axs[i][j].set_xlabel(self.tex_alt(r'$\gamma$','gamma'))
                axs[i][j].set_ylabel(self.tex_alt(r'$\beta$','beta'))
        fig.suptitle(self.model, fontsize=16)
        plt.savefig(os.path.join(self.outdir,self.default_plot_name()))
        plt.cla()
        plt.clf()
        plt.close()

    def plotSIS_alt(self):
        beta = self.extract_set('beta')
        gamma = self.extract_set('gamma')
        left   = 0.0 #min(gamma) #0.0
        right  = 1.0 #max(gamma) #1.0
        bottom = 0.0 #min(beta) #0.0
        top    = 1.0 #max(beta) #1.0
        extent = [left, right, bottom, top]
        cmap_white = cmap = ListedColormap(["white"], name='WhiteMap')
        top = cmap_white.resampled(128)
        middle = mpl.colormaps['RdYlGn'].resampled(1280)
        bottom = cmap_white.resampled(128)
        newcolors = np.vstack((top(np.linspace(0, 1, 128)),
                       middle(np.linspace(0, 1, 1280)),
                       bottom(np.linspace(0, 1, 128))))
        newcmp = ListedColormap(newcolors, name='OrangeBlue')
        im = [None for x in range(4)]
        fig, axs = plt.subplots(1, 4, figsize=(16, 4), layout='constrained')
        NRMSE_S = self.build_matrix('beta','gamma','NRMSE_S')
        NRMSE_I = self.build_matrix('beta','gamma','NRMSE_I')
        Pearson_S = self.build_matrix('beta','gamma','Pearson_S')
        Pearson_I = self.build_matrix('beta','gamma','Pearson_I')
        
        im[0] = axs[0].imshow(RSquared_S, cmap=newcmp, origin='lower', vmin=-1.2, vmax=1.2, extent=extent)
        im[1] = axs[1].imshow(RSquared_I, cmap=newcmp, origin='lower', vmin=-1.2, vmax=1.2, extent=extent)
        im[2] = axs[2].imshow(Pearson_S, cmap=newcmp, origin='lower', vmin=-1.2, vmax=1.2, extent=extent)
        im[3] = axs[3].imshow(Pearson_I, cmap=newcmp, origin='lower', vmin=-1.2, vmax=1.2, extent=extent)
        for item in im:
            fig.colorbar(item, fraction=0.046, pad=0.04)
        axs[0].title.set_text(self.rmse_label + '[S]')
        axs[1].title.set_text(self.rmse_label + '[I]')
        axs[2].title.set_text(self.pearson_label + '[S]')
        axs[3].title.set_text(self.pearson_label + '[I]')
        for j in range(0,3):
            axs[j].set_xlabel(self.tex_alt(r'$\gamma$','gamma'))
            axs[j].set_ylabel(self.tex_alt(r'$\beta$','beta'))
        fig.suptitle(self.model, fontsize=16)
        plt.savefig(os.path.join(self.outdir,self.default_plot_name()))
        plt.cla()
        plt.clf()
        plt.close()

    def plotSIS_alt2(self):
        base_results = os.path.dirname(self.resultpath)
        si_results_path = os.path.join(base_results,'SI_results.csv')
        si_df = pd.read_csv(si_results_path)
        beta = self.extract_set('beta')
        gamma = self.extract_set('gamma')
        left   = 0.0 #min(gamma) #0.0
        right  = 1.0 #max(gamma) #1.0
        bottom = 0.0 #min(beta) #0.0
        top    = 1.0 #max(beta) #1.0
        extent = [left, right, bottom, top]
        cmap_white = cmap = ListedColormap(["white"], name='WhiteMap')
        top = cmap_white.resampled(128)
        middle = mpl.colormaps['RdYlGn'].resampled(1280)
        bottom = cmap_white.resampled(128)
        newcolors = np.vstack((top(np.linspace(0, 1, 128)),
                       middle(np.linspace(0, 1, 1280)),
                       bottom(np.linspace(0, 1, 128))))
        newcmp = ListedColormap(newcolors, name='OrangeBlue')
        im = [None for x in range(4)]
        fig, axs = plt.subplots(2, 4, figsize=(16, 8), layout='constrained')
        RSquared_S = self.build_matrix('beta','gamma','RSquared_S')
        RSquared_I = self.build_matrix('beta','gamma','RSquared_I')
        Pearson_S = self.build_matrix('beta','gamma','Pearson_S')
        Pearson_I = self.build_matrix('beta','gamma','Pearson_I')
        
        im[0] = axs[0][0].imshow(RSquared_S, cmap=newcmp, origin='lower', vmin=-1.2, vmax=1.2, extent=extent)
        im[1] = axs[0][1].imshow(RSquared_I, cmap=newcmp, origin='lower', vmin=-1.2, vmax=1.2, extent=extent)
        im[2] = axs[1][0].imshow(Pearson_S, cmap=newcmp, origin='lower', vmin=-1.2, vmax=1.2, extent=extent)
        im[3] = axs[1][1].imshow(Pearson_I, cmap=newcmp, origin='lower', vmin=-1.2, vmax=1.2, extent=extent)

        axs[0][2].plot(si_df['beta'],si_df['RSquared_S'])
        axs[0][3].plot(si_df['beta'],si_df['RSquared_I'])
        axs[1][2].plot(si_df['beta'],si_df['Pearson_S'])
        axs[1][3].plot(si_df['beta'],si_df['Pearson_I'])
        
        #axs[0][2].scatter(si_df['beta'], si_df['RSquared_S'], c=cm.hot(np.abs(si_df['RSquared_S'])), edgecolor='none')
        #axs[0][3].scatter(si_df['beta'], si_df['RSquared_I'], c=cm.hot(np.abs(si_df['RSquared_I'])), edgecolor='none')
        #axs[1][2].scatter(si_df['beta'], si_df['Pearson_S'], c=cm.hot(np.abs(si_df['Pearson_S'])), edgecolor='none')
        #axs[1][3].scatter(si_df['beta'], si_df['Pearson_I'], c=cm.hot(np.abs(si_df['Pearson_I'])), edgecolor='none')
        
        #axs[0][2].set_ylabel(self.rsq_label + '[S]')
        #axs[0][3].set_ylabel(self.rsq_label + '[I]')
        #axs[1][2].set_ylabel(self.pearson_label + '[S]')
        #axs[1][3].set_ylabel(self.pearson_label + '[I]')

        for item in im:
            fig.colorbar(item, fraction=0.046, pad=0.04)
        axs[0][0].title.set_text(self.rsq_label + '[S]')
        axs[0][1].title.set_text(self.rsq_label + '[I]')
        axs[1][0].title.set_text(self.pearson_label + '[S]')
        axs[1][1].title.set_text(self.pearson_label + '[I]')
        axs[0][2].title.set_text(self.rsq_label + '[S]')
        axs[0][3].title.set_text(self.rsq_label + '[I]')
        axs[1][2].title.set_text(self.pearson_label + '[S]')
        axs[1][3].title.set_text(self.pearson_label + '[I]')
        for i in range(0,2):
            for j in range(0,2):
                axs[i][j].set_xlabel(self.tex_alt(r'$\gamma$','gamma'))
                axs[i][j].set_ylabel(self.tex_alt(r'$\beta$','beta'))
        for i in range(0,2):
            for j in range(2,4):
                ymin, ymax = axs[i][j].get_ylim()
                axs[i][j].set_xlabel(self.tex_alt(r'$\beta$','beta'))
                axs[i][j].set_ylim([max(-1,ymin), min(1,ymax)])
                #axs[i][j].grid()
        fig.suptitle("SIS Model (left) and SI Model (right)", fontsize=16)
        plt.savefig(os.path.join(self.outdir,self.default_plot_name()))
        plt.cla()
        plt.clf()
        plt.close()

    def plotSIS_alt3(self,gamma):
        beta = self.extract_set('beta')
        left   = 0.0 #min(gamma) #0.0
        right  = 1.0 #max(gamma) #1.0
        bottom = 0.0 #min(beta) #0.0
        top    = 1.0 #max(beta) #1.0
        extent = [left, right, bottom, top]
        cmap_white = cmap = ListedColormap(["white"], name='WhiteMap')
        top = cmap_white.resampled(128)
        middle = mpl.colormaps['RdYlGn'].resampled(1280)
        bottom = cmap_white.resampled(128)
        newcolors = np.vstack((top(np.linspace(0, 1, 128)),
                       middle(np.linspace(0, 1, 1280)),
                       bottom(np.linspace(0, 1, 128))))
        newcmp = ListedColormap(newcolors, name='OrangeBlue')
        im = [None for x in range(4)]
        fig, axs = plt.subplots(2, 4, figsize=(16, 8), layout='constrained')
        NRMSE_S = self.build_matrix('beta','gamma','NRMSE_S')
        NRMSE_I = self.build_matrix('beta','gamma','NRMSE_I')
        Pearson_S = self.build_matrix('beta','gamma','Pearson_S')
        Pearson_I = self.build_matrix('beta','gamma','Pearson_I')
        
        im[0] = axs[0][0].imshow(NRMSE_S, cmap='RdYlGn_r', origin='lower', vmin=0, vmax=1, extent=extent)
        im[1] = axs[0][1].imshow(NRMSE_I, cmap='RdYlGn_r', origin='lower', vmin=0, vmax=1, extent=extent)
        im[2] = axs[1][0].imshow(Pearson_S, cmap=newcmp, origin='lower', vmin=-1.2, vmax=1.2, extent=extent)
        im[3] = axs[1][1].imshow(Pearson_I, cmap=newcmp, origin='lower', vmin=-1.2, vmax=1.2, extent=extent)
        axs[0][2].plot(list(beta),self.get_beta_for_fixed_gamma(gamma,'NRMSE_S'), color='black')
        axs[0][3].plot(list(beta),self.get_beta_for_fixed_gamma(gamma,'NRMSE_I'), color='black')
        axs[1][2].plot(list(beta),self.get_beta_for_fixed_gamma(gamma,'Pearson_S'), color='black')
        axs[1][3].plot(list(beta),self.get_beta_for_fixed_gamma(gamma,'Pearson_I'), color='black')
        for item in im:
            fig.colorbar(item, fraction=0.046, pad=0.04)
        axs[0][0].title.set_text(self.rmse_label + '[S]')
        axs[0][1].title.set_text(self.rmse_label + '[I]')
        axs[1][0].title.set_text(self.pearson_label + '[S]')
        axs[1][1].title.set_text(self.pearson_label + '[I]')
        axs[0][2].title.set_text(self.rmse_label + '[S]')
        axs[0][3].title.set_text(self.rmse_label + '[I]')
        axs[1][2].title.set_text(self.pearson_label + '[S]')
        axs[1][3].title.set_text(self.pearson_label + '[I]')
        for i in range(0,2):
            for j in range(0,2):
                axs[i][j].set_xlabel(self.tex_alt(r'$\gamma$','gamma'))
                axs[i][j].set_ylabel(self.tex_alt(r'$\beta$','beta'))
        for i in range(0,2):
            for j in range(2,4):
                axs[i][j].set_xlabel(self.tex_alt(r'$\beta$','beta'))
                axs[i][j].axis('square')
                axs[i][j].set_xlim([0 , 1])
                axs[i][j].set_ylim([0 , 1])
        #fig.suptitle(self.model, fontsize=16)
        
        plt.savefig(os.path.join(self.outdir,self.default_plot_name()) + '_' + str(gamma) + '.png')
        plt.cla()
        plt.clf()
        plt.close()

    def pearson_rule(self,pearson_nrmse_tuple):
        pearson_val = pearson_nrmse_tuple[0]
        nrmse_val = pearson_nrmse_tuple[1]
        if not(np.isnan(pearson_val)):
            return pearson_val
        elif np.isnan(pearson_val) and math.isclose(nrmse_val, 0.0):
            return 1.0
        else:
            return 0.0

    def alter_pearson(self,pearson_matrix,nrmse_matrix):
        retval = nrmse_matrix.copy()
        for i in range(0,np.shape(nrmse_matrix)[0]):
            for j in range(0,np.shape(nrmse_matrix)[1]):
                retval[i][j] = self.pearson_rule((pearson_matrix[i][j],nrmse_matrix[i][j]))
        return retval

    def plotSIS_alt4(self):
        base_results = os.path.dirname(self.resultpath)
        si_results_path = os.path.join(base_results,'SI_results.csv')
        si_df = pd.read_csv(si_results_path)
        beta = self.extract_set('beta')
        gamma = self.extract_set('gamma')
        left   = 0.0 #min(gamma) #0.0
        right  = 1.0 #max(gamma) #1.0
        bottom = 0.0 #min(beta) #0.0
        top    = 1.0 #max(beta) #1.0
        extent = [left, right, bottom, top]
        cmap_white = cmap = ListedColormap(["white"], name='WhiteMap')
        top = cmap_white.resampled(128)
        middle = mpl.colormaps['RdYlGn'].resampled(1280)
        bottom = cmap_white.resampled(128)
        newcolors = np.vstack((top(np.linspace(0, 1, 128)),
                       middle(np.linspace(0, 1, 1280)),
                       bottom(np.linspace(0, 1, 128))))
        newcmp = ListedColormap(newcolors, name='OrangeBlue')
        im = [None for x in range(4)]
        fig, axs = plt.subplots(2, 4, figsize=(16, 8), layout='constrained')
        NRMSE_S = self.build_matrix('beta','gamma','NRMSE_S')
        NRMSE_I = self.build_matrix('beta','gamma','NRMSE_I')
        Pearson_S = self.build_matrix('beta','gamma','Pearson_S')
        Pearson_I = self.build_matrix('beta','gamma','Pearson_I')

        Pearson_S = self.alter_pearson(Pearson_S,NRMSE_S)
        Pearson_I = self.alter_pearson(Pearson_I,NRMSE_I)

        
        
        im[0] = axs[0][0].imshow(NRMSE_S, cmap='RdYlGn_r', origin='lower', vmin=0, vmax=1, extent=extent)
        im[1] = axs[0][1].imshow(NRMSE_I, cmap='RdYlGn_r', origin='lower', vmin=0, vmax=1, extent=extent)
        im[2] = axs[1][0].imshow(Pearson_S, cmap='RdYlGn', origin='lower', vmin=-1, vmax=1, extent=extent)
        im[3] = axs[1][1].imshow(Pearson_I, cmap='RdYlGn', origin='lower', vmin=-1, vmax=1, extent=extent)
        axs[0][2].plot(si_df['beta'],si_df['NRMSE_S'], color='black')
        axs[0][3].plot(si_df['beta'],si_df['NRMSE_I'], color='black')
        axs[1][2].plot(si_df['beta'],si_df['Pearson_S'], color='black')
        axs[1][3].plot(si_df['beta'],si_df['Pearson_I'], color='black')
        for item in im:
            fig.colorbar(item, fraction=0.046, pad=0.04)
        axs[0][0].title.set_text(self.rmse_label + '[S]')
        axs[0][1].title.set_text(self.rmse_label + '[I]')
        axs[1][0].title.set_text(self.pearson_label + '[S]')
        axs[1][1].title.set_text(self.pearson_label + '[I]')
        axs[0][2].title.set_text(self.rmse_label + '[S]')
        axs[0][3].title.set_text(self.rmse_label + '[I]')
        axs[1][2].title.set_text(self.pearson_label + '[S]')
        axs[1][3].title.set_text(self.pearson_label + '[I]')
        for i in range(0,2):
            for j in range(0,2):
                axs[i][j].set_xlabel(self.tex_alt(r'$\gamma$','gamma'))
                axs[i][j].set_ylabel(self.tex_alt(r'$\beta$','beta'))
        for i in range(0,2):
            for j in range(2,4):
                axs[i][j].set_xlabel(self.tex_alt(r'$\beta$','beta'))
                axs[i][j].axis('square')
                axs[i][j].set_xlim([0 , 1])
                axs[i][j].set_ylim([0 , 1])
        #fig.suptitle(self.model, fontsize=16)
        
        plt.savefig(os.path.join(self.outdir,self.default_plot_name()))
        plt.cla()
        plt.clf()
        plt.close()

    def plotSIR(self):
        beta = self.extract_set('beta')
        gamma = self.extract_set('gamma')
        left   = 0.0 #min(gamma) #0.0
        right  = 1.0 #max(gamma) #1.0
        bottom = 0.0 #min(beta) #0.0
        top    = 1.0 #max(beta) #1.0
        extent = [left, right, bottom, top]
        cmap_white = cmap = ListedColormap(["white"], name='WhiteMap')
        top = cmap_white.resampled(128)
        middle = mpl.colormaps['RdYlGn'].resampled(1280)
        bottom = cmap_white.resampled(128)
        newcolors = np.vstack((top(np.linspace(0, 1, 128)),
                       middle(np.linspace(0, 1, 1280)),
                       bottom(np.linspace(0, 1, 128))))
        newcmp = ListedColormap(newcolors, name='OrangeBlue')
        im = [None for x in range(6)]
        fig, axs = plt.subplots(2, 3, figsize=(12, 8), layout='constrained')
        NRMSE_S = self.build_matrix('beta','gamma','NRMSE_S')
        NRMSE_I = self.build_matrix('beta','gamma','NRMSE_I')
        NRMSE_R = self.build_matrix('beta','gamma','NRMSE_R')
        Pearson_S = self.build_matrix('beta','gamma','Pearson_S')
        Pearson_I = self.build_matrix('beta','gamma','Pearson_I')
        Pearson_R = self.build_matrix('beta','gamma','Pearson_R')

        Pearson_S = self.alter_pearson(Pearson_S,NRMSE_S)
        Pearson_I = self.alter_pearson(Pearson_I,NRMSE_I)
        Pearson_R = self.alter_pearson(Pearson_R,NRMSE_R)
        
        im[0] = axs[0][0].imshow(NRMSE_S, cmap='RdYlGn_r', origin='lower', vmin=0, vmax=1, extent=extent)
        im[1] = axs[0][1].imshow(NRMSE_I, cmap='RdYlGn_r', origin='lower', vmin=0, vmax=1, extent=extent)
        im[2] = axs[0][2].imshow(NRMSE_R, cmap='RdYlGn_r', origin='lower', vmin=0, vmax=1, extent=extent)
        im[3] = axs[1][0].imshow(Pearson_S, cmap='RdYlGn', origin='lower', vmin=-1, vmax=1, extent=extent)
        im[4] = axs[1][1].imshow(Pearson_I, cmap='RdYlGn', origin='lower', vmin=-1, vmax=1, extent=extent)
        im[5] = axs[1][2].imshow(Pearson_R, cmap='RdYlGn', origin='lower', vmin=-1, vmax=1, extent=extent)
        for item in im:
            fig.colorbar(item, fraction=0.046, pad=0.04)
        axs[0][0].title.set_text(self.rmse_label + '[S]')
        axs[0][1].title.set_text(self.rmse_label + '[I]')
        axs[0][2].title.set_text(self.rmse_label + '[R]')
        axs[1][0].title.set_text(self.pearson_label + '[S]')
        axs[1][1].title.set_text(self.pearson_label + '[I]')
        axs[1][2].title.set_text(self.pearson_label + '[R]')
        for i in range(0,2):
            for j in range(0,3):
                axs[i][j].set_xlabel(self.tex_alt(r'$\gamma$','gamma'))
                axs[i][j].set_ylabel(self.tex_alt(r'$\beta$','beta'))
        #fig.suptitle(self.model, fontsize=16)
        plt.savefig(os.path.join(self.outdir,self.default_plot_name()))
        plt.cla()
        plt.clf()
        plt.close()
        
    def plotSIRS(self,fixedcol = 'xi', fixedval = 1.0):
        if fixedcol == 'xi':
            xparam = 'gamma'
            yparam = 'beta'
        elif fixedcol == 'gamma':
            xparam = 'beta'
            yparam = 'xi'
        elif fixedcol == 'beta':
            xparam = 'gamma'
            yparam = 'xi'

        ycol = self.extract_set(yparam)
        xcol = self.extract_set(xparam)
        zcol = self.extract_set(fixedcol)
        
        left   = 0.0 #min(gamma) #0.0
        right  = 1.0 #max(gamma) #1.0
        bottom = 0.0 #min(beta) #0.0
        top    = 1.0 #max(beta) #1.0
        extent = [left, right, bottom, top]
        cmap_white = cmap = ListedColormap(["white"], name='WhiteMap')
        top = cmap_white.resampled(128)
        middle = mpl.colormaps['RdYlGn'].resampled(1280)
        bottom = cmap_white.resampled(128)
        newcolors = np.vstack((top(np.linspace(0, 1, 128)),
                       middle(np.linspace(0, 1, 1280)),
                       bottom(np.linspace(0, 1, 128))))
        newcmp = ListedColormap(newcolors, name='OrangeBlue')
        im = [None for x in range(6)]
        fig, axs = plt.subplots(2, 3, figsize=(12, 8), layout='constrained')
        NRMSE_S = self.build_matrix(yparam,xparam,'NRMSE_S', filter1col = fixedcol, filter1val = fixedval)
        NRMSE_I = self.build_matrix(yparam,xparam,'NRMSE_I', filter1col = fixedcol, filter1val = fixedval)
        NRMSE_R = self.build_matrix(yparam,xparam,'NRMSE_R', filter1col = fixedcol, filter1val = fixedval)
        Pearson_S = self.build_matrix(yparam,xparam,'Pearson_S', filter1col = fixedcol, filter1val = fixedval)
        Pearson_I = self.build_matrix(yparam,xparam,'Pearson_I', filter1col = fixedcol, filter1val = fixedval)
        Pearson_R = self.build_matrix(yparam,xparam,'Pearson_I', filter1col = fixedcol, filter1val = fixedval)

        Pearson_S = self.alter_pearson(Pearson_S,NRMSE_S)
        Pearson_I = self.alter_pearson(Pearson_I,NRMSE_I)
        Pearson_R = self.alter_pearson(Pearson_R,NRMSE_R)
        
        im[0] = axs[0][0].imshow(NRMSE_S, cmap='RdYlGn_r', origin='lower', vmin=0, vmax=1, extent=extent)
        im[1] = axs[0][1].imshow(NRMSE_I, cmap='RdYlGn_r', origin='lower', vmin=0, vmax=1, extent=extent)
        im[2] = axs[0][2].imshow(NRMSE_R, cmap='RdYlGn_r', origin='lower', vmin=0, vmax=1, extent=extent)
        im[3] = axs[1][0].imshow(Pearson_S, cmap='RdYlGn', origin='lower', vmin=-1, vmax=1, extent=extent)
        im[4] = axs[1][1].imshow(Pearson_I, cmap='RdYlGn', origin='lower', vmin=-1, vmax=1, extent=extent)
        im[5] = axs[1][2].imshow(Pearson_R, cmap='RdYlGn', origin='lower', vmin=-1, vmax=1, extent=extent)
        for item in im:
            fig.colorbar(item, fraction=0.046, pad=0.04)
        axs[0][0].title.set_text(self.rmse_label + '[S]')
        axs[0][1].title.set_text(self.rmse_label + '[I]')
        axs[0][2].title.set_text(self.rmse_label + '[R]')
        axs[1][0].title.set_text(self.pearson_label + '[S]')
        axs[1][1].title.set_text(self.pearson_label + '[I]')
        axs[1][2].title.set_text(self.pearson_label + '[R]')
        for i in range(0,2):
            for j in range(0,3):
                axs[i][j].set_xlabel(self.tex_alt('$\\' + xparam + '$',xparam))
                axs[i][j].set_ylabel(self.tex_alt('$\\' + yparam + '$',yparam)) 
        #fig.suptitle(self.model + ', ' +  self.tex_alt('$\\' + str(fixedcol) + ' = ' + str(fixedval) + '$',str(fixedcol) + ' = ' + str(fixedval)), fontsize=16)
        plt.savefig(os.path.join(self.outdir,self.default_plot_name(fixedcol,fixedval)))
        plt.cla()
        plt.clf()
        plt.close()
        
    def plotSEIR(self,fixedcol = 'sigma', fixedval = 1.0):
        if fixedcol == 'sigma':
            xparam = 'gamma'
            yparam = 'beta'
        elif fixedcol == 'gamma':
            xparam = 'beta'
            yparam = 'sigma'
        elif fixedcol == 'beta':
            xparam = 'gamma'
            yparam = 'sigma'

        ycol = self.extract_set(yparam)
        xcol = self.extract_set(xparam)
        zcol = self.extract_set(fixedcol)
        
        left   = 0.0 #min(gamma) #0.0
        right  = 1.0 #max(gamma) #1.0
        bottom = 0.0 #min(beta) #0.0
        top    = 1.0 #max(beta) #1.0
        extent = [left, right, bottom, top]
        cmap_white = cmap = ListedColormap(["white"], name='WhiteMap')
        top = cmap_white.resampled(128)
        middle = mpl.colormaps['RdYlGn'].resampled(1280)
        bottom = cmap_white.resampled(128)
        newcolors = np.vstack((top(np.linspace(0, 1, 128)),
                       middle(np.linspace(0, 1, 1280)),
                       bottom(np.linspace(0, 1, 128))))
        newcmp = ListedColormap(newcolors, name='OrangeBlue')
        im = [None for x in range(8)]
        fig, axs = plt.subplots(2, 4, figsize=(16, 8), layout='constrained')
        NRMSE_S = self.build_matrix(yparam,xparam,'NRMSE_S', filter1col = fixedcol, filter1val = fixedval)
        NRMSE_E = self.build_matrix(yparam,xparam,'NRMSE_E', filter1col = fixedcol, filter1val = fixedval)
        NRMSE_I = self.build_matrix(yparam,xparam,'NRMSE_I', filter1col = fixedcol, filter1val = fixedval)
        NRMSE_R = self.build_matrix(yparam,xparam,'NRMSE_R', filter1col = fixedcol, filter1val = fixedval)
        Pearson_S = self.build_matrix(yparam,xparam,'Pearson_S', filter1col = fixedcol, filter1val = fixedval)
        Pearson_E = self.build_matrix(yparam,xparam,'Pearson_E', filter1col = fixedcol, filter1val = fixedval)
        Pearson_I = self.build_matrix(yparam,xparam,'Pearson_I', filter1col = fixedcol, filter1val = fixedval)
        Pearson_R = self.build_matrix(yparam,xparam,'Pearson_R', filter1col = fixedcol, filter1val = fixedval)

        Pearson_S = self.alter_pearson(Pearson_S,NRMSE_S)
        Pearson_I = self.alter_pearson(Pearson_I,NRMSE_I)
        Pearson_R = self.alter_pearson(Pearson_R,NRMSE_R)
        Pearson_E = self.alter_pearson(Pearson_E,NRMSE_E)
        
        im[0] = axs[0][0].imshow(NRMSE_S, cmap='RdYlGn_r', origin='lower', vmin=0, vmax=1, extent=extent)
        im[1] = axs[0][1].imshow(NRMSE_E, cmap='RdYlGn_r', origin='lower', vmin=0, vmax=1, extent=extent)
        im[2] = axs[0][2].imshow(NRMSE_I, cmap='RdYlGn_r', origin='lower', vmin=0, vmax=1, extent=extent)
        im[3] = axs[0][3].imshow(NRMSE_R, cmap='RdYlGn_r', origin='lower', vmin=0, vmax=1, extent=extent)
        im[4] = axs[1][0].imshow(Pearson_S, cmap='RdYlGn', origin='lower', vmin=-1, vmax=1, extent=extent)
        im[5] = axs[1][1].imshow(Pearson_E, cmap='RdYlGn', origin='lower', vmin=-1, vmax=1, extent=extent)
        im[6] = axs[1][2].imshow(Pearson_I, cmap='RdYlGn', origin='lower', vmin=-1, vmax=1, extent=extent)
        im[7] = axs[1][3].imshow(Pearson_R, cmap='RdYlGn', origin='lower', vmin=-1, vmax=1, extent=extent)
        for item in im:
            fig.colorbar(item, fraction=0.046, pad=0.04)
        axs[0][0].title.set_text(self.rmse_label + '[S]')
        axs[0][1].title.set_text(self.rmse_label + '[E]')
        axs[0][2].title.set_text(self.rmse_label + '[I]')
        axs[0][3].title.set_text(self.rmse_label + '[R]')
        axs[1][0].title.set_text(self.pearson_label + '[S]')
        axs[1][1].title.set_text(self.pearson_label + '[E]')
        axs[1][2].title.set_text(self.pearson_label + '[I]')
        axs[1][3].title.set_text(self.pearson_label + '[R]')
        for i in range(0,2):
            for j in range(0,4):
                axs[i][j].set_xlabel(self.tex_alt('$\\' + xparam + '$',xparam))
                axs[i][j].set_ylabel(self.tex_alt('$\\' + yparam + '$',yparam))
        #fig.suptitle(self.model + ', ' + self.tex_alt('$\\' + str(fixedcol) + ' = ' + str(fixedval) + '$',str(fixedcol) + ' = ' + str(fixedval)), fontsize=16)
        plt.savefig(os.path.join(self.outdir,self.default_plot_name(fixedcol,fixedval)))
        plt.cla()
        plt.clf()
        plt.close()

    def plotSEIRS(self, fixedcol1 = 'sigma', fixedval1 = 1.0, fixedcol2 = 'xi', fixedval2 = 1.0):
        fixed = [ fixedcol1 , fixedcol2 ]
        if 'sigma' in fixed and 'xi' in fixed:
            xparam = 'gamma'
            yparam = 'beta'
        elif 'gamma' in fixed and 'xi' in fixed:
            xparam = 'sigma'
            yparam = 'beta'
        elif 'beta' in fixed and 'xi' in fixed:
            xparam = 'gamma'
            yparam = 'sigma'
        elif 'sigma' in fixed and 'gamma' in fixed:
            xparam = 'xi'
            yparam = 'beta'
        elif 'beta' in fixed and 'gamma' in fixed:
            xparam = 'sigma'
            yparam = 'xi'
        elif 'sigma' in fixed and 'beta' in fixed:
            xparam = 'gamma'
            yparam = 'xi'
        else:
            xparam = 'gamma'
            yparam = 'beta'

        logging.info('plotSEIRS(): xparam = ' + str(xparam) + ', yparam = ' + str(yparam))
            
        ycol = self.extract_set(yparam)
        xcol = self.extract_set(xparam)
        zcol1 = self.extract_set(fixedcol1)
        zcol2 = self.extract_set(fixedcol2)
        
        left   = 0.0 #min(gamma) #0.0
        right  = 1.0 #max(gamma) #1.0
        bottom = 0.0 #min(beta) #0.0
        top    = 1.0 #max(beta) #1.0
        extent = [left, right, bottom, top]
        cmap_white = cmap = ListedColormap(["white"], name='WhiteMap')
        top = cmap_white.resampled(128)
        middle = mpl.colormaps['RdYlGn'].resampled(1280)
        bottom = cmap_white.resampled(128)
        newcolors = np.vstack((top(np.linspace(0, 1, 128)),
                       middle(np.linspace(0, 1, 1280)),
                       bottom(np.linspace(0, 1, 128))))
        newcmp = ListedColormap(newcolors, name='OrangeBlue')
        im = [None for x in range(8)]
        
        fig, axs = plt.subplots(2, 4, figsize=(16, 8), layout='constrained')
        NRMSE_S = self.build_matrix(yparam,xparam,'NRMSE_S', filter1col = fixedcol1, filter1val = fixedval1, filter2col = fixedcol2, filter2val = fixedval2)
        NRMSE_E = self.build_matrix(yparam,xparam,'NRMSE_E', filter1col = fixedcol1, filter1val = fixedval1, filter2col = fixedcol2, filter2val = fixedval2)
        NRMSE_I = self.build_matrix(yparam,xparam,'NRMSE_I', filter1col = fixedcol1, filter1val = fixedval1, filter2col = fixedcol2, filter2val = fixedval2)
        NRMSE_R = self.build_matrix(yparam,xparam,'NRMSE_R', filter1col = fixedcol1, filter1val = fixedval1, filter2col = fixedcol2, filter2val = fixedval2)
        Pearson_S = self.build_matrix(yparam,xparam,'Pearson_S', filter1col = fixedcol1, filter1val = fixedval1, filter2col = fixedcol2, filter2val = fixedval2)
        Pearson_E = self.build_matrix(yparam,xparam,'Pearson_E', filter1col = fixedcol1, filter1val = fixedval1, filter2col = fixedcol2, filter2val = fixedval2)
        Pearson_I = self.build_matrix(yparam,xparam,'Pearson_I', filter1col = fixedcol1, filter1val = fixedval1, filter2col = fixedcol2, filter2val = fixedval2)
        Pearson_R = self.build_matrix(yparam,xparam,'Pearson_R', filter1col = fixedcol1, filter1val = fixedval1, filter2col = fixedcol2, filter2val = fixedval2)

        Pearson_S = self.alter_pearson(Pearson_S,NRMSE_S)
        Pearson_I = self.alter_pearson(Pearson_I,NRMSE_I)
        Pearson_R = self.alter_pearson(Pearson_R,NRMSE_R)
        Pearson_E = self.alter_pearson(Pearson_E,NRMSE_E)
        
        im[0] = axs[0][0].imshow(NRMSE_S, cmap='RdYlGn_r', origin='lower', vmin=0, vmax=1, extent=extent)
        im[1] = axs[0][1].imshow(NRMSE_E, cmap='RdYlGn_r', origin='lower', vmin=0, vmax=1, extent=extent)
        im[2] = axs[0][2].imshow(NRMSE_I, cmap='RdYlGn_r', origin='lower', vmin=0, vmax=1, extent=extent)
        im[3] = axs[0][3].imshow(NRMSE_R, cmap='RdYlGn_r', origin='lower', vmin=0, vmax=1, extent=extent)
        im[4] = axs[1][0].imshow(Pearson_S, cmap='RdYlGn', origin='lower', vmin=-1, vmax=1, extent=extent)
        im[5] = axs[1][1].imshow(Pearson_E, cmap='RdYlGn', origin='lower', vmin=-1, vmax=1, extent=extent)
        im[6] = axs[1][2].imshow(Pearson_I, cmap='RdYlGn', origin='lower', vmin=-1, vmax=1, extent=extent)
        im[7] = axs[1][3].imshow(Pearson_R, cmap='RdYlGn', origin='lower', vmin=-1, vmax=1, extent=extent)
        for item in im:
            fig.colorbar(item, fraction=0.046, pad=0.04)
        axs[0][0].title.set_text(self.rmse_label + '[S]')
        axs[0][1].title.set_text(self.rmse_label + '[E]')
        axs[0][2].title.set_text(self.rmse_label + '[I]')
        axs[0][3].title.set_text(self.rmse_label + '[R]')
        axs[1][0].title.set_text(self.pearson_label + '[S]')
        axs[1][1].title.set_text(self.pearson_label + '[E]')
        axs[1][2].title.set_text(self.pearson_label + '[I]')
        axs[1][3].title.set_text(self.pearson_label + '[R]')
        for i in range(0,2):
            for j in range(0,4):
                axs[i][j].set_xlabel(self.tex_alt('$\\' + xparam + '$',xparam))
                axs[i][j].set_ylabel(self.tex_alt('$\\' + yparam + '$',yparam))
        #fig.suptitle(self.model + ', ' + self.tex_alt('$\\' + str(fixedcol1) + ' = ' + str(fixedval1) + '$',str(fixedcol1) + ' = ' + str(fixedval1)) + ', ' + self.tex_alt('$\\' + str(fixedcol2) + ' = ' + str(fixedval2) + '$',str(fixedcol2) + ' = ' + str(fixedval2)), fontsize=16)
        plt.savefig(os.path.join(self.outdir,self.default_plot_name(fixedcol1,fixedval1,fixedcol2,fixedval2)))
        plt.cla()
        plt.clf()
        plt.close()

    def plotSI_Pearson(self):
        fig, axs = plt.subplots(1, 2, figsize=(8, 4), layout='constrained')
        axs[0].plot(self.dat['beta'],self.dat['Pearson_S'])
        axs[1].plot(self.dat['beta'],self.dat['Pearson_I'])
        axs[0].set_ylabel(self.pearson_label + '[S]')
        axs[1].set_ylabel(self.pearson_label + '[I]')
        for j in range(0,2):
            axs[j].set_xlabel(self.tex_alt(r'$\beta$','beta'))
            axs[j].grid()
        fig.suptitle('SI Model', fontsize=16)
        plt.savefig(os.path.join(self.outdir,self.default_plot_name()))
        plt.cla()
        plt.clf()
        plt.close()

    def plotSIS_Pearson(self):
        beta = self.extract_set('beta')
        gamma = self.extract_set('gamma')
        left   = 0.0 #min(gamma) #0.0
        right  = 1.0 #max(gamma) #1.0
        bottom = 0.0 #min(beta) #0.0
        top    = 1.0 #max(beta) #1.0
        extent = [left, right, bottom, top]
        cmap_white = cmap = ListedColormap(["white"], name='WhiteMap')
        top = cmap_white.resampled(128)
        middle = mpl.colormaps['RdYlGn'].resampled(1280)
        bottom = cmap_white.resampled(128)
        newcolors = np.vstack((top(np.linspace(0, 1, 128)),
                       middle(np.linspace(0, 1, 1280)),
                       bottom(np.linspace(0, 1, 128))))
        newcmp = ListedColormap(newcolors, name='OrangeBlue')
        im = [None for x in range(2)]
        fig, axs = plt.subplots(1, 2, figsize=(8, 4), layout='constrained')
        Pearson_S = self.build_matrix('beta','gamma','Pearson_S')
        Pearson_I = self.build_matrix('beta','gamma','Pearson_I')
        
        im[0] = axs[0].imshow(Pearson_S, cmap=newcmp, origin='lower', vmin=-1.2, vmax=1.2, extent=extent)
        im[1] = axs[1].imshow(Pearson_I, cmap=newcmp, origin='lower', vmin=-1.2, vmax=1.2, extent=extent)
        for item in im:
            fig.colorbar(item, fraction=0.046, pad=0.04)
        axs[0].title.set_text(self.pearson_label + '[S]')
        axs[1].title.set_text(self.pearson_label + '[I]')
        for j in range(0,2):
            axs[j].set_xlabel(self.tex_alt(r'$\gamma$','gamma'))
            axs[j].set_ylabel(self.tex_alt(r'$\beta$','beta'))
        fig.suptitle(self.model, fontsize=16)
        plt.savefig(os.path.join(self.outdir,self.default_plot_name()))
        plt.cla()
        plt.clf()
        plt.close()

    def plotSIR_Pearson(self):
        beta = self.extract_set('beta')
        gamma = self.extract_set('gamma')
        left   = 0.0 #min(gamma) #0.0
        right  = 1.0 #max(gamma) #1.0
        bottom = 0.0 #min(beta) #0.0
        top    = 1.0 #max(beta) #1.0
        extent = [left, right, bottom, top]
        cmap_white = cmap = ListedColormap(["white"], name='WhiteMap')
        top = cmap_white.resampled(128)
        middle = mpl.colormaps['RdYlGn'].resampled(1280)
        bottom = cmap_white.resampled(128)
        newcolors = np.vstack((top(np.linspace(0, 1, 128)),
                       middle(np.linspace(0, 1, 1280)),
                       bottom(np.linspace(0, 1, 128))))
        newcmp = ListedColormap(newcolors, name='OrangeBlue')
        im = [None for x in range(3)]
        fig, axs = plt.subplots(1, 3, figsize=(12, 4), layout='constrained')
        Pearson_S = self.build_matrix('beta','gamma','Pearson_S')
        Pearson_I = self.build_matrix('beta','gamma','Pearson_I')
        Pearson_R = self.build_matrix('beta','gamma','Pearson_R')
        
        im[0] = axs[0].imshow(Pearson_S, cmap=newcmp, origin='lower', vmin=-1.2, vmax=1.2, extent=extent)
        im[1] = axs[1].imshow(Pearson_I, cmap=newcmp, origin='lower', vmin=-1.2, vmax=1.2, extent=extent)
        im[2] = axs[2].imshow(Pearson_R, cmap=newcmp, origin='lower', vmin=-1.2, vmax=1.2, extent=extent)
        for item in im:
            fig.colorbar(item, fraction=0.046, pad=0.04)
        axs[0].title.set_text(self.pearson_label + '[S]')
        axs[1].title.set_text(self.pearson_label + '[I]')
        axs[2].title.set_text(self.pearson_label + '[R]')
        for j in range(0,3):
            axs[j].set_xlabel(self.tex_alt(r'$\gamma$','gamma'))
            axs[j].set_ylabel(self.tex_alt(r'$\beta$','beta'))
        fig.suptitle(self.model, fontsize=16)
        plt.savefig(os.path.join(self.outdir,self.default_plot_name()))
        plt.cla()
        plt.clf()
        plt.close()

    def plotSIRS_Pearson(self,fixedcol = 'xi', fixedval = 1.0):
        if fixedcol == 'xi':
            xparam = 'gamma'
            yparam = 'beta'
        elif fixedcol == 'gamma':
            xparam = 'beta'
            yparam = 'xi'
        elif fixedcol == 'beta':
            xparam = 'gamma'
            yparam = 'xi'

        ycol = self.extract_set(yparam)
        xcol = self.extract_set(xparam)
        zcol = self.extract_set(fixedcol)
        
        left   = 0.0 #min(gamma) #0.0
        right  = 1.0 #max(gamma) #1.0
        bottom = 0.0 #min(beta) #0.0
        top    = 1.0 #max(beta) #1.0
        extent = [left, right, bottom, top]
        cmap_white = cmap = ListedColormap(["white"], name='WhiteMap')
        top = cmap_white.resampled(128)
        middle = mpl.colormaps['RdYlGn'].resampled(1280)
        bottom = cmap_white.resampled(128)
        newcolors = np.vstack((top(np.linspace(0, 1, 128)),
                       middle(np.linspace(0, 1, 1280)),
                       bottom(np.linspace(0, 1, 128))))
        newcmp = ListedColormap(newcolors, name='OrangeBlue')
        im = [None for x in range(3)]
        fig, axs = plt.subplots(1, 3, figsize=(12, 4), layout='constrained')
        Pearson_S = self.build_matrix(yparam,xparam,'Pearson_S', filter1col = fixedcol, filter1val = fixedval)
        Pearson_I = self.build_matrix(yparam,xparam,'Pearson_I', filter1col = fixedcol, filter1val = fixedval)
        Pearson_R = self.build_matrix(yparam,xparam,'Pearson_I', filter1col = fixedcol, filter1val = fixedval)
        
        im[0] = axs[0].imshow(Pearson_S, cmap=newcmp, origin='lower', vmin=-1.2, vmax=1.2, extent=extent)
        im[1] = axs[1].imshow(Pearson_I, cmap=newcmp, origin='lower', vmin=-1.2, vmax=1.2, extent=extent)
        im[2] = axs[2].imshow(Pearson_R, cmap=newcmp, origin='lower', vmin=-1.2, vmax=1.2, extent=extent)
        for item in im:
            fig.colorbar(item, fraction=0.046, pad=0.04)
        axs[0].title.set_text(self.pearson_label + '[S]')
        axs[1].title.set_text(self.pearson_label + '[I]')
        axs[2].title.set_text(self.pearson_label + '[R]')
        for j in range(0,3):
            axs[j].set_xlabel(self.tex_alt('$\\' + xparam + '$',xparam))
            axs[j].set_ylabel(self.tex_alt('$\\' + yparam + '$',yparam)) 
        fig.suptitle(self.model + ', ' +  self.tex_alt('$\\' + str(fixedcol) + ' = ' + str(fixedval) + '$',str(fixedcol) + ' = ' + str(fixedval)), fontsize=16)
        plt.savefig(os.path.join(self.outdir,self.default_plot_name(fixedcol,fixedval)))
        plt.cla()
        plt.clf()
        plt.close()

    def plotSEIR_Pearson(self,fixedcol = 'sigma', fixedval = 1.0):
        if fixedcol == 'sigma':
            xparam = 'gamma'
            yparam = 'beta'
        elif fixedcol == 'gamma':
            xparam = 'beta'
            yparam = 'sigma'
        elif fixedcol == 'beta':
            xparam = 'gamma'
            yparam = 'sigma'

        ycol = self.extract_set(yparam)
        xcol = self.extract_set(xparam)
        zcol = self.extract_set(fixedcol)
        
        left   = 0.0 #min(gamma) #0.0
        right  = 1.0 #max(gamma) #1.0
        bottom = 0.0 #min(beta) #0.0
        top    = 1.0 #max(beta) #1.0
        extent = [left, right, bottom, top]
        cmap_white = cmap = ListedColormap(["white"], name='WhiteMap')
        top = cmap_white.resampled(128)
        middle = mpl.colormaps['RdYlGn'].resampled(1280)
        bottom = cmap_white.resampled(128)
        newcolors = np.vstack((top(np.linspace(0, 1, 128)),
                       middle(np.linspace(0, 1, 1280)),
                       bottom(np.linspace(0, 1, 128))))
        newcmp = ListedColormap(newcolors, name='OrangeBlue')
        im = [None for x in range(4)]
        fig, axs = plt.subplots(1, 4, figsize=(16, 4), layout='constrained')
        Pearson_S = self.build_matrix(yparam,xparam,'Pearson_S', filter1col = fixedcol, filter1val = fixedval)
        Pearson_E = self.build_matrix(yparam,xparam,'Pearson_E', filter1col = fixedcol, filter1val = fixedval)
        Pearson_I = self.build_matrix(yparam,xparam,'Pearson_I', filter1col = fixedcol, filter1val = fixedval)
        Pearson_R = self.build_matrix(yparam,xparam,'Pearson_R', filter1col = fixedcol, filter1val = fixedval)
        
        im[0] = axs[0].imshow(Pearson_S, cmap=newcmp, origin='lower', vmin=-1.2, vmax=1.2, extent=extent)
        im[1] = axs[1].imshow(Pearson_E, cmap=newcmp, origin='lower', vmin=-1.2, vmax=1.2, extent=extent)
        im[2] = axs[2].imshow(Pearson_I, cmap=newcmp, origin='lower', vmin=-1.2, vmax=1.2, extent=extent)
        im[3] = axs[3].imshow(Pearson_R, cmap=newcmp, origin='lower', vmin=-1.2, vmax=1.2, extent=extent)
        for item in im:
            fig.colorbar(item, fraction=0.046, pad=0.04)
        axs[0].title.set_text(self.pearson_label + '[S]')
        axs[1].title.set_text(self.pearson_label + '[E]')
        axs[2].title.set_text(self.pearson_label + '[I]')
        axs[3].title.set_text(self.pearson_label + '[R]')
        for j in range(0,4):
            axs[j].set_xlabel(self.tex_alt('$\\' + xparam + '$',xparam))
            axs[j].set_ylabel(self.tex_alt('$\\' + yparam + '$',yparam))
        fig.suptitle(self.model + ', ' + self.tex_alt('$\\' + str(fixedcol) + ' = ' + str(fixedval) + '$',str(fixedcol) + ' = ' + str(fixedval)), fontsize=16)
        plt.savefig(os.path.join(self.outdir,self.default_plot_name(fixedcol,fixedval)))
        plt.cla()
        plt.clf()
        plt.close()

    def plotSEIRS_Pearson(self, fixedcol1 = 'sigma', fixedval1 = 1.0, fixedcol2 = 'xi', fixedval2 = 1.0):
        fixed = [ fixedcol1 , fixedcol2 ]
        if 'sigma' in fixed and 'xi' in fixed:
            xparam = 'gamma'
            yparam = 'beta'
        elif 'gamma' in fixed and 'xi' in fixed:
            xparam = 'sigma'
            yparam = 'beta'
        elif 'beta' in fixed and 'xi' in fixed:
            xparam = 'gamma'
            yparam = 'sigma'
        elif 'sigma' in fixed and 'gamma' in fixed:
            xparam = 'xi'
            yparam = 'beta'
        elif 'beta' in fixed and 'gamma' in fixed:
            xparam = 'sigma'
            yparam = 'xi'
        elif 'sigma' in fixed and 'beta' in fixed:
            xparam = 'gamma'
            yparam = 'xi'
        else:
            xparam = 'gamma'
            yparam = 'beta'

        logging.info('plotSEIRS(): xparam = ' + str(xparam) + ', yparam = ' + str(yparam))
            
        ycol = self.extract_set(yparam)
        xcol = self.extract_set(xparam)
        zcol1 = self.extract_set(fixedcol1)
        zcol2 = self.extract_set(fixedcol2)
        
        left   = 0.0 #min(gamma) #0.0
        right  = 1.0 #max(gamma) #1.0
        bottom = 0.0 #min(beta) #0.0
        top    = 1.0 #max(beta) #1.0
        extent = [left, right, bottom, top]
        cmap_white = cmap = ListedColormap(["white"], name='WhiteMap')
        top = cmap_white.resampled(128)
        middle = mpl.colormaps['RdYlGn'].resampled(1280)
        bottom = cmap_white.resampled(128)
        newcolors = np.vstack((top(np.linspace(0, 1, 128)),
                       middle(np.linspace(0, 1, 1280)),
                       bottom(np.linspace(0, 1, 128))))
        newcmp = ListedColormap(newcolors, name='OrangeBlue')
        im = [None for x in range(4)]
        
        fig, axs = plt.subplots(1, 4, figsize=(16, 4), layout='constrained')
        Pearson_S = self.build_matrix(yparam,xparam,'Pearson_S', filter1col = fixedcol1, filter1val = fixedval1, filter2col = fixedcol2, filter2val = fixedval2)
        Pearson_E = self.build_matrix(yparam,xparam,'Pearson_E', filter1col = fixedcol1, filter1val = fixedval1, filter2col = fixedcol2, filter2val = fixedval2)
        Pearson_I = self.build_matrix(yparam,xparam,'Pearson_I', filter1col = fixedcol1, filter1val = fixedval1, filter2col = fixedcol2, filter2val = fixedval2)
        Pearson_R = self.build_matrix(yparam,xparam,'Pearson_R', filter1col = fixedcol1, filter1val = fixedval1, filter2col = fixedcol2, filter2val = fixedval2)
        
        im[0] = axs[0].imshow(Pearson_S, cmap=newcmp, origin='lower', vmin=-1.2, vmax=1.2, extent=extent)
        im[1] = axs[1].imshow(Pearson_E, cmap=newcmp, origin='lower', vmin=-1.2, vmax=1.2, extent=extent)
        im[2] = axs[2].imshow(Pearson_I, cmap=newcmp, origin='lower', vmin=-1.2, vmax=1.2, extent=extent)
        im[3] = axs[3].imshow(Pearson_R, cmap=newcmp, origin='lower', vmin=-1.2, vmax=1.2, extent=extent)
        for item in im:
            fig.colorbar(item, fraction=0.046, pad=0.04)
        axs[0].title.set_text(self.pearson_label + '[S]')
        axs[1].title.set_text(self.pearson_label + '[E]')
        axs[2].title.set_text(self.pearson_label + '[I]')
        axs[3].title.set_text(self.pearson_label + '[R]')
        for j in range(0,4):
            axs[j].set_xlabel(self.tex_alt('$\\' + xparam + '$',xparam))
            axs[j].set_ylabel(self.tex_alt('$\\' + yparam + '$',yparam))
        fig.suptitle(self.model + ', ' + self.tex_alt('$\\' + str(fixedcol1) + ' = ' + str(fixedval1) + '$',str(fixedcol1) + ' = ' + str(fixedval1)) + ', ' + self.tex_alt('$\\' + str(fixedcol2) + ' = ' + str(fixedval2) + '$',str(fixedcol2) + ' = ' + str(fixedval2)), fontsize=16)
        plt.savefig(os.path.join(self.outdir,self.default_plot_name(fixedcol1,fixedval1,fixedcol2,fixedval2)))
        plt.cla()
        plt.clf()
        plt.close()
