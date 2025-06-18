#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Cristian Berceanu
# Copyright 2023 Cristian Berceanu. All rights reserved.

import sys
import os

from . import model_SI
from . import model_SIS
from . import model_SIR
from . import model_SIRS
from . import model_SEIR
from . import model_SEIRS

def build_model(model_type,beta,gamma,sigma,xi):
    computed = None
    if model_type == 'SI':
        computed = model_SI.SI_Model(beta=beta,mu=0,nu=0,rho=0,tau=0,theta=0)
    elif model_type == 'SIS':
        computed = model_SIS.SIS_Model(beta=beta,gamma=gamma,mu=0,nu=0,rho=0,tau=0,theta=0)
    elif model_type == 'SIR':
        computed = model_SIR.SIR_Model(beta=beta,gamma=gamma,mu=0,nu=0,rho=0,tau=0,theta=0)
    elif model_type == 'SIRS':
        computed = model_SIRS.SIRS_Model(beta=beta,gamma=gamma,xi=xi,mu=0,nu=0,rho=0,tau=0,theta=0)
    elif model_type == 'SEIR':
        computed = model_SEIR.SEIR_Model(beta=beta,gamma=gamma,sigma=sigma,mu=0,nu=0,rho=0,tau=0,theta=0)
    else:
        computed = model_SEIRS.SEIRS_Model(beta=beta,gamma=gamma,sigma=sigma,xi=xi,mu=0,nu=0,rho=0,tau=0,theta=0)
    return computed
    
