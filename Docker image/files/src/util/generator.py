#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Cristian Berceanu
# Copyright 2023 Cristian Berceanu. All rights reserved.

import os
import lxml
import lxml.etree
import lxml.builder 

class XMLGenerator:
        def __init__(self,experiment,repetitions,model,xmltype):
                self.experiment = experiment
                self.repetitions = repetitions
                self.model = model
                self.xmltype = xmltype
                self.params = {}
                self.params["sigma"] = 0.2
                self.params["gamma"] = 0.213
                self.params["max-ticks"] = 200
                self.params["misinfo-lower-right?"] = "false"
                self.params["Model"] = "&quot;" + model + "&quot;"
                self.params["xi"] = 0.1
                self.params["initial_immune"] = 0
                self.params["misinfo-upper-right?"] = "false"
                self.params["beta"] = 0.75
                self.params["misinfo-lower-left?"] = "false"    
                self.params["misinfo-upper-left?"] = "false"
                self.params["stop-after?"] = "true"
                self.params["info-regrowth-rate"] = 0.03
                if xmltype == 'large':
                        self.params["initial_exposed"] = 225
                        self.params["initial_infected"] = 225
                        self.params["initial_susceptible"] = 900
                        self.params["use-logistic-map"] = "false"
                        self.params["starting-energy-infected"] = 50
                        self.params["loss-move-exposed"] = 2
                        self.params["loss-move-infected"] = 2
                        self.params["loss-move-susceptible"] = 2
                        self.params["posting-delay-recovered"] = 5
                        self.params["posting-delay-infected"] = 5
                        self.params["starting-energy-exposed"] = 50
                        self.params["posting-loss-recovered"] = 5
                        self.params["loss-move-recovered"] = 2
                        self.params["posting-delay-exposed"] = 5
                        self.params["energy-gain-susceptible"] = 10
                        self.params["max-spread-in-radius"] = 2
                        self.params["energy-gain-recovered"] = 10
                        self.params["starting-energy-recovered"] = 50
                        self.params["posting-loss-susceptible"] = 5
                        self.params["energy-gain-exposed"] = 10
                        self.params["attachment-group"] = 20
                        self.params["posting-loss-exposed"] = 5
                        self.params["posting-delay-susceptible"] = 5
                        self.params["r"] = 0.36
                        self.params["posting-loss-infected"] = 35
                        self.params["starting-energy-susceptible"] = 50
                        self.params["spread-radius"] = 2
                        self.params["energy-gain-infected"] = 10
                        self.params["stop-after?"] = "true"
                elif xmltype == 'small':
                        self.params["initial_exposed"] = 25
                        self.params["initial_infected"] = 25
                        self.params["initial_susceptible"] = 100
                        self.params["agent-starting-energy"] = 50
                        self.params["agent-loss-move"] = 2

        def setparams(self,beta,gamma,sigma,xi,maxtick):
                self.params["beta"] = beta
                self.params["gamma"] = gamma
                self.params["sigma"] = sigma
                self.params["xi"] = xi
                self.params["max-ticks"] = maxtick

        def setinitial(self,S0_small,E0_small,I0_small,R0_small,S0_large,E0_large,I0_large,R0_large):
                if self.xmltype == 'small':
                        self.params["initial_susceptible"] = S0_small
                        self.params["initial_exposed"] = E0_small
                        self.params["initial_infected"] = I0_small
                        self.params["initial_immune"] = R0_small
                elif self.xmltype == 'large':
                        self.params["initial_susceptible"] = S0_large
                        self.params["initial_exposed"] = E0_large
                        self.params["initial_infected"] = I0_large
                        self.params["initial_immune"] = R0_large

        def generate(self, filename = None, folder = None):
                if folder == None:
                        folder = os.getcwd()
                if filename == None:
                        filename = self.experiment
                E = lxml.builder.ElementMaker()
                ROOT = E.experiments
                DOC = E.experiment
                SETUP = E.setup
                GO = E.go
                METRIC1 = E.metric
                METRIC2 = E.metric
                METRIC3 = E.metric
                METRIC4 = E.metric
                METRIC5 = E.metric
                METRIC6 = E.metric
                the_doc = ROOT(
                        DOC(
                                SETUP('setup'),
                                GO('go'),
                                METRIC1('count turtles'),
                                METRIC2('count susceptible'),
                                METRIC3('count infected'),
                                METRIC4('count exposed'),
                                METRIC5('count immune'),
                                METRIC6('run-seed'),
                                name=self.experiment,
                                repetitions=self.repetitions,
                                runMetricsEveryStep="true",
                                )
                        )
                contentnav = the_doc.find('./experiment')
                for key, value in self.params.items():
                        contentnav.append(lxml.etree.XML("<enumeratedValueSet variable=\"" + str(key) + "\"> <value value=\"" + str(value) + "\" /> </enumeratedValueSet>"))
                tree = lxml.etree.ElementTree(the_doc)
                filepath = os.path.join(folder,str(filename) + '.xml')
                tree.write(filepath, pretty_print=True, xml_declaration=True, encoding="utf-8", doctype="<!DOCTYPE experiments SYSTEM \"behaviorspace.dtd\">")
                return filepath
                """Generates and writes a NetLogo experiment XML file in current directory or a specified directory. If the filename parameter is missing, it is automatically generated."""

if __name__ == "__main__":
        print('NetLogo Experiment XML Generator')
