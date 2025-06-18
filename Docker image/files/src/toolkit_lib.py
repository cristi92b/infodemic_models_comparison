import os
import sys
import logging
import csv
import tqdm
import numpy as np
import re
import configparser
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
import subprocess
import operator
import math
import pandas
import jinja2
import statistics

from model import model_SI
from model import model_SIS
from model import model_SIR
from model import model_SIRS
from model import model_SEIR
from model import model_SEIRS
from model import model_factory
from plot import plot_engine
from util import generator
from util import dataload
from util import comparison
from util import archiver


class NetLogoToolkit:
    
    def __init__(self,paramsfile = 'params.ini',resultdir = 'results',plotdir = 'plots'):
        self.cwd = os.getcwd()
        self.resultdir = os.path.join(self.cwd,resultdir)
        self.plotdir = os.path.join(self.cwd,plotdir)
        self.paramsfile = paramsfile
        self.runparams = {}
        self.runexps = []
        self.runmodels = []
        self.exps = {}
        params = configparser.ConfigParser()
        params.read(paramsfile)
        for section in params.sections():
            logging.info("[" + str(section) + "] Parameter Section")
            section_dict = {}
            for k,v in params.items(section):
                logging.info("Loading parameter " + str(k) + ", value = " + str(v))
                try:
                    if str(k) in [ 'beta' , 'gamma' , 'sigma' , 'xi' ]:
                        numberarr = re.findall(r"[-+]?(?:\d*\.*\d+)", v)
                        assert(len(numberarr) == 3)
                        paramval = (float(numberarr[0]) , float(numberarr[1]) , int(numberarr[2]))
                        section_dict[k] = paramval
                    elif str(k) in [ 'maxtick' , 'nbruns' , 's0_small' , 'e0_small' , 'i0_small' , 'r0_small' , 's0_large' , 'e0_large' , 'i0_large' , 'r0_large' ]:
                        section_dict[k] = int(v)
                    else:
                        section_dict[k] = v
                except Exception as e:
                    logging.warning('Exception occurred while doading parameter: ' + str(e))
            self.runparams[str(section)] = section_dict
        logging.info("Parameters Loaded")
        logging.info(self.runparams)
        try:
            for param_key, param_val in self.runparams['NetLogo'].items():
                if param_key == 'enable_small_simple' and param_val == 'True':
                    self.runexps.append('small_simple')
                elif param_key == 'enable_large_simple' and param_val == 'True':
                    self.runexps.append('large_simple')
                elif param_key == 'enable_large_complex' and param_val == 'True':
                    self.runexps.append('large_complex')
            for param_key, param_val in self.runparams['Models'].items():
                if param_key == 'enable_si' and param_val == 'True':
                    self.runmodels.append('SI')
                elif param_key == 'enable_sis' and param_val == 'True':
                    self.runmodels.append('SIS')
                elif param_key == 'enable_sir' and param_val == 'True':
                    self.runmodels.append('SIR')
                elif param_key == 'enable_sirs' and param_val == 'True':
                    self.runmodels.append('SIRS')
                elif param_key == 'enable_seir' and param_val == 'True':
                    self.runmodels.append('SEIR')
                elif param_key == 'enable_seirs' and param_val == 'True':
                    self.runmodels.append('SEIRS')
                    
            self.beta     = self.runparams['SimulationRanges']['beta']
            self.gamma    = self.runparams['SimulationRanges']['gamma']
            self.sigma    = self.runparams['SimulationRanges']['sigma']
            self.xi       = self.runparams['SimulationRanges']['xi']
        
            self.S0_small = self.runparams['ConstantParams']['s0_small']
            self.E0_small = self.runparams['ConstantParams']['e0_small']
            self.I0_small = self.runparams['ConstantParams']['i0_small']
            self.R0_small = self.runparams['ConstantParams']['r0_small']
            self.S0_large = self.runparams['ConstantParams']['s0_large']
            self.E0_large = self.runparams['ConstantParams']['e0_large']
            self.I0_large = self.runparams['ConstantParams']['i0_large']
            self.R0_large = self.runparams['ConstantParams']['r0_large']
        
            self.maxtick  = self.runparams['ConstantParams']['maxtick']
            self.nbruns   = self.runparams['ConstantParams']['nbruns']

            self.maxthreads      = self.runparams['ExecOptions']['maxthreads']
            self.multithreading  = self.runparams['ExecOptions']['multithreading']
            self.enable_validate = self.runparams['ExecOptions']['enable_validate']

            self.beta_range  = np.around(np.linspace(*self.beta),4)
            self.gamma_range = np.around(np.linspace(*self.gamma),4)
            self.sigma_range = np.around(np.linspace(*self.sigma),4)
            self.xi_range    = np.around(np.linspace(*self.xi),4)
            
        except Exception as e:
            logging.warning('Exception occurred wile processing parameters: ' + str(e))
        logging.info('Experiments: ' + str(self.runexps))
        logging.info('Models: ' + str(self.runmodels))

    def default_filename(self,model,beta,gamma,sigma,xi):
        return str(model) + '_' + str(beta) + '_'  + str(gamma) + '_'  + str(sigma) + '_'  + str(xi)

    def xml_type(self,expname):
        retval = 'small'
        if 'large' in expname:
            retval = 'large'
        return retval

    def nlogo_file(self,expname):
        retval = ''
        if expname == 'small_simple':
            retval = 'small_simple_v1.nlogo'
        elif expname == 'large_simple':
            retval = 'large_simple_v2.nlogo'
        elif expname == 'large_complex':
            retval = 'large_complex_v3.nlogo'
        return retval

    def check_params(self,model,beta,gamma,sigma,xi):
        retval = False
        if model == 'SI' and beta in self.beta_range:
            retval = True
            if not(math.isclose(gamma,0.0) and math.isclose(sigma,0.0) and math.isclose(xi,0.0)):
                logging.warning('check_params(' + str(model) + ',' + str(beta) + ',' + str(gamma) + ',' + str(sigma) + ',' + str(xi) + '): parameters valid but not in the canonical form. Prameters that are not used must be = 0.0 .')
        elif model == 'SIS' and beta in self.beta_range and gamma in self.gamma_range:
            retval = True
            if not(math.isclose(sigma,0.0) and math.isclose(xi,0.0)):
                logging.warning('check_params(' + str(model) + ',' + str(beta) + ',' + str(gamma) + ',' + str(sigma) + ',' + str(xi) + '): parameters valid but not in the canonical form. Prameters that are not used must be = 0.0 .')
        elif model == 'SIR' and beta in self.beta_range and gamma in self.gamma_range:
            retval = True
            if not(math.isclose(sigma,0.0) and math.isclose(xi,0.0)):
                logging.warning('check_params(' + str(model) + ',' + str(beta) + ',' + str(gamma) + ',' + str(sigma) + ',' + str(xi) + '): parameters valid but not in the canonical form. Prameters that are not used must be = 0.0 .')
        elif model == 'SIRS' and beta in self.beta_range and gamma in self.gamma_range and xi in self.xi_range:
            retval = True
            if not(math.isclose(sigma,0.0)):
                logging.warning('check_params(' + str(model) + ',' + str(beta) + ',' + str(gamma) + ',' + str(sigma) + ',' + str(xi) + '): parameters valid but not in the canonical form. Prameters that are not used must be = 0.0 .')
        elif model == 'SEIR' and beta in self.beta_range and gamma in self.gamma_range and sigma in self.sigma_range:
            retval = True
            if not(math.isclose(xi,0.0)):
                logging.warning('check_params(' + str(model) + ',' + str(beta) + ',' + str(gamma) + ',' + str(sigma) + ',' + str(xi) + '): parameters valid but not in the canonical form. Prameters that are not used must be = 0.0 .')
        elif model == 'SEIRS' and beta in self.beta_range and gamma in self.gamma_range and sigma in self.sigma_range and xi in self.xi_range:
            retval = True
        else:
            retval = False
            logging.warning('check_params(' + str(model) + ',' + str(beta) + ',' + str(gamma) + ',' + str(sigma) + ',' + str(xi) + '): Invalid parameters!')
        return retval
            
            

    def experlist_load(self,infile = 'experiments.csv'):
        retlist = {}
        with open(os.path.join(self.cwd,infile)) as csv_file:
            csvreader = csv.reader(csv_file, delimiter=',', quotechar='"')
            for row in csvreader:
                if len(row) >= 7:
                    retlist[ ( row[0] , row[1] , row[2] , row[3] , row[4] , row[5] ) ] = row[6]
        self.exps = retlist
        logging.info('experlist_load(): ' + str(len(retlist)) + ' experiments')
        return retlist

    def experlist(self,outfile = 'experiments.csv'):
        retlist = {}
        beta_range  = np.around(np.linspace(*self.beta),4)
        gamma_range = np.around(np.linspace(*self.gamma),4)
        sigma_range = np.around(np.linspace(*self.sigma),4)
        xi_range    = np.around(np.linspace(*self.xi),4)
        for exp in self.runexps:
            expdir = os.path.join(self.resultdir,exp)
            #if not os.path.exists(expdir):
            #    os.makedirs(expdir)
            for model in self.runmodels:
                modeldir = os.path.join(expdir,model)
                #if not os.path.exists(modeldir):
                #    os.makedirs(modeldir)
                if model == 'SI':
                    for beta in beta_range:
                        filename = self.default_filename(model,beta,'0.0','0.0','0.0')
                        retlist[( exp , model , beta , 0.0 , 0.0 , 0.0 )] = os.path.join(modeldir,filename)
                elif model == 'SIS' or model == 'SIR':
                    for gamma in gamma_range:
                        for beta in beta_range:
                            filename = self.default_filename(model,beta,gamma,'0.0','0.0')
                            retlist[( exp , model , beta , gamma , 0.0 , 0.0 )] = os.path.join(modeldir,filename)
                elif model == 'SIRS':
                    for xi in xi_range:
                        for gamma in gamma_range:
                            for beta in beta_range:
                                filename = self.default_filename(model,beta,gamma,'0.0',xi)
                                retlist[( exp , model , beta , gamma , 0.0 , xi )] = os.path.join(modeldir,filename)
                elif model == 'SEIR':
                    for sigma in sigma_range:
                        for gamma in gamma_range:
                            for beta in beta_range:
                                filename = self.default_filename(model,beta,gamma,sigma,'0.0')
                                retlist[( exp , model , beta , gamma , sigma , 0.0 )] = os.path.join(modeldir,filename)
                elif model == 'SEIRS':
                    for xi in xi_range:
                        for sigma in sigma_range:
                            for gamma in gamma_range:
                                for beta in beta_range:
                                    filename = self.default_filename(model,beta,gamma,sigma,xi)
                                    retlist[( exp , model , beta , gamma , sigma , xi )] = os.path.join(modeldir,filename)
        self.exps = retlist
        logging.info('experlist(): ' + str(len(retlist)) + ' experiments')
        if outfile != None:
            with open(os.path.join(self.cwd,outfile), 'w', newline='') as csv_file:
                writer = csv.writer(csv_file, delimiter=',', quotechar='"')
                for k,v in retlist.items():
                    writer.writerow([ k[0],k[1],k[2],k[3],k[4],k[5],v ])
        return retlist

    def exclude_existing(self,outfile = 'missing.csv'):
        allexps = self.experlist()
        to_remove = set()
        for exp in self.runexps:
            expdir = os.path.join(self.resultdir,exp)
            if not os.path.exists(expdir):
                os.makedirs(expdir)
            for model in self.runmodels:
                modeldir = os.path.join(expdir,model)
                if not os.path.exists(modeldir):
                    os.makedirs(modeldir)
                diritems = os.listdir(modeldir)
                for item in diritems:
                    itempath = os.path.join(modeldir,item)
                    if os.path.isfile(itempath):
                        numberarr = re.findall(r"[-+]?(?:\d*\.*\d+)", item)
                        if len(numberarr) >= 4 and '.csv' in item:
                            beta  = float(numberarr[0])
                            gamma = float(numberarr[1])
                            sigma = float(numberarr[2])
                            xi    = float(numberarr[3])
                            to_remove.add( (exp, model , beta , gamma , sigma , xi ) )
                            logging.debug('Adding ' + str((exp, model , beta , gamma , sigma , xi )) + ' to remove list')
                        else:
                            logging.debug('Invalid file name: ' + str(item))
        logging.info('Excluding ' + str(len(to_remove)) + ' items')
        for k in allexps.copy():
            if k in to_remove:
                logging.debug('Removing ' + str(k))
                del allexps[k]
        logging.info('Total ' + str(len(allexps)) + ' experiments to run')
        return allexps
        

    def run_exp_simple(self,parameters):
        exp   = parameters[0]
        model = parameters[1]
        beta  = parameters[2]
        gamma = parameters[3]
        sigma = parameters[4]
        xi    = parameters[5]
        xmlgen = generator.XMLGenerator(self.default_filename(model,beta,gamma,sigma,xi), str(self.nbruns) , model=model, xmltype=self.xml_type(exp))
        xmlgen.setparams(beta,gamma,sigma,xi,self.maxtick)
        xmlgen.setinitial(self.S0_small,self.E0_small,self.I0_small,self.R0_small,self.S0_large,self.E0_large,self.I0_large,self.R0_large)
        expdir   = os.path.join(self.resultdir,exp)
        modeldir = os.path.join(expdir,model)
        filepath = xmlgen.generate(folder = modeldir)
        filename = os.path.basename(filepath)
        csvname = str(os.path.splitext(filename)[0]) + '.csv'
        command = 'NetLogo_Console --headless --model ' +  str(self.nlogo_file(exp))  + ' --setup-file ' + str(filepath) + ' --spreadsheet ' + str(os.path.join(modeldir,csvname))
        p = subprocess.Popen(command, shell=True)
        p.wait()
        return p.returncode

    def run_all(self,experlist):
        multithreading = True if (self.multithreading == 'True') else False
        maxthreads     = int(multiprocessing.cpu_count()/2)
        if multithreading:
            executor = ThreadPoolExecutor(maxthreads)
            results = list(tqdm.tqdm(executor.map(self.run_exp_simple, experlist), total=len(experlist)))
            executor.shutdown(wait=True)
        else:
            results = []
            for exper in experlist:
                outcome = self.run_exp_simple(exper)
                results.append(outcome)
        return results

    def nb_agents(self,exp):
        retval = 0
        if exp in [ 'small_simple' ]:
            retval = int(self.S0_small) + int(self.E0_small) + int(self.I0_small) + int(self.R0_small)
        elif exp in [ 'large_simple' , 'large_complex' ]:
            retval = int(self.S0_large) + int(self.E0_large) + int(self.I0_large) + int(self.R0_large)
        logging.info('nb_agents(): returning ' + str(retval) + ' for ' + str(exp))
        return retval

    def calculate_result(self,parameters):
        exp   = parameters[0]
        model = parameters[1]
        beta  = parameters[2]
        gamma = parameters[3]
        sigma = parameters[4]
        xi    = parameters[5]
        computed = model_factory.build_model(model,beta,gamma,sigma,xi)
        data = dataload.SEIRS_Data(xlimit = self.maxtick)
        expdir = os.path.join(self.resultdir,exp)
        modeldir = os.path.join(expdir,model)
        filepath = os.path.join(modeldir, self.default_filename(model,beta,gamma,sigma,xi) + '.csv')
        data.load(filepath, nbruns = self.nbruns)
        nbagents = 150
        cmp = comparison.Comparison(data, computed, self.maxtick, self.nb_agents(exp), parameters)
        xml = self.xml_type(exp)
        F0 = 47600
        if xml == 'small':
            S0 = self.S0_small
            E0 = self.E0_small
            I0 = self.I0_small
            R0 = self.R0_small
        else:
            S0 = self.S0_large
            E0 = self.E0_large
            I0 = self.I0_large
            R0 = self.R0_large
        rmse    = [ float("nan") , float("nan") , float("nan") , float("nan") ]
        rsq2    = [ float("nan") , float("nan") , float("nan") , float("nan") ]
        pearson = [ float("nan") , float("nan") , float("nan") , float("nan") ]
        error = False
        try:
            rmse = cmp.compute_nrmse(S0=S0,E0=E0,I0=I0,R0=R0,F0=F0)
        except Exception as e:
            error = True
            logging.warning('Exception occurred while calculating RMSE for ' + str(parameters) + ' : ' + str(e))
        try:
            pearson = cmp.compute_pearson(S0=S0,E0=E0,I0=I0,R0=R0,F0=F0)
        except Exception as e:
            error = True
            logging.warning('Exception occurred while calculating Pearson Coefficient for ' + str(parameters) + ' : ' + str(e))
        try:
            rsq2 = cmp.compute_rsquared(S0=S0,E0=E0,I0=I0,R0=R0,F0=F0)
        except Exception as e:
            error = True
            logging.warning('Exception occurred while calculating R-Squared for ' + str(parameters) + ' : ' + str(e))
        return [ str(exp) , str(model), str(beta), str(gamma), str(sigma), str(xi), str(rmse[0]), str(rmse[1]), str(rmse[2]), str(rmse[3]), str(pearson[0]), str(pearson[1]), str(pearson[2]), str(pearson[3]), str(rsq2[0]), str(rsq2[1]), str(rsq2[2]), str(rsq2[3]), str(error) ]
        
    def process_results(self,writeresults = True, writeinvalid = True, outinvalid = 'rm_invalid.bat'):
        all_failed = []
        invalid_files = []
        for exp in self.runexps:
            expdir = os.path.join(self.resultdir,exp)
            for model in self.runmodels:
                paramlist = set()
                csv_rows = []
                csv_rows.append([ 'Experiment' , 'Model' , 'beta' , 'gamma' , 'sigma' , 'xi' , 'NRMSE_S' , 'NRMSE_E' , 'NRMSE_I' , 'NRMSE_R' , 'Pearson_S' , 'Pearson_E' , 'Pearson_I' , 'Pearson_R',  'RSquared_S' , 'RSquared_E' , 'RSquared_I' , 'RSquared_R' , 'Error' ])
                modeldir = os.path.join(expdir,model)
                if not os.path.exists(modeldir):
                    os.makedirs(modeldir)
                diritems = os.listdir(modeldir)
                for item in diritems:
                    itempath = os.path.join(modeldir,item)
                    if os.path.isfile(itempath):
                        numberarr = re.findall(r"[-+]?(?:\d*\.*\d+)", item)
                        if len(numberarr) >= 4:
                            beta  = float(numberarr[0])
                            gamma = float(numberarr[1])
                            sigma = float(numberarr[2])
                            xi    = float(numberarr[3])
                            is_valid = self.check_params(model,beta,gamma,sigma,xi)
                            if is_valid:
                                paramlist.add(( exp , model , beta , gamma , sigma , xi ))
                            else:
                                invalid_files.append(itempath)
                                logging.warning('process_results(): found invalid parameters tuple: (' + str(exp) + ',' + str(model) + ',' + str(beta) + ',' + str(gamma) + ',' + str(sigma) + ',' + str(xi) +')')
                        else:
                            logging.debug('Skipping ' + item + ' file')
                            invalid_files.append(itempath)
                multithreading = True if (self.multithreading == 'True') else False
                maxthreads     = int(multiprocessing.cpu_count()/2)
                if multithreading:
                    executor = ThreadPoolExecutor(maxthreads)
                    results = list(tqdm.tqdm(executor.map(self.calculate_result, list(paramlist)), total=len(paramlist)))
                    executor.shutdown(wait=True)
                else:
                    results = []
                    for exper in paramlist:
                        outcome = self.calculate_result(exper)
                        results.extend(outcome)
                results.sort(key = operator.itemgetter(2, 3, 4, 5))
                if writeresults:
                    csv_rows.extend(results)
                    outfilepath = os.path.join(expdir,model) + '_results.csv'
                    with open(outfilepath, 'w', newline='') as csv_file:
                        writer = csv.writer(csv_file)
                        logging.info('Writing results to file ' + str(outfilepath))
                        writer.writerows(csv_rows)
                else:
                    logging.info('process_results(): Skipping results writing')
                failed = [(x[0] , x[1] , x[2] , x[3] , x[4] , x[5]) for x in results if x[18] == 'True']
                if(len(failed) > 0):
                    logging.warning('process_results(): found ' + str(len(failed)) + ' failed results for ' + str(exp) + ' ' + str(model))
                all_failed.extend(failed)
        if writeinvalid and len(invalid_files) > 0:
            outinvalidpath = os.path.join(self.cwd,outinvalid)
            with open(outinvalidpath, 'w') as f:
                f.write('@echo on\n')
                rm_commands = [ ('del ' + x + '\n') for x in invalid_files ]
                f.writelines(rm_commands)
        return all_failed

    def plot_dir_mode(self,plot_mode):
        if plot_mode == plot_engine.PlotMode.DEFAULT:
            return self.plotdir
        elif plot_mode == plot_engine.PlotMode.ALTERNATE:
            return self.plotdir
        elif plot_mode == plot_engine.PlotMode.PEARSON:
            return self.plotdir + '_pearson'
        elif plot_mode == plot_engine.PlotMode.RSQUARED:
            return self.plotdir + '_rsq'
        else:
            return self.plotdir
    
    def plot_result(self,parameters, plot_mode = plot_engine.PlotMode.DEFAULT):
        logging.info('Plotting ' + str(parameters))
        exp   = parameters[0]
        model = parameters[1]
        beta_range = parameters[2]
        gamma_range = parameters[3]
        sigma_range = parameters[4]
        xi_range = parameters[5]
        expdir = os.path.join(self.resultdir,exp)
        resultsfile = model + '_results.csv'
        resultspath = os.path.join(expdir,resultsfile)
        plotdir = self.plot_dir_mode(plot_mode)
        outdir = os.path.join(plotdir,exp)
        outfile = model + '.png'
        if os.path.exists(resultspath):
            plot = plot_engine.ResultPlot(exp,model,outdir,resultspath)
            plot.plot_all(plot_mode)
        else:
            logging.warning('Results file does not exists: ' + resultspath)
        return outfile

    def plot_all_heat(self, plot_mode = plot_engine.PlotMode.DEFAULT):
        multithreading = True if (self.multithreading == 'True') else False
        maxthreads     = int(multiprocessing.cpu_count()/2)
        for exp in self.runexps:
            for model in self.runmodels:
                self.plot_result((exp , model, self.beta, self.gamma, self.sigma, self.xi), plot_mode)

    def genlatex(self):
        outdir = os.path.join(self.cwd,'latex_tables')
        for exp in self.runexps:
            expdir = os.path.join(self.resultdir,exp)
            outdir_exp = os.path.join(outdir,exp)
            if not os.path.exists(outdir_exp):
                os.makedirs(outdir_exp)
            for model in self.runmodels:
                resultfilepath = os.path.join(expdir,model) + '_results.csv'
                df = pandas.read_csv(resultfilepath)
                outfilepath = os.path.join(outdir_exp,model) + '.tex'
                df.to_latex(outfilepath, columns = [ 'Model' , 'beta' , 'gamma' , 'sigma' , 'xi' , 'NRMSE_S' , 'NRMSE_E' , 'NRMSE_I' , 'NRMSE_R' , 'Pearson_S' , 'Pearson_E' , 'Pearson_I' , 'Pearson_R' ], float_format="%.2f")

    def writetex(self,filepath,data):
        latex_jinja_env = jinja2.Environment(
            block_start_string = '\BLOCK{',
            block_end_string = '}',
            variable_start_string = '\VAR{',
            variable_end_string = '}',
            comment_start_string = '\#{',
            comment_end_string = '}',
            line_statement_prefix = '%%',
            line_comment_prefix = '%#',
            trim_blocks = True,
            autoescape = False,
            loader = jinja2.FileSystemLoader(os.path.abspath('.'))
        )
        template = latex_jinja_env.get_template('jinja_template3.tex')
        content = template.render(data = data)
        with open(filepath,'w') as file:
            file.write(content)
            
    def genlatex2(self):
        outdir = os.path.join(self.cwd,'latex_tables')
        for exp in self.runexps:
            expdir = os.path.join(self.resultdir,exp)
            outdir_exp = os.path.join(outdir,exp)
            if not os.path.exists(outdir_exp):
                os.makedirs(outdir_exp)
            for model in self.runmodels:
                resultfilepath = os.path.join(expdir,model) + '_results.csv'
                df = pandas.read_csv(resultfilepath)
                outfilepath = os.path.join(outdir_exp,model) + '.tex'
                data = df.loc[:, ~df.columns.isin(['Experiment', 'RSquared_S','RSquared_E','RSquared_I','RSquared_R','Error'])].to_numpy()
                self.writetex(outfilepath,data)
                #df.to_latex(outfilepath, columns = [ 'Model' , 'beta' , 'gamma' , 'sigma' , 'xi' , 'NRMSE_S' , 'NRMSE_E' , 'NRMSE_I' , 'NRMSE_R' , 'Pearson_S' , 'Pearson_E' , 'Pearson_I' , 'Pearson_R' ], float_format="%.2f")

    def pearson_rule(self,pearson_nrmse_tuple):
        pearson_val = pearson_nrmse_tuple[0]
        nrmse_val = pearson_nrmse_tuple[1]
        if not(np.isnan(pearson_val)):
            return pearson_val
        elif np.isnan(pearson_val) and math.isclose(nrmse_val, 0.0):
            return 1.0
        else:
            return 0.0

    def genlatex3(self):
        outdir = os.path.join(self.cwd,'latex_tables')
        for exp in self.runexps:
            expdir = os.path.join(self.resultdir,exp)
            outdir_exp = os.path.join(outdir,exp)
            outfilepath = os.path.join(outdir_exp,exp) + '.tex'
            outarray = []
            if not os.path.exists(outdir_exp):
                os.makedirs(outdir_exp)
            for model in self.runmodels:
                resultfilepath = os.path.join(expdir,model) + '_results.csv'
                df = pandas.read_csv(resultfilepath)
                NRMSE_S = df['NRMSE_S'].to_numpy()
                NRMSE_E = df['NRMSE_E'].to_numpy()
                NRMSE_I = df['NRMSE_I'].to_numpy()
                NRMSE_R = df['NRMSE_R'].to_numpy()
                Pearson_S = df['Pearson_S'].to_numpy()
                Pearson_E = df['Pearson_E'].to_numpy()
                Pearson_I = df['Pearson_I'].to_numpy()
                Pearson_R = df['Pearson_R'].to_numpy()
                #NRMSE_S = [x for x in NRMSE_S if not(np.isnan(x))]
                #NRMSE_E = [x for x in NRMSE_E if not(np.isnan(x))]
                #NRMSE_I = [x for x in NRMSE_I if not(np.isnan(x))]
                #NRMSE_R = [x for x in NRMSE_R if not(np.isnan(x))]
                #Pearson_S = [x for x in Pearson_S if not(np.isnan(x))]
                #Pearson_E = [x for x in Pearson_E if not(np.isnan(x))]
                #Pearson_I = [x for x in Pearson_I if not(np.isnan(x))]
                #Pearson_R = [x for x in Pearson_R if not(np.isnan(x))]
                Pearson_S = [self.pearson_rule(x) for x in np.column_stack((Pearson_S, NRMSE_S))]
                Pearson_E = [self.pearson_rule(x) for x in np.column_stack((Pearson_E, NRMSE_E))]
                Pearson_I = [self.pearson_rule(x) for x in np.column_stack((Pearson_I, NRMSE_I))]
                Pearson_R = [self.pearson_rule(x) for x in np.column_stack((Pearson_R, NRMSE_R))]
                print(len(Pearson_S))
                print(len(Pearson_E))
                print(len(Pearson_I))
                print(len(Pearson_R))
                NRMSE_S_mean = float("nan")
                NRMSE_S_std  = float("nan")
                NRMSE_E_mean = float("nan")
                NRMSE_I_std  = float("nan")
                NRMSE_I_mean = float("nan")
                NRMSE_I_std  = float("nan")
                NRMSE_R_mean = float("nan")
                NRMSE_R_std  = float("nan")
                Pearson_S_mean = float("nan")
                Pearson_S_std  = float("nan")
                Pearson_E_mean = float("nan")
                Pearson_E_std  = float("nan")
                Pearson_I_mean = float("nan")
                Pearson_I_std  = float("nan")
                Pearson_R_mean = float("nan")
                Pearson_R_std  = float("nan")
                try:
                    NRMSE_S_mean = statistics.mean(NRMSE_S)
                    NRMSE_S_std  = statistics.stdev(NRMSE_S)
                except Exception as e:
                    print("Exception: " + str(e))
                    print(NRMSE_S)
                try:
                    NRMSE_E_mean = statistics.mean(NRMSE_E)
                    NRMSE_E_std  = statistics.stdev(NRMSE_E)
                except Exception as e:
                    print("Exception: " + str(e))
                    print(NRMSE_E)
                try:
                    NRMSE_I_mean = statistics.mean(NRMSE_I)
                    NRMSE_I_std  = statistics.stdev(NRMSE_I)
                except Exception as e:
                    print("Exception: " + str(e))
                    print(NRMSE_I)
                try:
                    NRMSE_R_mean = statistics.mean(NRMSE_R)
                    NRMSE_R_std  = statistics.stdev(NRMSE_R)
                except Exception as e:
                    print("Exception: " + str(e))
                    print(NRMSE_R)
                try:
                    Pearson_S_mean = statistics.mean(Pearson_S)
                    Pearson_S_std = statistics.stdev(Pearson_S)
                except Exception as e:
                    print("Exception: " + str(e))
                    print(Pearson_S)
                try:
                    Pearson_E_mean = statistics.mean(Pearson_E)
                    Pearson_E_std = statistics.stdev(Pearson_E)
                except Exception as e:
                    print("Exception: " + str(e))
                    print(Pearson_E)
                try:
                    Pearson_I_mean = statistics.mean(Pearson_I)
                    Pearson_I_std = statistics.stdev(Pearson_I)
                except Exception as e:
                    print("Exception: " + str(e))
                    print(Pearson_I)
                try:
                    Pearson_R_mean = statistics.mean(Pearson_R)
                    Pearson_R_std = statistics.stdev(Pearson_R)
                except Exception as e:
                    print("Exception: " + str(e))
                    print(Pearson_R)
                data = []
                data.append(str(model))
                data.append("%.2f (%.2f)" % (NRMSE_S_mean, NRMSE_S_std))
                if model in [ 'SEIR' , 'SEIRS' ]:
                    data.append("%.2f (%.2f)" % (NRMSE_E_mean, NRMSE_E_std))
                else:
                    data.append("-")
                data.append("%.2f (%.2f)" % (NRMSE_I_mean, NRMSE_I_std))
                if model in [ 'SIR' , 'SIRS' , 'SEIR' , 'SEIRS' ]:
                    data.append("%.2f (%.2f)" % (NRMSE_R_mean, NRMSE_R_std))
                else:
                    data.append("-")
                data.append("%.2f (%.2f)" % (Pearson_S_mean, Pearson_S_std))
                if model in [ 'SEIR' , 'SEIRS' ]:
                    data.append("%.2f (%.2f)" % (Pearson_E_mean, Pearson_E_std))
                else:
                    data.append("-")
                data.append("%.2f (%.2f)" % (Pearson_I_mean, Pearson_I_std))
                if model in [ 'SIR' , 'SIRS' , 'SEIR' , 'SEIRS' ]:
                    data.append("%.2f (%.2f)" % (Pearson_R_mean, Pearson_R_std))
                else:
                    data.append("-")
                outarray.append(data)
            print(outarray)
            self.writetex(outfilepath,outarray)

    def runpdflatex(self):
        latexdir = os.path.join(self.cwd,'latex_tables')
        for exp in self.runexps:
            subdir = os.path.join(latexdir,exp)
            items = os.listdir(subdir)
            for item in items:
                print('checking ' + str(item))
                itempath = os.path.join(subdir,item)
                if os.path.isfile(itempath) and item.lower().endswith('.tex'):
                    os.system('pdflatex -output-directory ' + str(subdir) + ' ' + str(itempath))

def main():
    cwd = os.getcwd()
    x = NetLogoToolkit()
    exps = x.exclude_existing()
    x.run_all(exps)
    failed = x.process_results(False)
    x.run_all(failed)
    x.process_results()
    x.plot_all_heat(plot_engine.PlotMode.ALTERNATE)
    #x.plot_all_heat(plot_engine.PlotMode.PEARSON)
    #x.genlatex3()
    #x.runpdflatex()

if __name__ == '__main__':
    logging.basicConfig(filename='toolkit_lib.log', level=logging.INFO, encoding='utf-8', filemode='w', format='[%(levelname)s] %(message)s')
    main()
        
