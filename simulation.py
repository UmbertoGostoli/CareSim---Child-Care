# -*- coding: utf-8 -*-
"""
Created on Thu Nov 02 12:44:00 2017

@author: ug4d
"""

from society import Person
from society import Population
from space import House
from space import Town
from space import Map
import random
import math
import pylab
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_pdf import PdfPages
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.exceptions import NotFittedError
import pandas as pd
# import seaborn as sns
from time import gmtime, strftime
import os
import Tkinter
import struct
import time
import sys
import pprint
import pickle
import numpy as np
import operator
import networkx as nx
import csv
import itertools
from itertools import izip_longest
from collections import OrderedDict

class Sim:
    """Instantiates a single run of the simulation."""    
    def __init__ (self, params):
       
        self.p = OrderedDict(params)
        self.p['num5YearAgeClasses'] = int(self.p['num5YearAgeClasses'])
        self.p['numCareLevels'] = int(self.p['numCareLevels'])
        
        self.socialClassShares = []
        self.townClassShares = []
        self.careNeedShares = []
        self.householdsList = []
        ## Statistical tallies
        self.periodCount = 0
        self.year = 0
        ###################### Demographic outputs ###################
        self.Outputs = ['year', 'currentPop', 'numReceivers', 'taxPayers', 'numUnskilled', 'numSkilled', 'numLowClass', 'numMidClass', 'numUpClass', 'shareLoneParents', 'shareDistantParents',
                   'shareUnskilled', 'shareSkilled', 'shareLowClass', 'shareMidClass', 'shareUpClass', 'numOccupiedHouses', 'averageHouseholdSize', 
                   'marriageTally', 'divorceTally', 'averageHouseholdSize_1', 'averageHouseholdSize_2', 'averageHouseholdSize_3', 'averageHouseholdSize_4', 
                   'averageHouseholdSize_5', 'totalCareSupply', 'informalCareSupply', 'formalCareSupply', 'totalCareNeed', 'socialCareNeed', 'childCareNeed', 
                   'shareCareGivers', 'shareCareGivers_1', 'shareCareGivers_2', 'shareCareGivers_3', 'shareCareGivers_4', 'shareCareGivers_5', 
                   'shareSocialCareTakers_N1', 'shareSocialCareTakers_N2', 'shareSocialCareTakers_N3', 'shareSocialCareTakers_N4', 
                   'meanInformalSocialCareReceived_N1', 'meanFormalSocialCareReceived_N1', 'meanUnmetSocialCareNeed_N1', 'meanInformalSocialCareReceived_N2', 
                   'meanFormalSocialCareReceived_N2', 'meanUnmetSocialCareNeed_N2', 'meanInformalSocialCareReceived_N3', 'meanFormalSocialCareReceived_N3', 'meanUnmetSocialCareNeed_N3', 
                   'meanInformalSocialCareReceived_N4', 'meanFormalSocialCareReceived_N4', 'meanUnmetSocialCareNeed_N4', 'shareSocialCareDemand', 'shareSocialCare_1',
                   'shareSocialCare_2', 'shareSocialCare_3', 'shareSocialCare_4', 'shareSocialCare_5', 'perCapitaCareReceived', 'perCapitaUnmetCareDemand', 'perCapitaSocialCareReceived',
                   'perCapitaUnmetSocialCareDemand', 'perCapitaChildCareReceived', 'perCapitaUnmetChildCareDemand', 'informalCareReceived', 'formalCareReceived', 'totalCareReceived',
                   'totalUnnmetCareNeed', 'shareInformalCareReceived', 'shareInformalCareReceived_1',
                   'shareInformalCareReceived_2', 'shareInformalCareReceived_3', 'shareInformalCareReceived_4', 'shareInformalCareReceived_5', 'shareInformalSocialCare', 'shareInformalSocialCare_1',
                   'shareInformalSocialCare_2', 'shareInformalSocialCare_3', 'shareInformalSocialCare_4', 'shareInformalSocialCare_5', 'shareInformalChildCare', 'shareInformalChildCare_1',
                   'shareInformalChildCare_2', 'shareInformalChildCare_3', 'shareInformalChildCare_4', 'shareInformalChildCare_5', 'informalSocialCareReceived', 'formalSocialCareReceived',
                   'unmetSocialCareNeed', 'informalChildCareReceived', 'formalChildCareReceived', 'unmetChildCareNeed', 'shareUnmetCareDemand', 'shareUnmetCareDemand_1', 'shareUnmetCareDemand_2',
                   'shareUnmetCareDemand_3', 'shareUnmetCareDemand_4', 'shareUnmetCareDemand_5', 'shareUnmetSocialCareDemand', 'shareUnmetSocialCareDemand_1', 'shareUnmetSocialCareDemand_2',
                   'shareUnmetSocialCareDemand_3', 'shareUnmetSocialCareDemand_4', 'shareUnmetSocialCareDemand_5', 'shareUnmetChildCareDemand', 'shareUnmetChildCareDemand_1',
                   'shareUnmetChildCareDemand_2', 'shareUnmetChildCareDemand_3', 'shareUnmetChildCareDemand_4', 'shareUnmetChildCareDemand_5', 'perCapitaUnmetCareDemand_1', 'perCapitaUnmetCareDemand_2',
                   'perCapitaUnmetCareDemand_3', 'perCapitaUnmetCareDemand_4', 'perCapitaUnmetCareDemand_5', 'averageUnmetCareDemand', 'averageUnmetCareDemand_1', 'averageUnmetCareDemand_2',
                   'averageUnmetCareDemand_3', 'averageUnmetCareDemand_4', 'averageUnmetCareDemand_5', 'informalCareReceived_1', 'informalCareReceived_2', 'informalCareReceived_3',
                   'informalCareReceived_4', 'informalCareReceived_5', 'formalCareReceived_1', 'formalCareReceived_2', 'formalCareReceived_3', 'formalCareReceived_4', 'formalCareReceived_5',
                   'unmetCareNeed_1', 'unmetCareNeed_2', 'unmetCareNeed_3', 'unmetCareNeed_4', 'unmetCareNeed_5',
                   'informalCarePerRecipient', 'informalCarePerRecipient_1', 'informalCarePerRecipient_2', 'informalCarePerRecipient_3', 'informalCarePerRecipient_4', 'informalCarePerRecipient_5',
                   'formalCarePerRecipient', 'formalCarePerRecipient_1', 'formalCarePerRecipient_2', 'formalCarePerRecipient_3', 'formalCarePerRecipient_4', 'formalCarePerRecipient_5', 'carePerRecipient',
                   'carePerRecipient_1', 'carePerRecipient_2', 'carePerRecipient_3', 'carePerRecipient_4', 'carePerRecipient_5', 'unmetCarePerRecipient', 'unmetCarePerRecipient_1', 'unmetCarePerRecipient_2',
                   'unmetCarePerRecipient_3', 'unmetCarePerRecipient_4', 'unmetCarePerRecipient_5',
                   'informalSocialCarePerRecipient', 'informalSocialCarePerRecipient_1', 'informalSocialCarePerRecipient_2', 'informalSocialCarePerRecipient_3', 'informalSocialCarePerRecipient_4',
                   'informalSocialCarePerRecipient_5', 'formalSocialCarePerRecipient', 'formalSocialCarePerRecipient_1', 'formalSocialCarePerRecipient_2', 'formalSocialCarePerRecipient_3',
                   'formalSocialCarePerRecipient_4', 'formalSocialCarePerRecipient_5', 'socialCarePerRecipient', 'socialCarePerRecipient_1', 'socialCarePerRecipient_2', 'socialCarePerRecipient_3',
                   'socialCarePerRecipient_4', 'socialCarePerRecipient_5', 'unmetSocialCarePerRecipient', 'unmetSocialCarePerRecipient_1', 'unmetSocialCarePerRecipient_2', 'unmetSocialCarePerRecipient_3',
                   'unmetSocialCarePerRecipient_4', 'unmetSocialCarePerRecipient_5',
                   'informalChildCarePerRecipient', 'informalChildCarePerRecipient_1', 'informalChildCarePerRecipient_2', 'informalChildCarePerRecipient_3', 'informalChildCarePerRecipient_4',
                   'informalChildCarePerRecipient_5', 'formalChildCarePerRecipient', 'formalChildCarePerRecipient_1', 'formalChildCarePerRecipient_2', 'formalChildCarePerRecipient_3',
                   'formalChildCarePerRecipient_4', 'formalChildCarePerRecipient_5', 'childCarePerRecipient', 'childCarePerRecipient_1', 'childCarePerRecipient_2', 'childCarePerRecipient_3',
                   'childCarePerRecipient_4', 'childCarePerRecipient_5', 'unmetChildCarePerRecipient', 'unmetChildCarePerRecipient_1', 'unmetChildCarePerRecipient_2', 'unmetChildCarePerRecipient_3',
                   'unmetChildCarePerRecipient_4', 'unmetChildCarePerRecipient_5',
                   'informalSocialCareReceived_1', 'informalSocialCareReceived_2', 'informalSocialCareReceived_3', 'informalSocialCareReceived_4',
                   'informalSocialCareReceived_5', 'formalSocialCareReceived_1', 'formalSocialCareReceived_2', 'formalSocialCareReceived_3', 'formalSocialCareReceived_4', 'formalSocialCareReceived_5',
                   'unmetSocialCareNeed_1', 'unmetSocialCareNeed_2', 'unmetSocialCareNeed_3', 'unmetSocialCareNeed_4', 'unmetSocialCareNeed_5', 'informalChildCareReceived_1',
                   'informalChildCareReceived_2', 'informalChildCareReceived_3', 'informalChildCareReceived_4', 'informalChildCareReceived_5', 'formalChildCareReceived_1', 'formalChildCareReceived_2',
                   'formalChildCareReceived_3', 'formalChildCareReceived_4', 'formalChildCareReceived_5', 'unmetChildCareNeed_1', 'unmetChildCareNeed_2', 'unmetChildCareNeed_3', 'unmetChildCareNeed_4',
                   'unmetChildCareNeed_5', 'informalCarePerCarer', 'informalCarePerCarer_1', 'informalCarePerCarer_2', 'informalCarePerCarer_3', 'informalCarePerCarer_4', 'informalCarePerCarer_5', 
                   'formalCarePerCarer', 'formalCarePerCarer_1', 'formalCarePerCarer_2', 'formalCarePerCarer_3', 'formalCarePerCarer_4', 'formalCarePerCarer_5', 'informalSocialCarePerCarer', 
                   'informalSocialCarePerCarer_1', 'informalSocialCarePerCarer_2', 'informalSocialCarePerCarer_3', 'informalSocialCarePerCarer_4', 'informalSocialCarePerCarer_5', 'formalSocialCarePerCarer', 
                   'formalSocialCarePerCarer_1', 'formalSocialCarePerCarer_2', 'formalSocialCarePerCarer_3', 'formalSocialCarePerCarer_4', 'formalSocialCarePerCarer_5',
                   'informalChildCarePerCarer', 'informalChildCarePerCarer_1', 'informalChildCarePerCarer_2', 'informalChildCarePerCarer_3', 'informalChildCarePerCarer_4',
                   'informalChildCarePerCarer_5', 'formalChildCarePerCarer', 'formalChildCarePerCarer_1', 'formalChildCarePerCarer_2', 'formalChildCarePerCarer_3',
                   'formalChildCarePerCarer_4', 'formalChildCarePerCarer_5', 'sumNoK_informalSupplies[0]', 'sumNoK_informalSupplies[1]',
                   'sumNoK_informalSupplies[2]', 'sumNoK_informalSupplies[3]', 'sumNoK_formalSupplies[0]', 'sumNoK_formalSupplies[1]', 'sumNoK_formalSupplies[2]', 'sumNoK_formalSupplies[3]',
                   'shareInformalCareSuppliedByFemales', 'shareInformalCareSuppliedByFemales_1', 'shareInformalCareSuppliedByFemales_2', 'shareInformalCareSuppliedByFemales_3',
                   'shareInformalCareSuppliedByFemales_4', 'shareInformalCareSuppliedByFemales_5', 'informalCareSuppliedByFemales_1', 'informalCareSuppliedByFemales_2',
                   'informalCareSuppliedByFemales_3', 'informalCareSuppliedByFemales_4', 'informalCareSuppliedByFemales_5', 'informalCareSuppliedByMales_1', 'informalCareSuppliedByMales_2',
                   'informalCareSuppliedByMales_3', 'informalCareSuppliedByMales_4', 'informalCareSuppliedByMales_5', 'ratioWage', 'ratioWage_1', 'ratioWage_2', 'ratioWage_3', 'ratioWage_4', 'ratioWage_5',
                   'averageMalesWage', 'averageMalesWage_1', 'averageMalesWage_2', 'averageMalesWage_3', 'averageMalesWage_4', 'averageMalesWage_5', 'averageFemalesWage', 'averageFemalesWage_1',
                   'averageFemalesWage_2', 'averageFemalesWage_3', 'averageFemalesWage_4', 'averageFemalesWage_5', 'ratioIncome', 'ratioIncome_1', 'ratioIncome_2', 'ratioIncome_3', 'ratioIncome_4', 
                   'ratioIncome_5', 'averageMalesIncome', 'averageMalesIncome_1', 'averageMalesIncome_2', 'averageMalesIncome_3', 'averageMalesIncome_4', 'averageMalesIncome_5', 'averageFemalesIncome', 
                   'averageFemalesIncome_1', 'averageFemalesIncome_2', 'averageFemalesIncome_3', 'averageFemalesIncome_4', 'averageFemalesIncome_5', 'taxBurden', 'marriageProp', 'hospitalizationCost', 
                   'perCapitaHospitalizationCost', 'unmetSocialCareNeedGiniCoefficient', 'unmetSocialCareNeedGiniCoefficient_1', 'unmetSocialCareNeedGiniCoefficient_2', 'unmetSocialCareNeedGiniCoefficient_3',
                   'unmetSocialCareNeedGiniCoefficient_4', 'unmetSocialCareNeedGiniCoefficient_5', 'shareUnmetSocialCareNeedGiniCoefficient', 'shareUnmetSocialCareNeedGiniCoefficient_1',
                   'shareUnmetSocialCareNeedGiniCoefficient_2', 'shareUnmetSocialCareNeedGiniCoefficient_3', 'shareUnmetSocialCareNeedGiniCoefficient_4', 'shareUnmetSocialCareNeedGiniCoefficient_5',
                   'publicSupply', 'costDirectFunding','totQALY', 'meanQALY', 'discountedQALY', 'averageDiscountedQALY', 'ratioUnmetNeed_CareSupply', 'ratioUnmetNeed_CareSupply_1', 'ratioUnmetNeed_CareSupply_2',
                   'ratioUnmetNeed_CareSupply_3', 'ratioUnmetNeed_CareSupply_4', 'ratioUnmetNeed_CareSupply_5', 'totalTaxRefund', 'pensionExpenditure', 'careCreditSupply', 'socialCareCredits', 'socialCreditSpent', 
                   'shareCreditsSpent','careCreditCost', 'govBudget', 'perCapitaBudget', 'totalCost', 'totalPolicyCost', 'perCapitaCost', 'perCapitaPolicyCost', 'taxRevenue',
                   'perCapitaTaxRefund', 'perCapitaCostDirectFunding', 'perCapitaCareCreditCost', 'shareCarers', 'shareWomenCarers', 'shareMenCarers', 'policyCostWithHC', 'perCapitaPolicyCostWithHC']
        
#        self.checkValues = ['perCapitaHouseholdIncome', 'socialCareMapValues', 'relativeEducationCost', 'probKeepStudying', 'stageStudent', 'changeJobRate', 'changeJobdIncome',
#                            'relocationCareLoss', 'relocationCost', 'townRelocationAttractio', 'townRelativeAttraction', 'townsJobProb', 'townJobAttraction', 'unemployedIncomeDiscountingFactor',
#                            'relativeTownAttraction', 'houseScore', 'deltaHouseOccupants', 'careTransitionRate_1', 'careTransitionRate_2','careTransitionRate_3', 'careTransitionRate_4',
#                            'careTransitionRate_5', 'potentialHostSupply', 'spousesTownSocialAttraction']
        
        ########################## Mobility outputs ######################
        self.marriageTally = 0
        self.divorceTally = 0
        self.totalRelocations = 0
        self.jobRelocations_1 = 0
        self.jobRelocations_2 = 0
        self.jobRelocations_3 = 0
        self.jobRelocations_4 = 0
        self.jobRelocations_5 = 0
        self.marriageRelocations = 0
        self.sizeRelocations = 0
        self.retiredRelocations = 0
        self.townChanges = 0
        
        ######################## Other outputs #############################

        # Check variables
        # self.deathProb = []
        # self.careLevel = []
        self.perCapitaHouseholdIncome = []
        self.socialCareMapValues = []
        self.relativeEducationCost = []
        self.probKeepStudying = []
        self.stageStudent = []
        self.changeJobRate = []
        self.changeJobdIncome = []
        self.relocationCareLoss = []
        self.relocationCost = []
        self.townRelocationAttraction = []
        self.townRelativeAttraction = []
        self.townsJobProb = []
        self.townJobAttraction = []
        self.unemployedIncomeDiscountingFactor = []
        self.relativeTownAttraction = []
        self.houseScore = []
        self.deltaHouseOccupants = []
        self.careTransitionRate = []
        self.potentialHostSupply = []
        self.spousesTownSocialAttraction = []
        self.volunteersTotalSupply = []
        self.numberSuppliers = []
        # Counters and storage
        
        self.check = False
        self.exitWork = 0
        self.enterWork = 0
        
        self.hospitalizationCost = 0
        
        # Budget variables
        self.sharePublicCare = 0
        self.totalTaxRefund = 0
        self.taxRevenue = 0
        self.publicSupply = 0
        self.pensionExpenditure = 0
        self.careCreditSupply = 0
        self.initialCareCredits = 0
        self.socialCareCredits = 0
        self.socialCreditSpent = 0
        
        self.year = self.p['startYear']
        self.pyramid = PopPyramid(self.p['num5YearAgeClasses'],
                                  self.p['numCareLevels'])
        self.textUpdateList = []
        
        self.inputsMortality = []
        self.outputMortality = []
        self.regressionModels_M = []
        
        self.inputsFertility = []
        self.outputFertility = []
        self.regressionModels_F = []
        
        self.unemploymentRateClasses = []
        self.meanUnemploymentRates = []

#        if self.p['interactiveGraphics']:
#            self.window = Tkinter.Tk()
#            self.canvas = Tkinter.Canvas(self.window,
#                                         width=self.p['screenWidth'],
#                                         height=self.p['screenHeight'],
#                                         background=self.p['bgColour'])
        
    def interactiveGraphics(self):
        if self.p['interactiveGraphics']:
            print "Entering main loop to hold graphics up there."
            self.window.mainloop()
            
    def saveChecks(self, folder):     
        
        values = izip_longest(self.perCapitaHouseholdIncome, self.socialCareMapValues, 
                         self.relativeEducationCost, self.probKeepStudying, self.stageStudent, self.changeJobRate, 
                         self.changeJobdIncome, self.relocationCareLoss, self.relocationCost, self.townRelocationAttraction, 
                         self.townRelativeAttraction, self.townsJobProb, self.townJobAttraction, 
                         self.unemployedIncomeDiscountingFactor, self.relativeTownAttraction, self.houseScore, 
                         self.deltaHouseOccupants, self.careTransitionRate[0], self.careTransitionRate[1], 
                         self.careTransitionRate[2], self.careTransitionRate[3], self.careTransitionRate[4], 
                         self.potentialHostSupply, self.spousesTownSocialAttraction, self.volunteersTotalSupply, self.numberSuppliers, 
                         fillvalue='')
            
        headers = ['perCapitaHouseholdIncome', 'socialCareMapValues', 
                     'relativeEducationCost', 'probKeepStudying', 'stageStudent', 'changeJobRate',
                     'changeJobdIncome', 'relocationCareLoss', 'relocationCost', 'townRelocationAttraction',
                     'townRelativeAttraction', 'townsJobProb', 'townJobAttraction',
                     'unemployedIncomeDiscountingFactor', 'relativeTownAttraction', 'houseScore',
                     'deltaHouseOccupants', 'careTransitionRate_I', 'careTransitionRate_II', 'careTransitionRate_III',
                     'careTransitionRate_IV', 'careTransitionRate_V', 'potentialHostSupply', 'spousesTownSocialAttraction',
                     'volunteersTotalSupply', 'numberSuppliers']
            
#        filename = folder + '/Check_Value.csv'
#        np.savetxt(filename, values, delimiter=',', fmt='%f', header=names, comments="")
        
        with open(folder + "check_Values.csv", "wb") as f:
            csv.writer(f).writerow([g for g in headers])
            csv.writer(f).writerows(values)  
        
    def run(self, policyParams):
        
        print 'Implement policies from year: ' + str(self.p['implementPoliciesFromYear'])
                        
        # Set the random seeds
        random.seed(int(self.p['favouriteSeed']))
        np.random.seed(int(self.p['favouriteSeed']))
        self.randomSeed = int(self.p['favouriteSeed'])
        
        if self.p['numRepeats'] > 1:
            rdTime = (int)(time.time())
            self.randomSeed = rdTime
            self.p['favouriteSeed'] = self.randomSeed
            random.seed(rdTime)
            np.random.seed(rdTime)
        
        # Simulation indexes
        
        initialParamsIndex = str(int(self.p['paramIndex']))
        runsIndex = str(int(self.p['runNumber']))
        policyParamsIndex = str(policyParams['policyIndex'])
        
        self.folder = 'Results/Scenario_' + initialParamsIndex + '/Policy_' + policyParamsIndex + '/Run_' + runsIndex
        
        del self.p['paramIndex']
        del self.p['runNumber']
        
        print 'Scenario ' + initialParamsIndex + ' - Policy ' + policyParamsIndex + ' - Run ' + runsIndex
        
        # Save initial parameter
        
        
        scenarioFolder = 'Results/Scenario_' + initialParamsIndex
        paramFolder = scenarioFolder + '/Parameters'
        if not os.path.exists(paramFolder):
            os.makedirs(paramFolder)
        filename = paramFolder + '/initialParameters.csv'
        # Made a copy of dictionary
        c = self.p.copy()
        for key, value in c.iteritems():
            if not isinstance(value, list):
                c[key] = [value]
        with open(filename,  "wb") as f:
            csv.writer(f).writerow(c.keys())
            csv.writer(f).writerows(itertools.izip_longest(*c.values()))
        
        policyFolder = scenarioFolder + '/Policy_' + policyParamsIndex
        paramFolder = policyFolder + '/Parameters'
        if not os.path.exists(paramFolder):
            os.makedirs(paramFolder)
        filename = paramFolder + '/policyParameters.csv'
        c = policyParams.copy()
        for key, value in c.iteritems():
            if not isinstance(value, list):
                c[key] = [value]
        with open(filename,  "wb") as f:
            csv.writer(f).writerow(c.keys())
            csv.writer(f).writerows(itertools.izip_longest(*c.values()))
        
        # Start simulation: initialize...
        self.initializePop()
        #....and start the year loop.
        self.p['startYear'] = int(self.p['startYear'])
        self.p['endYear'] = int(self.p['endYear'])
        for year in range(self.p['startYear'], self.p['endYear']+1):
            
            print(" ")
            print(year)
            
            # At the year of policy implementation.....
            if year == int(self.p['implementPoliciesFromYear']):
                # ...change the policy parameters and....
                for key, value in policyParams.iteritems():
                    if key not in self.p:
                        continue
                    self.p[key] = policyParams[key]
                
            self.doOneYear(year) 
        
        if self.p['doGraphs'] == True:
            self.doGraphs_fromFile(folder)
        
        if self.p['saveChecks']:
            checkFolder = self.folder + '/Dataset/'
            self.saveChecks(checkFolder)

        # self.interactiveGraphics()
            
        
    def initializePop(self):
        
#        if self.p['interactiveGraphics'] == True:
#                self.initializeCanvas()
        
        if self.p['loadFromFile'] == False:
            self.map = Map(self.p['mapGridXDimension'], 
                           self.p['mapGridYDimension'],
                           self.p['townGridDimension'],
                           self.p['cdfHouseClasses'],
                           self.p['ukMap'],
                           self.p['ukClassBias'],
                           self.p['mapDensityModifier'],
                           self.randomSeed)
        else:
            self.map = pickle.load(open("initMap.txt", "rb"))
            
        if self.p['loadFromFile'] == False:
            
            self.socialClassShares = [0.0, 0.0, 0.0, 0.0, 0.0]
            
            while (self.socialClassShares[0] < 0.15 or self.socialClassShares[0] > 0.25 ) or (self.socialClassShares[1] < 0.2 or self.socialClassShares[1] > 0.3 ) or (self.socialClassShares[2] < 0.25 or self.socialClassShares[2] > 0.35 ) or self.socialClassShares[0] > self.socialClassShares[1] or self.socialClassShares[1] > self.socialClassShares[2] or (self.socialClassShares[3] < 0.15 or self.socialClassShares[3] > 0.25 ) or self.socialClassShares[3] > self.socialClassShares[1] or (self.socialClassShares[4] < 0.04 or self.socialClassShares[4] > 0.06 ):
                
                self.pop = Population(self.p['initialPop'], self.p['startYear'],
                                      self.p['minStartAge'], self.p['maxStartAge'],
                                      self.p['numberClasses'],
                                      self.p['initialClassShares'],
                                      self.p['workingAge'],
                                      self.p['incomeInitialLevels'],
                                      self.p['incomeFinalLevels'],
                                      self.p['incomeGrowthRate'],
                                      self.p['workDiscountingTime'],
                                      self.randomSeed)
                
                self.computeClassShares()
            
            men = [x for x in self.pop.allPeople if x.sex == 'male']
            remainingHouses = []
            remainingHouses.extend(self.map.allHouses)
            for man in men:
                # G = nx.Graph()
                house = random.choice(remainingHouses)
                man.house = house
                # man.sec = man.house.size
                # Assumes house classes = SEC classes!
                self.map.occupiedHouses.append(man.house)
                remainingHouses.remove(man.house)
                woman = man.partner
                man.independentStatus = True
                woman.independentStatus = True
                woman.house = man.house
                man.house.occupants.append(man)
                man.house.occupants.append(woman)
                man.house.initialOccupants = 2
                
            
                
        else:
            self.pop = pickle.load(open("initPop.txt", "rb"))

        self.displayHouse = self.pop.allPeople[0].house
        self.nextDisplayHouse = None

        self.fert_data = np.genfromtxt('babyrate.txt.csv',
                                       skip_header=0, delimiter=',')
        self.death_female = np.genfromtxt('deathrate.fem.csv',
                                          skip_header=0, delimiter=',')
        self.death_male = np.genfromtxt('deathrate.male.csv',
                                        skip_header=0, delimiter=',')
        
        # Initialize mortality rates' dataset
        self.p['numberClasses'] = int(self.p['numberClasses'])
        self.p['numCareLevels'] = int(self.p['numCareLevels'])
        for k in range(2):
            self.inputsMortality.append([])
            self.outputMortality.append([])
            self.regressionModels_M.append([])
        for k in range(2):    
            for i in range(self.p['numberClasses']):
                self.inputsMortality[k].append([])
                self.outputMortality[k].append([])
                self.regressionModels_M[k].append([])
        for k in range(2):
            for i in range(5):
                for j in range(self.p['numCareLevels']):
                    self.inputsMortality[k][i].append([])
                    self.outputMortality[k][i].append([])
                    self.regressionModels_M[k][i].append(RandomForestRegressor(n_estimators=500, random_state=0)) # LinearRegression())
        
        for i in range(self.p['numberClasses']):
                self.inputsFertility.append([])
                self.outputFertility.append([])
                self.regressionModels_F.append(RandomForestRegressor(n_estimators=500, random_state=0)) # LinearRegression())           
        
        for i in range(self.p['numberClasses']):
            self.unemploymentRateClasses.append([])
            self.meanUnemploymentRates.append([])
            for j in range(6):
                self.unemploymentRateClasses[i].append([])
                self.meanUnemploymentRates[i].append([])
        
        for i in range (self.p['numberClasses']):
            self.careTransitionRate.append([])
        
        visitedHouses = []
        maxSize = 0
        index = -1
        for person in self.pop.livingPeople:
            if person.house not in visitedHouses:
                visitedHouses.append(person.house)
                if len(person.house.occupants) > maxSize:
                    maxSize = len(person.house.occupants)
                    index = person.house.id
        
    def updatePolicyParameters(self, policyParameters):
        # self.p['socialCareCreditShare'] = policyParameters[0]
        self.p['taxBreakRate'] = policyParameters[0]
        # self.p['ageOfRetirement'] = policyParameters[2] 
        self.p['socialSupportLevel'] = policyParameters[1] 
                    
    def doOneYear(self, year):
        
        self.year = year
        
        """Run one year of simulated time."""
        executionTimes = []
        
        print('Population: ' + str(len(self.pop.livingPeople)))
        
        start = time.time()
        self.computeClassShares()
        end = time.time()
        # print 'Execution time of computeClassTime: ' + str(end-start)
        executionTimes.append(end-start)
        
        start = time.time()
        self.doRegressions()
        end = time.time()
        # print 'Execution time of doRegressions: ' + str(end-start)
        executionTimes.append(end-start)
        
#        start = time.time()
#        self.householdList(0) 
#        self.checkCouples(0)
#        print 'Execution time of double check 0: ' + str(end-start)
#        executionTimes.append(end-start)
#        
        # Marriages (+ join couples)
        start = time.time()
        self.doMarriages()
        end = time.time()
        # print 'Execution time of doMarriages: ' + str(end-start)
        executionTimes.append(end-start)
        
#        start = time.time()
#        self.householdList(1)
#        self.checkCouples(1)
#        end = time.time()
#        print 'Execution time of double check 1: ' + str(end-start)
#        executionTimes.append(end-start)
        
        # Births 
        start = time.time()
        self.doBirths()
        end = time.time()
        # print 'Execution time of doBirths: ' + str(end-start)
        executionTimes.append(end-start)
        
        # Allocate Care
#        start = time.time()
#        self.careNeeds()
#        end = time.time()
        # print 'Execution time of careNeeds: ' + str(end-start)
        executionTimes.append(end-start)
        
        start = time.time()
        self.careCreditsAllocation()
        end = time.time()
        # print 'Execution time of careCreditsAllocation: ' + str(end-start)
        
#        start = time.time()
#        self.householdList(1)
#        end = time.time()
#        print 'Execution time of household list check 1: ' + str(end-start)
        
#        start = time.time()
#        self.careSupplies()
#        end = time.time()
        # print 'Execution time of careSupplies: ' + str(end-start)
        executionTimes.append(end-start)
        
        start = time.time()
        self.allocateCare()
        end = time.time()
        # print 'Execution time of allocateCare: ' + str(end-start)
        executionTimes.append(end-start)
        
        start = time.time()
        self.careBankingAllocation()
        end = time.time()
        # print 'Execution time of careBankingAllocation: ' + str(end-start)
        
        # Health Care cost
        start = time.time()
        self.healthServiceCost()
        end = time.time()
        # print 'Execution time of healthServiceCost: ' + str(end-start)
        executionTimes.append(end-start)
        
        # Update net Income 
        start = time.time()
        self.computeNetIncome()
        end = time.time()
        # print 'Execution time of computeNetIncome: ' + str(end-start)
        executionTimes.append(end-start)
        
        # Stats:
        start = time.time()
        self.saveStats()
        end = time.time()
        # print 'Execution time of saveStats: ' + str(end-start)
        executionTimes.append(end-start)
        
        start = time.time()
        self.ageTransitions()
        end = time.time()
        # print 'Execution time of ageTransitions: ' + str(end-start)
        executionTimes.append(end-start)
        
#        start = time.time()
#        self.householdList(2)
#        self.checkCouples(2)
#        end = time.time()
#        print 'Execution time of double check 2: ' + str(end-start)
        
        start = time.time()
        self.socialTransition()
        end = time.time()
        # print 'Execution time of socialTransition: ' + str(end-start)
        executionTimes.append(end-start)
        
#        start = time.time()
#        self.householdList(3)
#        self.checkCouples(3)
#        end = time.time()
#        print 'Execution time of double check 3: ' + str(end-start)
        
        # - care
        start = time.time()
        self.careTransitions()
        end = time.time()
        # print 'Execution time of careTransitions: ' + str(end-start)
        executionTimes.append(end-start)
        
#        start = time.time()
#        self.householdList(5)
#        end = time.time()
#        print 'Execution time of household list check 2: ' + str(end-start)
        
        # Divorce
        start = time.time()
        self.doDivorces()
        end = time.time()
        # print 'Execution time of doDivorces: ' + str(end-start)
        executionTimes.append(end-start)
        
#        start = time.time()
#        self.householdList(6)
#        self.checkCouples(6)
#        end = time.time()
#        print 'Execution time of double check 4: ' + str(end-start)
        
        # Deaths
        start = time.time()
        self.doDeaths()
        end = time.time()
        # print 'Execution time of doDeaths: ' + str(end-start)
        executionTimes.append(end-start)
        
        # self.householdList(7)
        
        # Check orphans, lone depending people, people without income
        
        # Forced relocations: orphans and lone people with high social care needs
        start = time.time()
        self.relocateOrphans()
        end = time.time()
        # print 'Execution time of relocateOrphans: ' + str(end-start)
        executionTimes.append(end-start)

#        start = time.time()
        # self.householdList(8)
#        end = time.time()
#        print 'Execution time of household list check 3: ' + str(end-start)
        
        # Voluntary Relocations
        start = time.time()
        self.jobRelocation() 
        end = time.time()
        # print 'Execution time of jobRelocation: ' + str(end-start)
        executionTimes.append(end-start)
        
        
#        start = time.time()
        # self.householdList(9)
#        end = time.time()
#        print 'Execution time of household list check 4: ' + str(end-start)
        
        start = time.time()
        self.relocatePensioners()
        end = time.time()
        # print 'Execution time of relocatingPensioners: ' + str(end-start)
        executionTimes.append(end-start)
        
#        start = time.time()
#        self.householdList(11)
#        self.checkCouples(2)
#        end = time.time()
#        print 'Execution time of double check 5: ' + str(end-start)
        
        start = time.time()
        self.updateRelocationVar()
        end = time.time()
        # print 'Execution time of updateRelocationVar: ' + str(end-start)
        
        start = time.time()
        self.updateWage()
        end = time.time()
        # print 'Execution time of updateWage: ' + str(end-start)
        
        totTime = sum(executionTimes)
        shareExecutionTimes = [x/totTime for x in executionTimes]
        # print(shareExecutionTimes)

        # self.householdSize()
        
#        self.pyramid.update(self.year, self.p['num5YearAgeClasses'],
#                            self.p['numCareLevels'],
#                            self.p['pixelsInPopPyramid'],
#                            self.pop.livingPeople)
        
        
#        if (self.p['interactiveGraphics']):
#            self.updateCanvas()
    
    def householdList(self, n):
        
        self.householdsList[:] = []
        visited = []
        for person in self.pop.livingPeople:
            if person in visited:
                continue
            household = list(person.house.occupants)
            
            householdIncome = sum([x.income for x in household])
            indipendentMembers = len([x for x in household if x.independentStatus == True])
            
            ids = [x.id for x in household]
            idNumbers = []
            for i in ids:
                if i in idNumbers:
                    print 'Error: id already in household'
                else:
                    idNumbers.append(i)
            
            
            if householdIncome == 0:
                print 'Error: no earning members: step ' + str(n)
                for member in household:
                    print member.id
                    print member.age
                    print member.status
                    print member.sex
                    print member.income
                    print member.netIncome
                    print member.offWorkCare
                    print member.house
                    if member.partner != None:
                        print member.partner.id
                    else: 
                        print 'No partner'
                    if member.father != None:
                        print member.father.dead
                        print member.mother.dead
                        if member.mother.partner != None:
                            print member.mother.partner.id
                            print member.mother.partner.house
                        else:
                            print 'Mother has no partner'
                    sys.exit()
                        
            if indipendentMembers == 0:
                print 'Error: no independent members: step ' + str(n)
                for member in household:
                    print member.id
                    print member.age
                    print member.status
                    print member.sex
                    print member.independentStatus
                    if member.partner != None:
                        print member.partner.id
                    else: 
                        print 'No partner'
                    sys.exit()
                    
            if len(ids) != len(set(ids)):
                print 'Error: duplicate in household: step ' + str(n)
                for member in household:
                    print member.id
                    print member.age
                    print member.status
                    print member.sex
                    if member.partner != None:
                        print member.partner.id
                    else: 
                        print 'No partner'
                    sys.exit()
            
            visited.extend(household)
            for member in household:
                member.household = household 

            if len(household) > 0:
                self.householdsList.append(household)
        
    def computeClassShares(self):
        
        self.socialClassShares[:] = []
        self.careNeedShares[:] = []
        
        classNum = []
        for c in range(int(self.p['numberClasses'])):
            classPop = [x for x in self.pop.livingPeople if x.classRank == c]
            classNum.append(float(len(classPop)))
            needNum = []
            for b in range(int(self.p['numCareLevels'])):
                needPop = [x for x in classPop if x.careNeedLevel == b]
                needNum.append(float(len(needPop)))
            if sum(needNum) > 0:
                self.careNeedShares.append([x/sum(needNum) for x in needNum])
            else:
                self.careNeedShares.append([0.0, 0.0, 0.0, 0.0, 0.0])
        self.socialClassShares = [x/sum(classNum) for x in classNum]
    
    def checkCouples(self, n):
        for person in self.pop.livingPeople:
            if person.status == 'employed' and person.income == 0.0:
                print 'Error: employed with no income! in step' + str(n)
                sys.exit()
            if person.partner != None and person.house != person.partner.house:
                print 'Error: couple not joined after step: ' + str(n)
                print(person.independentStatus)
                print(person.id)
                print(person.sex)
                print(person.status)
                print(person.partner.independentStatus)
                print(person.partner.id)
                print(person.partner.sex)
                print(person.partner.status)
                sys.exit()
    
    def checkPartners(self, n):
        check = False
        for house in self.map.occupiedHouses:
            if len([x for x in house.occupants if x.independentStatus == True]) == 0:
                if n != 1 and n != 5:
                    print('Error: house with no independent people after step ' + str(n))
                    sys.exit()
        for person in self.pop.livingPeople:
            if person.partner != None and person.independentStatus + person.partner.independentStatus < 2 and len([x for x in person.house.occupants if x.independentStatus == True]) == 0:
                if n != 1 and n != 5:
                    print('Error: not independent person in married couple after step ' + str(n))
                    print('Error: couple not joined after step ' + str(n))
                    print(person.id)
                    print(person.sex)
                    print(person.status)
                    print(person.classRank)
                    print(person.independentStatus)
                    print(person.age)
                    print(person.ageStartWorking)
                    print(person.justMarried)
                    print(person.yearMarried)
                    print(person.yearsSeparated)
                    print(person.numberPartner)
                    print('')
                    print(person.partner.id)
                    print(person.partner.sex)
                    print(person.partner.status)
                    print(person.partner.classRank)
                    print(person.partner.independentStatus)
                    print(person.partner.age)
                    print(person.partner.ageStartWorking)
                    print(person.partner.justMarried)
                    print(person.partner.yearMarried)
                    print(person.partner.yearsSeparated)
                    print(person.partner.numberPartner)
                    sys.exit()
            if person.partner != None and person.house != person.partner.house:
                check = True
                if n != 1:
                    print('Error: couple not joined after step ' + str(n))
                    print(person.id)
                    print(person.sex)
                    print(person.status)
                    print(person.classRank)
                    print(person.independentStatus)
                    print(person.age)
                    print(person.ageStartWorking)
                    print(person.justMarried)
                    print(person.yearMarried)
                    print(person.yearsSeparated)
                    print(person.numberPartner)
                    print('')
                    print(person.partner.id)
                    print(person.partner.sex)
                    print(person.partner.status)
                    print(person.partner.classRank)
                    print(person.partner.independentStatus)
                    print(person.partner.age)
                    print(person.partner.ageStartWorking)
                    print(person.partner.justMarried)
                    print(person.partner.yearMarried)
                    print(person.partner.yearsSeparated)
                    print(person.partner.numberPartner)

                
        return check
    
    def doMarriages(self):
       
        eligibleMen = []
        eligibleWomen = []

        for i in self.pop.livingPeople:
            if i.partner == None:
                # Men need to be employed to marry
                if i.sex == 'male' and i.status == 'employed':
                    eligibleMen.append(i)
                    
        ######     Otional: select a subset of eligible men based on age    ##########################################
        potentialGrooms = []
        for m in eligibleMen:
            incomeFactor = 1.0 # (math.exp(self.p['incomeMarriageParam']*m.income)-1)/math.exp(self.p['incomeMarriageParam']*m.income)
            decade = int(m.age/10)
            if decade > 13:
                decade = 13
            manMarriageProb = self.p['basicMaleMarriageProb']*self.p['maleMarriageModifierByDecade'][decade]*incomeFactor 
            if random.random() < manMarriageProb:
                potentialGrooms.append(m)
        ###########################################################################################################
        
        for man in potentialGrooms: # for man in eligibleMen: # 
            # maxEncounters = self.datingActivity(man)
            eligibleWomen = [x for x in self.pop.livingPeople if x.sex == 'female' and x.age >= self.p['minPregnancyAge'] and x.house != man.house and x.partner == None]
            
            potentialBrides = []
            for woman in eligibleWomen:
                if man.mother != None and woman.mother != None:
                    if man.mother != woman and woman.father != man and man.mother != woman.mother and man not in woman.children and woman not in man.children:
                        potentialBrides.append(woman)
                else:
                    if man not in woman.children and woman not in man.children:
                        potentialBrides.append(woman)
                        
            # if maxEncounters < len(potentialBrides):
               #  numberEncounters = maxEncounters
            # else:
               #  numberEncounters = len(potentialBrides)
            if len(potentialBrides) > 0:
                manTown = man.house.town
                bridesWeights = []
                for woman in potentialBrides:
                    studentFactor = 1.0
                    if woman.status == 'student' or woman.status == 'outOfTownStudent':
                        studentFactor = self.p['studentFactorParam']
                    womanTown = woman.house.town
                    geoDistance = self.manhattanDistance(manTown, womanTown)/float(self.p['mapGridXDimension'] + self.p['mapGridYDimension'])
                    geoFactor = 1/math.exp(self.p['betaGeoExp']*geoDistance)
                    statusDistance = float(abs(man.classRank-woman.classRank))/float((self.p['numberClasses']-1))
                    if man.classRank < woman.classRank:
                        betaExponent = self.p['betaSocExp']
                    else:
                        betaExponent = self.p['betaSocExp']*self.p['rankGenderBias']
                    socFactor = 1/math.exp(betaExponent*statusDistance)
                    ageFactor = self.p['deltaAgeProb'][self.deltaAge(man.age-woman.age)]
                    marriageProb = geoFactor*socFactor*ageFactor*studentFactor
                    bridesWeights.append(marriageProb)
                if sum(bridesWeights) > 0:
                    bridesProb = [i/sum(bridesWeights) for i in bridesWeights]
                    woman = np.random.choice(potentialBrides, p = bridesProb)
                else:
                    woman = np.random.choice(potentialBrides)
                man.partner = woman
                man.yearMarried = self.year
                woman.partner = man
                if man in woman.previousPartners:
                    woman.previousPartners.remove(man)
                if woman in man.previousPartners:
                    man.previousPartners.remove(woman)
                woman.yearMarried = self.year
                man.yearsSeparated = 0
                woman.yearsSeparated = 0
                man.numberPartner += 1
                woman.numberPartner += 1
                man.justMarried = woman.id
                woman.justMarried = man.id
                
                newHousehold = [man, woman]
                self.joiningSpouses(newHousehold)
                self.marriageTally += 1
    
                if man.house == self.displayHouse or woman.house == self.displayHouse:
                    messageString = str(self.year) + ": #" + str(man.id) + " (age " + str(man.age) + ")"
                    messageString += " and #" + str(woman.id) + " (age " + str(woman.age)
                    messageString += ") marry."
                    self.textUpdateList.append(messageString)
    
    def deathProb(self, base, classRank, needLevel, shareUnmetNeed, classPop):
        a = 0
        for i in range(self.p['numberClasses']):
            a += self.socialClassShares[i]*math.pow(self.p['mortalityBias'], i)
        lowClassRate = base/a
        classRate = lowClassRate*math.pow(self.p['mortalityBias'], classRank)
        a = 0
        for i in range(self.p['numCareLevels']):
            a += self.careNeedShares[classRank][i]*math.pow(self.p['careNeedBias'], (self.p['numCareLevels']-1) - i)
        higherNeedRate = classRate/a
        classRate = higherNeedRate*math.pow(self.p['careNeedBias'], (self.p['numCareLevels']-1) - needLevel) # deathProb
        
        # Add the effect of unmet care need on mortality rate for each care need level
        a = 0
        for x in classPop:
            a += math.pow(self.p['unmetCareNeedBias'], 1-x.averageShareUnmetNeed)
        higherUnmetNeed = (classRate*len(classPop))/a
        deathProb = higherUnmetNeed*math.pow(self.p['unmetCareNeedBias'], 1-shareUnmetNeed)
        
        return (deathProb)
    
    def doDeaths(self):
        
        preDeath = len(self.pop.livingPeople)
        
        deaths = [0, 0, 0, 0, 0]
        """Consider the possibility of death for each person in the sim."""
        for person in self.pop.livingPeople:
            age = person.age
            
            ####     Death process with histroical data  after 1950   ##################
            if self.year > 1950:
                if age > 109:
                    age = 109
                if person.sex == 'male':
                    rawRate = self.death_male[age, self.year-1950]
                if person.sex == 'female':
                    rawRate = self.death_female[age, self.year-1950]
                    
                classPop = [x for x in self.pop.livingPeople if x.careNeedLevel == person.careNeedLevel]
                dieProb = self.deathProb(rawRate, person.classRank, person.careNeedLevel, person.averageShareUnmetNeed, classPop)
                
                # if self.p['policyIndex'] != 0:
                if  self.year < self.p['implementPoliciesFromYear'] and self.year >= self.p['regressionCollectFrom']:
                    age = person.age
                    unmetNeed = person.averageShareUnmetNeed
                    year = self.year-self.p['regressionCollectFrom']
                    regressors = [age, math.log(age), unmetNeed, year, math.log(year+1)]
                    self.inputsMortality[person.sexIndex][person.classRank][person.careNeedLevel].append(regressors)
                    dependentVariable = dieProb # [dieProb]
                    self.outputMortality[person.sexIndex][person.classRank][person.careNeedLevel].append(dependentVariable)
                    
                elif self.year >= self.p['implementPoliciesFromYear']:
                    age = person.age
                    unmetNeed = person.averageShareUnmetNeed
                    year = self.year-self.p['regressionCollectFrom']
                    regressors = [age, math.log(age), unmetNeed, year, math.log(year+1)]
                    s = person.sexIndex
                    r = person.classRank
                    n = person.careNeedLevel
                    try:
                        dieProb = self.regressionModels_M[s][r][n].predict([regressors])
                    except NotFittedError as e:
                        for i in reversed(xrange(r+1)):
                            for j in reversed(xrange(n)):
                                try:
                                    dieProb = self.regressionModels_M[s][i][j].predict([regressors])
                                    break
                                except NotFittedError as e:
                                    continue
            #############################################################################
            
                if random.random() < dieProb:
                    person.dead = True
                    
#                    members = person.householdNetwork.neighbors(person)
#                    for member in members:
#                        member.householdNetwork.remove_node(person)
#                    if person.partner != None and person.sex == 'female':
#                        self.householdsNetwork.remove_node(person.householdNetwork)  
#                        self.householdsNetwork.add_node(person.partner.householdNetwork)
                        
                    person.house.occupants.remove(person)
                    if len(person.house.occupants) == 0:
                        self.map.occupiedHouses.remove(person.house)
#                        if (self.p['interactiveGraphics']):
#                            self.canvas.itemconfig(person.house.icon, state='hidden')
                    if person.partner != None:
                        partner = person.partner
                        if partner.status == 'student':
                            partner.classRank = partner.temporaryClassRank
                            self.enterWorkForce(partner)
                        if partner.careNeedLevel > 2:
                            partner.income = self.p['stateSupport']
                            partner.netIncome = self.p['stateSupport'] 
                        partner.partner = None
                    if person.house == self.displayHouse:
                        messageString = str(self.year) + ": #" + str(person.id) + " died aged " + str(age) + "." 
                        self.textUpdateList.append(messageString)
                
            else: 
                #######   Death process with made-up rates  ######################
                babyDieProb = 0.0
                if age < 1:
                    babyDieProb = self.p['babyDieProb']
                if person.sex == 'male':
                    ageDieProb = (math.exp(age/self.p['maleAgeScaling']))*self.p['maleAgeDieProb'] 
                else:
                    ageDieProb = (math.exp(age/self.p['femaleAgeScaling']))* self.p['femaleAgeDieProb']
                rawRate = self.p['baseDieProb'] + babyDieProb + ageDieProb
                
                classPop = [x for x in self.pop.livingPeople if x.careNeedLevel == person.careNeedLevel]
                dieProb = self.deathProb(rawRate, person.classRank, person.careNeedLevel, person.averageShareUnmetNeed, classPop)
                
                # if self.p['policyIndex'] != 0:
                if self.year < self.p['implementPoliciesFromYear'] and self.year >= self.p['regressionCollectFrom']:
                    age = person.age
                    unmetNeed = person.averageShareUnmetNeed
                    year = self.year-self.p['regressionCollectFrom']
                    regressors = [age, math.log(age), unmetNeed, year, math.log(year+1)]
                    self.inputsMortality[person.sexIndex][person.classRank][person.careNeedLevel].append(regressors)
                    dependentVariable = dieProb # [dieProb]
                    self.outputMortality[person.sexIndex][person.classRank][person.careNeedLevel].append(dependentVariable)
                    
                elif self.year >= self.p['implementPoliciesFromYear']:
                    age = person.age
                    unmetNeed = person.averageShareUnmetNeed
                    year = self.year-self.p['regressionCollectFrom']
                    regressors = [age, math.log(age), unmetNeed, year, math.log(year+1)]
                    s = person.sexIndex
                    r = person.classRank
                    n = person.careNeedLevel
                    try:
                        dieProb = self.regressionModels_M[s][r][n].predict([regressors])
                    except NotFittedError as e:
                        for i in reversed(xrange(r+1)):
                            for j in reversed(xrange(n)):
                                try:
                                    dieProb = self.regressionModels_M[s][i][j].predict([regressors])
                                    break
                                except NotFittedError as e:
                                    continue
                
                if random.random() < dieProb:
                    person.dead = True
                    
                    # Remove perosn from the network of household's members
                    
#                    members = person.householdNetwork.neighbors(person)
#                    for member in members:
#                        member.householdNetwork.remove_node(person)
#                    if person.partner != None and person.sex == 'female':
#                        self.householdsNetwork.remove_node(person.householdNetwork)  
#                        self.householdsNetwork.add_node(person.partner.householdNetwork)
                        
                    deaths[person.classRank] += 1
                    person.house.occupants.remove(person)
                    if len(person.house.occupants) == 0:
                        self.map.occupiedHouses.remove(person.house)
#                        if (self.p['interactiveGraphics']):
#                            self.canvas.itemconfig(person.house.icon, state='hidden')
                    if person.partner != None:
                        partner = person.partner
                        if partner.status == 'student':
                            partner.classRank = partner.temporaryClassRank
                            self.enterWorkForce(partner)
                        if partner.careNeedLevel > 2:
                            partner.income = self.p['stateSupport']
                            partner.netIncome = self.p['stateSupport'] 
                        partner.partner = None
                    if person.house == self.displayHouse:
                        messageString = str(self.year) + ": #" + str(person.id) + " died aged " + str(age) + "." 
                        self.textUpdateList.append(messageString)
                        
                  
        self.pop.livingPeople[:] = [x for x in self.pop.livingPeople if x.dead == False]
        
        postDeath = len(self.pop.livingPeople)
        
        print('the number of people who died is: ' + str(preDeath - postDeath))
        
    def relocateOrphans(self):
        
        orphans = [x for x in self.pop.livingPeople if x.age < self.p['minWorkingAge'] and x.mother != None 
                   and x.mother.dead == True and (x.father.dead == True or x.mother.partner == None)]
        
        loneStudents = [x for x in self.pop.livingPeople if x.age >= self.p['minWorkingAge'] and x.mother != None 
                   and x.mother.dead == True and (x.father.dead == True or x.mother.partner == None) 
                   and (x.status == 'student' or x.status == 'outOfTownStudent')]
        
        for person in loneStudents:
            self.enterWorkForce(person)
        
        for orphan in orphans:
            adoptiveMothers = [x for x in self.pop.livingPeople if x.sex == 'female' and x.partner != None 
                               and x.independentStatus == True and self.householdIncome(x.house.occupants) > 0]
            adoptiveMother = random.choice(adoptiveMothers)
            orphan.mother = adoptiveMother
            adoptiveMother.children.append(orphan)
            orphan.father = adoptiveMother.partner
            adoptiveMother.partner.children.append(orphan)           
            if adoptiveMother.house == self.displayHouse:
                self.textUpdateList.append(str(self.year) + ": #" + str(orphan.id) +
                               " and brothers have been newly adopted by " + str(adoptiveMother.id) + "." )
                            
            self.movePeopleIntoChosenHouse(adoptiveMother.house, orphan.house, [orphan], 'relocateOrphans')

    def doRegressions(self):
        if self.year == self.p['implementPoliciesFromYear']:
            for k in range(2):
                for i in range(self.p['numberClasses']):
                    for j in range(self.p['numCareLevels']):
#                        print('cat: ' + str(k) + ' ' + str(i) + ' ' + str(j))
#                        print(len(self.inputsMortality[k][i][j]))
#                        print(len(self.outputMortality[k][i][j]))
                        # self.regressionModels_M[k][i][j] = LinearRegression()
                        if len(self.inputsMortality[k][i][j]) == 0:
                            print('Warning: RandomForestRegressor instance not fitted yet')
                        if len(self.inputsMortality[k][i][j]) > 0:
                            self.regressionModels_M[k][i][j].fit(self.inputsMortality[k][i][j], self.outputMortality[k][i][j])
                        
                            # mr_predict = self.regressionModels_M[k][i][j].predict(self.inputsMortality[k][i][j])
                            # self.plotRegressions(self.outputMortality[k][i][j], mr_predict)
                            # print(self.regressionModels_M[k][i][j].score(self.inputsMortality[k][i][j], self.outputMortality[k][i][j]))
                        
            for i in range(self.p['numberClasses']):
                # self.regressionModels_F[i]  = LinearRegression()
                self.regressionModels_F[i].fit(self.inputsFertility[i], self.outputFertility[i])
    
    def plotRegressions(self, mr, prediction):
        plt.scatter(mr, prediction)
        plt.show()
    
    def doBirths(self):
        
        preBirth = len(self.pop.livingPeople)
        marriedLadies = 0
        adultLadies = 0
        births = [0, 0, 0, 0, 0]
        marriedPercentage = []
        
        notMarriedReproductiveWomen = [x for x in self.pop.livingPeople
                                       if x.sex == 'female'
                                       and x.age >= self.p['minPregnancyAge']
                                       and x.age <= self.p['maxPregnancyAge']
                                       and x.careNeedLevel < 3]
        
        womenOfReproductiveAge = [x for x in self.pop.livingPeople
                                  if x.sex == 'female'
                                  and x.age >= self.p['minPregnancyAge']
                                  and x.age <= self.p['maxPregnancyAge']
                                  and x.partner != None and x.careNeedLevel < 3]
        
        adultLadies_1 = [x for x in notMarriedReproductiveWomen if x.classRank == 0]   
        marriedLadies_1 = len([x for x in adultLadies_1 if x.partner != None])
        if len(adultLadies_1) > 0:
            marriedPercentage.append(marriedLadies_1/float(len(adultLadies_1)))
        else:
            marriedPercentage.append(0)
        adultLadies_2 = [x for x in notMarriedReproductiveWomen if x.classRank == 1]    
        marriedLadies_2 = len([x for x in adultLadies_2 if x.partner != None])
        if len(adultLadies_2) > 0:
            marriedPercentage.append(marriedLadies_2/float(len(adultLadies_2)))
        else:
            marriedPercentage.append(0)
        adultLadies_3 = [x for x in notMarriedReproductiveWomen if x.classRank == 2]   
        marriedLadies_3 = len([x for x in adultLadies_3 if x.partner != None]) 
        if len(adultLadies_3) > 0:
            marriedPercentage.append(marriedLadies_3/float(len(adultLadies_3)))
        else:
            marriedPercentage.append(0)
        adultLadies_4 = [x for x in notMarriedReproductiveWomen if x.classRank == 3]  
        marriedLadies_4 = len([x for x in adultLadies_4 if x.partner != None])   
        if len(adultLadies_4) > 0:
            marriedPercentage.append(marriedLadies_4/float(len(adultLadies_4)))
        else:
            marriedPercentage.append(0)
        adultLadies_5 = [x for x in notMarriedReproductiveWomen if x.classRank == 4]   
        marriedLadies_5 = len([x for x in adultLadies_5 if x.partner != None]) 
        if len(adultLadies_5) > 0:
            marriedPercentage.append(marriedLadies_5/float(len(adultLadies_5)))
        else:
            marriedPercentage.append(0)
        
        # print(marriedPercentage)
        
#        for person in self.pop.livingPeople:
#           
#            if person.sex == 'female' and person.age >= self.p['minPregnancyAge']:
#                adultLadies += 1
#                if person.partner != None:
#                    marriedLadies += 1
#        marriedPercentage = float(marriedLadies)/float(adultLadies)
        
        for woman in womenOfReproductiveAge:
            
            
            if self.year < 1951:
                rawRate = self.p['growingPopBirthProb']
            else:
                rawRate = self.fert_data[(self.year - woman.birthdate)-16, self.year-1950]
                
            birthProb = self.computeBirthProb(self.p['fertilityBias'], rawRate, woman.classRank)
            
            # if self.p['policyIndex'] != 0:
            if self.year < self.p['implementPoliciesFromYear'] and self.year >= self.p['regressionCollectFrom']:
                age = woman.age-16
                year = self.year-self.p['regressionCollectFrom']
                regressors = [age, math.log(age), year, math.log(year+1)]
                self.inputsFertility[woman.classRank].append(regressors)
                dependentVariable = birthProb # [birthProb]
                self.outputFertility[woman.classRank].append(dependentVariable)
                
            elif self.year >= self.p['implementPoliciesFromYear']:
                age = woman.age-16
                year = self.year-self.p['regressionCollectFrom']
                regressors = [age, math.log(age), year, math.log(year+1)]
                r = woman.classRank
                try:
                    birthProb = self.regressionModels_F[r].predict([regressors])
                except NotFittedError as e:
                    for i in reversed(xrange(r)):
                        try:
                            birthProb = self.regressionModels_F[i].predict([regressors])
                            break
                        except NotFittedError as e:
                            continue
                    
            #baseRate = self.baseRate(self.socialClassShares, self.p['fertilityBias'], rawRate)
            #fertilityCorrector = (self.socialClassShares[woman.classRank] - self.p['initialClassShares'][woman.classRank])/self.p['initialClassShares'][woman.classRank]
            #baseRate *= 1/math.exp(self.p['fertilityCorrector']*fertilityCorrector)
            #birthProb = baseRate*math.pow(self.p['fertilityBias'], woman.classRank)
            
            if random.random() < (birthProb/marriedPercentage[woman.classRank])*0.85:
                # (self, mother, father, age, birthYear, sex, status, house,
                # classRank, sec, edu, wage, income, finalIncome):
                sex = random.choice(['male', 'female'])
                baby = Person(woman, woman.partner, 0, self.year, sex, 
                              'child', woman.house, woman.classRank, 0, 0, 0, 0, 0)
                births[woman.classRank] += 1
                self.pop.allPeople.append(baby)
                self.pop.livingPeople.append(baby)
                woman.house.occupants.append(baby)
                woman.children.append(baby)
                woman.partner.children.append(baby)
                if woman.house == self.displayHouse:
                    messageString = str(self.year) + ": #" + str(woman.id) + " had a baby, #" + str(baby.id) + "." 
                    self.textUpdateList.append(messageString)
        postBirth = len(self.pop.livingPeople)
        
        print('the number of births is: ' + str(postBirth - preBirth))
    
    def computeBirthProb(self, fertilityBias, rawRate, womanRank):
        
        womenOfReproductiveCondition = [x for x in self.pop.livingPeople
                                  if x.sex == 'female' and x.age >= self.p['minPregnancyAge'] 
                                  and x.age <= self.p['maxPregnancyAge'] and x.careNeedLevel < 3]
        womanClassShares = []
        womanClassShares.append(float(len([x for x in womenOfReproductiveCondition if x.classRank == 0]))/float(len(womenOfReproductiveCondition)))
        womanClassShares.append(float(len([x for x in womenOfReproductiveCondition if x.classRank == 1]))/float(len(womenOfReproductiveCondition)))
        womanClassShares.append(float(len([x for x in womenOfReproductiveCondition if x.classRank == 2]))/float(len(womenOfReproductiveCondition)))
        womanClassShares.append(float(len([x for x in womenOfReproductiveCondition if x.classRank == 3]))/float(len(womenOfReproductiveCondition)))
        womanClassShares.append(float(len([x for x in womenOfReproductiveCondition if x.classRank == 4]))/float(len(womenOfReproductiveCondition)))
        a = 0
        for i in range(self.p['numberClasses']):
            a += womanClassShares[i]*math.pow(self.p['fertilityBias'], i)
        baseRate = rawRate/a
        birthProb = baseRate*math.pow(self.p['fertilityBias'], womanRank)
        return(birthProb)

    def careNeeds(self):
        
        for person in self.pop.livingPeople:
            person.visitedCarer = False
            person.hoursDemand = 0
            person.residualNeed = 0
            person.informalCare = 0
            person.formalCare = 0
            person.careReceived = 0
            person.hoursSocialCareDemand = 0
            person.residualSocialCareNeed = 0
            person.residualIncomeCare = 0
            person.maxFormalCareSupply = 0
            person.residualWorkingHours = 0
            person.incomeByTaxBands = []
            person.hoursChildCareDemand = 0
            person.residualChildCareNeed = 0
            person.socialWork = 0
            person.workToCare = 0
            person.totalSupply = 0
            person.householdSupply = 0
            person.informalSupplyByKinship = [0.0, 0.0, 0.0, 0.0]
            person.formalSupplyByKinship = [0.0, 0.0, 0.0, 0.0]
            
            person.residualInformalSupply = [0.0, 0.0, 0.0, 0.0]
            person.residualFormalSupply = [0.0, 0.0, 0.0, 0.0]
            person.hoursInformalSupply = [0.0, 0.0, 0.0, 0.0]
            person.hoursFormalSupply = [0.0, 0.0, 0.0, 0.0]
            person.extraworkCare = [0.0, 0.0, 0.0, 0.0]
            
            person.careNetwork.clear()
            person.careNetwork.add_node(person)
            
            person.supplyNetwork.clear()
            person.supplyNetwork.add_node(person)
            
            person.householdTotalSupply = 0
            
            person.volunteerCareSupply = 0
            person.potentialVolunteer = False
            person.maxNokSupply = 0
            person.residualNetNeed = 0
            
            person.careReceivers = []
            person.totalCareSupplied = []
            
            careNeed = self.p['careDemandInHours'][person.careNeedLevel]

            person.hoursDemand = careNeed
            person.residualNeed = person.hoursDemand
            
            if person.careNeedLevel >= self.p['socialSupportLevel']:
                self.publicSupply += person.hoursDemand
                person.residualNeed = 0.0 # person.hoursDemand
                
#            person.hoursSocialCareDemand = careNeed
#            person.residualSocialCareNeed = person.hoursDemand
                
            if person.house == self.displayHouse:
                messageString = str(self.year) + ": #" + str(person.id) + " now has "
                messageString += self.p['careLevelNames'][person.careNeedLevel] + " care needs." 
                self.textUpdateList.append(messageString)
        
        # Childcare need
        
        children = [x for x in self.pop.livingPeople if x.age < self.p['ageTeenagers']]
#        
        for child in children:
            if child.age == 0:
                child.status == 'child'
                childCare = self.p['zeroYearCare']
                if child.hoursDemand < childCare:
                    child.hoursDemand = childCare
                    child.residualNeed = child.hoursDemand

            if child.age == 0 and child.mother.socialCareReceiver == False:
                child.mother.socialWork = 0 #self.p['zeroYearCare']
                child.mother.childCareWork = self.p['zeroYearCare']
                # child.mother.income = 0
                # child.mother.disposableIncome = child.mother.income
                # child.mother.netIncome = child.mother.income
                child.mother.status = 'maternity'
                child.mother.babyCarer = True
                child.residualNeed = 0
                child.informalCare = self.p['zeroYearCare']
                
        totalCareDemand = sum([x.hoursDemand for x in self.pop.livingPeople if x.careNeedLevel > 0])
        totalResidualNeed = sum([x.residualNeed for x in self.pop.livingPeople if x.careNeedLevel > 0])
        self.sharePublicCare = 0
        if totalCareDemand > 0:
            self.sharePublicCare = 1.0 - float(totalResidualNeed)/float(totalCareDemand)
#                
#        for person in self.pop.livingPeople:
#            person.hoursDemand = person.hoursSocialCareDemand + person.hoursChildCareDemand
    

    
    def careCreditsAllocation(self):
        # Computing the quantity of social credit to be created (and allocated)
        
        newCredit = 0
        if self.year == self.p['implementPoliciesFromYear']:
            totalCareNeed = sum([x.residualNeed for x in self.pop.livingPeople])
            self.initialCareCredits = math.ceil(totalCareNeed*self.p['socialCareCreditShare'])
            newCredit = self.initialCareCredits
        if self.year > self.p['implementPoliciesFromYear']:
            totalCareCredits = 0
            creditPop = [x for x in self.pop.livingPeople if x.socialCareCredits > 0]
            totalCareCredits = sum([x.socialCareCredits for x in creditPop])
            if self.p['absoluteCreditQuantity'] == True:
                newCredit = max(self.initialCareCredits*self.p['quantityYearlyIncrease'] - totalCareCredits, 0)
            else:
                totalCareNeed = sum([x.residualNeed for x in self.pop.livingPeople])
                targetQuantity = math.ceil(totalCareNeed*self.p['socialCareCreditShare'])
                newCredit = max(targetQuantity - totalCareCredits, 0)
        
        # Allocation of care Credits
        careReceivers = [x for x in self.pop.livingPeople if x.residualNeed > 0]
        for person in careReceivers:
            person.creditNeedRatio = float(person.socialCareCredits)/float(person.residualNeed)
        while newCredit > 0:
            careReceivers.sort(key=operator.attrgetter("creditNeedRatio"))
            receiver = careReceivers[0]
            receiver.socialCareCredits += 1
            receiver.creditNeedRatio = float(receiver.socialCareCredits)/float(receiver.residualNeed)
            newCredit -= 1
        for person in careReceivers:
            person.maxNokSupply = max(person.residualNeed - round(person.socialCareCredits*(1-self.p['kinshipNetworkCarePropension'])), 0)
            person.residualNetNeed = int((person.maxNokSupply+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
        self.socialCareCredits = sum([x.socialCareCredits for x in self.pop.livingPeople if x.socialCareCredits > 0])
        
    def careTransitions(self):
        
        peopleNotInCriticalCare = [x for x in self.pop.livingPeople if x.careNeedLevel < self.p['numCareLevels']-1]
        
        for person in peopleNotInCriticalCare:
            if person.sex == 'male':
                ageCareProb = ( ( math.exp( person.age /
                                            self.p['maleAgeCareScaling'] ) )
                               * self.p['personCareProb'] )
            else:
                ageCareProb = ( ( math.exp( person.age /
                                           self.p['femaleAgeCareScaling'] ) )
                               * self.p['personCareProb'] )
            careProb = (self.p['baseCareProb'] + ageCareProb)
            baseProb = self.baseRate(self.p['careBias'], careProb)
            
            unmetNeedFactor = 1/math.exp(self.p['unmetNeedExponent']*person.averageShareUnmetNeed)
            
            careProb = baseProb*math.pow(self.p['careBias'], person.classRank)/unmetNeedFactor 
            
            if self.year == self.p['getCheckVariablesAtYear']:
                self.careTransitionRate[person.classRank].append(careProb)
            
            if random.random() < careProb:
                person.socialCareReceiver = True
                baseTransition = self.baseRate(self.p['careBias'], 1-self.p['careTransitionRate'])
                if person.careNeedLevel > 0:
                    unmetNeedFactor = 1/math.exp(self.p['unmetNeedExponent']*person.averageShareUnmetNeed)
                else:
                    unmetNeedFactor = 1.0
                transitionRate = (1.0 - baseTransition*math.pow(self.p['careBias'], person.classRank))*unmetNeedFactor

                stepCare = 1
                bound = transitionRate
                while random.random() > bound and stepCare < self.p['numCareLevels'] - 1:
                    stepCare += 1
                    bound += (1-bound)*transitionRate
                person.careNeedLevel += stepCare
                
                if person.careNeedLevel >= self.p['numCareLevels']:
                    person.careNeedLevel = self.p['numCareLevels'] - 1
                
                if person.careNeedLevel > 2:
                    person.status = 'inactive'
                
                if person.age < self.p['ageOfRetirement'] and person.ageStartWorking != -1:
                    shareWorkingLife = (person.age - person.ageStartWorking)/float(self.p['ageOfRetirement'] - person.ageStartWorking)
                    # print(shareWorkingLife)
                    person.income = self.p['pensionWage'][person.classRank]*self.p['weeklyHours']
                    if person.careNeedLevel < self.p['hillHealthLevelThreshold']:
                        person.income *= shareWorkingLife
                    else:
                        person.income *= (shareWorkingLife + self.p['seriouslyHillSupportRate']*(1-shareWorkingLife))
                    if person.income < self.p['stateSupport']:
                        person.income = self.p['stateSupport']
                        person.netIncome = person.income
                
                if person.status == 'inactive' and person.ageStartWorking == -1:
                    person.income = self.p['stateSupport']
                    person.netIncome = self.p['stateSupport'] 
#                    if person.income == 0:
#                        print('Inactive person ' + str(person.id) + ' is ' + str(person.income))
            if person.house == self.displayHouse:
                messageString = str(self.year) + ": #" + str(person.id) + " now has "
                messageString += self.p['careLevelNames'][person.careNeedLevel] + " care needs." 
                self.textUpdateList.append(messageString)
                       
    def careSupplies(self):

        listHouseholds = [list(x.occupants) for x in self.map.occupiedHouses]
        
        for household in listHouseholds:
                
            householdCarers = [x for x in household if x.hoursDemand == 0 and x.status != 'maternity']
            notWorking = [x for x in householdCarers if x.status == 'teenager' or x.status == 'retired' or x.status == 'student']
            for member in notWorking:
                if member.status == 'teenager':
                    member.residualInformalSupply = list(self.p['teenAgersHours'])
                elif member.status == 'student':
                    member.residualInformalSupply = list(self.p['studentHours'])
                elif member.status == 'retired':
                    member.residualInformalSupply = list(self.p['retiredHours'])
                member.hoursInformalSupply = member.residualInformalSupply

            employed = [x for x in householdCarers if x.status == 'employed']
            employed.sort(key=operator.attrgetter("wage"))

            householdIncome = self.householdIncome(household)
            
            householdPerCapitaIncome = householdIncome/float(len(household))
            
            # Check time series
            if self.year == self.p['getCheckVariablesAtYear']:
                self.perCapitaHouseholdIncome.append(householdPerCapitaIncome)
            
            # Compute the total income devoted to informal care supply
            incomeCareParameter = self.p['incomeCareParam']
            incomeCoefficient = 1/math.exp(incomeCareParameter*householdPerCapitaIncome) # Min-Max: 0 - 1500
            residualIncomeForCare = householdIncome*(1 - incomeCoefficient)
        
            for member in household:
                member.residualIncomeCare = residualIncomeForCare
                if member.status == 'employed':
                    member.residualWorkingHours = self.p['weeklyHours']
                    member.income = member.residualWorkingHours*member.wage
            
            incomes = [x.income for x in household if x.income > 0]
            # Compute income by tax band
            incomeByTaxBand = self.updateTaxBrackets(incomes)
            
            for member in household:
                member.incomeByTaxBands = incomeByTaxBand
                
            for worker in employed:
                worker.extraworkCare = list(self.p['employedHours'])
                worker.hoursInformalSupply = worker.extraworkCare
                
            totHours = self.maxCareSupplyHours(household)
            householdSupplyHours = int((totHours+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
            distanceOneSupplyHours = int((totHours*self.p['formalCareDiscountFactor']+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
            formalSupplyHours = [householdSupplyHours, distanceOneSupplyHours, 0, 0]
            
            earningMembers = [x for x in household if x.income > 0]
        
            if len(earningMembers) == 0 and formalSupplyHours[0] > 0:
                print('Error: no income to pay social care from (careSupplies)')
                
            for member in household:
                member.residualFormalSupply = formalSupplyHours
                member.hoursFormalSupply = formalSupplyHours 

    def spousesCareLocation(self, household, town):
        
        kinshipWeight_1 = 1/math.pow(self.p['networkDistanceParam'], 0.0)
        kinshipWeight_2 = 1/math.pow(self.p['networkDistanceParam'], 1.0)
        kinshipWeight_3 = 1/math.pow(self.p['networkDistanceParam'], 2.0) 
        
        nok_1 = []
        nok_2 = []
        nok_3 = []
        visited = []
        
        for i in household:
            if i.father != None:
                nok = i.father
                if nok.dead == False and nok not in household and nok not in visited:
                    nok_1.append(nok)
                    visited.extend(nok.household)
                nok = i.mother
                if nok.dead == False and nok not in household and nok not in visited:
                    nok_1.append(nok)
                    visited.extend(nok.household)
            for child in i.children:
                nok = child
                if nok.dead == False and nok not in household and nok not in visited:
                    nok_1.append(nok)
                    visited.extend(nok.household)
                        
        for i in household:
            if i.father != None:
                if i.father.father != None:
                    nok = i.father.father
                    if nok.dead == False and nok not in household and nok not in visited:
                        nok_2.append(nok)
                        visited.extend(nok.household)
                    nok = i.father.mother
                    if nok.dead == False and nok not in household and nok not in visited:
                        nok_2.append(nok)
                        visited.extend(nok.household)
                if i.mother.father != None:
                    nok = i.mother.father
                    if nok.dead == False and nok not in household and nok not in visited:
                        nok_2.append(nok)
                        visited.extend(nok.household)
                    nok = i.mother.mother
                    if nok.dead == False and nok not in household and nok not in visited:
                        nok_2.append(nok)
                        visited.extend(nok.household)
                brothers = list(set(i.father.children + i.mother.children))
                brothers.remove(i)
                for brother in brothers:
                    nok = brother
                    if nok.dead == False and nok not in household and nok not in visited:
                        nok_2.append(nok)
                        visited.extend(nok.household)
            for child in i.children:
                for grandchild in child.children:
                    nok = grandchild
                    if nok.dead == False and nok not in household and nok not in visited:
                        nok_2.append(nok)
                        visited.extend(nok.household)
                        
        for i in household:
            uncles = []
            if i.father != None:
                if i.father.father != None:
                    uncles = list(set(i.father.father.children + i.father.mother.children))
                    uncles.remove(i.father)
                if i.mother.father != None:
                    uncles.extend(list(set(i.mother.father.children + i.mother.mother.children)))
                    uncles.remove(i.mother)
                for uncle in uncles:
                    nok = uncle
                    if nok.dead == False and nok not in household and nok not in visited:
                        nok_3.append(nok)
                        visited.extend(nok.household)
                brothers = list(set(i.father.children + i.mother.children))
                brothers.remove(i)
                for brother in brothers:
                    for child in brother.children:
                        nok = child
                        if nok.dead == False and nok not in household and nok not in visited:
                            nok_3.append(nok)
                            visited.extend(nok.household)

        networkSize_currentTown = 0
        networkSize_currentTown += sum([float(len(x.house.occupants)) for x in nok_1 if x.house.town == town])*kinshipWeight_1
        networkSize_currentTown += sum([float(len(x.house.occupants)) for x in nok_2 if x.house.town == town])*kinshipWeight_2
        networkSize_currentTown += sum([float(len(x.house.occupants)) for x in nok_3 if x.house.town == town])*kinshipWeight_3
        
        networkSize_otherTowns = 0
        networkSize_otherTowns += sum([float(len(x.house.occupants)) for x in nok_1 if x.house.town != town])*kinshipWeight_1
        networkSize_otherTowns += sum([float(len(x.house.occupants)) for x in nok_2 if x.house.town != town])*kinshipWeight_2
        networkSize_otherTowns += sum([float(len(x.house.occupants)) for x in nok_3 if x.house.town != town])*kinshipWeight_3
        
        if float(networkSize_currentTown)+float(networkSize_otherTowns) > 0:
            return float(networkSize_currentTown)/(float(networkSize_currentTown)+float(networkSize_otherTowns))
        else:
            return 1.0
    
    def resetVariables(self, house):
        house.careNetwork.clear()
        house.totalSocialCareNeed = 0
        house.totalChildCareNeed = 0
        house.careNeedIndex = 0
        house.childCareNeeds = []
        house.childCarePrices = []
        house.residualIncomeForCare = []
        house.householdInformalSupply = []
        house.householdFormalSupply = []
        house.networkSupply = 0
        house.networkTotalSupplies = []
        house.networkInformalSupply = []
        house.informalChildCareReceived = 0
        house.informalSocialCareReceived = 0
        house.formalChildCareReceived = 0
        house.formalSocialCareReceived = 0
        house.householdFormalSupplyCost = 0
        house.incomeByTaxBand = []

        household = list(house.occupants)
        for person in household:
            person.hoursChildCareDemand = 0
            person.residualChildCareNeed = 0
            person.hoursDemand = 0
            person.residualNeed = 0
            person.informalChildCareReceived = 0
            person.formalChildCareReceived = 0
            person.informalSocialCareReceived = 0
            person.formalSocialCareReceived = 0
            person.childWork = 0
            person.socialWork = 0
            person.residualInformalSupplies = [0.0, 0.0, 0.0, 0.0]
            person.hoursInformalSupplies = [0.0, 0.0, 0.0, 0.0]
            person.residualInformalSupply = 0
            person.residualWorkingHours = 0
        
            # Check variables
            person.informalCare = 0
            person.formalCare = 0
            person.careReceived = 0
            person.residualSocialCareNeed = 0
            person.residualIncomeCare = 0
            person.maxFormalCareSupply = 0
            person.hoursChildCareDemand = 0
            person.residualChildCareNeed = 0
            person.socialWork = 0
            person.workToCare = 0
            person.totalSupply = 0
            person.householdSupply = 0
            person.informalSupplyByKinship = [0.0, 0.0, 0.0, 0.0]
            person.formalSupplyByKinship = [0.0, 0.0, 0.0, 0.0]
            
            person.supplyNetwork.clear()
            person.supplyNetwork.add_node(person)
            
            person.volunteerCareSupply = 0
            person.potentialVolunteer = False
            person.maxNokSupply = 0
            person.residualNetNeed = 0
            
            person.careReceivers = []
            person.totalCareSupplied = []
            
    
    def computeChildCareNeeds(self, house):
        household = list(house.occupants)
        newBorns = [x for x in household if x.age == 0]
        if len(newBorns) > 0:
            for child in newBorns:
                child.hoursChildCareDemand = self.p['zeroYearCare']
                child.informalChildCareReceived = self.p['zeroYearCare']
                child.mother.childWork = self.p['zeroYearCare']
                child.mother.status = 'maternity'
            
        children = [x for x in household if x.age > 0 and x.age < self.p['ageTeenagers']]
        ages = [x.age for x in children]
        house.formalChilCareReceived = [0]*len(ages)
        income = sum([x.income for x in household])
        if income  < self.p['maxHouseholdIncomeChildCareSupport']:
            firstGroup = [x for x in children if x.age < 2]
            for child in firstGroup:
                childCareNeed = self.p['childCareDemand']
                child.hoursChildCareDemand = max(0, childCareNeed - child.residualNeed)
                child.residualChildCareNeed = child.hoursChildCareDemand
                house.totalChildCareNeed += child.residualChildCareNeed
            secondGroup = [x for x in children if x.age  == 2]
            for child in secondGroup:
                childCareNeed = self.p['childCareDemand']-self.p['freeChildCareHoursToddlers']
                child.hoursChildCareDemand = max(0, childCareNeed - child.residualNeed)
                child.residualChildCareNeed = child.hoursChildCareDemand
                house.totalChildCareNeed += child.residualChildCareNeed
            thirdGroup = [x for x in children if x.age > 2 and x.age < 5]
            for child in thirdGroup:
                childCareNeed = self.p['childCareDemand']-self.p['freeChildCareHoursPreSchool']
                child.hoursChildCareDemand = max(0, childCareNeed - child.residualNeed)
                child.residualChildCareNeed = child.hoursChildCareDemand
                house.totalChildCareNeed += child.residualChildCareNeed
            fourthGroup = [x for x in children if x.age > 4]
            for child in fourthGroup:
                childCareNeed = self.p['childCareDemand']-self.p['freeChildCareHoursSchool']
                child.hoursChildCareDemand = max(0, childCareNeed - child.residualNeed)
                child.residualChildCareNeed = child.hoursChildCareDemand
                house.totalChildCareNeed += child.residualChildCareNeed
        else:
            firstGroup = [x for x in children if x.age < 3]
            for child in firstGroup:
                childCareNeed = self.p['childCareDemand']
                child.hoursChildCareDemand = max(0, childCareNeed - child.residualNeed)
                child.residualChildCareNeed = child.hoursChildCareDemand
                house.totalChildCareNeed += child.residualChildCareNeed
            secondGroup = [x for x in children if x.age > 2 and x < 5]
            for child in secondGroup:
                childCareNeed = self.p['childCareDemand'] - self.p['freeChildCareHoursPreSchool']
                child.hoursChildCareDemand = max(0, childCareNeed - child.residualNeed)
                child.residualChildCareNeed = child.hoursChildCareDemand
                house.totalChildCareNeed += child.residualChildCareNeed
            thirdGroup = [x for x in children if x.age > 4]
            for child in thirdGroup:
                childCareNeed = self.p['childCareDemand'] - self.p['freeChildCareHoursSchool']
                child.hoursChildCareDemand = max(0, childCareNeed - child.residualNeed)
                child.residualChildCareNeed = child.hoursChildCareDemand
                house.totalChildCareNeed += child.residualChildCareNeed
                
        children.sort(key=operator.attrgetter("residualChildCareNeed"))
        residualNeeds = [x.residualChildCareNeed for x in children]
        marginalNeeds = []
        numbers = []
        toSubtract = 0
        for need in residualNeeds:
            marginalNeed = need-toSubtract
            if marginalNeed > 0:
                marginalNeeds.append(marginalNeed)
                num = len([x for x in residualNeeds if x >= need])
                numbers.append(num)                
                toSubtract = need
        house.childCareNeeds = marginalNeeds
        
        prices = []
        residualCare = 0
        cumulatedCare = 0
        for i in range(len(numbers)):
            cost = 0
            residualCare = house.childCareNeeds[i]
            for child in children[-numbers[i]:]:
                if cumulatedCare + residualCare + child.formalChildCareReceived <= self.p['childcareTaxFreeCap']:
                    cost += p['priceChildCare']*(1-p['childCareTaxFreeRate'])*residualCare
                else:
                    if child.formalChildCareReceived + cumulatedCare >= self.p['childcareTaxFreeCap']:
                        cost += p['priceChildCare']*residualCare
                    else:
                        discountedCare = self.p['childcareTaxFreeCap'] - (child.formalChildCareReceived + cumulatedCare)
                        cost1 = discountedCare*p['priceChildCare']*(1-p['childCareTaxFreeRate'])
                        fullPriceCare = residualCare - discountedCare
                        cost2 = fullPriceCare*p['priceChildCare']
                        cost += (cost1 + cost2)
            cumulatedCare += house.childCareNeeds[i]
            prices.append(cost/house.childCareNeeds[i])
        house.childCarePrices = prices
    
    def updateFinancialWealth(self, house):
        household = list(house.occupants)
        ageClass = 0
        for member in household:
            if member.age >=25 and member.age < 35:
                ageClass == 1
            elif member.age >=35 and member.age < 45:
                ageClass == 2
            elif member.age >=45 and member.age < 55:
                ageClass == 3
            elif member.age >=55 and member.age < 65:
                ageClass == 4
            elif member.age >=65 and member.age < 75:
                ageClass == 5
            elif member.age >=75 and member.age < 85:
                ageClass == 6
            elif member.age > 85:
                ageClass == 7
            if member.classRank == 0:
                member.wealth = self.p['savings_SES_I'][ageClass]
            elif member.classRank == 1:
                member.wealth = self.p['savings_SES_II'][ageClass]
            elif member.classRank == 2:
                member.wealth = self.p['savings_SES_III'][ageClass]
            elif member.classRank == 3:
                member.wealth = self.p['savings_SES_IV'][ageClass]
            elif member.classRank == 4:
                member.wealth = self.p['savings_SES_V'][ageClass]
            
    def computeSocialCareNeeds(self, house):
        household = list(house.occupants)
        for person in household:
            careNeed = self.p['careDemandInHours'][person.careNeedLevel]
            person.hoursDemand = careNeed
            person.residualNeed = person.hoursDemand
            if person.careNeedLevel >= self.p['socialSupportLevel'] and person.wealth < self.p['maxSavingsMeansTest'] and person.age > self.p['minAgeForSupport']:
                self.publicSupply += person.hoursDemand
                person.residualNeed = 0.0 
        house.totalSocialCareNeed = sum([x.residualNeed for x in household])
        
        totalCareDemand = sum([x.hoursDemand for x in self.pop.livingPeople if x.careNeedLevel > 0])
        totalResidualNeed = sum([x.residualNeed for x in self.pop.livingPeople if x.careNeedLevel > 0])
        self.sharePublicCare = 0
        if totalCareDemand > 0:
            self.sharePublicCare = 1.0 - float(totalResidualNeed)/float(totalCareDemand)
        # Compute social care needs according to prices (considering tax deduction)
#        incomes = [x.income for x in household]
#        incomeByTaxBand = [0]*self.p['taxBandsNumber']
#        incomeByTaxBand[-1] = sum(incomes)
#        for i in range(int(self.p['taxBandsNumber'])-1):
#            for income in incomes:
#                if income > self.p['taxBrackets'][i]:
#                    bracket = income-self.p['taxBrackets'][i]
#                    incomeByTaxBand[i] += bracket
#                    incomeByTaxBand[-1] -= bracket
#                    incomes[incomes.index(income)] -= bracket
#        house.incomeBrackets = incomeByTaxBand
#        # Create bands of social care according to costs
#        prices = [p['priceSocialCare']*(1.0-x*self.p['taxBreakRate']) for x in self.p['bandsTaxationRates']]
#        maxFormalCare = []
#        for i in range(int(self.p['taxBandsNumber'])):
#            maxFormalCare.append(house.incomeBrackets[i]/prices[i])
#        residualCare = house.totalSocialCareNeed
#        house.socialCareNeeds = []
#        house.socialCarePrices = []
#        for i in range(int(self.p['taxBandsNumber'])):
#            if maxFormalCare[i] > 0 and residualCare > 0:
#                if maxFormalCare[i] >= residualCare:
#                    house.socialCareNeeds.append(residualCare)
#                    residualCare = 0
#                    break
#                else:
#                    house.socialCareNeeds.append(maxFormalCare[i])
#                    residualCare -= maxFormalCare[i]
#                house.socialCarePrices.append(prices[i])
#        if residualCare > 0:  
#            house.socialCareNeeds.append(residualCare)
#            house.socialCarePrices.append(p['priceSocialCare'])
    
    def householdCareNetwork(self, house):
    
        household = list(house.occupants)
        visited = []
        # Distance 1
        for member in household:
            
            if member.father != None:
                nok = member.father
                if nok.dead == False and nok not in household and nok.house not in visited:
                    house.careNetwork.add_edge(house, nok.house, distance = 1)
                    visited.append(nok.house)
                nok = member.mother
                if nok.dead == False and nok not in household and nok.house not in visited:
                    house.careNetwork.add_edge(house, nok.house, distance = 1)
                    visited.append(nok.house)
            for child in member.children:
                nok = child
                if nok.dead == False and nok not in household and nok.house not in visited:
                    house.careNetwork.add_edge(house, nok.house, distance = 1)
                    visited.append(nok.house)
                    
        # Distance 2
        for member in household:
            if member.father != None:
                if member.father.father != None:
                    nok = member.father.father
                    if nok.dead == False and nok not in household and nok.house not in visited:
                        house.careNetwork.add_edge(house, nok.house, distance = 2)
                        visited.append(nok.house)
                    nok = member.father.mother
                    if nok.dead == False and nok not in household and nok.house not in visited:
                        house.careNetwork.add_edge(house, nok.house, distance = 2)
                        visited.append(nok.house)
                if member.mother.father != None:
                    nok = member.mother.father
                    if nok.dead == False and nok not in household and nok.house not in visited:
                        house.careNetwork.add_edge(house, nok.house, distance = 2)
                        visited.append(nok.house)
                    nok = member.mother.mother
                    if nok.dead == False and nok not in household and nok.house not in visited:
                        house.careNetwork.add_edge(house, nok.house, distance = 2)
                        visited.append(nok.house)
                brothers = list(set(member.father.children + member.mother.children))
                brothers.remove(member)
                for brother in brothers:
                    nok = brother
                    if nok.dead == False and nok not in household and nok.house not in visited:
                        house.careNetwork.add_edge(house, nok.house, distance = 2)
                        visited.append(nok.house)
            for child in member.children:
                for grandchild in child.children:
                    nok = grandchild
                    if nok.dead == False and nok not in household and nok.house not in visited:
                        house.careNetwork.add_edge(house, nok.house, distance = 2)
                        visited.append(nok.house)
                        
        # Distance 3
        for member in household:
            uncles = []
            if member.father != None:
                if member.father.father != None:
                    uncles = list(set(member.father.father.children + member.father.mother.children))
                    uncles.remove(member.father)
                if member.mother.father != None:
                    uncles.extend(list(set(member.mother.father.children + member.mother.mother.children)))
                    uncles.remove(member.mother)
                for uncle in uncles:
                    nok = uncle
                    if nok.dead == False and nok not in household and nok.house not in visited:
                        house.careNetwork.add_edge(house, nok.house, distance = 3)
                        visited.extend(nok.household)
                brothers = list(set(member.father.children + member.mother.children))
                brothers.remove(member)
                for brother in brothers:
                    for child in brother.children:
                        nok = child
                        if nok.dead == False and nok not in household and nok.house not in visited:
                            house.careNetwork.add_edge(house, nok.house, distance = 3)
                            visited.extend(nok.household)
         
    def updateCareNeedIndex(self, house):
        house.childCareNeedShare = 0
        if house.totalChildCareNeed+house.totalSocialCareNeed > 0:
            house.childCareNeedShare = house.totalChildCareNeed/(house.totalChildCareNeed+house.totalSocialCareNeed)
        household = list(house.occupants)
        num1 = sum([x.residualChildCareNeed for x in household])*self.p['priceChildCare']
        num2 = sum([x.residualNeed for x in household])*self.p['priceSocialCare']
        house.careNeedIndex = (num1+num2)
        
    def computeCareSupplies(self, house):
        household = list(house.occupants)
        householdCarers = [x for x in household if x.hoursDemand == 0 and x.status != 'maternity']
        notWorking = [x for x in householdCarers if x.status == 'teenager' or x.status == 'retired' or x.status == 'student']
        employed = [x for x in householdCarers if x.status == 'employed']
        
        for member in notWorking:
            if member.status == 'teenager':
                member.residualInformalSupplies = list(self.p['teenAgersHours'])
            elif member.status == 'student':
                member.residualInformalSupplies = list(self.p['studentHours'])
            elif member.status == 'retired':
                member.residualInformalSupplies = list(self.p['retiredHours'])
            member.hoursInformalSupplies = member.residualInformalSupplies
            
        for worker in employed:
            worker.residualInformalSupplies = list(self.p['employedHours'])
            worker.hoursInformalSupplies = worker.residualInformalSupplies
            worker.residualWorkingHours = self.p['weeklyHours']
            worker.income = worker.residualWorkingHours*worker.wage
        
        house.householdInformalSupply = []
        for i in range(4):
            house.householdInformalSupply.append(sum([x.residualInformalSupplies[i] for x in householdCarers]))
        
        income = sum([x.income for x in household])
        incomePerCapita = income/len(household)
        
        incomes = [x.income for x in household]
        house.incomeByTaxBand = [0]*int(self.p['taxBandsNumber'])
        house.incomeByTaxBand[-1] = sum(incomes)
        for i in range(int(self.p['taxBandsNumber'])-1):
            for income in incomes:
                if income > self.p['taxBrackets'][i]:
                    bracket = income-self.p['taxBrackets'][i]
                    house.incomeByTaxBand[i] += bracket
                    house.incomeByTaxBand[-1] -= bracket
                    incomes[incomes.index(income)] -= bracket
        
        ############  Check Variable  ############################
        if self.year == self.p['getCheckVariablesAtYear']:
            self.perCapitaHouseholdIncome.append(incomePerCapita)
        ##########################################################
        
        incomeForCareShare_D0 = 1.0 - 1/math.exp(self.p['incomeCareParam']*incomePerCapita)
        incomeForCareShare_D1 = (1.0 - 1/math.exp(self.p['incomeCareParam']*incomePerCapita))*self.p['formalCareDiscountFactor']
        residualIncomeForCare_D0 = income*incomeForCareShare_D0
        residualIncomeForCare_D1 = income*incomeForCareShare_D1
        house.residualIncomeForCare = [residualIncomeForCare_D0, residualIncomeForCare_D1, 0, 0]
        
    def computeNetworkSupply(self, house):
        # Compute households' supplies and total network supply
        town = house.town
        house.suppliers = [house]
        house.suppliers.extend(list(house.careNetwork.neighbors(house)))
        for supplier in house.suppliers:
            
            householdCarers = [x for x in list(supplier.occupants) if x.hoursDemand == 0 and x.status != 'maternity']
            supplier.householdInformalSupply = []
            for i in range(4):
                supplier.householdInformalSupply.append(sum([x.residualInformalSupplies[i] for x in householdCarers]))
                
            distance = 0
            if supplier != house:
                distance = house.careNetwork[house][supplier]['distance']
            # Compute total supply fo supplier (informal + formal). The formal is a weighted average of social and childcare formal supply, 
            # where the weight is the relative weight of child and social care need in the receiving household.
            relativeChildCare = 0
            if house.totalChildCareNeed+house.totalSocialCareNeed > 0:
                relativeChildCare = house.totalChildCareNeed/(house.totalChildCareNeed+house.totalSocialCareNeed)
            
            suppliesSocialCare = self.updateFormalSocialCareSupplies(supplier)
            supplier.householdFormalSocialCareSupply = suppliesSocialCare
            suppliesChildCare = self.updateFormalChildCareSupplies(supplier, house)
            supplier.householdFormalChildCareSupply = suppliesChildCare
            
            formalSupply = suppliesChildCare[distance]*relativeChildCare + suppliesSocialCare[distance]*(1.0-relativeChildCare)
            formalSupply = int((formalSupply+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
            
            informalSupply = 0
            if supplier.town == town:
                informalSupply = supplier.householdInformalSupply[distance]
            house.networkInformalSupply.append(informalSupply)
            
            supply = formalSupply + informalSupply
            
            house.networkTotalSupplies.append(supply)
            
            house.networkSupply += supply
    
    def residualInformalCareSupplies(self, house, town, distance):
        supply = 0
        if house.town == town:
            supply = house.householdInformalSupply[distance]
        return(supply)
    
    def residualCareSupplies(self, house, town, distance, weightedCarePrice):
        residualIncome = house.residualIncomeForCare[distance]
        residualHoursOfFormalCare = residualIncome/weightedCarePrice
        residualHoursOfFormalCare = int((hoursOfFormalCare+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
        totsupply = 0
        if distance == 0 or distance == 1:
            totsupply += residualHoursOfFormalCare
        if house.town == town:
            totsupply += house.householdInformalSupply[distance]
        return(totsupply)
        
    def transferCare(self, receiver, supplier):
        # Transfer quantim of care: decide who trasfers which kind of care (informal or formal) to whom
        distance = 0
        if receiver != supplier:
            distance = receiver.careNetwork[receiver][supplier]['distance']
        # Select kind of care based on supplier availability
        kindsOfCare = ['informal care', 'formal care']
        care = 'formal care'
        if supplier.town == receiver.town:
            formalCareSupply = supplier.householdFormalChildCareSupply[distance]*receiver.childCareNeedShare
            formalCareSupply += supplier.householdFormalSocialCareSupply[distance]*(1.0-receiver.socialCareNeedShare)
            careSupplies = [supplier.householdInformalSupply[distance], formalCareSupply]
            careProbs = [x/sum(careSupplies) for x in careSupplies]
            care = np.random.choice(kindsOfCare, p = careProbs) 
        
        # If 'informal care' is selected: informal care provider are sorted in decreasing order.
        # Their supply is used to satisfy the most expensive care need.
        if care == 'informal care':
            householdCarers = [x for x in list(supplier.occupants) if x.residualInformalSupplies[distance] > 0 and x.status != 'maternity']
            for member in householdCarers:
                member.residualInformalSupply = residualInformalSupplies[distance]
            householdCarers.sort(key=operator.attrgetter("residualInformalSupply"), reverse=True)
            
            # Single supplier
#            carer = householdCarers[0]
#            for i in range(4):
#                i.residualInformalSupplies[i] -= self.p['quantumCare']
#                i.residualInformalSupplies[i] = max(i.residualInformalSupplies[i], 0)
                
            # Assuming that the quantum care is transferred, this may involve more than a supplier (if none of them has enough supply left)
            residualCare = self.p['quantumCare']
            for i in householdCarers:
                careForNeed = min(i.residualInformalSupply, residualCare)
                if careForNeed > 0:
                    for i in range(4):
                        i.residualInformalSupplies[i] -= careForNeed
                        i.residualInformalSupplies[i] = max(i.residualInformalSupplies[i], 0)
                    residualCare -= careForNeed
                    if residualCare <= 0:
                        break
                    
            # The 'quantum' of care is transferred to the most expensive care need: compute cost of care need.
            residualCare = self.p['quantumCare']
            costChild = 0
            for i in house.childCareNeeds:
                care = min(i, residualCare)
                if care > 0:
                    costChild += care*house.childCarePrices[i]
                residualCare -= care
                if residualCare <= 0:
                        break
            priceChild = costChild/self.p['quantumCare']
            
            costSocial = self.socialCareCost(supplier)
            priceSocial = costSocial/self.p['quantumCare']
            
            if costChild > costSocial and receiver.totalChildCareNeed > 0:
                # Transfer quantum to childcare.
                carer.childWork += self.p['quantumCare']
                children = [x for x in list(receiver.occupants) if x.age > 0 and x.age < self.p['ageTeenagers']]
                
                residualCare = self.p['quantumCare']
                for child in children:
                    child.residualChildCareNeed -= self.p['quantumCare']
                    if child.residualChildCareNeed >= 0:
                        child.informalChildCareReceived += self.p['quantumCare']
                    child.residualChildCareNeed = max(child.residualChildCareNeed, 0)
                receiver.totalChildCareNeed = sum([x.residualChildCareNeed for x in children])
                receiver.informalChildCareReceived += self.p['quantumCare']
                self.updateChildCareNeeds(receiver)
            else:
                # Transfer quantum to social care.
                carer.socialWork += self.p['quantumCare']
                socialCareReceivers = [x for x in list(receiver.occupants) if x.hoursDemand > 0]
                socialCareReceivers.sort(key=operator.attrgetter("residualNeed"), reverse=True)
                residualCare = self.p['quantumCare']
                for person in socialCareReceivers:
                    careForPerson = min(person.residualNeed, residualCare)
                    if careForPerson > 0:
                        person.informalSocialCareReceived += careForPerson
                        person.residualNeed -= careForPerson
                        person.residualNeed = max(receivingMember.residualNeed, 0)
                    residualCare -= careForPerson
                    if residualCare <= 0:
                        break
                receiver.totalSocialCareNeed = sum([x.residualNeed for x in socialCareReceivers])
                receiver.informalSocialCareReceived += self.p['quantumCare']
        else: # Select formal vs informal out-of-income care
            if supplier.town != receiver.town: 
                # Only formal care is possible: use it to satisfy the  cheapest care need.
                children = [x for x in list(receiver.occupants) if x.age > 0 and x.age < self.p['ageTeenagers'] and x.residualChildCareNeed > 0]
                socialCareReceivers = [x for x in list(receiver.occupants) if x.residualNeed > 0]
                # childrenCares = sorted([x.formalChildCareReceived for x in children])
                costChild = self.childCareCost(children)
                priceChild = costChild/self.p['quantumCare']
                # price of social care depends on supplier's income brackets.
                costSocial = self.socialCareCost(supplier)
                priceSocial = costSocial/self.p['quantumCare']
                # 2) Check prices and reduce the higher-price need
                if costChild < costSocial and receiver.totalChildCareNeed > 0:
                    # reduce income for care and provide childcare to child with the lowest formal childcare
                    supplier.residualIncomeForCare -= costChild
                    supplier.residualIncomeForCare = max(receiver.residualIncomeForCare, 0)
                    supplier.householdFormalSupplyCost += costChild
                    formalChildCares = [x.formalChildCareReceived for x in children if x.formalChildCareReceived < self.p['childcareTaxFreeCap']]
                    if len(formalChildCares) > 0:
                        children.sort(key=operator.attrgetter("formalChildCareReceived"))
                    else:
                        children.sort(key=operator.attrgetter("residualChildCareNeed"), reverse = True)
                    residualCare = self.p['quantumCare']
                    for child in children:
                        careForChild = min(child.residualChildCareNeed, residualCare)
                        if careForChild > 0:
                            child.formalChildCareReceived += careForChild
                            child.residualChildCareNeed -= careForChild
                        residualCare -= careForChild
                        if residualCare <= 0:
                            break
                    receiver.totalChildCareNeed = sum([x.residualChildCareNeed for x in children])
                    receiver.formalChildCareReceived += self.p['quantumCare']  
                    self.updateChildCareNeeds(receiver)
                else:
                    # reduce income for care and provide social care to person with highest residual need.
                    supplier.residualIncomeForCare -= costSocial
                    supplier.residualIncomeForCare = max(receiver.residualIncomeForCare, 0)
                    supplier.householdFormalSupplyCost += costSocial
                    socialCareReceivers.sort(key=operator.attrgetter("residualNeed"), reverse=True)
                    residualCare = self.p['quantumCare']
                    for person in socialCareReceivers:
                        careForPerson = min(person.residualNeed, residualCare)
                        if careForPerson > 0:
                            person.formalSocialCareReceived += careForPerson
                            person.residualNeed -= careForPerson
                        residualCare -= careForPerson
                        if residualCare <= 0:
                            break
                    receiver.totalSocialCareNeed = sum([x.residualNeed for x in socialCareReceivers])
                    receiver.formalSocialCareReceived += self.p['quantumCare']
            
            else: 
                # Both are possible: choice depends on price of most expensive care and lowest wage.
                employed = [x for x in householdCarers if x.status == 'employed' and x.residualWorkingHours > 0]
                employed.sort(key=operator.attrgetter("wage"))
                carer = employed[0]
                children = [x for x in list(receiver.occupants) if x.age > 0 and x.age < self.p['ageTeenagers'] and x.residualChildCareNeed > 0]
                socialCareReceivers = [x for x in list(receiver.occupants) if x.residualNeed > 0]
                # Find the highest price and the lowest price, among all kinds of care
                residualCare = self.p['quantumCare']
                costChild_I = 0
                for i in house.childCareNeeds:
                    care = min(i, residualCare)
                    if care > 0:
                        costChild_I += care*house.childCarePrices[i]
                    residualCare -= care
                    if residualCare <= 0:
                        break
                priceInformalChildcare = costChild_I/self.p['quantumCare']
                
                costChild_F = self.childCareCost(children)
                priceFormalChildcare = costChild_F/self.p['quantumCare']
                
                costSocial = self.socialCareCost(supplier)
                priceSocial = costSocial/self.p['quantumCare']
                
                maxPrice = max(priceInformalChildcare, priceSocial)
                minPrice = max(priceFormalChildcare, priceSocial)
                
                if carer.wage > maxPrice: # In this case pay formal care for the kind of care associated to minPrice
                    if minPrice == priceFormalChildcare and receiver.totalChildCareNeed > 0: # Formal care for childcare
                        supplier.residualIncomeForCare -= costChild_F
                        supplier.residualIncomeForCare = max(receiver.residualIncomeForCare, 0)
                        supplier.householdFormalSupplyCost += costChild_F
                        formalChildCares = [x.formalChildCareReceived for x in children if x.formalChildCareReceived < self.p['childcareTaxFreeCap']]
                        if len(formalChildCares) > 0:
                            children.sort(key=operator.attrgetter("formalChildCareReceived"))
                        else:
                            children.sort(key=operator.attrgetter("residualChildCareNeed"), reverse = True)
                        residualCare = self.p['quantumCare']
                        for child in children:
                            careForChild = min(child.residualChildCareNeed, residualCare)
                            child.formalChildCareReceived += careForChild
                            if careForChild > 0:
                                child.residualChildCareNeed -= careForChild
                                residualCare -= careForChild
                            if residualCare <= 0:
                                break
                        receiver.totalChildCareNeed = sum([x.residualChildCareNeed for x in children])
                        receiver.formalChildCareReceived += self.p['quantumCare']  
                        self.updateChildCareNeeds(receiver)
                    else: # Formal care for social care
                        supplier.residualIncomeForCare -= costSocial
                        supplier.residualIncomeForCare = max(receiver.residualIncomeForCare, 0)
                        supplier.householdFormalSupplyCost += costSocial
                        socialCareReceivers.sort(key=operator.attrgetter("residualNeed"), reverse=True)
                        residualCare = self.p['quantumCare']
                        for person in socialCareReceivers:
                            careForPerson = min(person.residualNeed, residualCare)
                            person.formalSocialCareReceived += careForPerson
                            if careForPerson > 0:
                                person.residualNeed -= careForPerson
                                residualCare -= careForPerson
                            if residualCare <= 0:
                                break
                        receiver.totalSocialCareNeed = sum([x.residualNeed for x in socialCareReceivers])
                        receiver.formalSocialCareReceived += self.p['quantumCare']
                elif supplier.wage < minPrice: # In this case supply informal care to care need associated to maxPrice
                    carer.residualWorkingHours -= self.p['quantumCare']
                    if maxPrice == priceInformalChildcare and receiver.totalChildCareNeed > 0: # Supply informal care for childcare
                        carer.childWork += self.p['quantumCare']
                        children = [x for x in list(receiver.occupants) if x.age > 0 and x.age < self.p['ageTeenagers']]
                        residualCare = self.p['quantumCare']
                        for child in children:
                            child.residualChildCareNeed -= self.p['quantumCare']
                            if child.residualChildCareNeed >= 0:
                                child.informalChildCareReceived += self.p['quantumCare']
                            child.residualChildCareNeed = max(child.residualChildCareNeed, 0)
                        receiver.totalChildCareNeed = sum([x.residualChildCareNeed for x in children])
                        receiver.informalChildCareReceived += self.p['quantumCare']
                        self.updateChildCareNeeds(receiver)
                    else: # Supply informal care to social care
                        carer.socialWork += self.p['quantumCare']
                        socialCareReceivers = [x for x in list(receiver.occupants) if x.hoursDemand > 0]
                        residualCare = self.p['quantumCare']
                        for person in socialCareReceivers:
                            careForPerson = min(person.residualNeed, residualCare)
                            if careForPerson > 0:
                                person.informalSocialCareReceived += careForPerson
                                person.residualNeed -= careForPerson
                                person.residualNeed = max(receivingMember.residualNeed, 0)
                            residualCare -= careForPerson
                            if residualCare <= 0:
                                break
                        receiver.totalSocialCareNeed = sum([x.residualNeed for x in socialCareReceivers])
                        receiver.informalSocialCareReceived += self.p['quantumCare']
                else: # Compare the differences between wage and prices
                    d1 = carer.wage - minPrice
                    d2 = maxPrice - carer.wage
                    if d1 > d2: # Wage closer to maxPrice: more convenient to pay for formal care (for care need associated to min price)
                        if minPrice == priceFormalChildcare and receiver.totalChildCareNeed > 0: # Formal care for childcare
                            supplier.residualIncomeForCare -= costChild_F
                            supplier.residualIncomeForCare = max(receiver.residualIncomeForCare, 0)
                            supplier.householdFormalSupplyCost += costChild
                            formalChildCares = [x.formalChildCareReceived for x in children if x.formalChildCareReceived < self.p['childcareTaxFreeCap']]
                            if len(formalChildCares) > 0:
                                children.sort(key=operator.attrgetter("formalChildCareReceived"))
                            else:
                                children.sort(key=operator.attrgetter("residualChildCareNeed"), reverse = True)
                            residualCare = self.p['quantumCare']
                            for child in children:
                                careForChild = min(child.residualChildCareNeed, residualCare)
                                child.formalChildCareReceived += careForChild
                                if careForChild > 0:
                                    child.residualChildCareNeed -= careForChild
                                    residualCare -= careForChild
                                if residualCare <= 0:
                                    break
                            receiver.totalChildCareNeed = sum([x.residualChildCareNeed for x in children])
                            receiver.formalChildCareReceived += self.p['quantumCare']  
                            self.updateChildCareNeeds(receiver)
                        else: # Formal care for social care
                            supplier.residualIncomeForCare -= costSocial
                            supplier.residualIncomeForCare = max(receiver.residualIncomeForCare, 0)
                            supplier.householdFormalSupplyCost += costSocial
                            socialCareReceivers.sort(key=operator.attrgetter("residualNeed"), reverse=True)
                            residualCare = self.p['quantumCare']
                            for person in socialCareReceivers:
                                careForPerson = min(person.residualNeed, residualCare)
                                person.formalSocialCareReceived += careForPerson
                                if careForPerson > 0:
                                    person.residualNeed -= careForPerson
                                    residualCare -= careForPerson
                                if residualCare <= 0:
                                    break
                            receiver.totalSocialCareNeed = sum([x.residualNeed for x in socialCareReceivers])
                            receiver.formalSocialCareReceived += self.p['quantumCare']
                        
                    else: # Wage closer to minPrice: more convenient to supply informal care (to care need associated to max price)
                        carer.residualWorkingHours -= self.p['quantumCare']
                        if maxPrice == priceInformalChildcare and receiver.totalChildCareNeed > 0: # Supply informal care for childcare
                            carer.childWork += self.p['quantumCare']
                            children = [x for x in list(receiver.occupants) if x.age > 0 and x.age < self.p['ageTeenagers']]
                            residualCare = self.p['quantumCare']
                            for child in children:
                                child.residualChildCareNeed -= self.p['quantumCare']
                                if child.residualChildCareNeed >= 0:
                                    child.informalChildCareReceived += self.p['quantumCare']
                                child.residualChildCareNeed = max(child.residualChildCareNeed, 0)
                            receiver.totalChildCareNeed = sum([x.residualChildCareNeed for x in children])
                            receiver.informalChildCareReceived += self.p['quantumCare']
                            self.updateChildCareNeeds(receiver)
                        else: # Supply informal care to social care
                            carer.socialWork += self.p['quantumCare']
                            socialCareReceivers = [x for x in list(receiver.occupants) if x.hoursDemand > 0]
                            residualCare = self.p['quantumCare']
                            for person in socialCareReceivers:
                                careForPerson = min(person.residualNeed, residualCare)
                                if careForPerson > 0:
                                    person.informalSocialCareReceived += careForPerson
                                    person.residualNeed -= careForPerson
                                    person.residualNeed = max(receivingMember.residualNeed, 0)
                                residualCare -= careForPerson
                                if residualCare <= 0:
                                    break
                            receiver.totalSocialCareNeed = sum([x.residualNeed for x in socialCareReceivers])
                            receiver.informalSocialCareReceived += self.p['quantumCare']
                    
    def updateChildCareNeeds(self, house):
        children = [x for x in list(house.occupants) if x.age > 0 and x.age < self.p['ageTeenagers']]
        children.sort(key=operator.attrgetter("residualChildCareNeed"))
        residualNeeds = [x.residualChildCareNeed for x in children]
        marginalNeeds = []
        numbers = []
        toSubtract = 0
        for need in residualNeeds:
            marginalNeed = need-toSubtract
            marginalNeed = max(marginalNeed, 0)
            if marginalNeed > 0:
                marginalNeeds.append(marginalNeed)
                num = len([x for x in residualNeeds if x >= need])
                numbers.append(num)                
                toSubtract = need
        house.childCareNeeds = marginalNeeds
        
        prices = []
        residualCare = 0
        cumulatedCare = 0
        for i in range(len(numbers)):
            cost = 0
            residualCare = house.childCareNeeds[i]
            for child in children[-numbers[i]:]:
                if cumulatedCare + residualCare + child.formalChildCareReceived <= self.p['childcareTaxFreeCap']:
                    cost += p['priceChildCare']*(1-p['childCareTaxFreeRate'])*residualCare
                else:
                    if child.formalChildCareReceived + cumulatedCare >= self.p['childcareTaxFreeCap']:
                        cost += p['priceChildCare']*residualCare
                    else:
                        discountedCare = self.p['childcareTaxFreeCap'] - (child.formalChildCareReceived + cumulatedCare)
                        cost1 = discountedCare*p['priceChildCare']*(1-p['childCareTaxFreeRate'])
                        fullPriceCare = residualCare - discountedCare
                        cost2 = fullPriceCare*p['priceChildCare']
                        cost += (cost1 + cost2)
            cumulatedCare += house.childCareNeeds[i]
            prices.append(cost/house.childCareNeeds[i])
        house.childCarePrices = prices
    
    def childCareCost(self, children):
        children.sort(key=operator.attrgetter("formalChildCareReceived"))
        cost = 0
        residualCare = self.p['quantumCare']
        for child in children:
            careForChild = min(child.residualChildCareNeed, residualCare)
            if careForChild + child.formalChildCareReceived <= self.p['childcareTaxFreeCap']:
                cost += p['priceChildCare']*(1-p['childCareTaxFreeRate'])*careForChild
            else:
                if child.formalChildCareReceived >= self.p['childcareTaxFreeCap']:
                    cost += p['priceChildCare']*careForChild
                else:
                    discountedCare = self.p['childcareTaxFreeCap']-child.formalChildCareReceived
                    cost1 = discountedCare*p['priceChildCare']*(1-p['childCareTaxFreeRate'])
                    fullPriceCare = careForChild - discountedCare
                    cost2 = fullPriceCare*p['priceChildCare']
                    cost += (cost1 + cost2)
            residualCare -= careForChild
            if residualCare <= 0:
                break
        return cost
    
    def socialCareCost(self, house):
        availableIncomeByTaxBand = self.updateIncomeByTaxBand(house)
        prices = [p['priceSocialCare']*(1.0-x*self.p['taxBreakRate']) for x in self.p['bandsTaxationRates']]
        cost = 0
        residualCare = self.p['quantumCare']
        for i in range(len(availableIncomeByTaxBand)):
            # house.incomeByTaxBand[i] needs to be updated at every transfer of formal care, net of time off work and total formal care cost
            if availableIncomeByTaxBand[i]/prices[i] > residualCare:
                cost += self.p['quantumCare']*prices[i]
                availableIncomeByTaxBand[i] -= cost
                break
            else:
                cost += availableIncomeByTaxBand[i]
                residualCare -= availableIncomeByTaxBand[i]/prices[i]
                availableIncomeByTaxBand[i] = 0
        return cost
    
    def updateIncomeByTaxBand(self, house):
        for member in household:
            member.netIncome = member.wage*member.residualWorkingHours
        incomes = [x.netIncome for x in household]
        house.incomeByTaxBand = [0]*self.p['taxBandsNumber']
        house.incomeByTaxBand[-1] = sum(incomes)
        for i in range(int(self.p['taxBandsNumber'])-1):
            for income in incomes:
                if income > self.p['taxBrackets'][i]:
                    bracket = income-self.p['taxBrackets'][i]
                    house.incomeByTaxBand[i] += bracket
                    house.incomeByTaxBand[-1] -= bracket
                    incomes[incomes.index(income)] -= bracket
        # Available income by tax band
        house.availableIncomeByTaxBand = house.incomeByTaxBand
        careExpense = house.householdFormalSupplyCost
        for i in range(len(house.availableIncomeByTaxBand)):
            if house.availableIncomeByTaxBand[i] > careExpense:
                house.availableIncomeByTaxBand[i] -= careExpense
                careExpense = 0
                break
            else:
                careExpense -= house.availableIncomeByTaxBand[i]
                house.availableIncomeByTaxBand[i] = 0
        return house.availableIncomeByTaxBand
    
    def updateFormalSocialCareSupplies(self, house):
        availableIncomeByTaxBand = list(self.updateIncomeByTaxBand(house))
        residualIncomeForCare = list(house.residualIncomeForCare)
        # How much social care can the household buy with the residual income for care?
        prices = [p['priceSocialCare']*(1.0-x*self.p['taxBreakRate']) for x in self.p['bandsTaxationRates']]
        socialCareSupplies = []
        for residualIncome in residualIncomeForCare:
            incomeByTaxBand = availableIncomeByTaxBand
            totalHours = 0
            for i in range(len(incomeByTaxBand)):
                if residualIncome > incomeByTaxBand[i]:
                    totalHours += incomeByTaxBand[i]/prices[i]
                    incomeByTaxBand[i] = 0
                    residualIncome -= incomeByTaxBand[i]
                else:
                    totalHours += residualIncome/prices[i]
                    break
            socialCareSupplies.append(totalHours)
        socialCareSupplies = [int((x+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare'] for x in socialCareSupplies]
        return socialCareSupplies
    
    def updateFormalChildCareSupplies(self, supplier, receiver):
        residualIncomeForCare = list(house.residualIncomeForCare)
        children = [x for x in list(receiver.occupants) if x.age > 0 and x.age < self.p['ageTeenagers']]
        formalChilCareReceived = [x.formalChildCareReceived for x in children]
        discountedNeed = [max(self.p['childcareTaxFreeCap']-x, 0) for x in formalChilCareReceived]
        discountedCost = sum(discountedNeed)*self.p['priceChildCare']*(1.0-self.p['childCareTaxFreeRate'])
        childCareSupplies = []
        for residualIncome in residualIncomeForCare:
            totHours = 0
            if residualIncome > discountedCost:
                totHours = sum(discountedNeed)
                residualIncome -= discountedCost
                totHours += residualIncome/self.p['priceChildCare']
            else:
                totHours = residualIncome/self.p['priceChildCare']*(1.0-self.p['childCareTaxFreeRate'])
            totHours = int((totHours+self.p['quantumCare']/2)/self.p['quantumCare'])*self.p['quantumCare']
        childCareSupplies.append(totHours)
        return childCareSupplies
        
    def allocateCare(self):
        
        for house in self.map.occupiedHouses:
            self.resetVariables(house)
            self.householdCareNetwork(house)
            self.updateFinancialWealth(house)
            self.computeSocialCareNeeds(house)
            self.computeChildCareNeeds(house)
            self.updateCareNeedIndex(house)
            self.computeCareSupplies(house)
        
        residualReceivers = [x for x in self.map.occupiedHouses if x.careNeedIndex > 0]
        for receiver in residualReceivers:
            self.computeNetworkSupply(receiver)
        residualReceivers = [x for x in residualReceivers if x.networkSupply > 0]
        
        while len(residualReceivers) > 0:
            # Select a receiving household based on total need (childcare plus social care)
            careIndexes = [x.careNeedIndex for x in residualReceivers]
            probReceivers = [i/sum(careIndexes) for i in careIndexes]
            receiver = np.random.choice(residualReceivers, p = probReceivers)
            supplies = [x for x in receiver.networkTotalSupplies]
            probSuppliers = [i/sum(supplies) for i in supplies]
            carer = np.random.choice(receiver.suppliers, p = probSuppliers)
            self.transferCare(receiver, supplier) # Update individual and household care needs and care need index
            self.updateCareNeedIndex(receiver)
            residualReceivers = [x for x in self.map.occupiedHouses if x.careNeedIndex > 0]
            for receiver in residualReceivers:
                self.computeNetworkSupply(receiver)
            residualReceivers = [x for x in residualReceivers if x.networkSupply > 0]
            
#        # The care need is satisfied by the household's informal care supply, starting from the social care need if present.
#        # First, select all the agents with care need in the population.
#        networkGroup = [x for x in self.pop.livingPeople if x.residualNetNeed > 0 or x.age >= self.p['socialCareBankingAge']]
#        careReceivers = [x for x in networkGroup if x.residualNetNeed > 0]
#        for member in networkGroup:
#            self.careNetwork(member, networkGroup.index(member))
#            # receiver.networkSupplies = []
#            # The total supply of informal care for the agent's kinship network is computed.
#            # It includes all the informal care supply except the time-off-work infromal care supply (which is parte of the income-funded social care supply).
#        for receiver in careReceivers:
#            receiver.totalSupply = self.totalSupply(receiver)
#            #receiver.totalInformalSupply = self.totalInformalSupply(receiver)
#            
#        residualReceivers = [x for x in self.pop.livingPeople if x.residualNetNeed > 0 and x.totalSupply > 0]
#        while len(residualReceivers) > 0:
#            
#            totalResidualNeed_init = sum([x.residualNetNeed for x in residualReceivers])
#            
#            careList = [x.residualNetNeed for x in residualReceivers]
#            probReceivers = [i/sum(careList) for i in careList]
#            receiver = np.random.choice(residualReceivers, p = probReceivers)
#            
#            self.getCare(receiver)
#            
#            careReceivers = [x for x in self.pop.livingPeople if x.residualNetNeed > 0]
#            for receiver in careReceivers:
#                receiver.totalSupply = self.totalSupply(receiver)
#            residualReceivers = [x for x in careReceivers if x.totalSupply > 0]
#            
#            # Check process
#            totalResidualNeed_end = sum([x.residualNetNeed for x in residualReceivers])
#            if totalResidualNeed_init == totalResidualNeed_end:
#                print('Error: final and initial need is equal')
        
        careReceivers = [x for x in self.pop.livingPeople if x.careNeedLevel > 0]
        for receiver in careReceivers:
            receiver.cumulativeUnmetNeed *= self.p['unmetCareNeedDiscountParam']
            receiver.cumulativeUnmetNeed += receiver.residualNeed
            receiver.totalDiscountedShareUnmetNeed *= self.p['shareUnmetNeedDiscountParam']
            receiver.totalDiscountedTime *= self.p['shareUnmetNeedDiscountParam']
            receiver.totalDiscountedShareUnmetNeed += receiver.residualNeed/receiver.hoursDemand
            receiver.totalDiscountedTime += 1
            receiver.averageShareUnmetNeed = receiver.totalDiscountedShareUnmetNeed/receiver.totalDiscountedTime
            # receiver.numSuppliers = receiver.supplyNetwork.degree(receiver)
            
            if self.year == self.p['getCheckVariablesAtYear']:
                self.numberSuppliers.append(receiver.numSuppliers)
    
    def careNetwork(self, pin, index):
        
        households = []
        for member in pin.house.occupants:
            if member.hoursDemand == 0 and member.house not in households:
                pin.careNetwork.add_edge(pin, member, distance = 0)      
                households.append(member.house)
                break
        
        # Parents
        if pin.father != None:
            if pin.father.dead == False and pin.father.house not in households:
                pin.careNetwork.add_edge(pin, pin.father, distance = 1) 
                households.append(pin.father.house)
            if pin.mother.dead == False and pin.mother.house not in households:
                pin.careNetwork.add_edge(pin, pin.mother, distance = 1)
                households.append(pin.mother.house)
        # Grandparents
        if pin.father != None and pin.father.father != None:
            if pin.father.father.dead == False and pin.father.father.house not in households and pin.father.father.house.town == pin.house.town:
                pin.careNetwork.add_edge(pin, pin.father.father, distance = 2)
                households.append(pin.father.father.house)
            if pin.father.mother.dead == False and pin.father.mother.house not in households and pin.father.mother.house.town == pin.house.town:
                pin.careNetwork.add_edge(pin, pin.father.mother, distance = 2)
                households.append(pin.father.mother.house)
        if pin.father != None and pin.mother.father != None:
            if pin.mother.father.dead == False and pin.mother.father.house not in households and pin.mother.father.house.town == pin.house.town:
                pin.careNetwork.add_edge(pin, pin.mother.father, distance = 2)
                households.append(pin.mother.father.house)
            if pin.mother.mother.dead == False and pin.mother.mother.house not in households and pin.mother.mother.house.town == pin.house.town:
                pin.careNetwork.add_edge(pin, pin.mother.mother, distance = 2)
                households.append(pin.mother.mother.house)
        # Indipendent children
        for child in pin.children:
            if child.dead == False and child.house not in households:
                pin.careNetwork.add_edge(pin, child, distance = 1)
                households.append(child.house)
        # Independent grandchildren
        for child in pin.children:
            for grandson in child.children:
                if grandson.dead == False and grandson.house not in households and grandson.house.town == pin.house.town:
                    pin.careNetwork.add_edge(pin, grandson, distance = 2)
                    households.append(grandson.house)
         # Indipendent brothers and sisters
        if pin.father != None:
            brothers = list(set(pin.father.children+pin.mother.children))
            brothers = [x for x in brothers if x.dead == False]
            brothers.remove(pin)
            for brother in brothers:
                if brother.dead == False and brother.house not in households and brother.house.town == pin.house.town:
                    pin.careNetwork.add_edge(pin, brother, distance = 2)
                    households.append(brother.house)
                for child in brother.children:
                    if child.dead == False and child.house not in households and child.house.town == pin.house.town:
                        pin.careNetwork.add_edge(pin, child, distance = 3)
                        households.append(child.house)
        # Uncles and aunts
        uncles = []
        maternalUncles = []
        paternalUncles = []
        if pin.father != None and pin.father.father != None:
            paternalUncles = list(set(pin.father.father.children + pin.father.mother.children))
            paternalUncles.remove(pin.father)
        if pin.father != None and pin.mother.father != None:   
            maternalUncles = list(set(pin.mother.father.children + pin.mother.mother.children))
            maternalUncles.remove(pin.mother)
        unclesList = list(set(maternalUncles+paternalUncles))
        unclesList = [x for x in unclesList if x.dead == False]
        for uncle in unclesList:
            if uncle.dead == False and uncle.house not in households and uncle.house.town == pin.house.town:
                pin.careNetwork.add_edge(pin, uncle, distance = 3)
                households.append(uncle.house)
                
    def totalSupply(self, receiver):
        totsupply = 0
        townReceiver = receiver.house.town
        for carer in receiver.careNetwork.neighbors(receiver):
            distance = receiver.careNetwork[receiver][carer]['distance']
            townCarer = carer.house.town
            household = [x for x in carer.house.occupants]
            formalSupplyHours = household[0].residualFormalSupply[distance]
            householdCarers = [x for x in household if x.hoursDemand == 0 and x.status != 'maternity']
            notWorking = [x for x in householdCarers if x.status == 'teenager' or x.status == 'retired' or x.status == 'student']
            employed = [x for x in householdCarers if x.status == 'employed']
            if distance == 0 or distance == 1:
                totsupply += formalSupplyHours
            if townCarer == townReceiver:
                for member in notWorking:
                    totsupply += member.residualInformalSupply[distance]
                for member in employed:
                    totsupply += member.extraworkCare[distance]
        return(totsupply)
        
    def getCare(self, receiver):
        receiver.residualNeed -= self.p['quantumCare'] 
        receiver.residualNetNeed -= self.p['quantumCare']
        townReceiver = receiver.house.town 
        informalCare = 0
        formalCare = 0

        probCarers = self.probSuppliers(receiver)
        suppliers = [x for x in receiver.careNetwork.neighbors(receiver)]
        carer = np.random.choice(suppliers, p = probCarers)
        
        d = receiver.careNetwork[receiver][carer]['distance']
        if receiver.supplyNetwork.has_edge(receiver, carer) == False:
            receiver.supplyNetwork.add_edge(receiver, carer, weight = 0, distance = d)
        totalCare = receiver.supplyNetwork[receiver][carer]['weight'] + self.p['quantumCare']
        receiver.supplyNetwork[receiver][carer]['weight'] = totalCare
        
        distance = receiver.careNetwork[receiver][carer]['distance']
        
        townCarer = carer.house.town
        household = carer.house.occupants

        residualIncomeForCare = household[0].residualIncomeCare
        residualFormalSupplyHours = household[0].residualFormalSupply[distance]
        
        householdCarers = [x for x in household if x.hoursDemand == 0 and x.status != 'maternity']
        notWorking = [x for x in householdCarers if x.residualInformalSupply > 0]
        
        householdsGroups = []
        groupsAvailability = []
        
        for member in notWorking:
            member.maxInformalSupply = member.residualInformalSupply[0]
        
        teenagers = [x for x in notWorking if x.status == 'teenager']
        teenagers.sort(key=operator.attrgetter("maxInformalSupply"), reverse=True)
        householdsGroups.append(teenagers)
        totTeenagersSupply = sum([x.residualInformalSupply[distance] for x in teenagers])
        groupsAvailability.append(totTeenagersSupply)

        retired = [x for x in notWorking if x.status == 'retired']
        retired.sort(key=operator.attrgetter("maxInformalSupply"), reverse=True)
        householdsGroups.append(retired)
        totRetiredSupply = sum([x.residualInformalSupply[distance] for x in retired])
        groupsAvailability.append(totRetiredSupply)
        
        students = [x for x in notWorking if x.status == 'student']
        students.sort(key=operator.attrgetter("maxInformalSupply"), reverse=True)
        householdsGroups.append(students)
        totStudentsSupply = sum([x.residualInformalSupply[distance] for x in students])
        groupsAvailability.append(totStudentsSupply)

        employed = [x for x in householdCarers if x.status == 'employed']
        for member in employed:
            member.maxInformalSupply = member.extraworkCare[0]
        employed.sort(key=operator.attrgetter("maxInformalSupply"), reverse=True)
        householdsGroups.append(employed)
        extraWorkSupply = sum([x.extraworkCare[distance] for x in employed])
        groupsAvailability.append(extraWorkSupply)
        
        householdsGroups.append('Out-of-Income Supply')
        incomeForCare = 0
        if len(household) > 0:
            incomeForCare = household[0].residualIncomeCare
            incomeByTaxBand = list(household[0].incomeByTaxBands)

        groupsAvailability.append(residualFormalSupplyHours)
        groupsProbabilities = [x/sum(groupsAvailability) for x in groupsAvailability]
        
        earningMembers = [x for x in household if x.income > 0]
        if len(earningMembers) == 0 and residualFormalSupplyHours > 0:
            print('Error: no income to pay social care from (Get Care)')
            
        # Finally, extract a 'quantum' of care from one of the selected household's members.
        supplier = 'none'
        if distance == 0 or distance == 1:
            if townCarer == townReceiver:
                carers = np.random.choice(householdsGroups, p = groupsProbabilities) 
                if carers == 'Out-of-Income Supply':
                    residualFormalSupplyHours -= self.p['quantumCare']
                    if residualFormalSupplyHours < 0:
                        residualFormalSupplyHours = 0
                    availableWorkers = [x for x in household if x.residualWorkingHours > 0]
                    if len(availableWorkers) > 0:
                        # Price of formal care and cost of informal care are compared to decide whether the former or the latter will be supplied.
                        # Cost of informal care: the wage of the worker with the lowest wage (if any)
                        availableWorkers.sort(key=operator.attrgetter("wage"))
                        costInformalCare = availableWorkers[0].wage
                        # Compute price of formal care
                        totalFormalCareCost = self.p['priceSocialCare']*self.p['quantumCare']
                        deductibleCost = totalFormalCareCost*self.p['taxBreakRate']
                        notDeductibleCost = totalFormalCareCost - deductibleCost
                        residualCost = deductibleCost
                        careBrackets = []
                        for i in range(int(self.p['taxBandsNumber'])):
                            careBrackets.append([])
                            careBrackets[i] = 0
                        for i in range(int(self.p['taxBandsNumber'])):
                            if residualCost > incomeByTaxBand[i]:
                                careBrackets[i] += incomeByTaxBand[i]
                                residualCost -= incomeByTaxBand[i]
                                incomeByTaxBand[i] = 0
                            else:
                                careBrackets[i] += residualCost
                                incomeByTaxBand[i] -= residualCost
                                residualCost = 0
                                break
                        taxRefund = sum([a*b for a,b in zip(careBrackets, self.p['bandsTaxationRates'])])
                        priceFormalCare = (totalFormalCareCost - taxRefund)/float(self.p['quantumCare'])
                        # Compare the cost of informal care and the price of formal care
                        if costInformalCare < priceFormalCare:
                            availableWorkers[0].residualWorkingHours -= self.p['quantumCare']
                            if availableWorkers[0].residualWorkingHours < 0:
                                availableWorkers[0].residualWorkingHours = 0
                            availableWorkers[0].income = availableWorkers[0].residualWorkingHours*availableWorkers[0].wage
                            earningMembers = [x for x in household if x.income > 0]
                            incomes = [x.income for x in earningMembers]
                            incomeByTaxBand = self.updateTaxBrackets(incomes)
                            availableWorkers[0].socialWork += self.p['quantumCare']
                            availableWorkers[0].offWorkCare += self.p['quantumCare']
                            residualIncomeForCare -= self.p['quantumCare']*costInformalCare
                            if residualIncomeForCare < 0:
                                residualIncomeForCare = 0
                            for member in household:
                                member.residualIncomeCare = residualIncomeForCare
                                member.incomeByTaxBands = incomeByTaxBand
                                for i in range(4):
                                    member.residualFormalSupply[i] -= self.p['quantumCare']
                                    if member.residualFormalSupply[i] < 0:
                                        member.residualFormalSupply[i] = 0
                            informalCare = self.p['quantumCare']
                            supplier = 'employed: informal care (close relative, in town)'
                        else:
                            residualIncomeForCare -= self.p['quantumCare']*priceFormalCare
                            self.totalTaxRefund += taxRefund
                            for member in household:
                                member.residualIncomeCare = residualIncomeForCare
                                member.incomeByTaxBands = incomeByTaxBand
                                for i in range(4):
                                    member.residualFormalSupply[i] -= self.p['quantumCare']
                                    if member.residualFormalSupply[i] < 0:
                                        member.residualFormalSupply[i] = 0
                            earningMembers[0].workToCare += self.p['quantumCare']
                            formalCare = self.p['quantumCare']
                            supplier = 'employed: formal care (close relative, in town)'
                    else: 
                        # If income not from work (e.g. pension) then only formal care is possible
                        # Compute price of formal care
                        totalFormalCareCost = self.p['priceSocialCare']*self.p['quantumCare']
                        deductibleCost = totalFormalCareCost*self.p['taxBreakRate']
                        notDeductibleCost = totalFormalCareCost - deductibleCost
                        residualCost = deductibleCost
                        careBrackets = []
                        for i in range(int(self.p['taxBandsNumber'])):
                            careBrackets.append([])
                            careBrackets[i] = 0
                        for i in range(int(self.p['taxBandsNumber'])):
                            if residualCost > incomeByTaxBand[i]:
                                careBrackets[i] += incomeByTaxBand[i]
                                residualCost -= incomeByTaxBand[i]
                                incomeByTaxBand[i] = 0
                            else:
                                careBrackets[i] += residualCost
                                incomeByTaxBand[i] -= residualCost
                                residualCost = 0
                                break
                        taxRefund = sum([a*b for a,b in zip(careBrackets, self.p['bandsTaxationRates'])])
                        priceFormalCare = (totalFormalCareCost - taxRefund)/float(self.p['quantumCare'])
                        residualIncomeForCare -= self.p['quantumCare']*priceFormalCare
                        if residualIncomeForCare < 0:
                            residualIncomeForCare
                        self.totalTaxRefund += taxRefund
                        for member in household:
                            member.residualIncomeCare = residualIncomeForCare
                            member.incomeByTaxBands = incomeByTaxBand
                            for i in range(4):
                                member.residualFormalSupply[i] -= self.p['quantumCare']
                                if member.residualFormalSupply[i] < 0:
                                    member.residualFormalSupply[i] = 0
                        # earningMembers[0].workToCare += self.p['quantumCare']
                        formalCare = self.p['quantumCare']
                        supplier = 'employed: formal care (close relative, in town)'    
                else:
                    # In this case, informal care is supplied
                    if carers[0].status == 'employed':
                        for i in range(4):
                            carers[0].extraworkCare[i] -= self.p['quantumCare']
                            if carers[0].extraworkCare[i] < 0:
                                carers[0].extraworkCare[i] = 0
                    else:
                        for i in range(4):
                            carers[0].residualInformalSupply[i] -= self.p['quantumCare']
                            if carers[0].residualInformalSupply[i] < 0:
                                carers[0].residualInformalSupply[i] = 0
                    carers[0].socialWork += self.p['quantumCare']
                    informalCare = self.p['quantumCare']
            else:
                # In this case, only formal care can be supplied
                if residualFormalSupplyHours > 0:
                    residualFormalSupplyHours -= self.p['quantumCare']
                    if residualFormalSupplyHours < 0:
                        residualFormalSupplyHours = 0
                    totalFormalCareCost = self.p['priceSocialCare']*self.p['quantumCare']
                    deductibleCost = totalFormalCareCost*self.p['taxBreakRate']
                    notDeductibleCost = totalFormalCareCost - deductibleCost
                    residualCost = deductibleCost
                    careBrackets = []
                    for i in range(int(self.p['taxBandsNumber'])):
                        careBrackets.append([])
                        careBrackets[i] = 0
                    for i in range(int(self.p['taxBandsNumber'])):
                        if residualCost > incomeByTaxBand[i]:
                            careBrackets[i] += incomeByTaxBand[i]
                            residualCost -= incomeByTaxBand[i]
                            incomeByTaxBand[i] = 0
                        else:
                            careBrackets[i] += residualCost
                            incomeByTaxBand[i] -= residualCost
                            residualCost = 0
                            break
                    taxRefund = sum([a*b for a,b in zip(careBrackets, self.p['bandsTaxationRates'])])
                    priceFormalCare = (totalFormalCareCost - taxRefund)/float(self.p['quantumCare'])
                    residualIncomeForCare -= self.p['quantumCare']*priceFormalCare
                    if residualIncomeForCare < 0:
                        residualIncomeForCare = 0
                    self.totalTaxRefund += taxRefund
                    for member in household:
                        member.residualIncomeCare = residualIncomeForCare
                        member.incomeByTaxBands = incomeByTaxBand
                        for i in range(4):
                            member.residualFormalSupply[i] -= self.p['quantumCare']
                            if member.residualFormalSupply[i] < 0:
                                member.residualFormalSupply[i] = 0
                    earningMembers[0].workToCare += self.p['quantumCare']
                    formalCare = self.p['quantumCare']
                    supplier = 'employed: formal care (close relative, not in town)'
        else:
            if townCarer == townReceiver: 
                groupsAvailability[-1] = 0.0
                groupsProbabilities = [x/sum(groupsAvailability) for x in groupsAvailability]
                carers = np.random.choice(householdsGroups, p = groupsProbabilities)
                if carers[0].status == 'employed':
                    for i in range(4):
                        carers[0].extraworkCare[i] -= self.p['quantumCare']
                        if carers[0].extraworkCare[i] < 0:
                            carers[0].extraworkCare[i] = 0
                else:
                    for i in range(4):
                        carers[0].residualInformalSupply[i] -= self.p['quantumCare']
                        if carers[0].residualInformalSupply[i] < 0:
                            carers[0].residualInformalSupply[i] = 0
                carers[0].socialWork += self.p['quantumCare']
                informalCare = self.p['quantumCare']
                
        receiver.informalCare += informalCare
        receiver.formalCare += formalCare
        receiver.careReceived += self.p['quantumCare']
        receiver.informalSupplyByKinship[int(receiver.careNetwork[receiver][carer]['distance'])] += informalCare
        receiver.formalSupplyByKinship[int(receiver.careNetwork[receiver][carer]['distance'])] += formalCare
        if informalCare == 0 and formalCare == 0:
            print('Error: no care is transferred')
            
        for carer in household:  
            if receiver not in carer.careReceivers:
                carer.careReceivers.append(receiver)
                carer.totalCareSupplied.append(formalCare+informalCare)
            else:
                carer.totalCareSupplied[carer.careReceivers.index(receiver)] += (formalCare+informalCare)
        # receiver.totalSupply -= self.p['quantumCare']
    
    def updateTaxBrackets(self, incomes):
        incomeByTaxBand = [0]*self.p['taxBandsNumber']
        incomeByTaxBand[-1] = sum(incomes)
        for i in range(int(self.p['taxBandsNumber'])-1):
            for income in incomes:
                if income > self.p['taxBrackets'][i]:
                    bracket = income-self.p['taxBrackets'][i]
                    incomeByTaxBand[i] += bracket
                    incomeByTaxBand[-1] -= bracket
                    incomes[incomes.index(income)] -= bracket
        return incomeByTaxBand
        
        
    def maxCareSupplyHours(self, household):
        incomeByTaxBand = household[0].incomeByTaxBands
        residualIncomeForCare = household[0].residualIncomeCare
        availableWorkers = [x for x in household if x.status == 'employed' and x.residualWorkingHours > 0]
        availableWorkers.sort(key=operator.attrgetter("wage"))
        residualWorkingHours = [x.residualWorkingHours for x in availableWorkers]
        wages = [x.wage for x in availableWorkers]
        
        totCareSupply = 0
        
        while residualIncomeForCare > 0:
            totalFormalCareCost = self.p['priceSocialCare']
            deductibleCost = totalFormalCareCost*self.p['taxBreakRate']
            notDeductibleCost = totalFormalCareCost - deductibleCost
            residualCost = deductibleCost
            careBrackets = []
            for i in range(int(self.p['taxBandsNumber'])):
                careBrackets.append([])
                careBrackets[i] = 0
            for i in range(int(self.p['taxBandsNumber'])):
                if residualCost > incomeByTaxBand[i]:
                    careBrackets[i] += incomeByTaxBand[i]
                    residualCost -= incomeByTaxBand[i]
                    incomeByTaxBand[i] = 0
                else:
                    careBrackets[i] += residualCost
                    incomeByTaxBand[i] -= residualCost
                    residualCost = 0
                    break
            taxRefund = sum([a*b for a,b in zip(careBrackets, self.p['bandsTaxationRates'])])
            priceFormalCare = (totalFormalCareCost - taxRefund)
            
            if sum(residualWorkingHours) > 0:
                index = -1
                for i in residualWorkingHours:
                    if i > 0:
                        index = residualWorkingHours.index(i)
                costInformalCare = wages[index]
                if costInformalCare < priceFormalCare:
                    residualWorkingHours[index] -= 1
                    residualIncomeForCare -= costInformalCare
                    incomes = [a*b for a,b in zip(residualWorkingHours, wages)]
                    incomeByTaxBand = self.updateTaxBrackets(incomes)
                    totCareSupply += 1
                else:
                    residualIncomeForCare -= priceFormalCare
                    for i in range(int(self.p['taxBandsNumber'])):
                        if priceFormalCare > incomeByTaxBand[i]:
                            priceFormalCare -= incomeByTaxBand[i]
                            incomeByTaxBand[i] = 0
                        else:
                            incomeByTaxBand[i] -= priceFormalCare
                            priceFormalCare = 0
                            break
                    totCareSupply += 1
            else:
                residualIncomeForCare -= priceFormalCare
                for i in range(int(self.p['taxBandsNumber'])):
                    if priceFormalCare > incomeByTaxBand[i]:
                        priceFormalCare -= incomeByTaxBand[i]
                        incomeByTaxBand[i] = 0
                    else:
                        incomeByTaxBand[i] -= priceFormalCare
                        priceFormalCare = 0
                        break
                totCareSupply += 1
                
        return totCareSupply
    
    def probSuppliers(self, receiver):       
        townReceiver = receiver.house.town 
        weightedSupplies = []
                
        for carer in receiver.careNetwork.neighbors(receiver): #receiver.networkList:
            distance = receiver.careNetwork[receiver][carer]['distance']
            townCarer = carer.house.town
            household = carer.house.occupants
            formalSupplyHours = household[0].residualFormalSupply[distance]
            householdCarers = [x for x in household if x.hoursDemand == 0]
            notWorking = [x for x in householdCarers if x.status == 'teenager' or x.status == 'retired' or x.status == 'student']
            employed = [x for x in householdCarers if x.status == 'employed']
            totsupply = 0
            if distance == 0 or distance == 1:
                totsupply += formalSupplyHours
            if townCarer == townReceiver:
                for member in notWorking:
                    totsupply += member.residualInformalSupply[distance]
                for member in employed:
                    totsupply += member.extraworkCare[distance]
                    
            weightedSupplies.append(totsupply)
        
        # Then, randomly select a supplier according to the weighted supplies
        probCarers = [i/sum(weightedSupplies) for i in weightedSupplies]
        return probCarers     
                
    def householdIncome(self, hm):
        income = 0
        for member in hm:
            income += member.income
        return(income)
        
    def householdMinWage(self, hm):
        wages = []
        for member in hm:
            if member.status == 'employed':
                wages.append(member.wage)
        minWage = min(wages)
        return(minWage)
         
    def ageTransitions(self):
       # peopleNotYetRetired = [x for x in self.pop.livingPeople if x.status != 'retired']
       
       # As the years go by, people change their status from 'child' to 'student', 
       # from 'student' to 'unemployed' (i.e. enter the workforce) and
       # from 'employed' (or 'unemployed') to retired
       # (additional states are: 'inactive', for people needing care; 
       # and 'maternity', for mothers of babies in their first year).
       

        for person in self.pop.livingPeople:
            person.age += 1
            # if self.year >= self.p['implementPoliciesFromYear']:
            needLevel = float(person.careNeedLevel)
            shareUnmetNeed = 0
            if needLevel > 0:
                shareUnmetNeed = float(person.residualNeed)/float(person.hoursDemand)
                
            person.qaly = 1/math.exp(self.p['qalyBeta']*pow(needLevel, self.p['qalyAlpha'])*(1.0+shareUnmetNeed))
            
            if person.status == 'child' and person.age >= self.p['ageTeenagers']:
                person.status = 'teenager'
            # person.justMarried = None
            if person.age >= 18 and person.careNeedLevel > 2:
                person.income = self.p['stateSupport']
                person.netIncome = self.p['stateSupport'] 
            
        for person in self.pop.livingPeople:
            if person.status == 'student':
                person.yearOfSchoolLeft -= 1
            if person.status == 'maternity':
                minAge = min([x.age for x in person.children])
                if minAge > 0:
                    person.babyCarer == False
                    if person.yearOfSchoolLeft == 0:
                        self.enterWorkForce(person)
                    else:
                        person.status = 'student'
            
        activePop = [x for x in self.pop.livingPeople if x.careNeedLevel < 3]
        
        for person in activePop:
            if person.age >= self.p['ageOfRetirement'] and person.status != 'retired':
                person.status = 'retired'
                person.income = self.p['pensionWage'][person.classRank]*self.p['weeklyHours']
                person.disposableIncome = person.income
                person.netIncome = person.income
                if person.house == self.displayHouse:
                    self.textUpdateList.append(str(self.year) + ": #" + str(person.id) + " has now retired.")
    
    
    def computeNetIncome(self):
        pensioners = [x for x in self.pop.livingPeople if x.status != 'employed' and x.income > 0]
        for person in pensioners:
            self.pensionExpenditure += person.income
        employedPop = [x for x in self.pop.livingPeople if x.status == 'employed']
        for person in employedPop:
            person.netIncome = person.residualWorkingHours*person.wage
            income = person.netIncome
            self.pensionExpenditure -= income*self.p['pensionContributionRate']
            for i in range(int(self.p['taxBandsNumber'])-1):
                if income > self.p['taxBrackets'][i]:
                    bracket = income-self.p['taxBrackets'][i]
                    self.taxRevenue += bracket*self.p['bandsTaxationRates'][i]
                    income -= bracket
    
    def careBankingAllocation(self): # Allocate care through social care credits
        # Compute volunteers' supply
        totSocialCredits = sum([x.socialCareCredits for x in self.pop.livingPeople if x.socialCareCredits > 0])
        if self.year >= self.p['implementPoliciesFromYear'] and totSocialCredits > 0:
            volunteers = [x for x in self.pop.livingPeople if x.age >= self.p['socialCareBankingAge'] and x.hoursDemand == 0]
            for person in volunteers:
                person.potentialVolunteer = True
                person.totalSupply += person.socialCareCredits
                # Check variable
                if self.year == self.p['getCheckVariablesAtYear']:
                    self.volunteersTotalSupply.append(person.totalSupply)
                    
                shareResidualSupply = 1/math.exp(self.p['volunteersCarePropensionCoefficient']*(1+person.totalSupply))
                person.volunteerCareSupply = round(person.residualInformalSupply*shareResidualSupply)
            # Create a network of next-of-kin volunteers
            potentialReceivers = [x for x in self.pop.livingPeople if x.residualNeed > 0 and x.socialCareCredits > 0]
            for receiver in potentialReceivers:
                availableVolunteers = [x for x in receiver.careNetwork.neighbors(receiver) if x.potentialVolunteer == True and x.house.town == receiver.house.town and x.volunteerCareSupply > 0]
                receiver.totalSupply = sum([x.volunteerCareSupply for x in availableVolunteers])
            residualReceivers = [x for x in potentialReceivers if x.totalSupply > 0]
            while len(residualReceivers) > 0:
                # Select receiver by residual need
                careList = [x.residualNeed for x in residualReceivers]
                probReceivers = [i/sum(careList) for i in careList]
                receiver = np.random.choice(residualReceivers, p = probReceivers)
                # Select receiver's volunteer by residual supply
                availableVolunteers = [x for x in receiver.careNetwork.neighbors(receiver) if x.potentialVolunteer == True and x.house.town == receiver.house.town and x.volunteerCareSupply > 0]
                supplyList = [x.volunteerCareSupply for x in availableVolunteers]
                probSuppliers = [i/sum(supplyList) for i in supplyList]
                supplier = np.random.choice(availableVolunteers, p = probSuppliers)
                # Transfer supply and social credit
                supplier.volunteerCareSupply -= 1
                receiver.residualNeed -= 1
                supplier.socialCareCredits += 1
                receiver.socialCareCredits -= 1
                supplier.socialWork += 1
                receiver.informalCare += 1
                self.socialCreditSpent += 1
                # Create new set of receivers
                potentialReceivers = [x for x in potentialReceivers if x.residualNeed > 0 and x.socialCareCredits > 0]
                for receiver in potentialReceivers:
                    availableVolunteers = [x for x in receiver.careNetwork.neighbors(receiver) if x.potentialVolunteer == True and x.house.town == receiver.house.town and x.volunteerCareSupply > 0]
                    receiver.totalSupply = sum([x.volunteerCareSupply for x in availableVolunteers])
                residualReceivers = [x for x in potentialReceivers if x.totalSupply > 0]
                
            # Repeat while loop with the set of suppliers being all volunteers in the same town of receiver
            potentialReceivers = [x for x in self.pop.livingPeople if x.residualNeed > 0 and x.socialCareCredits > 0]
            for receiver in potentialReceivers:
                availableVolunteers = [x for x in self.pop.livingPeople if x.potentialVolunteer == True and x.house.town == receiver.house.town and x.volunteerCareSupply > 0]
                receiver.totalSupply = sum([x.volunteerCareSupply for x in availableVolunteers])
            residualReceivers = [x for x in potentialReceivers if x.totalSupply > 0]
            while len(residualReceivers):
                careList = [x.residualNeed for x in residualReceivers]
                probReceivers = [i/sum(careList) for i in careList]
                receiver = np.random.choice(residualReceivers, p = probReceivers)
                # Select receiver's volunteer by residual supply
                availableVolunteers = [x for x in self.pop.livingPeople if x.potentialVolunteer == True and x.house.town == receiver.house.town and x.volunteerCareSupply > 0]
                supplyList = [x.volunteerCareSupply for x in availableVolunteers]
                probSuppliers = [i/sum(supplyList) for i in supplyList]
                supplier = np.random.choice(availableVolunteers, p = probSuppliers)
                # Transfer supply and social credit
                supplier.volunteerCareSupply -= 1
                receiver.residualNeed -= 1
                supplier.socialCareCredits += 1
                receiver.socialCareCredits -= 1
                supplier.socialWork += 1
                receiver.informalCare += 1
                self.socialCreditSpent += 1
                # Create new set of receivers
                potentialReceivers = [x for x in potentialReceivers if x.residualNeed > 0 and x.socialCareCredits > 0]
                for receiver in potentialReceivers:
                    availableVolunteers = [x for x in self.pop.livingPeople if x.potentialVolunteer == True and x.house.town == receiver.house.town and x.volunteerCareSupply > 0]
                    receiver.totalSupply = sum([x.volunteerCareSupply for x in availableVolunteers])
                residualReceivers = [x for x in potentialReceivers if x.totalSupply > 0]
            # If receivers have residual need and social credits left, supply public care equal to the smaller amount
            residualReceivers = [x for x in self.pop.livingPeople if x.residualNeed > 0 and x.socialCareCredits > 0]
            for person in residualReceivers:
                publicCare = min(person.residualNeed, person.socialCareCredits)
                self.careCreditSupply += publicCare
                if person.residualNeed > person.socialCareCredits:
                    person.residualNeed -= person.socialCareCredits
                    person.socialCareCredits = 0
                else:
                    person.socialCareCredits -= person.residualNeed
                    person.residualNeed = 0
                
    def healthServiceCost(self):
        
        peopleWithUnmetNeed = [x for x in self.pop.livingPeople if x.cumulativeUnmetNeed != 0 and x.careNeedLevel > 0]
        for person in peopleWithUnmetNeed:
            needLevelFactor = math.pow(self.p['needLevelParam'], person.careNeedLevel)
            unmetSocialCareFactor = math.pow(self.p['unmetSocialCareParam'], person.averageShareUnmetNeed)
            averageHospitalization = self.p['hospitalizationParam']*needLevelFactor*unmetSocialCareFactor
            self.hospitalizationCost += averageHospitalization*self.p['costHospitalizationPerDay']

    def socialTransition(self):
        
        activePop = [x for x in self.pop.livingPeople if x.careNeedLevel < 3]
        
        for person in activePop:
            if person.age == self.p['minWorkingAge']:
                person.status = 'student'
            # With a certain probability p the person enters the workforce, 
            # with a probability 1-p goes to the next educational level
                probStudy = self.transitionProb(person, 0)
                if random.random() > probStudy:
                    # person.classRank = 0
                    person.yearOfSchoolLeft = 0
                    person.classRank = person.temporaryClassRank
                    self.enterWorkForce(person)
                    if person.house == self.displayHouse:
                        self.textUpdateList.append(str(self.year) + ": #" + str(person.id) + " is now looking for a job.")
                else:
                    person.temporaryClassRank = 1
                    person.yearOfSchoolLeft = 2
                    if person.house == self.displayHouse:
                        self.textUpdateList.append(str(self.year) + ": #" + str(person.id) + " is now a student.")
            if person.age >= self.p['workingAge'][1] and person.status == 'student' and person.yearOfSchoolLeft == 0 and person.temporaryClassRank == 1:
            # With a certain probability p the person enters the workforce, 
            # with a probability 1-p goes to the next educational level
                probStudy = self.transitionProb(person, 1)
                if random.random() > probStudy:
                    # person.classRank = 1
                    person.yearOfSchoolLeft = 0
                    person.classRank = person.temporaryClassRank
                    self.enterWorkForce(person)
                    if person.house == self.displayHouse:
                        self.textUpdateList.append(str(self.year) + ": #" + str(person.id) + " is now looking for a job.")
                else:
                    if random.random < self.p['leaveHomeStudentProb']:
                        person.status = 'outOfTownStudent'
                    person.temporaryClassRank = 2
                    person.yearOfSchoolLeft = 2
            if person.age >= self.p['workingAge'][2] and (person.status == 'student' or person.status == 'outOfTownStudent') and person.yearOfSchoolLeft == 0 and person.temporaryClassRank == 2:
            # With a certain probability p the person enters the workforce, 
            # with a probability 1-p goes to the next educational level
                probStudy = self.transitionProb(person, 2)
                if random.random() > probStudy:
                    # person.classRank = 2
                    person.yearOfSchoolLeft = 0
                    person.classRank = person.temporaryClassRank
                    self.enterWorkForce(person)
                    if person.house == self.displayHouse:
                        self.textUpdateList.append(str(self.year) + ": #" + str(person.id) + " is now looking for a job.")
                else:
                    person.temporaryClassRank = 3
                    person.yearOfSchoolLeft = 2
            if person.age >= self.p['workingAge'][3] and (person.status == 'student' or person.status == 'outOfTownStudent') and person.yearOfSchoolLeft == 0 and person.temporaryClassRank == 3:
            # With a certain probability p the person enters the workforce, 
            # with a probability 1-p goes to the next educational level
                probStudy = self.transitionProb(person, 3)
                if random.random() > probStudy:
                    # person.classRank = 3
                    person.yearOfSchoolLeft = 0
                    person.classRank = person.temporaryClassRank
                    self.enterWorkForce(person)
                    if person.house == self.displayHouse:
                        self.textUpdateList.append(str(self.year) + ": #" + str(person.id) + " is now looking for a job.")
                else:
                    person.temporaryClassRank = 4
                    person.yearOfSchoolLeft = 2
            if person.age >= self.p['workingAge'][4] and (person.status == 'student' or person.status == 'outOfTownStudent') and person.yearOfSchoolLeft == 0 and person.temporaryClassRank == 4:
                # person.classRank = 4
                person.yearOfSchoolLeft = 0
                person.classRank = person.temporaryClassRank
                self.enterWorkForce(person)
                if person.house == self.displayHouse:
                    self.textUpdateList.append(str(self.year) + ": #" + str(person.id) + " is now looking for a job.")
         
            if (person.status == 'student' or person.status == 'outOfTownStudent') and len([x for x in person.house.occupants if x.independentStatus == True]) == 0:
                person.independentStatus = True
                self.enterWorkForce(person)
                if person.house == self.displayHouse:
                    self.textUpdateList.append(str(self.year) + ": #" + str(person.id) + " is now looking for a job.")

    def transitionProb (self, person, stage):
        household = [x for x in person.house.occupants]
        if person.father.dead + person.mother.dead != 2:
            pStudy = 0
            disposableIncome = 0
            perCapitaDisposableIncome = self.computeDisposableIncome(household)/float(len(household))
            
            # print('Per Capita Disposable Income: ' + str(perCapitaDisposableIncome))
            
            if perCapitaDisposableIncome > 0.0:
                forgoneSalary = self.p['incomeInitialLevels'][stage]*self.p['weeklyHours']
                educationCosts = self.p['educationCosts'][stage]
                relCost = (forgoneSalary+educationCosts)/perCapitaDisposableIncome
                
                # Check variable
                if self.year == self.p['getCheckVariablesAtYear']:
                    self.relativeEducationCost.append(relCost) # 0.2 - 5
                
                incomeEffect = self.p['costantIncomeParam']/(math.exp(self.p['eduWageSensitivity']*relCost) + (self.p['costantIncomeParam']-1)) # Min-Max: 0 - 10
                targetEL = max(person.father.classRank, person.mother.classRank)
                dE = targetEL - stage
                expEdu = math.exp(self.p['eduRankSensitivity']*dE)
                educationEffect = expEdu/(expEdu+self.p['costantEduParam'])
                careEffect = 1/math.exp(self.p['careEducationParam']*person.socialWork)
                pStudy = incomeEffect*educationEffect*careEffect
                # pStudy = math.pow(incomeEffect, self.p['incEduExp'])*math.pow(educationEffect, 1-self.p['incEduExp'])
                if pStudy < 0:
                    pStudy = 0
                # Check
                if self.year == self.p['getCheckVariablesAtYear']:
                    self.probKeepStudying.append(pStudy)
                    self.stageStudent.append(stage)
                
            else:
                # print('perCapitaDisposableIncome: ' + str(perCapitaDisposableIncome))
                pStudy = 0
        else:
            pStudy = 0
        # pWork = math.exp(-1*self.p['eduEduSensitivity']*dE1)
        # return (pStudy/(pStudy+pWork))
        #pStudy = 0.8
        return (pStudy)
    
    def wagesGrowth(self):
        for i in range(self.p['numberClasses']):
            self.p['pensionWage'][i] *= self.p['wageGrowthRate']
            self.p['incomeInitialLevels'][i] *= self.p['wageGrowthRate']
            self.p['incomeFinalLevels'][i] *= self.p['wageGrowthRate']
        for i in range(4):
            self.p['educationCosts'][i] *= self.p['wageGrowthRate']
        self.p['pricePublicSocialCare'] *= self.p['wageGrowthRate']
        self.p['priceSocialCare'] *= self.p['wageGrowthRate']    
            
            
    def enterWorkForce(self, person):
        person.independentStatus = True
        person.ageStartWorking = person.age
        person.status = 'employed'
        person.finalIncome = self.p['incomeFinalLevels'][person.classRank]
        person.workingTime = 0
        person.wage = self.marketWage(person)
        person.income = person.wage*self.p['weeklyHours']
        person.disposableIncome = person.wage*self.p['weeklyHours']
        person.netIncome = person.wage*self.p['weeklyHours']
        
    def marketWage(self, person):
        # Gompertz Law
        k = self.p['incomeFinalLevels'][person.classRank]
        r = self.p['incomeGrowthRate'][person.classRank]
        c = np.log(self.p['incomeInitialLevels'][person.classRank]/k)
        exp = c*math.exp(-1*r*person.workingTime)
        marketWage = k*math.exp(exp)
        return marketWage
    
    def doDivorces(self):
      
        menInRelationships = [x for x in self.pop.livingPeople if x.sex == 'male' and x.partner != None and x.elderlyWithFamily == False]
        for man in menInRelationships:
            if self.year < self.p['thePresent']:
                rawSplit = self.p['basicDivorceRate'] * self.p['divorceModifierByDecade'][man.age/10]
            else:
                rawSplit = self.p['variableDivorce'] * self.p['divorceModifierByDecade'][man.age/10]      
            baseRate = self.baseRate(self.p['divorceBias'], rawSplit)
            splitProb = baseRate*math.pow(self.p['divorceBias'], man.classRank)
            
            if random.random() < splitProb:
                man.movedThisYear = True
                wife = man.partner
                
                man.previousPartners.append(wife)
                wife.previousPartners.append(man)
                man.previousPartners = list(set(man.previousPartners))
                wife.previousPartners = list(set(wife.previousPartners))
                
                if wife.status == 'student':
                    wife.classRank = wife.temporaryClassRank
                    self.enterWorkForce(wife)
                if wife.careNeedLevel > 2:
                    wife.income = self.p['stateSupport']
                    wife.netIncome = self.p['stateSupport']
                man.partner = None
                wife.partner = None
                self.divorceTally += 1
                # Delete man from networks of household's members
#                members = man.householdNetwork.neighbors(man)
#                for member in members:
#                    member.householdNetwork.remove_node(man)
                # Find a new house: the choice should be based on social class
                # distance = random.choice(['near','far'])
                if man.house == self.displayHouse:
                    messageString = str(self.year) + ": #" + str(man.id) + " splits with #" + str(wife.id) + "."
                    self.textUpdateList.append(messageString)
                    
                house = self.findNewHouse([man], man.house.town, 'doDivorces')
                # Add new household with man to network
#                G = nx.Graph()
#                G.add_node(man)
#                man.householdNetwork = G
#                self.householdsNetwork.add_node(man.householdNetwork, house = house)
#                # Create links with children's households
#                links = self.householdsNetwork.neighbors(wife.householdNetwork)
#                for n in links:
#                    self.householdsNetwork.add_edge(man.householdNetwork, n)
        
    def getRelocationCost(self, household):
        reloCost = sum([math.pow(float(x.yearsInTown), self.p['yearsInTownSensitivityParam']) for x in household])
        # Check variable
        if self.year == self.p['getCheckVariablesAtYear']:
            self.relocationCost.append(reloCost)  # Min-Max: 0 - 8
            
        costExp = math.exp(self.p['relocationCostParam']*reloCost)
        reloCost = (costExp-1)/costExp # Scaling factor
        return reloCost
    
    def spouseRelocationDecision(self, spouses, household_1, household_2, case):
        a = spouses[0]
        b = spouses[1]
        town_1 = a.house.town
        town_2 = b.house.town
        sizeFactors = self.computeSizeAttractions()
        if town_1 == town_2 and sizeFactors[self.map.towns.index(town_1)] > 0:
            town = town_1
        else: 
            household = household_1 + household_2
            averageIncome = sum([x.income for x in household])/float(len(household))
            classRank = max([x.classRank for x in spouses])
            networkFactors = self.networkSize(household)
            socialFactors = self.computeSocialAttractions(classRank)
            relocationCostFactor_1 = self.getRelocationCost(household_1)
            relocationCostFactor_2 = self.getRelocationCost(household_2)
            if case == 'Not independent':
                if sizeFactors[self.map.towns.index(town_1)] > 0.0:
                    if sizeFactors[self.map.towns.index(town_2)] > 0.0:
                        socialFactor_1  = socialFactors[self.map.towns.index(town_1)]
                        socialFactor_2  = socialFactors[self.map.towns.index(town_2)]
                        # Network Factor
                        household = household_1 + household_2
                        networkFactor_1 = self.spousesCareLocation(household, town_1)
                        networkFactor_2 = self.spousesCareLocation(household, town_2)
                        # Relocation Cost Factor
                        sizefactor_1 = sizeFactors[self.map.towns.index(town_1)]
                        sizefactor_2 = sizeFactors[self.map.towns.index(town_2)]
                        networkExp_1 = self.p['networkBetaParam']*networkFactor_1
                        networkExp_2 = self.p['networkBetaParam']*networkFactor_2
                        socialExp_1 = self.p['socialBetaParam']*socialFactor_1
                        socialExp_2 = self.p['socialBetaParam']*socialFactor_2
                        costExp_1 = self.p['relocationCostBetaParam']*relocationCostFactor_1
                        costExp_2 = self.p['relocationCostBetaParam']*relocationCostFactor_2
                        
                        if (networkExp_1+socialExp_1+costExp_1)/averageIncome > 20:
                            print networkExp_1
                            print socialExp_1
                            print costExp_1
                            print averageIncome
                    
                        if (networkExp_2+socialExp_2+costExp_2)/averageIncome > 20:
                            print networkExp_2
                            print socialExp_2
                            print costExp_2
                            print averageIncome
                        
                        p_1 = sizefactor_1*math.exp((networkExp_1+socialExp_1+costExp_1)/averageIncome)
                        p_2 = sizefactor_2*math.exp((networkExp_2+socialExp_2+costExp_2)/averageIncome)
                        
                        town = np.random.choice([town_1, town_2], p = [p_1/(p_1+p_2), p_2/(p_1+p_2)])
                    else:
                        town = town_1
                else:
                    if sizeFactors[self.map.towns.index(town_2)] > 0.0:
                        town = town_2
                    else:
                        for t in self.map.towns:
                            socialFactor = socialFactors[self.map.towns.index(t)]
                            sizeFactor = sizeFactors[self.map.towns.index(t)]
                            networkFactor = networkFactors[self.map.towns.index(t)]
                            exp_1 = self.p['networkBetaParam']*networkFactor
                            exp_2 = self.p['socialBetaParam']*socialFactor
                            townWeights.append(sizeFactor*math.exp((exp_1 + exp_2)/averageIncome))
                        probs = [x/sum(townWeights) for x in townWeights]
                        town = np.random.choice(self.map.towns, p = probs)
            
            if case == 'One independent':
                if sizeFactors[self.map.towns.index(town_2)] == 0.0:
                    town = town_1
                else:
                    socialFactor_1  = socialFactors[self.map.towns.index(town_1)]
                    socialFactor_2  = socialFactors[self.map.towns.index(town_2)]
                    # Network Factor
                    household = household_1 + household_2
                    networkFactor_1 = self.spousesCareLocation(household, town_1)
                    networkFactor_2 = self.spousesCareLocation(household, town_2)
                    # Relocation Cost Factor
                    sizefactor_1 = sizeFactors[self.map.towns.index(town_1)]
                    sizefactor_2 = sizeFactors[self.map.towns.index(town_2)]
                    networkExp_1 = self.p['networkBetaParam']*networkFactor_1
                    networkExp_2 = self.p['networkBetaParam']*networkFactor_2
                    socialExp_1 = self.p['socialBetaParam']*socialFactor_1
                    socialExp_2 = self.p['socialBetaParam']*socialFactor_2
                    costExp_1 = self.p['relocationCostBetaParam']*relocationCostFactor_1
                    costExp_2 = self.p['relocationCostBetaParam']*relocationCostFactor_2
                    
                    if (networkExp_1+socialExp_1+costExp_1)/averageIncome > 20:
                        print networkExp_1
                        print socialExp_1
                        print costExp_1
                        print averageIncome
                    
                    if (networkExp_2+socialExp_2+costExp_2)/averageIncome > 20:
                        print networkExp_2
                        print socialExp_2
                        print costExp_2
                        print averageIncome
                    
                    p_1 = math.exp((networkExp_1+socialExp_1+costExp_1)/averageIncome)
                    p_2 = math.exp((networkExp_2+socialExp_2+costExp_2)/averageIncome)
                    
                    town = np.random.choice([town_1, town_2], p = [p_1/(p_1+p_2), p_2/(p_1+p_2)])
                
            if case == 'Both independent':
                # Social Factor
                if town_1 == town_2:
                    town = town_1
                else:
                    socialFactor_1  = socialFactors[self.map.towns.index(town_1)]
                    socialFactor_2  = socialFactors[self.map.towns.index(town_2)]
                    # Network Factor
                    household = household_1 + household_2
                    networkFactor_1 = self.spousesCareLocation(household, town_1)
                    networkFactor_2 = self.spousesCareLocation(household, town_2)
                    # Relocation Cost Factor
                    sizefactor_1 = sizeFactors[self.map.towns.index(town_1)]
                    sizefactor_2 = sizeFactors[self.map.towns.index(town_2)]
                    networkExp_1 = self.p['networkBetaParam']*networkFactor_1
                    networkExp_2 = self.p['networkBetaParam']*networkFactor_2
                    socialExp_1 = self.p['socialBetaParam']*socialFactor_1
                    socialExp_2 = self.p['socialBetaParam']*socialFactor_2
                    costExp_1 = self.p['relocationCostBetaParam']*relocationCostFactor_1
                    costExp_2 = self.p['relocationCostBetaParam']*relocationCostFactor_2
                    
                    if (networkExp_1+socialExp_1+costExp_1)/averageIncome > 20:
                        print networkExp_1
                        print socialExp_1
                        print costExp_1
                        print averageIncome
                        
                    if (networkExp_2+socialExp_2+costExp_2)/averageIncome > 20:
                        print networkExp_2
                        print socialExp_2
                        print costExp_2
                        print averageIncome
                    
                    p_1 = math.exp((networkExp_1+socialExp_1+costExp_1)/averageIncome)
                    p_2 = math.exp((networkExp_2+socialExp_2+costExp_2)/averageIncome)
                    
                    town = np.random.choice([town_1, town_2], p = [p_1/(p_1+p_2), p_2/(p_1+p_2)])
            
        return town

     
    def relocationDecision(self, household):
        townWeights = []
        currentTown = household[0].house.town
        averageIncome = sum([x.income for x in household])/float(len(household))
        classRank = max([x.classRank for x in household if x.independentStatus == True])
        networkFactors = self.networkSize(household)
        socialFactors = self.computeSocialAttractions(classRank)
        sizeFactors = self.computeSizeAttractions()
        for t in self.map.towns:
            socialFactor = socialFactors[self.map.towns.index(t)]
            sizeFactor = sizeFactors[self.map.towns.index(t)]
            networkFactor = networkFactors[self.map.towns.index(t)]
            if t == currentTown:
                townWeights.append(0.0)
            else:
                exp_1 = self.p['networkBetaParam']*networkFactor
                exp_2 = self.p['socialBetaParam']*socialFactor
                townWeights.append(sizeFactor*math.exp(exp_1 + exp_2))
        probs = [x/sum(townWeights) for x in townWeights]

        newTown = np.random.choice(self.map.towns, p = probs)
        
        return newTown
            
    def networkSize(self, household):
        
        kinshipWeight_1 = 1/math.pow(self.p['networkDistanceParam'], 0.0)
        kinshipWeight_2 = 1/math.pow(self.p['networkDistanceParam'], 1.0)
        kinshipWeight_3 = 1/math.pow(self.p['networkDistanceParam'], 2.0) 
        
        nok_1 = []
        nok_2 = []
        nok_3 = []
        visited = []
        
        networkSizes = []
        for i in household:
            if i.father != None:
                nok = i.father
                if nok.dead == False and nok not in household and nok not in visited:
                    nok_1.append(nok)
                    visited.extend(nok.household)
                nok = i.mother
                if nok.dead == False and nok not in household and nok not in visited:
                    nok_1.append(nok)
                    visited.extend(nok.household)
            for child in i.children:
                nok = child
                if nok.dead == False and nok not in household and nok not in visited:
                    nok_1.append(nok)
                    visited.extend(nok.household)
                        
        for i in household:
            if i.father != None:
                if i.father.father != None:
                    nok = i.father.father
                    if nok.dead == False and nok not in household and nok not in visited:
                        nok_2.append(nok)
                        visited.extend(nok.household)
                    nok = i.father.mother
                    if nok.dead == False and nok not in household and nok not in visited:
                        nok_2.append(nok)
                        visited.extend(nok.household)
                if i.mother.father != None:
                    nok = i.mother.father
                    if nok.dead == False and nok not in household and nok not in visited:
                        nok_2.append(nok)
                        visited.extend(nok.household)
                    nok = i.mother.mother
                    if nok.dead == False and nok not in household and nok not in visited:
                        nok_2.append(nok)
                        visited.extend(nok.household)
                brothers = list(set(i.father.children + i.mother.children))
                brothers.remove(i)
                for brother in brothers:
                    nok = brother
                    if nok.dead == False and nok not in household and nok not in visited:
                        nok_2.append(nok)
                        visited.extend(nok.household)
            for child in i.children:
                for grandchild in child.children:
                    nok = grandchild
                    if nok.dead == False and nok not in household and nok not in visited:
                        nok_2.append(nok)
                        visited.extend(nok.household)
                        
        for i in household:
            uncles = []
            if i.father != None:
                if i.father.father != None:
                    uncles = list(set(i.father.father.children + i.father.mother.children))
                    uncles.remove(i.father)
                if i.mother.father != None:
                    uncles.extend(list(set(i.mother.father.children + i.mother.mother.children)))
                    uncles.remove(i.mother)
                for uncle in uncles:
                    nok = uncle
                    if nok.dead == False and nok not in household and nok not in visited:
                        nok_3.append(nok)
                        visited.extend(nok.household)
                brothers = list(set(i.father.children + i.mother.children))
                brothers.remove(i)
                for brother in brothers:
                    for child in brother.children:
                        nok = child
                        if nok.dead == False and nok not in household and nok not in visited:
                            nok_3.append(nok)
                            visited.extend(nok.household)
                            
        for t in self.map.towns:
            networkSize = 0
            networkSize += sum([float(len(x.house.occupants)) for x in nok_1 if x.house.town == t])*kinshipWeight_1
            networkSize += sum([float(len(x.house.occupants)) for x in nok_2 if x.house.town == t])*kinshipWeight_2
            networkSize += sum([float(len(x.house.occupants)) for x in nok_3 if x.house.town == t])*kinshipWeight_3
        
        
            networkSizes.append(networkSize)
            
        if sum(networkSizes) > 0:
            networkWeights = [x/sum(networkSizes) for x in networkSizes]
        else:
            networkWeights = [1.0 for x in networkSizes]
        
        return networkWeights
    
    def relativeNetworkSize(self, household):
        
        currentTown = household[0].house.town
        
        kinshipWeight_1 = 1/math.pow(self.p['networkDistanceParam'], 0.0)
        kinshipWeight_2 = 1/math.pow(self.p['networkDistanceParam'], 1.0)
        kinshipWeight_3 = 1/math.pow(self.p['networkDistanceParam'], 2.0) 
        
        nok_1 = []
        nok_2 = []
        nok_3 = []
        visited = []
        
        networkSizes = []
        for i in household:
            if i.father != None:
                nok = i.father
                if nok.dead == False and nok not in household and nok not in visited:
                    nok_1.append(nok)
                    visited.extend(nok.household)
                nok = i.mother
                if nok.dead == False and nok not in household and nok not in visited:
                    nok_1.append(nok)
                    visited.extend(nok.household)
            for child in i.children:
                nok = child
                if nok.dead == False and nok not in household and nok not in visited:
                    nok_1.append(nok)
                    visited.extend(nok.household)
                        
        for i in household:
            if i.father != None:
                if i.father.father != None:
                    nok = i.father.father
                    if nok.dead == False and nok not in household and nok not in visited:
                        nok_2.append(nok)
                        visited.extend(nok.household)
                    nok = i.father.mother
                    if nok.dead == False and nok not in household and nok not in visited:
                        nok_2.append(nok)
                        visited.extend(nok.household)
                if i.mother.father != None:
                    nok = i.mother.father
                    if nok.dead == False and nok not in household and nok not in visited:
                        nok_2.append(nok)
                        visited.extend(nok.household)
                    nok = i.mother.mother
                    if nok.dead == False and nok not in household and nok not in visited:
                        nok_2.append(nok)
                        visited.extend(nok.household)
                brothers = list(set(i.father.children + i.mother.children))
                brothers.remove(i)
                for brother in brothers:
                    nok = brother
                    if nok.dead == False and nok not in household and nok not in visited:
                        nok_2.append(nok)
                        visited.extend(nok.household)
            for child in i.children:
                for grandchild in child.children:
                    nok = grandchild
                    if nok.dead == False and nok not in household and nok not in visited:
                        nok_2.append(nok)
                        visited.extend(nok.household)
                        
        for i in household:
            uncles = []
            if i.father != None:
                if i.father.father != None:
                    uncles = list(set(i.father.father.children + i.father.mother.children))
                    uncles.remove(i.father)
                if i.mother.father != None:
                    uncles.extend(list(set(i.mother.father.children + i.mother.mother.children)))
                    uncles.remove(i.mother)
                for uncle in uncles:
                    nok = uncle
                    if nok.dead == False and nok not in household and nok not in visited:
                        nok_3.append(nok)
                        visited.extend(nok.household)
                brothers = list(set(i.father.children + i.mother.children))
                brothers.remove(i)
                for brother in brothers:
                    for child in brother.children:
                        nok = child
                        if nok.dead == False and nok not in household and nok not in visited:
                            nok_3.append(nok)
                            visited.extend(nok.household)
        
        networkSize_currentTown = 0
        networkSize_currentTown += sum([float(len(x.house.occupants)) for x in nok_1 if x.house.town == currentTown])*kinshipWeight_1
        networkSize_currentTown += sum([float(len(x.house.occupants)) for x in nok_2 if x.house.town == currentTown])*kinshipWeight_2
        networkSize_currentTown += sum([float(len(x.house.occupants)) for x in nok_3 if x.house.town == currentTown])*kinshipWeight_3
        
        networkSize_otherTowns = 0
        networkSize_otherTowns += sum([float(len(x.house.occupants)) for x in nok_1 if x.house.town != currentTown])*kinshipWeight_1
        networkSize_otherTowns += sum([float(len(x.house.occupants)) for x in nok_2 if x.house.town != currentTown])*kinshipWeight_2
        networkSize_otherTowns += sum([float(len(x.house.occupants)) for x in nok_3 if x.house.town != currentTown])*kinshipWeight_3
        
        if float(networkSize_currentTown)+float(networkSize_otherTowns) > 0:
            return float(networkSize_currentTown)/(float(networkSize_currentTown)+float(networkSize_otherTowns))
        else:
            return 1.0
    
    def computeWage(self, agent, k):
        # Gompertz Law
        c = np.log(self.p['incomeInitialLevels'][agent.classRank]/k)
        exp = c*math.exp(-1*self.p['incomeGrowthRate'][agent.classRank]*agent.workingTime)
        wage = k*math.exp(exp)
        return (wage)
        
    def baseRate(self, bias, cp):
        a = 0
        for i in range(self.p['numberClasses']):
            a += self.socialClassShares[i]*math.pow(bias, i)
        baseRate = cp/a
        return (baseRate)
    
    def updateWage(self):
        employed = [x for x in self.pop.livingPeople if x.status == 'employed']
        for person in employed:
            person.workingTime *= self.p['workDiscountingTime']
            workTime = 0
            workingHours = float(max(self.p['weeklyHours'] - person.offWorkCare, 0))
            workTime = workingHours/float(self.p['weeklyHours'])
            person.workingTime += workTime
            # Gompertz Law
            k = self.p['incomeFinalLevels'][person.classRank]
            r = self.p['incomeGrowthRate'][person.classRank]
            c = np.log(self.p['incomeInitialLevels'][person.classRank]/k)
            exp = c*math.exp(-1*r*person.workingTime)
            person.wage = k*math.exp(exp)
            person.income = person.wage*self.p['weeklyHours']
            person.hourlyWage = person.wage
            
     
    def computeDisposableIncome(self, household):
        disposableIncome = sum([x.netIncome for x in household])
        if disposableIncome < 0:
            disposableIncome = 0
        return disposableIncome
    
    def updateRelocationVar(self):

        for i in self.pop.livingPeople:
            i.movedThisYear = False
            i.yearsInTown += 1.0
            
    def computeSocialAttractions(self, classRank):
        
        socialAttractions = []
        townClassShares = []
        
        for t in self.map.towns:
            townPop = [x for x in self.pop.livingPeople if x.house.town == t]
            classNum = []
            for c in range(self.p['numberClasses']):
                classNum.append(float(len([x for x in townPop if x.classRank == c])))
            if sum(classNum) > 0:
                townClassShares.append([x/sum(classNum) for x in classNum])
            else:
                townClassShares.append([0.0, 0.0, 0.0, 0.0, 0.0])

        for t in self.map.towns:
            exponent = 0.0
            for d in range(self.p['numberClasses']):
                distance = abs(d-classRank)
                weight = pow(distance, self.p['townWeightExp'])
                exponent += weight*townClassShares[self.map.towns.index(t)][d]
            socialAttraction = 1/math.exp(self.p['townAttractionParam']*exponent)
            socialAttractions.append(socialAttraction)
            
        return socialAttractions
            
    def computeSizeAttractions(self):
        townAvailableHouses = [float(len([x for x in t.houses if len(x.occupants) == 0])) for t in self.map.towns]
        sizeAttractions = [x/sum(townAvailableHouses) for x in townAvailableHouses]
        return sizeAttractions
         
        
    def jobRelocation(self):
        
        listHouseholds = [list(x.occupants) for x in self.map.occupiedHouses]
        
        for household in listHouseholds:
            workersWithParents = [x for x in household if x.status == 'employed' and x.independentStatus == False]
            for i in workersWithParents:
                if random.random < self.p['apprenticesRelocationProb']:
                    i.independentStatus = True
                    # Move from parent's house: choose town
                    household.remove(i)
                    averageIncome = i.income
                    for member in household:
                        member.household = household
                    newHousehold = [i]
                    classRank = i.classRank
                    networkFactors = self.networkSize(newHousehold)
                    socialFactors = self.computeSocialAttractions(classRank)
                    sizeFactors = self.computeSizeAttractions()
                    for t in self.map.towns:
                        socialFactor = socialFactors[self.map.towns.index(t)]
                        sizeFactor = sizeFactors[self.map.towns.index(t)]
                        networkFactor = networkFactors[self.map.towns.index(t)]
                        relocationCost = self.getRelocationCost(newHousehold)
                        exp_1 = self.p['networkBetaParam']*networkFactor
                        exp_2 = self.p['socialBetaParam']*socialFactor
                        townWeights.append(sizeFactor*math.exp(exp_1 + exp_2))
                    probs = [x/sum(townWeights) for x in townWeights]
                    town = np.random.choice(self.map.towns, probs)
                    
                    self.findNewHouse(newHousehold, town, 'jobRelocation')
                    
        listHouseholds = [list(x.occupants) for x in self.map.occupiedHouses]
        
        for household in listHouseholds:
            if len(household) > len(list(set(household))):
                print 'Error: person counted twice in household'
        
        householdWeights = []
        
        for household in listHouseholds:
            
            averageIncome = sum([x.income for x in household])/float(len(household))
            
            if averageIncome == 0:
                print 'Warning: household with zero income.'
                print(len(household))
                for member in household:
                    print x.id
                    print x.income
                    print x.netIncome
                    print x.age
                    print x.status
                    print x.sex
                    if x.partner != None:
                        print x.partner.id
                    else: 
                        print 'No partner'
                        
            networkFactor = self.relativeNetworkSize(household)
            relocationFactor = self.getRelocationCost(household)
            
            exp = networkFactor*relocationFactor/averageIncome
            
            householdWeights.append(math.exp(-1*self.p['relocationDecisionParam']*exp))
        
        probs = [x/sum(householdWeights) for x in householdWeights]
        
        numHouseholdToRelocate = int(float(len(listHouseholds))*self.p['shareHouseholdRelocation'])
        
        householdToRelocate = np.random.choice(listHouseholds, numHouseholdToRelocate, replace = False, p = probs)
        
        relocationCount = 0
        for household in householdToRelocate:
            
            currentTown = household[0].house.town
            
            town = self.relocationDecision(household)
            
            
            if town != currentTown:
                relocationCount += 1
                for i in household:        
                    repetitions = household.count(i)
                    if repetitions > 1:
                        print('Person ' + str(i.id) + ' is counted ' + str(repetitions) + ' times in jobRelocation')
                
                for member in household:
                    if member not in member.house.occupants:
                        print('ERROR: ' + str(member.id) + ' not among his house occupants in job Relocation!')
                        print(member.dead)
                        
                self.totalRelocations += 1 
                classRank = max([x.classRank for x in household])
                if classRank == 0:
                    self.jobRelocations_1 += 1 
                if classRank == 1:
                    self.jobRelocations_2 += 1 
                if classRank == 2:
                    self.jobRelocations_3 += 1 
                if classRank == 3:
                    self.jobRelocations_4 += 1 
                if classRank == 4:
                    self.jobRelocations_5 += 1 
                
                self.findNewHouse(household, town, 'jobRelocation')
                
        print 'Relocations: ' + str(float(relocationCount)/float(len(listHouseholds)))
  
    def joiningSpouses(self, couple):

        person = couple[0]
        person.partner = couple[1]
   
        if person.independentStatus + person.partner.independentStatus == 0:
          
            peopleNotToMove = [x for x in list(person.house.occupants) if (x.justMarried != None or x.independentStatus == True) and x != person]
            children = []
            for i in peopleNotToMove:
                children += [x for x in i.children if x.dead == False and x.house == i.house and
                             x.justMarried == None and x.independentStatus == False]
            peopleNotToMove += children
            peopleToMove_1 = [x for x in list(person.house.occupants) if x not in peopleNotToMove]
            
            peopleNotToMove = [x for x in list(person.partner.house.occupants) if (x.justMarried != None or x.independentStatus == True) and x != person.partner]
            children = []
            for i in peopleNotToMove:
                children += [x for x in i.children if x.dead == False and x.house == i.house and
                             x.justMarried == None and x.independentStatus == False]
            peopleNotToMove += children
            peopleToMove_2 = [x for x in list(person.partner.house.occupants) if x not in peopleNotToMove]
            
            town = self.spouseRelocationDecision([person, person.partner], peopleToMove_1, peopleToMove_2, 'Not independent')
        
            peopleToMove = peopleToMove_1 + peopleToMove_2
        
            for i in peopleToMove:     
                repetitions = peopleToMove.count(i)
                if repetitions > 1:
                    print('Person ' + str(i.id) + ' is counted ' + str(repetitions) + ' times in Join Spouses (1)')
                    
            self.totalRelocations += 1
            self.marriageRelocations += 1
            person.independentStatus = True
            person.elderlyWithFamily = False
            person.yearIndependent = self.year
            person.partner.independentStatus = True
            person.partner.elderlyWithFamily = False
            person.partner.yearIndependent = self.year
    
            # Find house for new household
            house = self.findNewHouse(peopleToMove, town, 'joiningSpouses (1)')
        
        # 2nd case: one living alone and the other living with parents
        elif person.independentStatus + person.partner.independentStatus == 1:
            
            if ( person.independentStatus == True and person.partner.independentStatus == False):

                a = person
                b = person.partner
            else:
                a = person.partner
                b = person
                
            peopleNotToMove = [x for x in list(a.house.occupants) if (x.justMarried != None or x.independentStatus == True) and x != a]
            children = []
            for i in peopleNotToMove:
                children += [x for x in i.children if x.dead == False and x.house == i.house and
                             x.justMarried == None and x.independentStatus == False]
            peopleNotToMove += children
            peopleToMove_1 = [x for x in list(a.house.occupants) if x not in peopleNotToMove]
            
            peopleNotToMove = [x for x in list(b.house.occupants) if (x.justMarried != None or x.independentStatus == True) and x != b]
            children = []
            for i in peopleNotToMove:
                children += [x for x in i.children if x.dead == False and x.house == i.house and
                             x.justMarried == None and x.independentStatus == False]
            peopleNotToMove += children
            peopleToMove_2 = [x for x in list(b.house.occupants) if x not in peopleNotToMove]

            town = self.spouseRelocationDecision([a, b], peopleToMove_1, peopleToMove_2, 'One independent')
            
            if town == a.house.town:
                
                peopleToMove = peopleToMove_2
                targetHouse = a.house
                
                if targetHouse == b.house:
                    print('Target house equal to departure house in 2')
                    
                for i in peopleToMove:
                    if i in targetHouse.occupants:
                        print('Error in Join Spouses 2')
                        print(peopleToMove.index(i))
                        
                for i in peopleToMove:    
                    repetitions = peopleToMove.count(i)
                    if repetitions > 1:
                        print('Person ' + str(i.id) + ' is counted ' + str(repetitions) + ' times in Join Spouses 2')    
                        
                self.totalRelocations += 1
                self.marriageRelocations += 1   
                b.independentStatus = True
                b.elderlyWithFamily = False
                b.yearIndependent = self.year
                self.movePeopleIntoChosenHouse(targetHouse, b.house, peopleToMove, 'joiningSpouses (4)')

            else:
               
                peopleToMove = peopleToMove_1 + peopleToMove_2
                
                for i in peopleToMove:  
                    repetitions = peopleToMove.count(i)
                    if repetitions > 1:
                        print('Person ' + str(i.id) + ' is counted ' + str(repetitions) + ' times in Join Spouses (4)')
                
                self.totalRelocations += 1
                self.marriageRelocations += 1
                b.independentStatus = True
                b.elderlyWithFamily = False
                b.yearIndependent = self.year
                house = self.findNewHouse(peopleToMove, town, 'joiningSpouses (6)')
                
        # 3rd case: both living alone
        elif person.independentStatus + person.partner.independentStatus == 2:
            
            peopleNotToMove = [x for x in list(person.house.occupants) if (x.justMarried != None or x.independentStatus == True) and x != person]
            children = []
            for i in peopleNotToMove:
                children += [x for x in i.children if x.dead == False and x.house == i.house and
                             x.justMarried == None and x.independentStatus == False]
            peopleNotToMove += children
            peopleToMove_1 = [x for x in list(person.house.occupants) if x not in peopleNotToMove]
            
            peopleNotToMove = [x for x in list(person.partner.house.occupants) if (x.justMarried != None or x.independentStatus == True) and x != person.partner]
            children = []
            for i in peopleNotToMove:
                children += [x for x in i.children if x.dead == False and x.house == i.house and
                             x.justMarried == None and x.independentStatus == False]
            peopleNotToMove += children
            peopleToMove_2 = [x for x in list(person.partner.house.occupants) if x not in peopleNotToMove]

            town = self.spouseRelocationDecision([person, person.partner], peopleToMove_1, peopleToMove_2, 'Both independent')
            
            if town == person.house.town:
                peopleToMove = peopleToMove_2
                targetHouse = person.house
                houseToLeave = person.partner.house
            else:
                peopleToMove = peopleToMove_1
                targetHouse = person.partner.house
                houseToLeave = person.house
                    
            if targetHouse == houseToLeave:
                print('Target house equal to departure house in 4')
            
            for i in peopleToMove:
                if i in targetHouse.occupants:
                    print('Error in Join Spouses 4')
                    print(peopleToMove.index(i))
                    
            for i in peopleToMove:        
                repetitions = peopleToMove.count(i)
                if repetitions > 1:
                    print('Person ' + str(i.id) + ' is counted ' + str(repetitions) + ' times in Join Spouses 4')      
             
            self.totalRelocations += 1
            self.marriageRelocations += 1
            
            self.movePeopleIntoChosenHouse(targetHouse, houseToLeave, peopleToMove, 'joiningSpouses (9)')   
            
    def computeTotalNeed(self, household):
        careNeed = 0
        for member in household:
            careNeed += self.p['careDemandInHours'][member.careNeedLevel]
        return careNeed
    
    def computeTotalSupply(self, household):
        distance = 1
        householdCarers = [x for x in household if x.hoursDemand == 0 and x.status != 'maternity']
        notWorking = [x for x in householdCarers if x.status == 'teenager' or x.status == 'retired' or x.status == 'student']
        employed = [x for x in householdCarers if x.status == 'employed']
        totsupply = 0
        for member in notWorking:
            totsupply += member.residualInformalSupply[distance]
        for member in employed:
            totsupply += member.extraworkCare[distance]
        return totsupply
                
    def relocatePensioners(self):
        
        inactiveHouseholds = [list(x.occupants) for x in self.map.occupiedHouses if len([i for i in list(x.occupants) if i.careNeedLevel < 3]) == 0]
        
        inactiveHouses = [x[0].house for x in inactiveHouseholds]
        
        for household in inactiveHouseholds:
            
            totalNeed = self.computeTotalNeed(household)
            
            indipendentChildren = []
            for member in household:
                for child in member.children:
                    if child not in indipendentChildren and child.dead == False and child.independentStatus == True:
                        indipendentChildren.append(child)
          
            if len(indipendentChildren) > 0:
                careSupplied = []
                for i in indipendentChildren:
                    
                    totalSupply = self.computeTotalSupply(i.house.occupants)
                            
                    careSupplied.append(totalSupply)
                
                if sum(careSupplied) > 0:
                    probs = [x/sum(careSupplied) for x in careSupplied]
                    potentialHost = np.random.choice(indipendentChildren, p = probs)
                    hostSupply = careSupplied[indipendentChildren.index(potentialHost)]
                    relocationFactor = math.exp(self.p['retiredRelocationParam']*hostSupply*totalNeed)
                    
                    inactiveInHousehold = len([x for x in potentialHost.house.occupants if x.careNeedLevel > 2])
                    totalInactive = inactiveInHousehold + len(household)
                    # Check variable
                    if self.year == self.p['getCheckVariablesAtYear']:
                        self.potentialHostSupply.append(potentialHost.householdSupply) # 
                        
                    if len([x for x in potentialHost.house.occupants if x.independentStatus == True]) == 0:
                        print('Error: potential host house with no independent people!')
                        sys.exit()
                        
                    relocationThreshold = (relocationFactor - 1)/relocationFactor
                    
                    if potentialHost.house != household[0].house and totalInactive < 3 and random.random() < relocationThreshold:
                        if household[0].house == self.displayHouse:
                            messageString = str(self.year) + ": #" + str(household[0].id) + " is going to live with one of their next of kin."
                            self.textUpdateList.append(messageString)
                                    
                        for i in household:
                            if i in potentialHost.house.occupants:
                                print('Retired already in next-of-kin house!')
                                
                        for i in household:        
                            repetitions = household.count(i)
                            if repetitions > 1:
                                print('Person ' + str(i.id) + ' is counted ' + str(repetitions) + ' times in relocatingPensioners')
                        
                        self.totalRelocations += 1
                        self.retiredRelocations += 1
                        
                        peopleToMove = list(household)
                        
                        for i in peopleToMove:
                            i.elderlyWithFamily = True
                            i.independentStatus = False
#                            
                        self.movePeopleIntoChosenHouse(potentialHost.house, household[0].house, peopleToMove, 'relocatingPensioners')
                        
                        
            
    def findNewHouse(self, personList, town, calledBy):
        # Find a new house with a 'good' neighborhood, in the chosen town

        newHouse = None
        person = personList[0]
        
        departureHouse = person.house
        availableHouses = [x for x in town.houses if len(x.occupants) == 0]
        if len(availableHouses) == 0:
            print 'Error: no available houses in town'
        newHouse = np.random.choice(availableHouses) # np.random.choice(town.houses, p = probHouses)
        while newHouse == departureHouse:
            newHouse = np.random.choice(availableHouses) # np.random.choice(town.houses, p = probHouses)
        
        if person.house.town != newHouse.town:
            self.townChanges += 1
        
        if len(newHouse.occupants) >  0:
            print('Moved in an occupied house!')
            
        if ( newHouse == person.house):
            print('Error: new house selected is departure house')    
            
        if newHouse == None:
            print "No houses left for person of SEC " + str(person.sec)
            sys.exit()
        # Actually make the chosen move
        for i in personList:
            if i in newHouse.occupants:
                print('New house not empty!')
                
#        for i in personList:
#            if i.partner != None and i.house != i.partner.house and calledBy != 'joiningSpouses':
#                print('Error: couple not joined after step FindNewHouse')
#                print(i.id)
#                print(i.sex)
#                print(i.status)
#                print(i.classRank)
#                print(i.independentStatus)
#                print(i.age)
#                print(i.ageStartWorking)
#                print(i.justMarried)
#                print(i.yearMarried)
#                print(i.yearsSeparated)
#                print(i.numberPartner)
#                print('')
#                print(i.partner.id)
#                print(i.partner.sex)
#                print(i.partner.status)
#                print(i.partner.classRank)
#                print(i.partner.independentStatus)
#                print(i.partner.age)
#                print(i.partner.ageStartWorking)
#                print(i.partner.justMarried)
#                print(i.partner.yearMarried)
#                print(i.partner.yearsSeparated)
#                print(i.partner.numberPartner)
#                
#                sys.exit()
                
        self.movePeopleIntoChosenHouse(newHouse, departureHouse, personList, calledBy)
        
        return newHouse
        
    def movePeopleIntoChosenHouse(self, newHouse, departureHouse, personList, calledBy):
        
        if len(newHouse.occupants) ==  0:
            newHouse.initialOccupants = len(personList)
        
        if ( newHouse == departureHouse):
            print('Error: new house is departure house')
            
        for i in personList:
            
            oldHouse = i.house
            
            repetitions = personList.count(i)
            if repetitions > 1:
               print('Person ' + str(i.id) + ' is counted ' + str(repetitions) + ' times!')
             
            if i in newHouse.occupants:
               print('Person ' + str(i.id) + ' already in new house!')
               
            if oldHouse.town != newHouse.town:
                i.yearsInTown = 0
                
            oldHouse.occupants.remove(i)
            
            if len(oldHouse.occupants) ==  0:
                oldHouse.initialOccupants = 0
                self.map.occupiedHouses.remove(oldHouse)
                ##print "This house is now empty: ", oldHouse
#                if (self.p['interactiveGraphics']):
#                    self.canvas.itemconfig(oldHouse.icon, state='hidden')
            newHouse.occupants.append(i)
            i.house = newHouse
            i.movedThisYear = True
        
        if ( newHouse not in self.map.occupiedHouses):
            self.map.occupiedHouses.append(newHouse)
            
#        if (self.p['interactiveGraphics']):
#            self.canvas.itemconfig(newHouse.icon, state='normal')
            
        ## Check whether we've moved into the display house
        if newHouse == self.displayHouse:
            self.textUpdateList.append(str(self.year) + ": New people are moving into " + newHouse.name)
            messageString = ""
            for k in personList:
                messageString += "#" + str(k.id) + " "
            self.textUpdateList.append(messageString)
            
        if departureHouse == self.displayHouse:
            self.nextDisplayHouse = newHouse
        
#        for i in personList:
#            if i.partner != None and i.house != i.partner.house:
#                print('Error: couple not joined after step MovPeoChosenHouse')
#                print(calledBy)
#                print(i.id)
#                print(i.sex)
#                print(i.status)
#                print(i.classRank)
#                print(i.independentStatus)
#                print(i.yearIndependent)
#                print(i.age)
#                print(i.ageStartWorking)
#                print(i.justMarried)
#                print(i.yearMarried)
#                print(i.yearsSeparated)
#                print(i.numberPartner)
#                print('')
#                print(i.partner.id)
#                print(i.partner.sex)
#                print(i.partner.status)
#                print(i.partner.classRank)
#                print(i.partner.independentStatus)
#                print(i.partner.yearIndependent)
#                print(i.partner.age)
#                print(i.partner.ageStartWorking)
#                print(i.partner.justMarried)
#                print(i.partner.yearMarried)
#                print(i.partner.yearsSeparated)
#                print(i.partner.numberPartner)
#                
#                sys.exit()
    
    def householdSize(self):
        visitedHouses = []
        maxSize = 0
        numberOccupants = 0
        for person in self.pop.livingPeople:
            if person.house not in visitedHouses:
                visitedHouses.append(person.house)
                numberOccupants += len(person.house.occupants)
                if len(person.house.occupants) > maxSize:
                    maxSize = len(person.house.occupants)
        print('The most numerous household has a size of ' + str(maxSize))
    
    def saveStats(self):
        
        # Population stats
        adultPop = [x for x in self.pop.livingPeople if x.age >= self.p['minWorkingAge'] and x.status != 'student']
        receivers = [x for x in self.pop.livingPeople if x.age > 0 and x.careNeedLevel > 0]
        numReceivers = float(len(receivers))
        numAdultPop = float(len(adultPop))
        currentPop = float(len(self.pop.livingPeople))
        caringAgePop = [x for x in self.pop.livingPeople if x.age >= self.p['ageTeenagers']]
        caringWomenPop = [x for x in caringAgePop if x.sex == 'female']
        caringMenPop = [x for x in caringAgePop if x.sex == 'male']
        
        informalCarers = [x for x in self.pop.livingPeople if x.socialWork > 0]
        womenCarers = [x for x in informalCarers if x.sex == 'female']
        menCarers = [x for x in informalCarers if x.sex == 'male']
        shareCarers = float(len(informalCarers))/float(len(caringAgePop))
        shareWomenCarers = float(len(womenCarers))/float(len(caringWomenPop))
        shareMenCarers = float(len(menCarers))/float(len(caringMenPop))
        
        numParents = float(len([x for x in self.pop.livingPeople if len(x.children) > 0]))
        numDistantParents = float(len([x for x in self.pop.livingPeople if len([y for y in x.children if y.house.town != x.house.town]) > 0]))
        shareDistantParents = 0
        if numParents> 0:
            shareDistantParents = numDistantParents/numParents
        
        totQALY = sum([x.qaly for x in receivers])
        meanQALY = 0
        if numReceivers > 0:
            meanQALY = totQALY/numReceivers
        
        
        meanQALY = totQALY/currentPop
        
        discountedQALY = 0
        if self.year >= self.p['implementPoliciesFromYear']:
            discountedQALY = totQALY/math.pow(1+self.p['qalyDiscountRate'], self.year-self.p['implementPoliciesFromYear'])
            
        averageDiscountedQALY = 0
        if self.year >= self.p['implementPoliciesFromYear']:
            averageDiscountedQALY = (totQALY/math.pow(1+self.p['qalyDiscountRate'], self.year-self.p['implementPoliciesFromYear']))/currentPop
        
        # Lone Parents
        parents = []
        for person in adultPop:
            for child in person.children:
                if person.house == child.house and (child.age <= 15 or (child.age <= 18 and child.status == 'student')): #self.p['maxWtWChildAge']:
                    parents.append(person)
                    break
        numberParents = len(parents)
        loneParents = []
        for person in parents:
            for child in person.children:
                if person.house == child.house and person.partner == None and (child.age <= 15 or (child.age <= 18 and child.status == 'student')): #self.p['maxWtWChildAge']:
                    loneParents.append(person)
                    break
        numberLoneParents = len(loneParents)
        shareLoneParents = float(numberLoneParents)/float(numberParents)
        
        print 'Share of lone parents: ' + str(shareLoneParents)
        
        # Compute line parents' shares by social class
        
        unskilled = [x for x in adultPop if x.classRank == 0]
        numUnskilled = float(len(unskilled))
        shareUnskilled = numUnskilled/numAdultPop
        print(shareUnskilled)

        skilled = [x for x in adultPop if x.classRank == 1]
        numSkilled = float(len(skilled))
        shareSkilled = numSkilled/numAdultPop
        print(shareSkilled)

        lowerclass = [x for x in adultPop if x.classRank == 2]
        numLowClass = float(len(lowerclass))
        shareLowClass = numLowClass/numAdultPop
        print(shareLowClass)

        middleclass = [x for x in adultPop if x.classRank == 3]
        numMidClass = float(len(middleclass))
        shareMidClass = numMidClass/numAdultPop
        print(shareMidClass)

        upperclass = [x for x in adultPop if x.classRank == 4]
        numUpClass = float(len(upperclass))
        shareUpClass = numUpClass/numAdultPop
        print(shareUpClass)
        
        ## Check for double-included houses by converting to a set and back again
        pre_checkLength = len(self.map.occupiedHouses)
        self.map.occupiedHouses = list(set(self.map.occupiedHouses))
        numOccupiedHouses = len(self.map.occupiedHouses)
        if pre_checkLength != numOccupiedHouses:
            print('Warning: list of occupied houses contains double-counted houses')
        averageHouseholdSize = float(numOccupiedHouses)/float(currentPop)

        #  Graph 34 #  if x.independentStatus == True
        households_1 = [h for h in self.map.occupiedHouses if max([x.classRank for x in h.occupants]) == 0]
        numHouseholds_1 = float(len(households_1))
        occupants_1 = 0.0
        for h in households_1:
            occupants_1 += float(len(h.occupants))
        averageHouseholdSize_1 = 0
        if numHouseholds_1 > 0:
            averageHouseholdSize_1 = occupants_1/numHouseholds_1
        
        households_2 = [h for h in self.map.occupiedHouses if max([x.classRank for x in h.occupants]) == 1]
        numHouseholds_2 = float(len(households_2))
        occupants_2 = 0.0
        for h in households_2:
            occupants_2 += float(len(h.occupants))
        averageHouseholdSize_2 = 0
        if numHouseholds_2 > 0:
            averageHouseholdSize_2 = occupants_2/numHouseholds_2
            
        households_3 = [h for h in self.map.occupiedHouses if max([x.classRank for x in h.occupants]) == 2]
        numHouseholds_3 = float(len(households_3))
        occupants_3 = 0.0
        for h in households_3:
            occupants_3 += float(len(h.occupants))
        averageHouseholdSize_3 = 0
        if numHouseholds_3 > 0:
            averageHouseholdSize_3 = occupants_3/numHouseholds_3
            
        households_4 = [h for h in self.map.occupiedHouses if max([x.classRank for x in h.occupants]) == 3]
        numHouseholds_4 = float(len(households_4))
        occupants_4 = 0.0
        for h in households_4:
            occupants_4 += float(len(h.occupants))
        averageHouseholdSize_4 = 0
        if numHouseholds_4 > 0:
            averageHouseholdSize_4 = occupants_4/numHouseholds_4
            
        households_5 = [h for h in self.map.occupiedHouses if max([x.classRank for x in h.occupants]) == 4]
        numHouseholds_5 = float(len(households_5))
        occupants_5 = 0.0
        for h in households_5:
            occupants_5 += float(len(h.occupants))
        averageHouseholdSize_5 = 0
        if numHouseholds_5 > 0:
            averageHouseholdSize_5 = occupants_5/numHouseholds_5
        
        # Graph 36
        totalAdultWomen = [x for x in self.pop.livingPeople if x.sex == 'female' and x.age >= self.p['minPregnancyAge']]
        numtotalAdultWomen = float(len(totalAdultWomen))
        totalMarriedAdultWomen = float(len([x for x in totalAdultWomen if x.partner != None]))
        marriageProp = 0
        if numtotalAdultWomen > 0:
            marriageProp = totalMarriedAdultWomen/numtotalAdultWomen
            
        informalCareSupply = sum([x.hoursInformalSupplies[0] for x in self.pop.livingPeople])
        visitedHousehold = []
        formalCareSupply = 0
        for x in self.pop.livingPeople:
            if x.house in visitedHousehold:
                continue
            visitedHousehold.append(x.house)
            formalCareSupply += x.hoursFormalSupply[0]
        
        # Graph 1
        totalCareSupply = informalCareSupply + formalCareSupply
        totalCareNeed = sum([x.hoursDemand for x in self.pop.livingPeople])
        unmetCareNeed = sum([x.residualNeed for x in self.pop.livingPeople])
        socialCareNeed = sum([x.hoursDemand for x in self.pop.livingPeople if x.socialCareReceiver == True])
        childCareNeed = totalCareNeed - socialCareNeed
        
        # Graph 2
        totalCareSuppliers = len([x for x in self.pop.livingPeople if x.hoursDemand == 0 and x.age >= self.p['ageTeenagers']])
        shareCareGivers = float(totalCareSuppliers)/currentPop
        
        class_1 = [x for x in self.pop.livingPeople if x.classRank == 0]
        numClass_1 = float(len(class_1))
        careGivers_1 = len([x for x in class_1 if x.hoursDemand == 0 and x.age >= self.p['ageTeenagers']])
        shareCareGivers_1 = float(careGivers_1)/numClass_1
        
        
        class_2 = [x for x in self.pop.livingPeople if x.classRank == 1]
        numClass_2 = float(len(class_2))
        careGivers_2 = len([x for x in class_2 if x.hoursDemand == 0 and x.age >= self.p['ageTeenagers']])
        shareCareGivers_2 = float(careGivers_2)/numClass_2
        
        class_3 = [x for x in self.pop.livingPeople if x.classRank == 2]
        numClass_3 = float(len(class_3))
        careGivers_3 = len([x for x in class_3 if x.hoursDemand == 0 and x.age >= self.p['ageTeenagers']])
        shareCareGivers_3 = float(careGivers_3)/numClass_3
        
        class_4 = [x for x in self.pop.livingPeople if x.classRank == 3]
        numClass_4 = float(len(class_4))
        careGivers_4 = len([x for x in class_4 if x.hoursDemand == 0 and x.age >= self.p['ageTeenagers']])
        shareCareGivers_4 = float(careGivers_4)/numClass_4
        
        class_5 = [x for x in self.pop.livingPeople if x.classRank == 4]
        numClass_5 = float(len(class_5))
        careGivers_5 = len([x for x in class_5 if x.hoursDemand == 0 and x.age >= self.p['ageTeenagers']])
        shareCareGivers_5 = float(careGivers_5)/numClass_5

        # Graph 3
        socialCareReceivers = [x for x in self.pop.livingPeople if x.hoursDemand > 0 and x.socialCareReceiver == True]
        totalSocialCareReceivers = float(len(socialCareReceivers))
        totalSocialCareReceivers_N1 = float(len([x for x in socialCareReceivers if x.careNeedLevel == 1]))
        informalSocialCareReceived_N1 = sum([x.informalCare for x in socialCareReceivers if x.careNeedLevel == 1])
        formalSocialCareReceived_N1 = sum([x.formalCare for x in socialCareReceivers if x.careNeedLevel == 1])
        unmetSocialCareNeed_N1 = sum([x.residualNeed for x in socialCareReceivers if x.careNeedLevel == 1])
        meanInformalSocialCareReceived_N1 = 0
        meanFormalSocialCareReceived_N1 = 0
        meanUnmetSocialCareNeed_N1 = 0
        if totalSocialCareReceivers_N1 > 0:
            meanInformalSocialCareReceived_N1 = informalSocialCareReceived_N1/totalSocialCareReceivers_N1
            meanFormalSocialCareReceived_N1 = formalSocialCareReceived_N1/totalSocialCareReceivers_N1
            meanUnmetSocialCareNeed_N1 = unmetSocialCareNeed_N1/totalSocialCareReceivers_N1
        
        totalSocialCareReceivers_N2 = float(len([x for x in socialCareReceivers if x.careNeedLevel == 2]))
        informalSocialCareReceived_N2 = sum([x.informalCare for x in socialCareReceivers if x.careNeedLevel == 2])
        formalSocialCareReceived_N2 = sum([x.formalCare for x in socialCareReceivers if x.careNeedLevel == 2])
        unmetSocialCareNeed_N2 = sum([x.residualNeed for x in socialCareReceivers if x.careNeedLevel == 2])
        meanInformalSocialCareReceived_N2 = 0
        meanFormalSocialCareReceived_N2 = 0
        meanUnmetSocialCareNeed_N2 = 0
        if totalSocialCareReceivers_N2 > 0:
            meanInformalSocialCareReceived_N2 = informalSocialCareReceived_N2/totalSocialCareReceivers_N2
            meanFormalSocialCareReceived_N2 = formalSocialCareReceived_N2/totalSocialCareReceivers_N2
            meanUnmetSocialCareNeed_N2 = unmetSocialCareNeed_N2/totalSocialCareReceivers_N2
        
        totalSocialCareReceivers_N3 = float(len([x for x in socialCareReceivers if x.careNeedLevel == 3]))
        informalSocialCareReceived_N3 = sum([x.informalCare for x in socialCareReceivers if x.careNeedLevel == 3])
        formalSocialCareReceived_N3 = sum([x.formalCare for x in socialCareReceivers if x.careNeedLevel == 3])
        unmetSocialCareNeed_N3 = sum([x.residualNeed for x in socialCareReceivers if x.careNeedLevel == 3])
        meanInformalSocialCareReceived_N3 = 0
        meanFormalSocialCareReceived_N3 = 0
        meanUnmetSocialCareNeed_N3 = 0
        if totalSocialCareReceivers_N3 > 0:
            meanInformalSocialCareReceived_N3 = informalSocialCareReceived_N3/totalSocialCareReceivers_N3
            meanFormalSocialCareReceived_N3 = formalSocialCareReceived_N3/totalSocialCareReceivers_N3
            meanUnmetSocialCareNeed_N3 = unmetSocialCareNeed_N3/totalSocialCareReceivers_N3
            
        totalSocialCareReceivers_N4 = float(len([x for x in socialCareReceivers if x.careNeedLevel == 4]))
        informalSocialCareReceived_N4 = sum([x.informalCare for x in socialCareReceivers if x.careNeedLevel == 4])
        formalSocialCareReceived_N4 = sum([x.formalCare for x in socialCareReceivers if x.careNeedLevel == 4])
        unmetSocialCareNeed_N4 = sum([x.residualNeed for x in socialCareReceivers if x.careNeedLevel == 4])
        meanInformalSocialCareReceived_N4 = 0
        meanFormalSocialCareReceived_N4 = 0
        meanUnmetSocialCareNeed_N4 = 0
        if totalSocialCareReceivers_N4 > 0:
            meanInformalSocialCareReceived_N4 = informalSocialCareReceived_N4/totalSocialCareReceivers_N4
            meanFormalSocialCareReceived_N4 = formalSocialCareReceived_N4/totalSocialCareReceivers_N4
            meanUnmetSocialCareNeed_N4 = unmetSocialCareNeed_N4/totalSocialCareReceivers_N4
            
        shareSocialCareTakers_N1 = 0
        shareSocialCareTakers_N2 = 0
        shareSocialCareTakers_N3 = 0
        shareSocialCareTakers_N4 = 0
        if totalSocialCareReceivers > 0:
            shareSocialCareTakers_N1 = totalSocialCareReceivers_N1/totalSocialCareReceivers
            shareSocialCareTakers_N2 = totalSocialCareReceivers_N2/totalSocialCareReceivers
            shareSocialCareTakers_N3 = totalSocialCareReceivers_N3/totalSocialCareReceivers
            shareSocialCareTakers_N4 = totalSocialCareReceivers_N4/totalSocialCareReceivers
        
            
        # Graph 4
        shareSocialCareDemand = 0
        if totalCareNeed > 0:
            shareSocialCareDemand = socialCareNeed/totalCareNeed
        
        inactivePeople_1 = [x for x in class_1 if x.socialCareReceiver == True]
        totalCareDemand_1 = float(sum([x.hoursDemand for x in class_1]))
        socialCareDemand_1 = float(sum([x.hoursDemand for x in inactivePeople_1]))
        shareSocialCare_1 = 0
        if totalCareDemand_1 > 0:
            shareSocialCare_1 = socialCareDemand_1/totalCareDemand_1
        
        inactivePeople_2 = [x for x in class_2 if x.socialCareReceiver == True]
        totalCareDemand_2 = float(sum([x.hoursDemand for x in class_2]))
        socialCareDemand_2 = float(sum([x.hoursDemand for x in inactivePeople_2]))
        shareSocialCare_2 = 0
        if totalCareDemand_2 > 0:
            shareSocialCare_2 = socialCareDemand_2/totalCareDemand_2
        
        inactivePeople_3 = [x for x in class_3 if x.socialCareReceiver == True]
        totalCareDemand_3 = float(sum([x.hoursDemand for x in class_3]))
        socialCareDemand_3 = float(sum([x.hoursDemand for x in inactivePeople_3]))
        shareSocialCare_3 = 0
        if totalCareDemand_3 > 0:
            shareSocialCare_3 = socialCareDemand_3/totalCareDemand_3
        
        inactivePeople_4 = [x for x in class_4 if x.socialCareReceiver == True]
        totalCareDemand_4 = float(sum([x.hoursDemand for x in class_4]))
        socialCareDemand_4 = float(sum([x.hoursDemand for x in inactivePeople_4]))
        shareSocialCare_4 = 0
        if totalCareDemand_4 > 0:
            shareSocialCare_4 = socialCareDemand_4/totalCareDemand_4
        
        inactivePeople_5 = [x for x in class_5 if x.socialCareReceiver == True]
        totalCareDemand_5 = float(sum([x.hoursDemand for x in class_5]))
        socialCareDemand_5 = float(sum([x.hoursDemand for x in inactivePeople_5]))
        shareSocialCare_5 = 0
        if totalCareDemand_5 > 0:
            shareSocialCare_5 = socialCareDemand_5/totalCareDemand_5
        
        # Graph 8
        informalCareReceived = sum([x.informalCare for x in self.pop.livingPeople])
        formalCareReceived = sum([x.formalCare for x in self.pop.livingPeople])
        totalCareReceived = informalCareReceived + formalCareReceived
        totalUnnmetCareNeed = sum([x.residualNeed for x in self.pop.livingPeople])
        
        # Graph 5 
        perCapitaCareReceived = totalCareReceived/currentPop
        perCapitaUnmetCareDemand = totalUnnmetCareNeed/currentPop
        
        # Graph 12
        informalSocialCareReceived = sum([x.informalCare for x in self.pop.livingPeople if x.socialCareReceiver == True])
        formalSocialCareReceived = sum([x.formalCare for x in self.pop.livingPeople if x.socialCareReceiver == True])
        socialCareReceived = informalSocialCareReceived + formalSocialCareReceived
        unmetSocialCareNeed = sum([x.residualNeed for x in self.pop.livingPeople if x.socialCareReceiver == True])
        
        if socialCareReceived != 0:
            print 'Share of unmet social care:' + str(unmetSocialCareNeed/socialCareReceived)
        
        # Graph 6
        perCapitaSocialCareReceived = socialCareReceived/currentPop
        perCapitaUnmetSocialCareDemand = unmetSocialCareNeed/currentPop
        
        # Graph 13
        informalChildCareReceived = sum([x.informalCare for x in self.pop.livingPeople if x.status == 'child'])
        formalChildCareReceived = sum([x.formalCare for x in self.pop.livingPeople if x.status == 'child'])
        childCareReceived = informalChildCareReceived + formalChildCareReceived
        unmetChildCareNeed = sum([x.residualNeed for x in self.pop.livingPeople if x.status == 'child'])
        
        # Graph 7
        perCapitaChildCareReceived = childCareReceived/currentPop
        perCapitaUnmetChildCareDemand = unmetChildCareNeed/currentPop
        
        # Graph 9: 
        shareInformalCareReceived = 0
        if totalCareReceived > 0:
            shareInformalCareReceived = informalCareReceived/totalCareReceived
        
        informalSocialCareReceived_1 = sum([x.informalCare for x in class_1 if x.socialCareReceiver == True])
        formalSocialCareReceived_1 = sum([x.formalCare for x in class_1 if x.socialCareReceiver == True])
        socialCareReceived_1 = informalSocialCareReceived_1 + formalSocialCareReceived_1
        informalChildCareReceived_1 = sum([x.informalCare for x in class_1 if x.status == 'child'])
        formalChildCareReceived_1 = sum([x.formalCare for x in class_1 if x.status == 'child'])
        childCareReceived_1 = informalChildCareReceived_1 + formalChildCareReceived_1
        totalInformalCare_1 = informalChildCareReceived_1 + informalSocialCareReceived_1
        totalFormalCare_1 = formalChildCareReceived_1 + formalSocialCareReceived_1
        totalCare_1 = socialCareReceived_1 + childCareReceived_1
        shareInformalCareReceived_1 = 0
        if totalCare_1 > 0:
            shareInformalCareReceived_1 = totalInformalCare_1/totalCare_1
        
        informalSocialCareReceived_2 = sum([x.informalCare for x in class_2 if x.socialCareReceiver == True])
        formalSocialCareReceived_2 = sum([x.formalCare for x in class_2 if x.socialCareReceiver == True])
        socialCareReceived_2 = informalSocialCareReceived_2 + formalSocialCareReceived_2
        informalChildCareReceived_2 = sum([x.informalCare for x in class_2 if x.status == 'child'])
        formalChildCareReceived_2 = sum([x.formalCare for x in class_2 if x.status == 'child'])
        childCareReceived_2 = informalChildCareReceived_2 + formalChildCareReceived_2
        totalInformalCare_2 = informalChildCareReceived_2 + informalSocialCareReceived_2
        totalFormalCare_2 = formalChildCareReceived_2 + formalSocialCareReceived_2
        totalCare_2 = socialCareReceived_2 + childCareReceived_2
        shareInformalCareReceived_2 = 0
        if totalCare_2 > 0:
            shareInformalCareReceived_2 = totalInformalCare_2/totalCare_2
        
        informalSocialCareReceived_3 = sum([x.informalCare for x in class_3 if x.socialCareReceiver == True])
        formalSocialCareReceived_3 = sum([x.formalCare for x in class_3 if x.socialCareReceiver == True])
        socialCareReceived_3 = informalSocialCareReceived_3 + formalSocialCareReceived_3
        informalChildCareReceived_3 = sum([x.informalCare for x in class_3 if x.status == 'child'])
        formalChildCareReceived_3 = sum([x.formalCare for x in class_3 if x.status == 'child'])
        childCareReceived_3 = informalChildCareReceived_3 + formalChildCareReceived_3
        totalInformalCare_3 = informalChildCareReceived_3 + informalSocialCareReceived_3
        totalFormalCare_3 = formalChildCareReceived_3 + formalSocialCareReceived_3
        totalCare_3 = socialCareReceived_3 + childCareReceived_3
        shareInformalCareReceived_3 = 0
        if totalCare_3 > 0:
            shareInformalCareReceived_3 = totalInformalCare_3/totalCare_3
        
        informalSocialCareReceived_4 = sum([x.informalCare for x in class_4 if x.socialCareReceiver == True])
        formalSocialCareReceived_4 = sum([x.formalCare for x in class_4 if x.socialCareReceiver == True])
        socialCareReceived_4 = informalSocialCareReceived_4 + formalSocialCareReceived_4
        informalChildCareReceived_4 = sum([x.informalCare for x in class_4 if x.status == 'child'])
        formalChildCareReceived_4 = sum([x.formalCare for x in class_4 if x.status == 'child'])
        childCareReceived_4 = informalChildCareReceived_4 + formalChildCareReceived_4
        totalInformalCare_4 = informalChildCareReceived_4 + informalSocialCareReceived_4
        totalFormalCare_4 = formalChildCareReceived_4 + formalSocialCareReceived_4
        totalCare_4 = socialCareReceived_4 + childCareReceived_4
        shareInformalCareReceived_4 = 0
        if totalCare_4 > 0:
            shareInformalCareReceived_4 = totalInformalCare_4/totalCare_4
        
        informalSocialCareReceived_5 = sum([x.informalCare for x in class_5 if x.socialCareReceiver == True])
        formalSocialCareReceived_5 = sum([x.formalCare for x in class_5 if x.socialCareReceiver == True])
        socialCareReceived_5 = informalSocialCareReceived_5 + formalSocialCareReceived_5
        informalChildCareReceived_5 = sum([x.informalCare for x in class_5 if x.status == 'child'])
        formalChildCareReceived_5 = sum([x.formalCare for x in class_5 if x.status == 'child'])
        childCareReceived_5 = informalChildCareReceived_5 + formalChildCareReceived_5
        totalInformalCare_5 = informalChildCareReceived_5 + informalSocialCareReceived_5
        totalFormalCare_5 = formalChildCareReceived_5 + formalSocialCareReceived_5
        totalCare_5 = socialCareReceived_5 + childCareReceived_5
        shareInformalCareReceived_5 = 0
        if totalCare_5 > 0:
            shareInformalCareReceived_5 = totalInformalCare_5/totalCare_5
        
        # Graph 10: 
        shareInformalSocialCare = 0
        if socialCareReceived > 0:
            shareInformalSocialCare = informalSocialCareReceived/socialCareReceived
        shareInformalSocialCare_1 = 0
        if socialCareReceived_1 > 0:
            shareInformalSocialCare_1 = informalSocialCareReceived_1/socialCareReceived_1
        shareInformalSocialCare_2 = 0
        if socialCareReceived_2 > 0:
            shareInformalSocialCare_2 = informalSocialCareReceived_2/socialCareReceived_2
        shareInformalSocialCare_3 = 0
        if socialCareReceived_3 > 0:
            shareInformalSocialCare_3 = informalSocialCareReceived_3/socialCareReceived_3
        shareInformalSocialCare_4 = 0
        if socialCareReceived_4 > 0:
            shareInformalSocialCare_4 = informalSocialCareReceived_4/socialCareReceived_4
        shareInformalSocialCare_5 = 0
        if socialCareReceived_5 > 0:
            shareInformalSocialCare_5 = informalSocialCareReceived_5/socialCareReceived_5
        
        # Garph 11
        shareInformalChildCare = 0
        if childCareReceived > 0:
            shareInformalChildCare = informalChildCareReceived/childCareReceived
        shareInformalChildCare_1 = 0
        if childCareReceived_1 > 0:
            shareInformalChildCare_1 = informalChildCareReceived_1/childCareReceived_1
        shareInformalChildCare_2 = 0
        if childCareReceived_2 > 0:
            shareInformalChildCare_2 = informalChildCareReceived_2/childCareReceived_2
        shareInformalChildCare_3 = 0
        if childCareReceived_3 > 0:
            shareInformalChildCare_3 = informalChildCareReceived_3/childCareReceived_3
        shareInformalChildCare_4 = 0
        if childCareReceived_4 > 0:
            shareInformalChildCare_4 = informalChildCareReceived_4/childCareReceived_4
        shareInformalChildCare_5 = 0
        if childCareReceived_5 > 0:
            shareInformalChildCare_5 = informalChildCareReceived_5/childCareReceived_5
        
        # Graph 14
        shareUnmetCareDemand = 0
        if totalCareNeed > 0:
            shareUnmetCareDemand = totalUnnmetCareNeed/totalCareNeed
        
        unmetCareNeed_1 = sum([x.residualNeed for x in class_1])
        shareUnmetCareDemand_1 = 0
        if totalCareDemand_1 > 0:
            shareUnmetCareDemand_1 = unmetCareNeed_1/totalCareDemand_1
        
        unmetCareNeed_2 = sum([x.residualNeed for x in class_2])
        shareUnmetCareDemand_2 = 0
        if totalCareDemand_2 > 0:
            shareUnmetCareDemand_2 = unmetCareNeed_2/totalCareDemand_2
        
        unmetCareNeed_3 = sum([x.residualNeed for x in class_3])
        shareUnmetCareDemand_3 = 0
        if totalCareDemand_3 > 0:
            shareUnmetCareDemand_3 = unmetCareNeed_3/totalCareDemand_3
        
        unmetCareNeed_4 = sum([x.residualNeed for x in class_4])
        shareUnmetCareDemand_4 = 0
        if totalCareDemand_4 > 0:
            shareUnmetCareDemand_4 = unmetCareNeed_4/totalCareDemand_4
        
        unmetCareNeed_5 = sum([x.residualNeed for x in class_5])
        shareUnmetCareDemand_5 = 0
        if totalCareDemand_5 > 0:
            shareUnmetCareDemand_5 = unmetCareNeed_5/totalCareDemand_5
        
        # Graph 15
        totalSocialCareNeed = sum([x.hoursDemand for x in self.pop.livingPeople if x.socialCareReceiver == True])
        shareUnmetSocialCareDemand = 0
        if totalSocialCareNeed > 0:
            shareUnmetSocialCareDemand = unmetSocialCareNeed/totalSocialCareNeed
        
        unmetSocialCareNeed_1 = sum([x.residualNeed for x in class_1 if x.socialCareReceiver == True])
        totalSocialCareNeed_1 = sum([x.hoursDemand for x in class_1 if x.socialCareReceiver == True])
        shareUnmetSocialCareDemand_1 = 0
        if totalSocialCareNeed_1 > 0:
            shareUnmetSocialCareDemand_1 = unmetSocialCareNeed_1/totalSocialCareNeed_1
        
        unmetSocialCareNeed_2 = sum([x.residualNeed for x in class_2 if x.socialCareReceiver == True])
        totalSocialCareNeed_2 = sum([x.hoursDemand for x in class_2 if x.socialCareReceiver == True])
        shareUnmetSocialCareDemand_2 = 0
        if totalSocialCareNeed_2 > 0:
            shareUnmetSocialCareDemand_2 = unmetSocialCareNeed_2/totalSocialCareNeed_2
        
        unmetSocialCareNeed_3 = sum([x.residualNeed for x in class_3 if x.socialCareReceiver == True])
        totalSocialCareNeed_3 = sum([x.hoursDemand for x in class_3 if x.socialCareReceiver == True])
        shareUnmetSocialCareDemand_3 = 0
        if totalSocialCareNeed_3 > 0:
            shareUnmetSocialCareDemand_3 = unmetSocialCareNeed_3/totalSocialCareNeed_3
        
        unmetSocialCareNeed_4 = sum([x.residualNeed for x in class_4 if x.socialCareReceiver == True])
        totalSocialCareNeed_4 = sum([x.hoursDemand for x in class_4 if x.socialCareReceiver == True])
        shareUnmetSocialCareDemand_4 = 0
        if totalSocialCareNeed_4 > 0:
            shareUnmetSocialCareDemand_4 = unmetSocialCareNeed_4/totalSocialCareNeed_4
        
        unmetSocialCareNeed_5 = sum([x.residualNeed for x in class_5 if x.socialCareReceiver == True])
        totalSocialCareNeed_5 = sum([x.hoursDemand for x in class_5 if x.socialCareReceiver == True])
        shareUnmetSocialCareDemand_5 = 0
        if totalSocialCareNeed_5 > 0:
            shareUnmetSocialCareDemand_5 = unmetSocialCareNeed_5/totalSocialCareNeed_5
        
        # Graph 16
        totalChildCareNeed = sum([x.hoursDemand for x in self.pop.livingPeople if x.status == 'child'])
        shareUnmetChildCareDemand = 0
        if totalChildCareNeed > 0:
            shareUnmetChildCareDemand = unmetChildCareNeed/totalChildCareNeed
        
        unmetChildCareNeed_1 = sum([x.residualNeed for x in class_1 if x.status == 'child'])
        totalChildCareNeed_1 = sum([x.hoursDemand for x in class_1 if x.status == 'child'])
        shareUnmetChildCareDemand_1 = 0
        if totalChildCareNeed_1 > 0:
            shareUnmetChildCareDemand_1 = unmetChildCareNeed_1/totalChildCareNeed_1
        
        unmetChildCareNeed_2 = sum([x.residualNeed for x in class_2 if x.status == 'child'])
        totalChildCareNeed_2 = sum([x.hoursDemand for x in class_2 if x.status == 'child'])
        shareUnmetChildCareDemand_2 = 0
        if totalChildCareNeed_2 > 0:
            shareUnmetChildCareDemand_2 = unmetChildCareNeed_2/totalChildCareNeed_2
        
        unmetChildCareNeed_3 = sum([x.residualNeed for x in class_3 if x.status == 'child'])
        totalChildCareNeed_3 = sum([x.hoursDemand for x in class_3 if x.status == 'child'])
        shareUnmetChildCareDemand_3 = 0
        if totalChildCareNeed_3 > 0:
            shareUnmetChildCareDemand_3 = unmetChildCareNeed_3/totalChildCareNeed_3
        
        unmetChildCareNeed_4 = sum([x.residualNeed for x in class_4 if x.status == 'child'])
        totalChildCareNeed_4 = sum([x.hoursDemand for x in class_4 if x.status == 'child'])
        shareUnmetChildCareDemand_4 = 0
        if totalChildCareNeed_4 > 0:
            shareUnmetChildCareDemand_4 = unmetChildCareNeed_4/totalChildCareNeed_4
        
        unmetChildCareNeed_5 = sum([x.residualNeed for x in class_5 if x.status == 'child'])
        totalChildCareNeed_5 = sum([x.hoursDemand for x in class_5 if x.status == 'child'])
        shareUnmetChildCareDemand_5 = 0
        if totalChildCareNeed_5 > 0:
            shareUnmetChildCareDemand_5 = unmetChildCareNeed_5/totalChildCareNeed_5
        
        # Graph 17
        perCapitaUnmetCareDemand_1 = 0
        if numClass_1 > 0:
            perCapitaUnmetCareDemand_1 = unmetCareNeed_1/numClass_1
        perCapitaUnmetCareDemand_2 = 0
        if numClass_2 > 0:
            perCapitaUnmetCareDemand_2 = unmetCareNeed_2/numClass_2
        perCapitaUnmetCareDemand_3 = 0
        if numClass_3 > 0:
            perCapitaUnmetCareDemand_3 = unmetCareNeed_3/numClass_3
        perCapitaUnmetCareDemand_4 = 0
        if numClass_4 > 0:
            perCapitaUnmetCareDemand_4 = unmetCareNeed_4/numClass_4
        perCapitaUnmetCareDemand_5 = 0
        if numClass_5 > 0:
            perCapitaUnmetCareDemand_5 = unmetCareNeed_5/numClass_5
        
        # Graph 18
        numReceivers = float(len([x for x in self.pop.livingPeople if x.hoursDemand > 0]))
        averageUnmetCareDemand = 0
        if numReceivers > 0:
            averageUnmetCareDemand = totalUnnmetCareNeed/numReceivers
        
        numReceivers_1 = float(len([x for x in class_1 if x.hoursDemand > 0]))
        averageUnmetCareDemand_1 = 0
        if numReceivers_1 > 0:
            averageUnmetCareDemand_1 = unmetCareNeed_1/numReceivers_1
        
        numReceivers_2 = float(len([x for x in class_2 if x.hoursDemand > 0]))
        averageUnmetCareDemand_2 = 0
        if numReceivers_2 > 0:
            averageUnmetCareDemand_2 = unmetCareNeed_2/numReceivers_2
        
        numReceivers_3 = float(len([x for x in class_3 if x.hoursDemand > 0]))
        averageUnmetCareDemand_3 = 0
        if numReceivers_3 > 0:
            averageUnmetCareDemand_3 = unmetCareNeed_3/numReceivers_3
        
        numReceivers_4 = float(len([x for x in class_4 if x.hoursDemand > 0]))
        averageUnmetCareDemand_4 = 0
        if numReceivers_4 > 0:
            averageUnmetCareDemand_4 = unmetCareNeed_4/numReceivers_4
        
        numReceivers_5 = float(len([x for x in class_5 if x.hoursDemand > 0]))
        averageUnmetCareDemand_5 = 0
        if numReceivers_5 > 0:
            averageUnmetCareDemand_5 = unmetCareNeed_5/numReceivers_5
        
        # Graph 19
        informalCareReceived_1 = sum([x.informalCare for x in class_1])
        formalCareReceived_1 = sum([x.formalCare for x in class_1])
        
        informalCareReceived_2 = sum([x.informalCare for x in class_2])
        formalCareReceived_2 = sum([x.formalCare for x in class_2])
        
        informalCareReceived_3 = sum([x.informalCare for x in class_3])
        formalCareReceived_3 = sum([x.formalCare for x in class_3])
        
        informalCareReceived_4 = sum([x.informalCare for x in class_4])
        formalCareReceived_4 = sum([x.formalCare for x in class_4])
        
        informalCareReceived_5 = sum([x.informalCare for x in class_5])
        formalCareReceived_5 = sum([x.formalCare for x in class_5])
        
        # Graph 20 and 42 and Additional Chart
        totalInformalCare = informalSocialCareReceived + informalChildCareReceived
        totalFormalCare = formalSocialCareReceived + formalChildCareReceived
        informalCarePerRecipient = 0
        formalCarePerRecipient = 0
        carePerRecipient = 0
        unmetCarePerRecipient = 0
        if numReceivers > 0:
            informalCarePerRecipient = totalInformalCare/numReceivers
            formalCarePerRecipient = totalFormalCare/numReceivers
            carePerRecipient = informalCarePerRecipient + formalCarePerRecipient
            unmetCarePerRecipient = unmetCareNeed/numReceivers
        
        informalCarePerRecipient_1 = 0
        formalCarePerRecipient_1 = 0
        carePerRecipient_1 = 0
        unmetCarePerRecipient_1 = 0
        if numReceivers_1 > 0:
            informalCarePerRecipient_1 = totalInformalCare_1/numReceivers_1
            formalCarePerRecipient_1 = totalFormalCare_1/numReceivers_1
            carePerRecipient_1 = informalCarePerRecipient_1 + formalCarePerRecipient_1
            unmetCarePerRecipient_1 = unmetCareNeed_1/numReceivers_1
        
        informalCarePerRecipient_2 = 0
        formalCarePerRecipient_2 = 0
        carePerRecipient_2 = 0
        unmetCarePerRecipient_2 = 0
        if numReceivers_2 > 0:
            informalCarePerRecipient_2 = totalInformalCare_2/numReceivers_2
            formalCarePerRecipient_2 = totalFormalCare_2/numReceivers_2
            carePerRecipient_2 = informalCarePerRecipient_2 + formalCarePerRecipient_2
            unmetCarePerRecipient_2 = unmetCareNeed_2/numReceivers_2
        
        informalCarePerRecipient_3 = 0
        formalCarePerRecipient_3 = 0
        carePerRecipient_3 = 0
        unmetCarePerRecipient_3 = 0
        if numReceivers_3 > 0:
            informalCarePerRecipient_3 = totalInformalCare_3/numReceivers_3
            formalCarePerRecipient_3 = totalFormalCare_3/numReceivers_3
            carePerRecipient_3 = informalCarePerRecipient_3 + formalCarePerRecipient_3
            unmetCarePerRecipient_3 = unmetCareNeed_3/numReceivers_3
        
        informalCarePerRecipient_4 = 0
        formalCarePerRecipient_4 = 0
        carePerRecipient_4 = 0
        unmetCarePerRecipient_4 = 0
        if numReceivers_4 > 0:
            informalCarePerRecipient_4 = totalInformalCare_4/numReceivers_4
            formalCarePerRecipient_4 = totalFormalCare_4/numReceivers_4
            carePerRecipient_4 = informalCarePerRecipient_4 + formalCarePerRecipient_4
            unmetCarePerRecipient_4 = unmetCareNeed_4/numReceivers_4
        
        informalCarePerRecipient_5 = 0
        formalCarePerRecipient_5 = 0
        carePerRecipient_5 = 0
        unmetCarePerRecipient_5 = 0
        if numReceivers_5 > 0:
            informalCarePerRecipient_5 = totalInformalCare_5/numReceivers_5
            formalCarePerRecipient_5 = totalFormalCare_5/numReceivers_5
            carePerRecipient_5 = informalCarePerRecipient_5 + formalCarePerRecipient_5
            unmetCarePerRecipient_5 = unmetCareNeed_5/numReceivers_5
        
        # Graph 21
        # informal and formal social care received and unmet social care need by class.
        
        # Graph 22 and Additional chart
        socialCareReceivers = float(len([x for x in self.pop.livingPeople if x.socialCareReceiver == True]))
        informalSocialCarePerRecipient = 0
        formalSocialCarePerRecipient = 0
        socialCarePerRecipient = 0
        unmetSocialCarePerRecipient = 0
        if socialCareReceivers > 0:
            informalSocialCarePerRecipient = informalSocialCareReceived/socialCareReceivers
            formalSocialCarePerRecipient = formalSocialCareReceived/socialCareReceivers
            socialCarePerRecipient = informalSocialCarePerRecipient + formalSocialCarePerRecipient
            unmetSocialCarePerRecipient = unmetSocialCareNeed/socialCareReceivers
        
        socialCareReceivers_1 = float(len([x for x in class_1 if x.socialCareReceiver == True]))
        informalSocialCarePerRecipient_1 = 0
        formalSocialCarePerRecipient_1 = 0
        socialCarePerRecipient_1 = 0
        unmetSocialCarePerRecipient_1 = 0
        if socialCareReceivers_1 > 0:
            informalSocialCarePerRecipient_1 = informalSocialCareReceived_1/socialCareReceivers_1
            formalSocialCarePerRecipient_1 = formalSocialCareReceived_1/socialCareReceivers_1
            socialCarePerRecipient_1 = informalSocialCarePerRecipient_1 + formalSocialCarePerRecipient_1
            unmetSocialCarePerRecipient_1 = unmetSocialCareNeed_1/socialCareReceivers_1
        
        socialCareReceivers_2 = float(len([x for x in class_2 if x.socialCareReceiver == True]))
        informalSocialCarePerRecipient_2 = 0
        formalSocialCarePerRecipient_2 = 0
        socialCarePerRecipient_2 = 0
        unmetSocialCarePerRecipient_2 = 0
        if socialCareReceivers_2 > 0:
            informalSocialCarePerRecipient_2 = informalSocialCareReceived_2/socialCareReceivers_2
            formalSocialCarePerRecipient_2 = formalSocialCareReceived_2/socialCareReceivers_2
            socialCarePerRecipient_2 = informalSocialCarePerRecipient_2 + formalSocialCarePerRecipient_2
            unmetSocialCarePerRecipient_2 = unmetSocialCareNeed_2/socialCareReceivers_2
        
        socialCareReceivers_3 = float(len([x for x in class_3 if x.socialCareReceiver == True]))
        informalSocialCarePerRecipient_3 = 0
        formalSocialCarePerRecipient_3 = 0
        socialCarePerRecipient_3 = 0
        unmetSocialCarePerRecipient_3 = 0
        if socialCareReceivers_3 > 0:
            informalSocialCarePerRecipient_3 = informalSocialCareReceived_3/socialCareReceivers_3
            formalSocialCarePerRecipient_3 = formalSocialCareReceived_3/socialCareReceivers_3
            socialCarePerRecipient_3 = informalSocialCarePerRecipient_3 + formalSocialCarePerRecipient_3
            unmetSocialCarePerRecipient_3 = unmetSocialCareNeed_3/socialCareReceivers_3
        
        socialCareReceivers_4 = float(len([x for x in class_4 if x.socialCareReceiver == True]))
        informalSocialCarePerRecipient_4 = 0
        formalSocialCarePerRecipient_4 = 0
        socialCarePerRecipient_4 = 0
        unmetSocialCarePerRecipient_4 = 0
        if socialCareReceivers_4 > 0:
            informalSocialCarePerRecipient_4 = informalSocialCareReceived_4/socialCareReceivers_4
            formalSocialCarePerRecipient_4 = formalSocialCareReceived_4/socialCareReceivers_4
            socialCarePerRecipient_4 = informalSocialCarePerRecipient_4 + formalSocialCarePerRecipient_4
            unmetSocialCarePerRecipient_4 = unmetSocialCareNeed_4/socialCareReceivers_4
        
        socialCareReceivers_5 = float(len([x for x in class_5 if x.socialCareReceiver == True]))
        informalSocialCarePerRecipient_5 = 0
        formalSocialCarePerRecipient_5 = 0
        socialCarePerRecipient_5 = 0
        unmetSocialCarePerRecipient_5 = 0
        if socialCareReceivers_5 > 0:
            informalSocialCarePerRecipient_5 = informalSocialCareReceived_5/socialCareReceivers_5
            formalSocialCarePerRecipient_5 = formalSocialCareReceived_5/socialCareReceivers_5
            socialCarePerRecipient_5 = informalSocialCarePerRecipient_5 + formalSocialCarePerRecipient_5
            unmetSocialCarePerRecipient_5 = unmetSocialCareNeed_5/socialCareReceivers_5
        
        # Graph 23
        # informal and formal child care received and unmet child care need by class.
        
        # Graph 24 and Additional Chart
        childCareReceivers = float(len([x for x in self.pop.livingPeople if x.status == 'child']))
        informalChildCarePerRecipient = 0
        formalChildCarePerRecipient = 0
        childCarePerRecipient = 0
        unmetChildCarePerRecipient = 0
        if childCareReceivers > 0:
            informalChildCarePerRecipient = informalChildCareReceived/childCareReceivers
            formalChildCarePerRecipient = formalChildCareReceived/childCareReceivers
            childCarePerRecipient = informalChildCarePerRecipient + formalChildCarePerRecipient
            unmetChildCarePerRecipient = unmetChildCareNeed/childCareReceivers
        
        childCareReceivers_1 = float(len([x for x in class_1 if x.status == 'child']))
        informalChildCarePerRecipient_1 = 0
        formalChildCarePerRecipient_1 = 0
        childCarePerRecipient_1 = 0
        unmetChildCarePerRecipient_1 = 0
        if childCareReceivers_1 > 0:
            informalChildCarePerRecipient_1 = informalChildCareReceived_1/childCareReceivers_1
            formalChildCarePerRecipient_1 = formalChildCareReceived_1/childCareReceivers_1
            childCarePerRecipient_1 = informalChildCarePerRecipient_1 + formalChildCarePerRecipient_1
            unmetChildCarePerRecipient_1 = unmetChildCareNeed_1/childCareReceivers_1
        
        childCareReceivers_2 = float(len([x for x in class_2 if x.status == 'child']))
        informalChildCarePerRecipient_2 = 0
        formalChildCarePerRecipient_2 = 0
        childCarePerRecipient_2 = 0
        unmetChildCarePerRecipient_2 = 0
        if childCareReceivers_2 > 0:
            informalChildCarePerRecipient_2 = informalChildCareReceived_2/childCareReceivers_2
            formalChildCarePerRecipient_2 = formalChildCareReceived_2/childCareReceivers_2
            childCarePerRecipient_2 = informalChildCarePerRecipient_2 + formalChildCarePerRecipient_2
            unmetChildCarePerRecipient_2 = unmetChildCareNeed_2/childCareReceivers_2
        
        childCareReceivers_3 = float(len([x for x in class_3 if x.status == 'child']))
        informalChildCarePerRecipient_3 = 0
        formalChildCarePerRecipient_3 = 0
        childCarePerRecipient_3 = 0
        unmetChildCarePerRecipient_3 = 0
        if childCareReceivers_3 > 0:
            informalChildCarePerRecipient_3 = informalChildCareReceived_3/childCareReceivers_3
            formalChildCarePerRecipient_3 = formalChildCareReceived_3/childCareReceivers_3
            childCarePerRecipient_3 = informalChildCarePerRecipient_3 + formalChildCarePerRecipient_3
            unmetChildCarePerRecipient_3 = unmetChildCareNeed_3/childCareReceivers_3
        
        childCareReceivers_4 = float(len([x for x in class_4 if x.status == 'child']))
        informalChildCarePerRecipient_4 = 0
        formalChildCarePerRecipient_4 = 0
        childCarePerRecipient_4 = 0
        unmetChildCarePerRecipient_4 = 0
        if childCareReceivers_4 > 0:
            informalChildCarePerRecipient_4 = informalChildCareReceived_4/childCareReceivers_4
            formalChildCarePerRecipient_4 = formalChildCareReceived_4/childCareReceivers_4
            childCarePerRecipient_4 = informalChildCarePerRecipient_4 + formalChildCarePerRecipient_4
            unmetChildCarePerRecipient_4 = unmetChildCareNeed_4/childCareReceivers_4
        
        childCareReceivers_5 = float(len([x for x in class_5 if x.status == 'child']))
        informalChildCarePerRecipient_5 = 0
        formalChildCarePerRecipient_5 = 0
        childCarePerRecipient_5 = 0
        unmetChildCarePerRecipient_5 = 0
        if childCareReceivers_5 > 0:
            informalChildCarePerRecipient_5 = informalChildCareReceived_5/childCareReceivers_5
            formalChildCarePerRecipient_5 = formalChildCareReceived_5/childCareReceivers_5
            childCarePerRecipient_5 = informalChildCarePerRecipient_5 + formalChildCarePerRecipient_5
            unmetChildCarePerRecipient_5 = unmetChildCareNeed_5/childCareReceivers_5
            
        # Graph 25
        numCarers = float(len([x for x in self.pop.livingPeople if x.hoursDemand == 0 and x.status != 'child']))
        informalCarePerCarer = 0
        formalCarePerCarer = 0
        if numCarers > 0:
            informalCarePerCarer = totalInformalCare/numCarers
            formalCarePerCarer = totalFormalCare/numCarers
        
        numCarers_1 = float(len([x for x in class_1 if x.hoursDemand == 0 and x.status != 'child']))
        informalCarePerCarer_1 = 0
        formalCarePerCarer_1 = 0
        if numCarers_1 > 0:
            informalCarePerCarer_1 = totalInformalCare_1/numCarers_1
            formalCarePerCarer_1 = totalFormalCare_1/numCarers_1
        
        numCarers_2 = float(len([x for x in class_2 if x.hoursDemand == 0 and x.status != 'child']))
        informalCarePerCarer_2 = 0
        formalCarePerCarer_2 = 0
        if numCarers_2 > 0:
            informalCarePerCarer_2 = totalInformalCare_2/numCarers_2
            formalCarePerCarer_2 = totalFormalCare_2/numCarers_2
        
        numCarers_3 = float(len([x for x in class_3 if x.hoursDemand == 0 and x.status != 'child']))
        informalCarePerCarer_3 = 0
        formalCarePerCarer_3 = 0
        if numCarers_3 > 0:
            informalCarePerCarer_3 = totalInformalCare_3/numCarers_3
            formalCarePerCarer_3 = totalFormalCare_3/numCarers_3
        
        numCarers_4 = float(len([x for x in class_4 if x.hoursDemand == 0 and x.status != 'child']))
        informalCarePerCarer_4 = 0
        formalCarePerCarer_4 = 0
        if numCarers_4 > 0:
            informalCarePerCarer_4 = totalInformalCare_4/numCarers_4
            formalCarePerCarer_4 = totalFormalCare_4/numCarers_4
        
        numCarers_5 = float(len([x for x in class_5 if x.hoursDemand == 0 and x.status != 'child']))
        informalCarePerCarer_5 = 0
        formalCarePerCarer_5 = 0
        if numCarers_5 > 0:
            informalCarePerCarer_5 = totalInformalCare_5/numCarers_5
            formalCarePerCarer_5 = totalFormalCare_5/numCarers_5
        
        # Graph 25 bis: social care per carer
        informalSocialCarePerCarer = 0
        formalSocialCarePerCarer = 0
        if numCarers > 0:
            informalSocialCarePerCarer = informalSocialCareReceived/numCarers
            formalSocialCarePerCarer = formalSocialCareReceived/numCarers
        
        informalSocialCarePerCarer_1 = 0
        formalSocialCarePerCarer_1 = 0
        if numCarers_1 > 0:
            informalSocialCarePerCarer_1 = informalSocialCareReceived_1/numCarers_1
            formalSocialCarePerCarer_1 = formalSocialCareReceived_1/numCarers_1
        
        informalSocialCarePerCarer_2 = 0
        formalSocialCarePerCarer_2 = 0
        if numCarers_2 > 0:
            informalSocialCarePerCarer_2 = informalSocialCareReceived_2/numCarers_2
            formalSocialCarePerCarer_2 = formalSocialCareReceived_2/numCarers_2
        
        informalSocialCarePerCarer_3 = 0
        formalSocialCarePerCarer_3 = 0
        if numCarers_3 > 0:
            informalSocialCarePerCarer_3 = informalSocialCareReceived_3/numCarers_3
            formalSocialCarePerCarer_3 = formalSocialCareReceived_3/numCarers_3
        
        informalSocialCarePerCarer_4 = 0
        formalSocialCarePerCarer_4 = 0
        if numCarers_4 > 0:
            informalSocialCarePerCarer_4 = informalSocialCareReceived_4/numCarers_4
            formalSocialCarePerCarer_4 = formalSocialCareReceived_4/numCarers_4
        
        informalSocialCarePerCarer_5 = 0
        formalSocialCarePerCarer_5 = 0
        if numCarers_5 > 0:
            informalSocialCarePerCarer_5 = informalSocialCareReceived_5/numCarers_5
            formalSocialCarePerCarer_5 = formalSocialCareReceived_5/numCarers_5
        
        # Graph 25 tris: child care per carer
        informalChildCarePerCarer = 0
        formalChildCarePerCarer = 0
        if numCarers > 0:
            informalChildCarePerCarer = informalChildCareReceived/numCarers
            formalChildCarePerCarer = formalChildCareReceived/numCarers
        
        informalChildCarePerCarer_1 = 0
        formalChildCarePerCarer_1 = 0
        if numCarers_1 > 0:
            informalChildCarePerCarer_1 = informalChildCareReceived_1/numCarers_1
            formalChildCarePerCarer_1 = formalChildCareReceived_1/numCarers_1
        
        informalChildCarePerCarer_2 = 0
        formalChildCarePerCarer_2 = 0
        if numCarers_2 > 0:
            informalChildCarePerCarer_2 = informalChildCareReceived_2/numCarers_2
            formalChildCarePerCarer_2 = formalChildCareReceived_2/numCarers_2
        
        informalChildCarePerCarer_3 = 0
        formalChildCarePerCarer_3 = 0
        if numCarers_3 > 0:
            informalChildCarePerCarer_3 = informalChildCareReceived_3/numCarers_3
            formalChildCarePerCarer_3 = formalChildCareReceived_3/numCarers_3
        
        informalChildCarePerCarer_4 = 0
        formalChildCarePerCarer_4 = 0
        if numCarers_4 > 0:
            informalChildCarePerCarer_4 = informalChildCareReceived_4/numCarers_4
            formalChildCarePerCarer_4 = formalChildCareReceived_4/numCarers_4
        
        informalChildCarePerCarer_5 = 0
        formalChildCarePerCarer_5 = 0
        if numCarers_5 > 0:
            informalChildCarePerCarer_5 = informalChildCareReceived_5/numCarers_5
            formalChildCarePerCarer_5 = formalChildCareReceived_5/numCarers_5
        
        # Graph 26
        sumNoK_informalSupplies = [0.0, 0.0, 0.0, 0.0]
        sumNoK_formalSupplies = [0.0, 0.0, 0.0, 0.0]
        receivers = [x for x in self.pop.livingPeople if x.hoursDemand > 0]
        
        totInformalSupply = 0
        for person in receivers:
            for i in range(4):
                totInformalSupply += person.informalSupplyByKinship[i]
                sumNoK_informalSupplies[i] += person.informalSupplyByKinship[i]
                sumNoK_formalSupplies[i] += person.formalSupplyByKinship[i]
    
        if totInformalSupply > 0:
            print 'Household informal supply share: ' + str(sumNoK_informalSupplies[0]/totInformalSupply)
                
        # Graph 27
        informalCareSuppliedByFemales = sum([x.socialWork for x in self.pop.livingPeople if x.sex == 'female'])
        totalInformalCare = sum([x.socialWork for x in self.pop.livingPeople])
        shareInformalCareSuppliedByFemales = 0
        if totalInformalCare > 0:
            shareInformalCareSuppliedByFemales = informalCareSuppliedByFemales/totalInformalCare
        
        informalCareSuppliedByFemales_1 = sum([x.socialWork for x in class_1 if x.sex == 'female'])
        totalInformalCare_1 = sum([x.socialWork for x in class_1])
        shareInformalCareSuppliedByFemales_1 = 0
        if totalInformalCare_1 > 0:
            shareInformalCareSuppliedByFemales_1 = informalCareSuppliedByFemales_1/totalInformalCare_1
        
        informalCareSuppliedByFemales_2 = sum([x.socialWork for x in class_2 if x.sex == 'female'])
        totalInformalCare_2 = sum([x.socialWork for x in class_2])
        shareInformalCareSuppliedByFemales_2 = 0
        if totalInformalCare_2 > 0:
            shareInformalCareSuppliedByFemales_2 = informalCareSuppliedByFemales_2/totalInformalCare_2
        
        informalCareSuppliedByFemales_3 = sum([x.socialWork for x in class_3 if x.sex == 'female'])
        totalInformalCare_3 = sum([x.socialWork for x in class_3])
        shareInformalCareSuppliedByFemales_3 = 0
        if totalInformalCare_3 > 0:
            shareInformalCareSuppliedByFemales_3 = informalCareSuppliedByFemales_3/totalInformalCare_3
        
        informalCareSuppliedByFemales_4 = sum([x.socialWork for x in class_4 if x.sex == 'female'])
        totalInformalCare_4 = sum([x.socialWork for x in class_4])
        shareInformalCareSuppliedByFemales_4 = 0
        if totalInformalCare_4 > 0:
            shareInformalCareSuppliedByFemales_4 = informalCareSuppliedByFemales_4/totalInformalCare_4
        
        informalCareSuppliedByFemales_5 = sum([x.socialWork for x in class_5 if x.sex == 'female'])
        totalInformalCare_5 = sum([x.socialWork for x in class_5])
        shareInformalCareSuppliedByFemales_5 = 0
        if totalInformalCare_5 > 0:
            shareInformalCareSuppliedByFemales_5 = informalCareSuppliedByFemales_5/totalInformalCare_5
        
        # Graph 28
        informalCareSuppliedByMales_1 = sum([x.socialWork for x in class_1 if x.sex == 'male'])
        informalCareSuppliedByMales_2 = sum([x.socialWork for x in class_2 if x.sex == 'male'])
        informalCareSuppliedByMales_3 = sum([x.socialWork for x in class_3 if x.sex == 'male'])
        informalCareSuppliedByMales_4 = sum([x.socialWork for x in class_4 if x.sex == 'male'])
        informalCareSuppliedByMales_5 = sum([x.socialWork for x in class_5 if x.sex == 'male'])
        
        # Graph 29 and 30
        employedMales = [x for x in self.pop.livingPeople if x.status == 'employed' and x.sex == 'male']
        numEmployedMales = float(len(employedMales))
        averageMalesWage = 0
        if numEmployedMales > 0:
            averageMalesWage = sum([x.hourlyWage for x in employedMales])/numEmployedMales
            
        employedFemales = [x for x in self.pop.livingPeople if x.status == 'employed' and x.sex == 'female']
        numEmployedFemales = float(len(employedFemales))
        averageFemalesWage = 0
        if numEmployedFemales > 0:
            averageFemalesWage = sum([x.hourlyWage for x in employedFemales])/numEmployedFemales
        ratioWage = 0
        if averageMalesWage > 0:
            ratioWage = averageFemalesWage/averageMalesWage
        
        employedMales_1 = [x for x in class_1 if x.status == 'employed' and x.sex == 'male']
        numEmployedMales_1 = float(len(employedMales_1))
        averageMalesWage_1 = 0
        if numEmployedMales_1 > 0:
            averageMalesWage_1 = sum([x.hourlyWage for x in employedMales_1])/numEmployedMales_1
        employedFemales_1 = [x for x in class_1 if x.status == 'employed' and x.sex == 'female']
        numEmployedFemales_1 = float(len(employedFemales_1))
        averageFemalesWage_1 = 0
        if numEmployedFemales_1 > 0:
            averageFemalesWage_1 = sum([x.hourlyWage for x in employedFemales_1])/numEmployedFemales_1
        ratioWage_1 = 0
        if averageMalesWage_1 > 0:
            ratioWage_1 = averageFemalesWage_1/averageMalesWage_1
        
        employedMales_2 = [x for x in class_2 if x.status == 'employed' and x.sex == 'male']
        numEmployedMales_2 = float(len(employedMales_2))
        averageMalesWage_2 = 0
        if numEmployedMales_2 > 0:
            averageMalesWage_2 = sum([x.hourlyWage for x in employedMales_2])/numEmployedMales_2
        employedFemales_2 = [x for x in class_2 if x.status == 'employed' and x.sex == 'female']
        numEmployedFemales_2 = float(len(employedFemales_2))
        averageFemalesWage_2 = 0
        if numEmployedFemales_2 > 0:
            averageFemalesWage_2 = sum([x.hourlyWage for x in employedFemales_2])/numEmployedFemales_2
        ratioWage_2 = 0
        if averageMalesWage_2 > 0:
            ratioWage_2 = averageFemalesWage_2/averageMalesWage_2
        
        employedMales_3 = [x for x in class_3 if x.status == 'employed' and x.sex == 'male']
        numEmployedMales_3 = float(len(employedMales_3))
        averageMalesWage_3 = 0
        if numEmployedMales_3 > 0:
            averageMalesWage_3 = sum([x.hourlyWage for x in employedMales_3])/numEmployedMales_3
        employedFemales_3 = [x for x in class_3 if x.status == 'employed' and x.sex == 'female']
        numEmployedFemales_3 = float(len(employedFemales_3))
        averageFemalesWage_3 = 0
        if numEmployedFemales_3 > 0:
            averageFemalesWage_3 = sum([x.hourlyWage for x in employedFemales_3])/numEmployedFemales_3
        ratioWage_3 = 0
        if averageMalesWage_3 > 0:
            ratioWage_3 = averageFemalesWage_3/averageMalesWage_3
        
        employedMales_4 = [x for x in class_4 if x.status == 'employed' and x.sex == 'male']
        numEmployedMales_4 = float(len(employedMales_4))
        averageMalesWage_4 = 0
        if numEmployedMales_4 > 0:
            averageMalesWage_4 = sum([x.hourlyWage for x in employedMales_4])/numEmployedMales_4
        employedFemales_4 = [x for x in class_4 if x.status == 'employed' and x.sex == 'female']
        numEmployedFemales_4 = float(len(employedFemales_4))
        averageFemalesWage_4 = 0
        if numEmployedFemales_4 > 0:
            averageFemalesWage_4 = sum([x.hourlyWage for x in employedFemales_4])/numEmployedFemales_4
        ratioWage_4 = 0
        if averageMalesWage_4 > 0:
            ratioWage_4 = averageFemalesWage_4/averageMalesWage_4
        
        employedMales_5 = [x for x in class_5 if x.status == 'employed' and x.sex == 'male']
        numEmployedMales_5 = float(len(employedMales_5))
        averageMalesWage_5 = 0
        if numEmployedMales_5 > 0:
            averageMalesWage_5 = sum([x.hourlyWage for x in employedMales_5])/numEmployedMales_5
        employedFemales_5 = [x for x in class_5 if x.status == 'employed' and x.sex == 'female']
        numEmployedFemales_5 = float(len(employedFemales_5))
        averageFemalesWage_5 = 0
        if numEmployedFemales_5 > 0:
            averageFemalesWage_5 = sum([x.hourlyWage for x in employedFemales_5])/numEmployedFemales_5
        ratioWage_5 = 0
        if averageMalesWage_5 > 0:
            ratioWage_5 = averageFemalesWage_5/averageMalesWage_5
        
        # Graph 31 and Graph 32
        averageMalesIncome = 0
        if employedMales > 0:
            averageMalesIncome = sum([x.netIncome for x in employedMales])/numEmployedMales
        averageFemalesIncome = 0
        if employedFemales > 0:
            averageFemalesIncome = sum([x.netIncome for x in employedFemales])/numEmployedFemales
        ratioIncome = 0
        if averageMalesIncome > 0:
            ratioIncome = averageFemalesIncome/averageMalesIncome
        
        averageMalesIncome_1 = 0
        if employedMales_1 > 0:
            averageMalesIncome_1 = sum([x.netIncome for x in employedMales_1])/numEmployedMales_1
        averageFemalesIncome_1 = 0
        if employedFemales_1 > 0:
            averageFemalesIncome_1 = sum([x.netIncome for x in employedFemales_1])/numEmployedFemales_1
        ratioIncome_1 = 0
        if averageMalesIncome_1 > 0:
            ratioIncome_1 = averageFemalesIncome_1/averageMalesIncome_1
        
        averageMalesIncome_2 = 0
        if employedMales_2 > 0:
            averageMalesIncome_2 = sum([x.netIncome for x in employedMales_2])/numEmployedMales_2
        averageFemalesIncome_2 = 0
        if employedFemales_2 > 0:
            averageFemalesIncome_2 = sum([x.netIncome for x in employedFemales_2])/numEmployedFemales_2
        ratioIncome_2 = 0
        if averageMalesIncome_2 > 0:
            ratioIncome_2 = averageFemalesIncome_2/averageMalesIncome_2
        
        averageMalesIncome_3 = 0
        if employedMales_3 > 0:
            averageMalesIncome_3 = sum([x.netIncome for x in employedMales_3])/numEmployedMales_3
        averageFemalesIncome_3 = 0
        if employedFemales_3 > 0:
            averageFemalesIncome_3 = sum([x.netIncome for x in employedFemales_3])/numEmployedFemales_3
        ratioIncome_3 = 0
        if averageMalesIncome_3 > 0:
            ratioIncome_3 = averageFemalesIncome_3/averageMalesIncome_3
        
        averageMalesIncome_4 = 0
        if employedMales_4 > 0:
            averageMalesIncome_4 = sum([x.netIncome for x in employedMales_4])/numEmployedMales_4
        averageFemalesIncome_4 = 0
        if employedFemales_4 > 0:
            averageFemalesIncome_4 = sum([x.netIncome for x in employedFemales_4])/numEmployedFemales_4
        ratioIncome_4 = 0
        if averageMalesIncome_4 > 0:
            ratioIncome_4 = averageFemalesIncome_4/averageMalesIncome_4
        
        averageMalesIncome_5 = 0
        if employedMales_5 > 0:
            averageMalesIncome_5 = sum([x.netIncome for x in employedMales_5])/numEmployedMales_5
        averageFemalesIncome_5 = 0
        if employedFemales_5 > 0:
            averageFemalesIncome_5 = sum([x.netIncome for x in employedFemales_5])/numEmployedFemales_5
        ratioIncome_5 = 0
        if averageMalesIncome_5 > 0:
            ratioIncome_5 = averageFemalesIncome_5/averageMalesIncome_5
        
        # Graph 33
        taxPayers = len([x for x in self.pop.livingPeople if x.income > 0])
        
        # Graph 35
        
        taxBurden = ( unmetCareNeed * self.p['pricePublicSocialCare'] * 52.18 ) / ( taxPayers * 1.0 )
        
       
        # Graph 37: hospitalization Cost
        
        # Graph 38
        perCapitaHospitalizationCost = self.hospitalizationCost/currentPop
        
        # Graph 39
        unmetSocialCareNeedDistribution = [x.residualNeed for x in self.pop.livingPeople if x.careNeedLevel > 0]
        unmetSocialCareNeedGiniCoefficient = self.computeGiniCoefficient(unmetSocialCareNeedDistribution)
        unmetSocialCareNeedDistribution_1 = [x.residualNeed for x in self.pop.livingPeople if x.classRank == 0 and x.careNeedLevel > 0]
        unmetSocialCareNeedGiniCoefficient_1 = self.computeGiniCoefficient(unmetSocialCareNeedDistribution_1)
        unmetSocialCareNeedDistribution_2 = [x.residualNeed for x in self.pop.livingPeople if x.classRank == 1 and x.careNeedLevel > 0]
        unmetSocialCareNeedGiniCoefficient_2 = self.computeGiniCoefficient(unmetSocialCareNeedDistribution_2)
        unmetSocialCareNeedDistribution_3 = [x.residualNeed for x in self.pop.livingPeople if x.classRank == 2 and x.careNeedLevel > 0]
        unmetSocialCareNeedGiniCoefficient_3 = self.computeGiniCoefficient(unmetSocialCareNeedDistribution_3)
        unmetSocialCareNeedDistribution_4 = [x.residualNeed for x in self.pop.livingPeople if x.classRank == 3 and x.careNeedLevel > 0]
        unmetSocialCareNeedGiniCoefficient_4 = self.computeGiniCoefficient(unmetSocialCareNeedDistribution_4)
        unmetSocialCareNeedDistribution_5 = [x.residualNeed for x in self.pop.livingPeople if x.classRank == 4 and x.careNeedLevel > 0]
        unmetSocialCareNeedGiniCoefficient_5 = self.computeGiniCoefficient(unmetSocialCareNeedDistribution_5)
        
        # Graph 40
        shareUnmetSocialCareNeedDistribution = [x.residualNeed/x.hoursDemand for x in self.pop.livingPeople if x.careNeedLevel > 0]
        shareUnmetSocialCareNeedGiniCoefficient = self.computeGiniCoefficient(shareUnmetSocialCareNeedDistribution)
        shareUnmetSocialCareNeedDistribution_1 = [x.residualNeed/x.hoursDemand for x in self.pop.livingPeople if x.classRank == 0 and x.careNeedLevel > 0]
        shareUnmetSocialCareNeedGiniCoefficient_1 = self.computeGiniCoefficient(shareUnmetSocialCareNeedDistribution_1)
        shareUnmetSocialCareNeedDistribution_2 = [x.residualNeed/x.hoursDemand for x in self.pop.livingPeople if x.classRank == 1 and x.careNeedLevel > 0]
        shareUnmetSocialCareNeedGiniCoefficient_2 = self.computeGiniCoefficient(shareUnmetSocialCareNeedDistribution_2)
        shareUnmetSocialCareNeedDistribution_3 = [x.residualNeed/x.hoursDemand for x in self.pop.livingPeople if x.classRank == 2 and x.careNeedLevel > 0]
        shareUnmetSocialCareNeedGiniCoefficient_3 = self.computeGiniCoefficient(shareUnmetSocialCareNeedDistribution_3)
        shareUnmetSocialCareNeedDistribution_4 = [x.residualNeed/x.hoursDemand for x in self.pop.livingPeople if x.classRank == 3 and x.careNeedLevel > 0]
        shareUnmetSocialCareNeedGiniCoefficient_4 = self.computeGiniCoefficient(shareUnmetSocialCareNeedDistribution_4)
        shareUnmetSocialCareNeedDistribution_5 = [x.residualNeed/x.hoursDemand for x in self.pop.livingPeople if x.classRank == 4 and x.careNeedLevel > 0]
        shareUnmetSocialCareNeedGiniCoefficient_5 = self.computeGiniCoefficient(shareUnmetSocialCareNeedDistribution_5)
        
        # Graph 41: Public supply of social care
        
        # Graph 48: 
        ratioUnmetNeed_CareSupply = 0
        if totalCareSupply > 0:
            ratioUnmetNeed_CareSupply = unmetCareNeed/totalCareSupply
        
        informalCareSupply = sum([x.hoursInformalSupply[0] for x in class_1])
        visitedHousehold = []
        formalCareSupply = 0
        for x in class_1:
            if x.house in visitedHousehold:
                continue
            visitedHousehold.append(x.house)
            formalCareSupply += x.hoursFormalSupply[0]
        totalCareSupply_1 = informalCareSupply + formalCareSupply
        ratioUnmetNeed_CareSupply_1 = 0
        if totalCareSupply_1 > 0:
            ratioUnmetNeed_CareSupply_1 = unmetCareNeed_1/totalCareSupply_1
        
        informalCareSupply = sum([x.hoursInformalSupply[0] for x in class_2])
        visitedHousehold = []
        formalCareSupply = 0
        for x in class_2:
            if x.house in visitedHousehold:
                continue
            visitedHousehold.append(x.house)
            formalCareSupply += x.hoursFormalSupply[0]
        totalCareSupply_2 = informalCareSupply + formalCareSupply
        ratioUnmetNeed_CareSupply_2 = 0
        if totalCareSupply_2 > 0:
            ratioUnmetNeed_CareSupply_2 = unmetCareNeed_2/totalCareSupply_2
        
        informalCareSupply = sum([x.hoursInformalSupply[0] for x in class_3])
        visitedHousehold = []
        formalCareSupply = 0
        for x in class_3:
            if x.house in visitedHousehold:
                continue
            visitedHousehold.append(x.house)
            formalCareSupply += x.hoursFormalSupply[0]
        totalCareSupply_3 = informalCareSupply + formalCareSupply
        ratioUnmetNeed_CareSupply_3 = 0
        if totalCareSupply_3 > 0:
            ratioUnmetNeed_CareSupply_3 = unmetCareNeed_3/totalCareSupply_3
        
        informalCareSupply = sum([x.hoursInformalSupply[0] for x in class_4])
        visitedHousehold = []
        formalCareSupply = 0
        for x in class_4:
            if x.house in visitedHousehold:
                continue
            visitedHousehold.append(x.house)
            formalCareSupply += x.hoursFormalSupply[0]
        totalCareSupply_4 = informalCareSupply + formalCareSupply
        ratioUnmetNeed_CareSupply_4 = 0
        if totalCareSupply_4 > 0:
            ratioUnmetNeed_CareSupply_4 = unmetCareNeed_4/totalCareSupply_4
        
        informalCareSupply = sum([x.hoursInformalSupply[0] for x in class_5])
        visitedHousehold = []
        formalCareSupply = 0
        for x in class_5:
            if x.house in visitedHousehold:
                continue
            visitedHousehold.append(x.house)
            formalCareSupply += x.hoursFormalSupply[0]
        totalCareSupply_5 = informalCareSupply + formalCareSupply
        ratioUnmetNeed_CareSupply_5 = 0
        if totalCareSupply_5 > 0:
            ratioUnmetNeed_CareSupply_5 = unmetCareNeed_5/totalCareSupply_5
        
        informalCareReceived = sum([x.informalCare for x in self.pop.livingPeople])
        formalCareReceived = sum([x.formalCare for x in self.pop.livingPeople])
        totalCareReceived = informalCareReceived + formalCareReceived
        totalUnnmetCareNeed = sum([x.residualNeed for x in self.pop.livingPeople])
        
        costDirectFunding = self.publicSupply*self.p['priceSocialCare']
        careCreditCost = self.careCreditSupply*self.p['priceSocialCare']
        
        govBudget = self.taxRevenue - self.pensionExpenditure
        perCapitaBudget = govBudget/currentPop
        
        # Add Costs
        
        totalPolicyCost = self.totalTaxRefund + costDirectFunding + careCreditCost # 3 policy levers. To be expanded as more policy levers are added
        perCapitaPolicyCost = totalPolicyCost/currentPop
        
        policyCostWithHC = 52*totalPolicyCost + self.hospitalizationCost
        perCapitaPolicyCostWithHC = policyCostWithHC/currentPop
        
        perCapitaTaxRefund = self.totalTaxRefund/currentPop
        perCapitaCostDirectFunding = costDirectFunding/currentPop
        perCapitaCareCreditCost = careCreditCost/currentPop
        
        totalCost = policyCostWithHC - 52*govBudget
        perCapitaCost = totalCost/currentPop
        
        if self.socialCareCredits > 0:
            shareCreditsSpent = float(self.socialCreditSpent)/float(self.socialCareCredits)
        else:
            shareCreditsSpent = 0
       
        outputs = [self.year, currentPop, numReceivers, taxPayers, numUnskilled, numSkilled, numLowClass, numMidClass, numUpClass, shareLoneParents, shareDistantParents,
                   shareUnskilled, shareSkilled, shareLowClass, shareMidClass, shareUpClass, numOccupiedHouses, averageHouseholdSize, self.marriageTally, self.divorceTally,
                   averageHouseholdSize_1, averageHouseholdSize_2, averageHouseholdSize_3, averageHouseholdSize_4, averageHouseholdSize_5, totalCareSupply, informalCareSupply,
                   formalCareSupply, totalCareNeed, socialCareNeed, childCareNeed, shareCareGivers, shareCareGivers_1, shareCareGivers_2, shareCareGivers_3, shareCareGivers_4, 
                   shareCareGivers_5, shareSocialCareTakers_N1, shareSocialCareTakers_N2, shareSocialCareTakers_N3, shareSocialCareTakers_N4, 
                   meanInformalSocialCareReceived_N1, meanFormalSocialCareReceived_N1, meanUnmetSocialCareNeed_N1, meanInformalSocialCareReceived_N2, meanFormalSocialCareReceived_N2, 
                   meanUnmetSocialCareNeed_N2, meanInformalSocialCareReceived_N3, meanFormalSocialCareReceived_N3, meanUnmetSocialCareNeed_N3, meanInformalSocialCareReceived_N4, 
                   meanFormalSocialCareReceived_N4, meanUnmetSocialCareNeed_N4, shareSocialCareDemand, shareSocialCare_1,
                   shareSocialCare_2, shareSocialCare_3, shareSocialCare_4, shareSocialCare_5, perCapitaCareReceived, perCapitaUnmetCareDemand, perCapitaSocialCareReceived,
                   perCapitaUnmetSocialCareDemand, perCapitaChildCareReceived, perCapitaUnmetChildCareDemand, informalCareReceived, formalCareReceived, totalCareReceived,
                   totalUnnmetCareNeed, shareInformalCareReceived, shareInformalCareReceived_1, 
                   shareInformalCareReceived_2, shareInformalCareReceived_3, shareInformalCareReceived_4, shareInformalCareReceived_5, shareInformalSocialCare, shareInformalSocialCare_1,
                   shareInformalSocialCare_2, shareInformalSocialCare_3, shareInformalSocialCare_4, shareInformalSocialCare_5, shareInformalChildCare, shareInformalChildCare_1,
                   shareInformalChildCare_2, shareInformalChildCare_3, shareInformalChildCare_4, shareInformalChildCare_5, informalSocialCareReceived, formalSocialCareReceived, 
                   unmetSocialCareNeed, informalChildCareReceived, formalChildCareReceived, unmetChildCareNeed, shareUnmetCareDemand, shareUnmetCareDemand_1, shareUnmetCareDemand_2,
                   shareUnmetCareDemand_3, shareUnmetCareDemand_4, shareUnmetCareDemand_5, shareUnmetSocialCareDemand, shareUnmetSocialCareDemand_1, shareUnmetSocialCareDemand_2,
                   shareUnmetSocialCareDemand_3, shareUnmetSocialCareDemand_4, shareUnmetSocialCareDemand_5, shareUnmetChildCareDemand, shareUnmetChildCareDemand_1, 
                   shareUnmetChildCareDemand_2, shareUnmetChildCareDemand_3, shareUnmetChildCareDemand_4, shareUnmetChildCareDemand_5, perCapitaUnmetCareDemand_1, perCapitaUnmetCareDemand_2,
                   perCapitaUnmetCareDemand_3, perCapitaUnmetCareDemand_4, perCapitaUnmetCareDemand_5, averageUnmetCareDemand, averageUnmetCareDemand_1, averageUnmetCareDemand_2,
                   averageUnmetCareDemand_3, averageUnmetCareDemand_4, averageUnmetCareDemand_5, informalCareReceived_1, informalCareReceived_2, informalCareReceived_3, 
                   informalCareReceived_4, informalCareReceived_5, formalCareReceived_1, formalCareReceived_2, formalCareReceived_3, formalCareReceived_4, formalCareReceived_5,
                   unmetCareNeed_1, unmetCareNeed_2, unmetCareNeed_3, unmetCareNeed_4, unmetCareNeed_5, 
                   informalCarePerRecipient, informalCarePerRecipient_1, informalCarePerRecipient_2, informalCarePerRecipient_3, informalCarePerRecipient_4, informalCarePerRecipient_5, 
                   formalCarePerRecipient, formalCarePerRecipient_1, formalCarePerRecipient_2, formalCarePerRecipient_3, formalCarePerRecipient_4, formalCarePerRecipient_5, carePerRecipient, 
                   carePerRecipient_1, carePerRecipient_2, carePerRecipient_3, carePerRecipient_4, carePerRecipient_5, unmetCarePerRecipient, unmetCarePerRecipient_1, unmetCarePerRecipient_2, 
                   unmetCarePerRecipient_3,unmetCarePerRecipient_4, unmetCarePerRecipient_5, 
                   informalSocialCarePerRecipient, informalSocialCarePerRecipient_1, informalSocialCarePerRecipient_2, informalSocialCarePerRecipient_3, informalSocialCarePerRecipient_4, 
                   informalSocialCarePerRecipient_5, formalSocialCarePerRecipient, formalSocialCarePerRecipient_1, formalSocialCarePerRecipient_2, formalSocialCarePerRecipient_3, 
                   formalSocialCarePerRecipient_4, formalSocialCarePerRecipient_5, socialCarePerRecipient, socialCarePerRecipient_1, socialCarePerRecipient_2, socialCarePerRecipient_3, 
                   socialCarePerRecipient_4, socialCarePerRecipient_5, unmetSocialCarePerRecipient, unmetSocialCarePerRecipient_1, unmetSocialCarePerRecipient_2, unmetSocialCarePerRecipient_3,
                   unmetSocialCarePerRecipient_4, unmetSocialCarePerRecipient_5,
                   informalChildCarePerRecipient, informalChildCarePerRecipient_1, informalChildCarePerRecipient_2, informalChildCarePerRecipient_3, informalChildCarePerRecipient_4, 
                   informalChildCarePerRecipient_5, formalChildCarePerRecipient, formalChildCarePerRecipient_1, formalChildCarePerRecipient_2, formalChildCarePerRecipient_3, 
                   formalChildCarePerRecipient_4, formalChildCarePerRecipient_5, childCarePerRecipient, childCarePerRecipient_1, childCarePerRecipient_2, childCarePerRecipient_3, 
                   childCarePerRecipient_4, childCarePerRecipient_5, unmetChildCarePerRecipient, unmetChildCarePerRecipient_1, unmetChildCarePerRecipient_2, unmetChildCarePerRecipient_3,
                   unmetChildCarePerRecipient_4, unmetChildCarePerRecipient_5, 
                   informalSocialCareReceived_1, informalSocialCareReceived_2, informalSocialCareReceived_3, informalSocialCareReceived_4,
                   informalSocialCareReceived_5, formalSocialCareReceived_1, formalSocialCareReceived_2, formalSocialCareReceived_3, formalSocialCareReceived_4, formalSocialCareReceived_5,
                   unmetSocialCareNeed_1, unmetSocialCareNeed_2, unmetSocialCareNeed_3, unmetSocialCareNeed_4, unmetSocialCareNeed_5, informalChildCareReceived_1, 
                   informalChildCareReceived_2, informalChildCareReceived_3, informalChildCareReceived_4, informalChildCareReceived_5, formalChildCareReceived_1, formalChildCareReceived_2,
                   formalChildCareReceived_3, formalChildCareReceived_4, formalChildCareReceived_5, unmetChildCareNeed_1, unmetChildCareNeed_2, unmetChildCareNeed_3, unmetChildCareNeed_4,
                   unmetChildCareNeed_5, informalCarePerCarer, informalCarePerCarer_1, informalCarePerCarer_2, informalCarePerCarer_3, informalCarePerCarer_4, informalCarePerCarer_5, formalCarePerCarer,
                   formalCarePerCarer_1, formalCarePerCarer_2, formalCarePerCarer_3, formalCarePerCarer_4, formalCarePerCarer_5, 
                   informalSocialCarePerCarer, informalSocialCarePerCarer_1, informalSocialCarePerCarer_2, informalSocialCarePerCarer_3, informalSocialCarePerCarer_4, 
                   informalSocialCarePerCarer_5, formalSocialCarePerCarer, formalSocialCarePerCarer_1, formalSocialCarePerCarer_2, formalSocialCarePerCarer_3, 
                   formalSocialCarePerCarer_4, formalSocialCarePerCarer_5,
                   informalChildCarePerCarer, informalChildCarePerCarer_1, informalChildCarePerCarer_2, informalChildCarePerCarer_3, informalChildCarePerCarer_4, 
                   informalChildCarePerCarer_5, formalChildCarePerCarer, formalChildCarePerCarer_1, formalChildCarePerCarer_2, formalChildCarePerCarer_3, 
                   formalChildCarePerCarer_4, formalChildCarePerCarer_5, sumNoK_informalSupplies[0], sumNoK_informalSupplies[1], 
                   sumNoK_informalSupplies[2], sumNoK_informalSupplies[3], sumNoK_formalSupplies[0], sumNoK_formalSupplies[1], sumNoK_formalSupplies[2], sumNoK_formalSupplies[3],
                   shareInformalCareSuppliedByFemales, shareInformalCareSuppliedByFemales_1, shareInformalCareSuppliedByFemales_2, shareInformalCareSuppliedByFemales_3, 
                   shareInformalCareSuppliedByFemales_4, shareInformalCareSuppliedByFemales_5, informalCareSuppliedByFemales_1, informalCareSuppliedByFemales_2, 
                   informalCareSuppliedByFemales_3, informalCareSuppliedByFemales_4, informalCareSuppliedByFemales_5, informalCareSuppliedByMales_1, informalCareSuppliedByMales_2, 
                   informalCareSuppliedByMales_3, informalCareSuppliedByMales_4, informalCareSuppliedByMales_5, ratioWage, ratioWage_1, ratioWage_2, ratioWage_3, ratioWage_4, ratioWage_5,
                   averageMalesWage, averageMalesWage_1, averageMalesWage_2, averageMalesWage_3, averageMalesWage_4, averageMalesWage_5, averageFemalesWage, averageFemalesWage_1, 
                   averageFemalesWage_2, averageFemalesWage_3, averageFemalesWage_4, averageFemalesWage_5, ratioIncome, ratioIncome_1, ratioIncome_2, ratioIncome_3, ratioIncome_4, ratioIncome_5,
                   averageMalesIncome, averageMalesIncome_1, averageMalesIncome_2, averageMalesIncome_3, averageMalesIncome_4, averageMalesIncome_5, averageFemalesIncome, averageFemalesIncome_1, 
                   averageFemalesIncome_2, averageFemalesIncome_3, averageFemalesIncome_4, averageFemalesIncome_5, taxBurden, marriageProp, self.hospitalizationCost, 
                   perCapitaHospitalizationCost, unmetSocialCareNeedGiniCoefficient, unmetSocialCareNeedGiniCoefficient_1, unmetSocialCareNeedGiniCoefficient_2, unmetSocialCareNeedGiniCoefficient_3, 
                   unmetSocialCareNeedGiniCoefficient_4, unmetSocialCareNeedGiniCoefficient_5, shareUnmetSocialCareNeedGiniCoefficient, shareUnmetSocialCareNeedGiniCoefficient_1, 
                   shareUnmetSocialCareNeedGiniCoefficient_2, shareUnmetSocialCareNeedGiniCoefficient_3, shareUnmetSocialCareNeedGiniCoefficient_4, shareUnmetSocialCareNeedGiniCoefficient_5, 
                   self.publicSupply, costDirectFunding, totQALY, meanQALY, discountedQALY, averageDiscountedQALY, ratioUnmetNeed_CareSupply, ratioUnmetNeed_CareSupply_1, ratioUnmetNeed_CareSupply_2, 
                   ratioUnmetNeed_CareSupply_3, ratioUnmetNeed_CareSupply_4, ratioUnmetNeed_CareSupply_5, self.totalTaxRefund, self.pensionExpenditure, self.careCreditSupply, 
                   self.socialCareCredits, self.socialCreditSpent, shareCreditsSpent, careCreditCost, govBudget, perCapitaBudget, totalCost, totalPolicyCost, perCapitaCost, perCapitaPolicyCost, 
                   self.taxRevenue, perCapitaTaxRefund, perCapitaCostDirectFunding, perCapitaCareCreditCost, shareCarers, shareWomenCarers, shareMenCarers, policyCostWithHC, perCapitaPolicyCostWithHC]
                   
        self.marriageTally = 0      
        self.divorceTally = 0 
        self.hospitalizationCost = 0
        self.taxRevenue = 0
        self.totalTaxRefund = 0
        self.publicSupply = 0
        self.pensionExpenditure = 0
        self.careCreditSupply = 0
        self.socialCareCredits = 0
        self.socialCreditSpent = 0
        
        outputFolder = self.folder + '/Dataset'
        if self.year == self.p['startYear']:
            if not os.path.exists(outputFolder):
                os.makedirs(outputFolder)
            with open(os.path.join(outputFolder, "outputSim.csv"), "w") as file:
                writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                writer.writerow((self.Outputs))
                writer.writerow(outputs)
        else:
            with open(os.path.join(outputFolder, "outputSim.csv"), "a") as file:
                writer = csv.writer(file, delimiter = ",", lineterminator='\r')
                writer.writerow(outputs)
        
        # Some additional debugging
        if self.p['verboseDebugging']:
            peopleCount = 0
            for i in self.pop.allPeople:
                if i.dead == False:
                    peopleCount += 1
            print "True pop counting non-dead people in allPeople list = ", peopleCount

            peopleCount = 0
            for h in self.map.occupiedHouses:
                peopleCount += len(h.occupants)
            print "True pop counting occupants of all occupied houses = ", peopleCount

            peopleCount = 0
            for h in self.map.allHouses:
                peopleCount += len(h.occupants)
            print "True pop counting occupants of ALL houses = ", peopleCount

            tally = [ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            for h in self.map.occupiedHouses:
                tally[len(h.occupants)] += 1
            for i in range(len(tally)):
                if tally[i] > 0:
                    print i, tally[i]
                
    def computeGiniCoefficient(self, unmetCareNeeds):
        sorted_list = sorted(unmetCareNeeds)
        height, area = 0, 0
        for value in sorted_list:
            height += float(value)
            area += height - float(value)/2.
        fair_area = height*len(unmetCareNeeds)/float(2)
        if fair_area > 0:
            return (fair_area-area)/fair_area
        else:
            return 0
    
    def manhattanDistance(self,t1,t2):
        """Calculates the distance between two towns"""
        xDist = abs(t1.x - t2.x)
        yDist = abs(t1.y - t2.y)
        return xDist + yDist 
        
    def deltaAge(self, dA):
        if dA <= -10 :
            cat = 0
        elif dA >= -9 and dA <= -3:
            cat = 1
        elif dA >= -2 and dA <= 0:
            cat = 2
        elif dA >= 1 and dA <= 4:
            cat = 3
        elif dA >= 5 and dA <= 9:
            cat = 4
        else:
            cat = 5
        return cat
     
    def initializeCanvas(self):
        """Put up a TKInter canvas window to animate the simulation."""
        self.canvas.pack()
        
         ## Draw some numbers for the population pyramid that won't be redrawn each time
        for a in range(0,self.p['num5YearAgeClasses']):
            self.canvas.create_text(170, 385 - (10 * a),
                                    text=str(5*a) + '-' + str(5*a+4),
                                    font='Helvetica 6',
                                    fill='white')

        ## Draw the overall map, including towns and houses (occupied houses only)
        for t in self.map.towns:
            xBasic = 580 + (t.x * self.p['pixelsPerTown'])
            yBasic = 15 + (t.y * self.p['pixelsPerTown'])
            self.canvas.create_rectangle(xBasic, yBasic,
                                         xBasic+self.p['pixelsPerTown'],
                                         yBasic+self.p['pixelsPerTown'],
                                         outline='grey',
                                         state = 'hidden' )

        for h in self.map.allHouses:
            t = h.town
            xBasic = 580 + (t.x * self.p['pixelsPerTown'])
            yBasic = 15 + (t.y * self.p['pixelsPerTown'])
            xOffset = xBasic + 2 + (h.x * 2)
            yOffset = yBasic + 2 + (h.y * 2)

            outlineColour = fillColour = self.p['houseSizeColour'][h.size]
            width = 1

            h.icon = self.canvas.create_rectangle(xOffset,yOffset,
                                                  xOffset + width, yOffset + width,
                                                  outline=outlineColour,
                                                  fill=fillColour,
                                                  state = 'normal' )

        self.canvas.update()
        time.sleep(0.5)
        self.canvas.update()

        for h in self.map.allHouses:
            self.canvas.itemconfig(h.icon, state='hidden')

        for h in self.map.occupiedHouses:
            self.canvas.itemconfig(h.icon, state='normal')

        self.canvas.update()
        self.updateCanvas()
        
    def updateCanvas(self):
        """Update the appearance of the graphics canvas."""

        ## First we clean the canvas off; some items are redrawn every time and others are not
        self.canvas.delete('redraw')

        ## Now post the current year and the current population size
        self.canvas.create_text(self.p['dateX'],
                                self.p['dateY'],
                                text='Year: ' + str(self.year),
                                font = self.p['mainFont'],
                                fill = self.p['fontColour'],
                                tags = 'redraw')
        self.canvas.create_text(self.p['popX'],
                                self.p['popY'],
                                text='Pop: ' + str(len(self.pop.livingPeople)),
                                font = self.p['mainFont'],
                                fill = self.p['fontColour'],
                                tags = 'redraw')

        self.canvas.create_text(self.p['popX'],
                                self.p['popY'] + 30,
                                text='Ever: ' + str(len(self.pop.allPeople)),
                                font = self.p['mainFont'],
                                fill = self.p['fontColour'],
                                tags = 'redraw')

        ## Also some other stats, but not on the first display
        if self.year > self.p['startYear']:
            self.canvas.create_text(350,20,
                                    text='Avg household: ' + str ( round ( self.avgHouseholdSize[-1] , 2 ) ),
                                    font = 'Helvetica 11',
                                    fill = 'white',
                                    tags = 'redraw')
            self.canvas.create_text(350,40,
                                    text='Marriages: ' + str(self.numMarriages[-1]),
                                    font = 'Helvetica 11',
                                    fill = 'white',
                                    tags = 'redraw')
            self.canvas.create_text(350,60,
                                    text='Divorces: ' + str(self.numDivorces[-1]),
                                    font = 'Helvetica 11',
                                    fill = 'white',
                                    tags = 'redraw')
            self.canvas.create_text(350,100,
                                    text='Total care demand: ' + str(round(self.totalCareDemand[-1], 0 ) ),
                                    font = 'Helvetica 11',
                                    fill = 'white',
                                    tags = 'redraw')
            self.canvas.create_text(350,120,
                                    text='Num taxpayers: ' + str(round(self.numTaxpayers[-1], 0 ) ),
                                    font = 'Helvetica 11',
                                    fill = 'white',
                                    tags = 'redraw')
            self.canvas.create_text(350,140,
                                    text='Family care ratio: ' + str(round(100.0 * self.totalFamilyCare[-1], 0 ) ) + "%",
                                    font = 'Helvetica 11',
                                    fill = 'white',
                                    tags = 'redraw')
            self.canvas.create_text(350,160,
                                    text='Tax burden: ' + str(round(self.totalTaxBurden[-1], 0 ) ),
                                    font = 'Helvetica 11',
                                    fill = 'white',
                                    tags = 'redraw')
            self.canvas.create_text(350,180,
                                    text='Marriage prop: ' + str(round(100.0 * self.marriageProp[-1], 0 ) ) + "%",
                                    font = 'Helvetica 11',
                                    fill = self.p['fontColour'],
                                    tags = 'redraw')

        

        ## Draw the population pyramid split by care categories
        for a in range(0,self.p['num5YearAgeClasses']):
            malePixel = 153
            femalePixel = 187
            for c in range(0,self.p['numCareLevels']):
                mWidth = self.pyramid.maleData[a,c]
                fWidth = self.pyramid.femaleData[a,c]

                if mWidth > 0:
                    self.canvas.create_rectangle(malePixel, 380 - (10*a),
                                                 malePixel - mWidth, 380 - (10*a) + 9,
                                                 outline=self.p['careLevelColour'][c],
                                                 fill=self.p['careLevelColour'][c],
                                                 tags = 'redraw')
                malePixel -= mWidth
                
                if fWidth > 0:
                    self.canvas.create_rectangle(femalePixel, 380 - (10*a),
                                                 femalePixel + fWidth, 380 - (10*a) + 9,
                                                 outline=self.p['careLevelColour'][c],
                                                 fill=self.p['careLevelColour'][c],
                                                 tags = 'redraw')
                femalePixel += fWidth

        ## Draw in the display house and the people who live in it
        if len(self.displayHouse.occupants) < 1:
            ## Nobody lives in the display house any more, choose another
            if self.nextDisplayHouse != None:
                self.displayHouse = self.nextDisplayHouse
                self.nextDisplayHouse = None
            else:
                self.displayHouse = random.choice(self.pop.livingPeople).house
                self.textUpdateList.append(str(self.year) + ": Display house empty, going to " + self.displayHouse.name + ".")
                messageString = "Residents: "
                for k in self.displayHouse.occupants:
                    messageString += "#" + str(k.id) + " "
                self.textUpdateList.append(messageString)
            

        outlineColour = self.p['houseSizeColour'][self.displayHouse.size]
        self.canvas.create_rectangle( 50, 450, 300, 650,
                                      outline = outlineColour,
                                      tags = 'redraw' )
        self.canvas.create_text ( 60, 660,
                                  text="Display house " + self.displayHouse.name,
                                  font='Helvetica 10',
                                  fill='white',
                                  anchor='nw',
                                  tags='redraw')
                                  

        ageBracketCounter = [ 0, 0, 0, 0, 0 ]

        for i in self.displayHouse.occupants:
            age = i.age
            ageBracket = age / 20
            if ageBracket > 4:
                ageBracket = 4
            careClass = i.careNeedLevel
            sex = i.sex
            idNumber = i.id
            self.drawPerson(age,ageBracket,ageBracketCounter[ageBracket],careClass,sex,idNumber)
            ageBracketCounter[ageBracket] += 1


        ## Draw in some text status updates on the right side of the map
        ## These need to scroll up the screen as time passes

        if len(self.textUpdateList) > self.p['maxTextUpdateList']:
            excess = len(self.textUpdateList) - self.p['maxTextUpdateList']
            self.textUpdateList = self.textUpdateList[excess:excess+self.p['maxTextUpdateList']]

        baseX = 1035
        baseY = 30
        for i in self.textUpdateList:
            self.canvas.create_text(baseX,baseY,
                                    text=i,
                                    anchor='nw',
                                    font='Helvetica 9',
                                    fill = 'white',
                                    width = 265,
                                    tags = 'redraw')
            baseY += 30

        ## Finish by updating the canvas and sleeping briefly in order to allow people to see it
        self.canvas.update()
        if self.p['delayTime'] > 0.0:
            time.sleep(self.p['delayTime'])


    def drawPerson(self, age, ageBracket, counter, careClass, sex, idNumber):
        baseX = 70 + ( counter * 30 )
        baseY = 620 - ( ageBracket * 30 )

        fillColour = self.p['careLevelColour'][careClass]

        self.canvas.create_oval(baseX,baseY,baseX+6,baseY+6,
                                fill=fillColour,
                                outline=fillColour,tags='redraw')
        if sex == 'male':
            self.canvas.create_rectangle(baseX-2,baseY+6,baseX+8,baseY+12,
                                fill=fillColour,outline=fillColour,tags='redraw')
        else:
            self.canvas.create_polygon(baseX+2,baseY+6,baseX-2,baseY+12,baseX+8,baseY+12,baseX+4,baseY+6,
                                fill=fillColour,outline=fillColour,tags='redraw')
        self.canvas.create_rectangle(baseX+1,baseY+13,baseX+5,baseY+20,
                                     fill=fillColour,outline=fillColour,tags='redraw')
            
        self.canvas.create_text(baseX+11,baseY,
                                text=str(age),
                                font='Helvetica 6',
                                fill='white',
                                anchor='nw',
                                tags='redraw')
        self.canvas.create_text(baseX+11,baseY+8,
                                text=str(idNumber),
                                font='Helvetica 6',
                                fill='grey',
                                anchor='nw',
                                tags='redraw')
        
    def doGraphs_fromFile(self, folder):
        """Plot the graphs needed at the end of one run."""

        # Load csv files
        filename = self.folder + '/Outputs.csv'
        output = pd.read_csv(filename, sep=',',header=0)

        # Chart 1: total social and child care demand and potential supply (from 1960 to 2020)
        fig, ax = plt.subplots()
        ax.plot(output['year'], output['totalCareSupply'], linewidth=2, label = 'Potential Supply', color = 'green')
        ax.stackplot(output['year'], output['socialCareNeed'], output['childCareNeed'], labels = ['Social Care Need','Child Care Need'])
        # ax.plot(years, self.totalSocialCareDemand, linewidth=2, label = 'Social Care Need', color = 'red')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours per week')
        # ax.set_xlabel('Year')
        ax.set_title('Care Needs and Potential Supply')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'DemandSupplyStackedChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 2: shares of care givers, total and by class shareCareGivers
        fig, ax = plt.subplots()
        p1, = ax.plot(output['year'], output['shareCareGivers'], linewidth = 3, label = 'Population')
        p2, = ax.plot(output['year'], output['shareCareGivers_1'], label = 'Class I')
        p3, = ax.plot(output['year'], output['shareCareGivers_2'], label = 'Class II')
        p4, = ax.plot(output['year'], output['shareCareGivers_3'], label = 'Class III')
        p5, = ax.plot(output['year'], output['shareCareGivers_4'], label = 'Class IV')
        p6, = ax.plot(output['year'], output['shareCareGivers_5'], label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Share of population')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Share of Care Givers')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'ShareCareGiversChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 3: shares of care takers by level of care need
        fig, ax = plt.subplots()
        ax.stackplot(output['year'], output['shareSocialCareTakers_N1'], output['shareSocialCareTakers_N2'], 
                      output['shareSocialCareTakers_N3'], output['shareSocialCareTakers_N4'],
                      labels = ['Need Level 1','Need Level 2', 'Need Level 3', 'Need level 4'])
        ax.set_xlim(left = self.p['statsCollectFrom'])
        # ax.set_ylabel('Share of Care Takers')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Share of Care Takers by Care Need Level')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.ylim(0, 1)
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'ShareByNeedLevelsStackedChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 4: Share of Social Care Needs (1960-2020)
        fig, ax = plt.subplots()
        p1, = ax.plot(output['year'], output['shareSocialCareDemand'], linewidth = 3, label = 'Population')
        p2, = ax.plot(output['year'], output['shareSocialCare_1'], label = 'Class I')
        p3, = ax.plot(output['year'], output['shareSocialCare_2'], label = 'Class II')
        p4, = ax.plot(output['year'], output['shareSocialCare_3'], label = 'Class III')
        p5, = ax.plot(output['year'], output['shareSocialCare_4'], label = 'Class IV')
        p6, = ax.plot(output['year'], output['shareSocialCare_5'], label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        # ax.set_ylabel('Share of Care Need')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Share of Social Care Need')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'ShareSocialCareNeedsChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 5: Per Capita total care demand and unmet care demand (1960-2020)    , 
        fig, ax = plt.subplots()
        ax.stackplot(output['year'], output['perCapitaCareReceived'], output['perCapitaUnmetCareDemand'], labels = ['Care Received','Unmet Care Need'])
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours per week')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Per Capita Received Care and Unmet Care Need')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'PerCapitaCareUnmetCareChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 6: Per Capita total social care demand and unmet social care demand (1960-2020) 
        fig, ax = plt.subplots()
        ax.stackplot(output['year'], output['perCapitaSocialCareReceived'], output['perCapitaUnmetSocialCareDemand'], labels = ['Care Received','Unmet Care Need'])
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours per week')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Per Capita Demand and Unmet Social Care Need')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'PerCapitaDemandUnmetSocialCareChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 7: Per Capita total child care demand and unmet child care demand (1960-2020)
        
        fig, ax = plt.subplots()
        ax.stackplot(output['year'], output['perCapitaChildCareReceived'], output['perCapitaUnmetChildCareDemand'], labels = ['Care Received','Unmet Care Need'])
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours per week')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Per Capita Demand and Unmet Child Care Need')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'PerCapitaDemandUnmetChildCareChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 8: total informal and formal care received and unmet care needs (from 1960 to 2020)
                   
        fig, ax = plt.subplots()
        ax.stackplot(output['year'], output['informalCareReceived'], output['formalCareReceived'], output['totalUnnmetCareNeed'], 
                     labels = ['Informal Care','Formal Care', 'Unmet Care Needs'])
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours per week')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Care by Type and Unmet Care Needs')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'CareReceivedStackedChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 9: Shares informal care received (from 1960 to 2020)
        
        #self.sharesInformalCare_M.append(np.mean(self.shareInformalCareReceived[-20:]))
        #self.sharesInformalCare_SD.append(np.std(self.shareInformalCareReceived[-20:]))
        
        fig, ax = plt.subplots()
        p1, = ax.plot(output['year'], output['shareInformalCareReceived'], linewidth = 3, label = 'Population')
        p2, = ax.plot(output['year'], output['shareInformalCareReceived_1'], label = 'Class I')
        p3, = ax.plot(output['year'], output['shareInformalCareReceived_2'], label = 'Class II')
        p4, = ax.plot(output['year'], output['shareInformalCareReceived_3'], label = 'Class III')
        p5, = ax.plot(output['year'], output['shareInformalCareReceived_4'], label = 'Class IV')
        p6, = ax.plot(output['year'], output['shareInformalCareReceived_5'], label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Share of care received')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Share of Informal Care Received')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'ShareInformalCareReceivedChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 10: Shares informal social care received (from 1960 to 2020)
        fig, ax = plt.subplots()
        p1, = ax.plot(output['year'], output['shareInformalSocialCare'], linewidth = 3, label = 'Population')
        p2, = ax.plot(output['year'], output['shareInformalSocialCare_1'], label = 'Class I')
        p3, = ax.plot(output['year'], output['shareInformalSocialCare_2'], label = 'Class II')
        p4, = ax.plot(output['year'], output['shareInformalSocialCare_3'], label = 'Class III')
        p5, = ax.plot(output['year'], output['shareInformalSocialCare_4'], label = 'Class IV')
        p6, = ax.plot(output['year'], output['shareInformalSocialCare_5'], label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Share of care received')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Share of Informal Social Care Received')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'ShareInformalSocialCareReceivedChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 11: Shares informal child care received (from 1960 to 2020)
        
        fig, ax = plt.subplots()
        p1, = ax.plot(output['year'], output['shareInformalChildCare'], linewidth = 3, label = 'Population')
        p2, = ax.plot(output['year'], output['shareInformalChildCare_1'], label = 'Class I')
        p3, = ax.plot(output['year'], output['shareInformalChildCare_2'], label = 'Class II')
        p4, = ax.plot(output['year'], output['shareInformalChildCare_3'], label = 'Class III')
        p5, = ax.plot(output['year'], output['shareInformalChildCare_4'], label = 'Class IV')
        p6, = ax.plot(output['year'], output['shareInformalChildCare_5'], label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Share of care received')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Share of Informal Child Care Received')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'ShareInformalChildCareReceivedChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 12: total informal and formal social care received and unmet social care needs (from 1960 to 2020)
        
        fig, ax = plt.subplots()
        ax.stackplot(output['year'], output['informalSocialCareReceived'], output['formalSocialCareReceived'], output['unmetSocialCareNeed'], 
                     labels = ['Informal Care','Formal Care', 'Unmet Care Needs'])
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours per week')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Social Care by Type and Unmet Care Needs')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'SocialCareReceivedStackedChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 13: total informal and formal child care received and unmet child care needs (from 1960 to 2020)
        
        fig, ax = plt.subplots()
        ax.stackplot(output['year'], output['informalChildCareReceived'], output['formalChildCareReceived'], output['unmetChildCareNeed'], 
                     labels = ['Informal Care','Formal Care', 'Unmet Care Needs'])
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours per week')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Child Care by Type and Unmet Care Needs')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        fig.tight_layout()
        path = os.path.join(folder, 'ChildCareReceivedStackedChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 14: Share of Unmet Care Need, total and by social class (from 1960 to 2020)
      
        fig, ax = plt.subplots()
        p1, = ax.plot(output['year'], output['shareUnmetCareDemand'], linewidth = 3, label = 'Population')
        p2, = ax.plot(output['year'], output['shareUnmetCareDemand_1'], label = 'Class I')
        p3, = ax.plot(output['year'], output['shareUnmetCareDemand_2'], label = 'Class II')
        p4, = ax.plot(output['year'], output['shareUnmetCareDemand_3'], label = 'Class III')
        p5, = ax.plot(output['year'], output['shareUnmetCareDemand_4'], label = 'Class IV')
        p6, = ax.plot(output['year'], output['shareUnmetCareDemand_5'], label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Share of care need')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Share of Unmet Care Need')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'ShareUnmetCareNeedChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 15: Share of Unmet Social Care Need, total and by social class (from 1960 to 2020)
        
        fig, ax = plt.subplots()
        p1, = ax.plot(output['year'], output['shareUnmetSocialCareDemand'], linewidth = 3, label = 'Population')
        p2, = ax.plot(output['year'], output['shareUnmetSocialCareDemand_1'], label = 'Class I')
        p3, = ax.plot(output['year'], output['shareUnmetSocialCareDemand_2'], label = 'Class II')
        p4, = ax.plot(output['year'], output['shareUnmetSocialCareDemand_3'], label = 'Class III')
        p5, = ax.plot(output['year'], output['shareUnmetSocialCareDemand_4'], label = 'Class IV')
        p6, = ax.plot(output['year'], output['shareUnmetSocialCareDemand_5'], label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Share of care need')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Share of Unmet Social Care Need')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'ShareUnmetSocialCareNeedChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 16: Share of Unmet Child Care Need, total and by social class (from 1960 to 2020)
        
        fig, ax = plt.subplots()
        p1, = ax.plot(output['year'], output['shareUnmetChildCareDemand'], linewidth = 3, label = 'Population')
        p2, = ax.plot(output['year'], output['shareUnmetChildCareDemand_1'], label = 'Class I')
        p3, = ax.plot(output['year'], output['shareUnmetChildCareDemand_2'], label = 'Class II')
        p4, = ax.plot(output['year'], output['shareUnmetChildCareDemand_3'], label = 'Class III')
        p5, = ax.plot(output['year'], output['shareUnmetChildCareDemand_4'], label = 'Class IV')
        p6, = ax.plot(output['year'], output['shareUnmetChildCareDemand_5'], label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Share of care need')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Share of Unmet Child Care Need')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'ShareUnmetChildCareNeedChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 17: Per Capita Unmet Care Need, total and by social class (from 1960 to 2020)
        fig, ax = plt.subplots()
        p1, = ax.plot(output['year'], output['perCapitaUnmetCareDemand'], linewidth = 3, label = 'Population')
        p2, = ax.plot(output['year'], output['perCapitaUnmetCareDemand_1'], label = 'Class I')
        p3, = ax.plot(output['year'], output['perCapitaUnmetCareDemand_2'], label = 'Class II')
        p4, = ax.plot(output['year'], output['perCapitaUnmetCareDemand_3'], label = 'Class III')
        p5, = ax.plot(output['year'], output['perCapitaUnmetCareDemand_4'], label = 'Class IV')
        p6, = ax.plot(output['year'], output['perCapitaUnmetCareDemand_5'], label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours per week')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Per Capita Unmet Care Need')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'PerCapitaUnmetNeedByClassChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 18: Average Unmet Care Need, total and by social class (from 1960 to 2020)
        fig, ax = plt.subplots()
        p1, = ax.plot(output['year'], output['averageUnmetCareDemand'], linewidth = 3, label = 'Population')
        p2, = ax.plot(output['year'], output['averageUnmetCareDemand_1'], label = 'Class I')
        p3, = ax.plot(output['year'], output['averageUnmetCareDemand_2'], label = 'Class II')
        p4, = ax.plot(output['year'], output['averageUnmetCareDemand_3'], label = 'Class III')
        p5, = ax.plot(output['year'], output['averageUnmetCareDemand_4'], label = 'Class IV')
        p6, = ax.plot(output['year'], output['averageUnmetCareDemand_5'], label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours per week')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Average Unmet Care Need')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'AverageUnmetCareNeedChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 19 
       
        n_groups = self.p['numberClasses']
        meanInformalCareReceived_1 = np.mean(output['informalCareReceived_1'][-20:])
        meanFormalCareReceived_1 = np.mean(output['formalCareReceived_1'][-20:])
        meanUnmetNeed_1 = np.mean(output['unmetCareNeed_1'][-20:])
        meanInformalCareReceived_2 = np.mean(output['informalCareReceived_2'][-20:])
        meanFormalCareReceived_2 = np.mean(output['formalCareReceived_2'][-20:])
        meanUnmetNeed_2 = np.mean(output['unmetCareNeed_2'][-20:])
        meanInformalCareReceived_3 = np.mean(output['informalCareReceived_3'][-20:])
        meanFormalCareReceived_3 = np.mean(output['formalCareReceived_3'][-20:])
        meanUnmetNeed_3 = np.mean(output['unmetCareNeed_3'][-20:])
        meanInformalCareReceived_4 = np.mean(output['informalCareReceived_4'][-20:])
        meanFormalCareReceived_4 = np.mean(output['formalCareReceived_4'][-20:])
        meanUnmetNeed_4 = np.mean(output['unmetCareNeed_4'][-20:])
        meanInformalCareReceived_5 = np.mean(output['informalCareReceived_5'][-20:])
        meanFormalCareReceived_5 = np.mean(output['formalCareReceived_5'][-20:])
        meanUnmetNeed_5 = np.mean(output['unmetCareNeed_5'][-20:])
        informalCare = (meanInformalCareReceived_1, meanInformalCareReceived_2, meanInformalCareReceived_3,
                        meanInformalCareReceived_4, meanInformalCareReceived_5)
        formalCare = (meanFormalCareReceived_1, meanFormalCareReceived_2, meanFormalCareReceived_3,
                      meanFormalCareReceived_4, meanFormalCareReceived_5)
        sumInformalFormalCare = [x + y for x, y in zip(informalCare, formalCare)]
        unmetNeeds = (meanUnmetNeed_1, meanUnmetNeed_2, meanUnmetNeed_3, meanUnmetNeed_4, meanUnmetNeed_5)
        ind = np.arange(n_groups)    # the x locations for the groups
        width = 0.4       # the width of the bars: can also be len(x) sequence
        
        fig, ax = plt.subplots()
        p1 = ax.bar(ind, informalCare, width, label = 'Informal Care')
        p2 = ax.bar(ind, formalCare, width, bottom = informalCare, label = 'Formal Care')
        p3 = ax.bar(ind, unmetNeeds, width, bottom = sumInformalFormalCare, label = 'Unmet Care Needs')
        ax.set_ylabel('Hours per week')
        ax.set_xticks(ind)
        plt.xticks(ind, ('I', 'II', 'III', 'IV', 'V'))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Informal, Formal and Unmet Care Need by Class')
        fig.tight_layout()
        path = os.path.join(folder, 'CareByClassStackedBarChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
         # Chart 20: informal care per recipient: population and by class
        
        fig, ax = plt.subplots()
        p1, = ax.plot(output['year'], output['informalCarePerRecipient'], linewidth = 3, label = 'Population')
        p2, = ax.plot(output['year'], output['informalCarePerRecipient_1'], label = 'Class I')
        p3, = ax.plot(output['year'], output['informalCarePerRecipient_2'], label = 'Class II')
        p4, = ax.plot(output['year'], output['informalCarePerRecipient_3'], label = 'Class III')
        p5, = ax.plot(output['year'], output['informalCarePerRecipient_4'], label = 'Class IV')
        p6, = ax.plot(output['year'], output['informalCarePerRecipient_5'], label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours per week')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Informal Care Per Recipient')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        ax.set_ylim([0, 50])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'InformalCarePerRecipientChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 21: formal care per recipient: population and by class
        fig, ax = plt.subplots()
        p1, = ax.plot(output['year'], output['formalCarePerRecipient'], linewidth = 3, label = 'Population')
        p2, = ax.plot(output['year'], output['formalCarePerRecipient_1'], label = 'Class I')
        p3, = ax.plot(output['year'], output['formalCarePerRecipient_2'], label = 'Class II')
        p4, = ax.plot(output['year'], output['formalCarePerRecipient_3'], label = 'Class III')
        p5, = ax.plot(output['year'], output['formalCarePerRecipient_4'], label = 'Class IV')
        p6, = ax.plot(output['year'], output['formalCarePerRecipient_5'], label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours per week')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Formal Care Per Recipient')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'FormalCarePerRecipientChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        
        
        # Chart 22: unmet care need per recipient: population and by class
        fig, ax = plt.subplots()
        p1, = ax.plot(output['year'], output['unmetCarePerRecipient'], linewidth = 3, label = 'Population')
        p2, = ax.plot(output['year'], output['unmetCarePerRecipient_1'], label = 'Class I')
        p3, = ax.plot(output['year'], output['unmetCarePerRecipient_2'], label = 'Class II')
        p4, = ax.plot(output['year'], output['unmetCarePerRecipient_3'], label = 'Class III')
        p5, = ax.plot(output['year'], output['unmetCarePerRecipient_4'], label = 'Class IV')
        p6, = ax.plot(output['year'], output['unmetCarePerRecipient_5'], label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours per week')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Unmet Care Need Per Recipient')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'UnmetCarePerRecipientChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 23: informal and formal care and unmet care need
        fig, ax = plt.subplots()
        p1, = ax.plot(output['year'], output['informalCarePerRecipient'], linewidth = 3, label = 'Informal Care')
        p2, = ax.plot(output['year'], output['formalCarePerRecipient'], linewidth = 3, label = 'Formal Care')
        p3, = ax.plot(output['year'], output['unmetCarePerRecipient'], linewidth = 3, label = 'Unmet Care')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours per week')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Delivered and Unmet Care Per Recipient')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        ax.set_ylim([0, 50])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'Delivered_UnmetCarePerRecipientChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 24: informal and formal care received and unmet care needs per recipient by social class (mean of last 20 years)
       
        n_groups = self.p['numberClasses']
        meanInformalCareReceived_1 = np.mean(output['informalCarePerRecipient_1'][-20:])
        meanFormalCareReceived_1 = np.mean(output['formalCarePerRecipient_1'][-20:])
        meanUnmetNeed_1 = np.mean(output['unmetCarePerRecipient_1'][-20:])
        meanInformalCareReceived_2 = np.mean(output['informalCarePerRecipient_2'][-20:])
        meanFormalCareReceived_2 = np.mean(output['formalCarePerRecipient_2'][-20:])
        meanUnmetNeed_2 = np.mean(output['unmetCarePerRecipient_2'][-20:])
        meanInformalCareReceived_3 = np.mean(output['informalCarePerRecipient_3'][-20:])
        meanFormalCareReceived_3 = np.mean(output['formalCarePerRecipient_3'][-20:])
        meanUnmetNeed_3 = np.mean(output['unmetCarePerRecipient_3'][-20:])
        meanInformalCareReceived_4 = np.mean(output['informalCarePerRecipient_4'][-20:])
        meanFormalCareReceived_4 = np.mean(output['formalCarePerRecipient_4'][-20:])
        meanUnmetNeed_4 = np.mean(output['unmetCarePerRecipient_4'][-20:])
        meanInformalCareReceived_5 = np.mean(output['informalCarePerRecipient_5'][-20:])
        meanFormalCareReceived_5 = np.mean(output['formalCarePerRecipient_5'][-20:])
        meanUnmetNeed_5 = np.mean(output['unmetCarePerRecipient_5'][-20:])
        informalCare = (meanInformalCareReceived_1, meanInformalCareReceived_2, meanInformalCareReceived_3,
                        meanInformalCareReceived_4, meanInformalCareReceived_5)
        formalCare = (meanFormalCareReceived_1, meanFormalCareReceived_2, meanFormalCareReceived_3,
                      meanFormalCareReceived_4, meanFormalCareReceived_5)
        sumInformalFormalCare = [x + y for x, y in zip(informalCare, formalCare)]
        unmetNeeds = (meanUnmetNeed_1, meanUnmetNeed_2, meanUnmetNeed_3, meanUnmetNeed_4, meanUnmetNeed_5)
        ind = np.arange(n_groups)    # the x locations for the groups
        width = 0.4       # the width of the bars: can also be len(x) sequence
        
        fig, ax = plt.subplots()
        p1 = ax.bar(ind, informalCare, width, label = 'Informal Care')
        p2 = ax.bar(ind, formalCare, width, bottom = informalCare, label = 'Formal Care')
        p3 = ax.bar(ind, unmetNeeds, width, bottom = sumInformalFormalCare, label = 'Unmet Care Needs')
        ax.set_ylabel('Hours per week')
        ax.set_xticks(ind)
        plt.xticks(ind, ('I', 'II', 'III', 'IV', 'V'))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Informal, Formal and Unmet Care Need per Recipient')
        fig.tight_layout()
        path = os.path.join(folder, 'CarePerRecipientByClassStackedBarChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
       # Chart 25: informal and formal social care received and unmet social care needs by social class (mean of last 20 years)
       
        n_groups = self.p['numberClasses']
        meanInformalCareReceived_1 = np.mean(output['informalSocialCareReceived_1'][-20:])
        meanFormalCareReceived_1 = np.mean(output['formalSocialCareReceived_1'][-20:])
        meanUnmetNeed_1 = np.mean(output['unmetSocialCareNeed_1'][-20:])
        meanInformalCareReceived_2 = np.mean(output['informalSocialCareReceived_2'][-20:])
        meanFormalCareReceived_2 = np.mean(output['formalSocialCareReceived_2'][-20:])
        meanUnmetNeed_2 = np.mean(output['unmetSocialCareNeed_2'][-20:])
        meanInformalCareReceived_3 = np.mean(output['informalSocialCareReceived_3'][-20:])
        meanFormalCareReceived_3 = np.mean(output['formalSocialCareReceived_3'][-20:])
        meanUnmetNeed_3 = np.mean(output['unmetSocialCareNeed_3'][-20:])
        meanInformalCareReceived_4 = np.mean(output['informalSocialCareReceived_4'][-20:])
        meanFormalCareReceived_4 = np.mean(output['formalSocialCareReceived_4'][-20:])
        meanUnmetNeed_4 = np.mean(output['unmetSocialCareNeed_4'][-20:])
        meanInformalCareReceived_5 = np.mean(output['informalSocialCareReceived_5'][-20:])
        meanFormalCareReceived_5 = np.mean(output['formalSocialCareReceived_5'][-20:])
        meanUnmetNeed_5 = np.mean(output['unmetSocialCareNeed_5'][-20:])
        informalCare = (meanInformalCareReceived_1, meanInformalCareReceived_2, meanInformalCareReceived_3,
                        meanInformalCareReceived_4, meanInformalCareReceived_5)
        formalCare = (meanFormalCareReceived_1, meanFormalCareReceived_2, meanFormalCareReceived_3,
                      meanFormalCareReceived_4, meanFormalCareReceived_5)
        sumInformalFormalCare = [x + y for x, y in zip(informalCare, formalCare)]
        unmetNeeds = (meanUnmetNeed_1, meanUnmetNeed_2, meanUnmetNeed_3, meanUnmetNeed_4, meanUnmetNeed_5)
        ind = np.arange(n_groups)    # the x locations for the groups
        width = 0.4       # the width of the bars: can also be len(x) sequence
        
        fig, ax = plt.subplots()
        p1 = ax.bar(ind, informalCare, width, label = 'Informal Care')
        p2 = ax.bar(ind, formalCare, width, bottom = informalCare, label = 'Formal Care')
        p3 = ax.bar(ind, unmetNeeds, width, bottom = sumInformalFormalCare, label = 'Unmet Care Needs')
        ax.set_ylabel('Hours per week')
        ax.set_xticks(ind)
        plt.xticks(ind, ('I', 'II', 'III', 'IV', 'V'))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Informal, Formal and Unmet Social Care Need by Class')
        fig.tight_layout()
        path = os.path.join(folder, 'SocialCareByClassStackedBarChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 26: informal and formal social care received and unmet social care needs per recipient by social class (mean of last 20 years)
   
        fig, ax = plt.subplots()
        p1, = ax.plot(output['year'], output['informalSocialCarePerRecipient'], linewidth = 3, label = 'Population')
        p2, = ax.plot(output['year'], output['informalSocialCarePerRecipient_1'], label = 'Class I')
        p3, = ax.plot(output['year'], output['informalSocialCarePerRecipient_2'], label = 'Class II')
        p4, = ax.plot(output['year'], output['informalSocialCarePerRecipient_3'], label = 'Class III')
        p5, = ax.plot(output['year'], output['informalSocialCarePerRecipient_4'], label = 'Class IV')
        p6, = ax.plot(output['year'], output['informalSocialCarePerRecipient_5'], label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours per week')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Informal Social Care Per Recipient')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'informalSocialCarePerRecipientChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 27: formal care per recipient: population and by class
        fig, ax = plt.subplots()
        p1, = ax.plot(output['year'], output['formalSocialCarePerRecipient'], linewidth = 3, label = 'Population')
        p2, = ax.plot(output['year'], output['formalSocialCarePerRecipient_1'], label = 'Class I')
        p3, = ax.plot(output['year'], output['formalSocialCarePerRecipient_2'], label = 'Class II')
        p4, = ax.plot(output['year'], output['formalSocialCarePerRecipient_3'], label = 'Class III')
        p5, = ax.plot(output['year'], output['formalSocialCarePerRecipient_4'], label = 'Class IV')
        p6, = ax.plot(output['year'], output['formalSocialCarePerRecipient_5'], label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours per week')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Formal Social Care Per Recipient')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'formalSocialCarePerRecipientChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()

        # Chart 28: unmet care need per recipient: population and by class
        fig, ax = plt.subplots()
        p1, = ax.plot(output['year'], output['unmetSocialCarePerRecipient'], linewidth = 3, label = 'Population')
        p2, = ax.plot(output['year'], output['unmetSocialCarePerRecipient_1'], label = 'Class I')
        p3, = ax.plot(output['year'], output['unmetSocialCarePerRecipient_2'], label = 'Class II')
        p4, = ax.plot(output['year'], output['unmetSocialCarePerRecipient_3'], label = 'Class III')
        p5, = ax.plot(output['year'], output['unmetSocialCarePerRecipient_4'], label = 'Class IV')
        p6, = ax.plot(output['year'], output['unmetSocialCarePerRecipient_5'], label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours per week')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Unmet Social Care Need Per Recipient')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'UnmetSocialCarePerRecipientChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 29: informal and formal care and unmet care need
        fig, ax = plt.subplots()
        p1, = ax.plot(output['year'], output['informalSocialCarePerRecipient'], linewidth = 3, label = 'Informal Care')
        p2, = ax.plot(output['year'], output['formalSocialCarePerRecipient'], linewidth = 3, label = 'Formal Care')
        p3, = ax.plot(output['year'], output['unmetSocialCarePerRecipient'], linewidth = 3, label = 'Unmet Care')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours per week')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Delivered and Unmet Care Per Recipient')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'Delivered_UnmetSocialCarePerRecipientChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 30

        n_groups = self.p['numberClasses']
        meanInformalCareReceived_1 = np.mean(output['informalSocialCarePerRecipient_1'][-20:])
        meanFormalCareReceived_1 = np.mean(output['formalSocialCarePerRecipient_1'][-20:])
        meanUnmetNeed_1 = np.mean(output['unmetSocialCarePerRecipient_1'][-20:])
        meanInformalCareReceived_2 = np.mean(output['informalSocialCarePerRecipient_2'][-20:])
        meanFormalCareReceived_2 = np.mean(output['formalSocialCarePerRecipient_2'][-20:])
        meanUnmetNeed_2 = np.mean(output['unmetSocialCarePerRecipient_2'][-20:])
        meanInformalCareReceived_3 = np.mean(output['informalSocialCarePerRecipient_3'][-20:])
        meanFormalCareReceived_3 = np.mean(output['formalSocialCarePerRecipient_3'][-20:])
        meanUnmetNeed_3 = np.mean(output['unmetSocialCarePerRecipient_3'][-20:])
        meanInformalCareReceived_4 = np.mean(output['informalSocialCarePerRecipient_4'][-20:])
        meanFormalCareReceived_4 = np.mean(output['formalSocialCarePerRecipient_4'][-20:])
        meanUnmetNeed_4 = np.mean(output['unmetSocialCarePerRecipient_4'][-20:])
        meanInformalCareReceived_5 = np.mean(output['informalSocialCarePerRecipient_5'][-20:])
        meanFormalCareReceived_5 = np.mean(output['formalSocialCarePerRecipient_5'][-20:])
        meanUnmetNeed_5 = np.mean(output['unmetSocialCarePerRecipient_5'][-20:])
        informalCare = (meanInformalCareReceived_1, meanInformalCareReceived_2, meanInformalCareReceived_3,
                        meanInformalCareReceived_4, meanInformalCareReceived_5)
        formalCare = (meanFormalCareReceived_1, meanFormalCareReceived_2, meanFormalCareReceived_3,
                      meanFormalCareReceived_4, meanFormalCareReceived_5)
        sumInformalFormalCare = [x + y for x, y in zip(informalCare, formalCare)]
        unmetNeeds = (meanUnmetNeed_1, meanUnmetNeed_2, meanUnmetNeed_3, meanUnmetNeed_4, meanUnmetNeed_5)
        ind = np.arange(n_groups)    # the x locations for the groups
        width = 0.4       # the width of the bars: can also be len(x) sequence
        
        fig, ax = plt.subplots()
        p1 = ax.bar(ind, informalCare, width, label = 'Informal Care')
        p2 = ax.bar(ind, formalCare, width, bottom = informalCare, label = 'Formal Care')
        p3 = ax.bar(ind, unmetNeeds, width, bottom = sumInformalFormalCare, label = 'Unmet Care Needs')
        ax.set_ylabel('Hours per week')
        ax.set_xticks(ind)
        plt.xticks(ind, ('I', 'II', 'III', 'IV', 'V'))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Informal, Formal and Unmet Social Care Need per Recipient')
        fig.tight_layout()
        path = os.path.join(folder, 'SocialCarePerRecipientByClassStackedBarChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 31: informal and formal child care received and unmet child care needs by social class (mean of last 20 years)
       
        n_groups = self.p['numberClasses']
        meanInformalCareReceived_1 = np.mean(output['informalChildCareReceived_1'][-20:])
        meanFormalCareReceived_1 = np.mean(output['formalChildCareReceived_1'][-20:])
        meanUnmetNeed_1 = np.mean(output['unmetChildCareNeed_1'][-20:])
        meanInformalCareReceived_2 = np.mean(output['informalChildCareReceived_2'][-20:])
        meanFormalCareReceived_2 = np.mean(output['formalChildCareReceived_2'][-20:])
        meanUnmetNeed_2 = np.mean(output['unmetChildCareNeed_2'][-20:])
        meanInformalCareReceived_3 = np.mean(output['informalChildCareReceived_3'][-20:])
        meanFormalCareReceived_3 = np.mean(output['formalChildCareReceived_3'][-20:])
        meanUnmetNeed_3 = np.mean(output['unmetChildCareNeed_3'][-20:])
        meanInformalCareReceived_4 = np.mean(output['informalChildCareReceived_4'][-20:])
        meanFormalCareReceived_4 = np.mean(output['formalChildCareReceived_4'][-20:])
        meanUnmetNeed_4 = np.mean(output['unmetChildCareNeed_4'][-20:])
        meanInformalCareReceived_5 = np.mean(output['informalChildCareReceived_5'][-20:])
        meanFormalCareReceived_5 = np.mean(output['formalChildCareReceived_5'][-20:])
        meanUnmetNeed_5 = np.mean(output['unmetChildCareNeed_5'][-20:])
        informalCare = (meanInformalCareReceived_1, meanInformalCareReceived_2, meanInformalCareReceived_3,
                        meanInformalCareReceived_4, meanInformalCareReceived_5)
        formalCare = (meanFormalCareReceived_1, meanFormalCareReceived_2, meanFormalCareReceived_3,
                      meanFormalCareReceived_4, meanFormalCareReceived_5)
        sumInformalFormalCare = [x + y for x, y in zip(informalCare, formalCare)]
        totCare = [sum(x) for x in zip(informalCare, formalCare)]
        unmetNeeds = (meanUnmetNeed_1, meanUnmetNeed_2, meanUnmetNeed_3, meanUnmetNeed_4, meanUnmetNeed_5)
        ind = np.arange(n_groups)    # the x locations for the groups
        width = 0.4       # the width of the bars: can also be len(x) sequence
        
        fig, ax = plt.subplots()
        p1 = ax.bar(ind, informalCare, width, label = 'Informal Care')
        p2 = ax.bar(ind, formalCare, width, bottom = informalCare, label = 'Formal Care')
        p3 = ax.bar(ind, unmetNeeds, width, bottom = sumInformalFormalCare, label = 'Unmet Care Needs')
        ax.set_ylabel('Hours per week')
        ax.set_ylim([0, max(totCare)*1.1])
        ax.set_xticks(ind)
        plt.xticks(ind, ('I', 'II', 'III', 'IV', 'V'))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Informal, Formal and Unmet Child Care Need by Class')
        fig.tight_layout()
        path = os.path.join(folder, 'ChildCareByClassStackedBarChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 32: informal and formal child care received and unmet child care needs per recipient by Child class (mean of last 20 years)

        ### Add the three charts for the child care
        fig, ax = plt.subplots()
        p1, = ax.plot(output['year'], output['informalChildCarePerRecipient'], linewidth = 3, label = 'Population')
        p2, = ax.plot(output['year'], output['informalChildCarePerRecipient_1'], label = 'Class I')
        p3, = ax.plot(output['year'], output['informalChildCarePerRecipient_2'], label = 'Class II')
        p4, = ax.plot(output['year'], output['informalChildCarePerRecipient_3'], label = 'Class III')
        p5, = ax.plot(output['year'], output['informalChildCarePerRecipient_4'], label = 'Class IV')
        p6, = ax.plot(output['year'], output['informalChildCarePerRecipient_5'], label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours per week')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Informal Child Care Per Recipient')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'informalChildCarePerRecipientChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 33: formal care per recipient: population and by class
        fig, ax = plt.subplots()
        p1, = ax.plot(output['year'], output['formalChildCarePerRecipient'], linewidth = 3, label = 'Population')
        p2, = ax.plot(output['year'], output['formalChildCarePerRecipient_1'], label = 'Class I')
        p3, = ax.plot(output['year'], output['formalChildCarePerRecipient_2'], label = 'Class II')
        p4, = ax.plot(output['year'], output['formalChildCarePerRecipient_3'], label = 'Class III')
        p5, = ax.plot(output['year'], output['formalChildCarePerRecipient_4'], label = 'Class IV')
        p6, = ax.plot(output['year'], output['formalChildCarePerRecipient_5'], label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours per week')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Formal Child Care Per Recipient')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'formalChildCarePerRecipientChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()

         # Chart 34: Average Supply by Class (from 1960 to 2020)
         
        fig, ax = plt.subplots()
        p1, = ax.plot(output['year'], output['carePerRecipient'], linewidth = 3, label = 'Population')
        p2, = ax.plot(output['year'], output['carePerRecipient_1'], label = 'Class I')
        p3, = ax.plot(output['year'], output['carePerRecipient_2'], label = 'Class II')
        p4, = ax.plot(output['year'], output['carePerRecipient_3'], label = 'Class III')
        p5, = ax.plot(output['year'], output['carePerRecipient_4'], label = 'Class IV')
        p6, = ax.plot(output['year'], output['carePerRecipient_5'], label = 'Class V')
        maxValues = [max(output['carePerRecipient']), max(output['carePerRecipient_1']), max(output['carePerRecipient_2']), max(output['carePerRecipient_3']), max(output['carePerRecipient_4']), max(output['carePerRecipient_5'])]
        maxValue = max(maxValues)
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylim([0, maxValue*2.0])
        ax.set_ylabel('Hours per week')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Average Hours of Care By Class')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_ylim([0, 60])
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'CarePerRecipientChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        

        # Chart 35: unmet care need per recipient: population and by class
        fig, ax = plt.subplots()
        p1, = ax.plot(output['year'], output['unmetChildCarePerRecipient'], linewidth = 3, label = 'Population')
        p2, = ax.plot(output['year'], output['unmetChildCarePerRecipient_1'], label = 'Class I')
        p3, = ax.plot(output['year'], output['unmetChildCarePerRecipient_2'], label = 'Class II')
        p4, = ax.plot(output['year'], output['unmetChildCarePerRecipient_3'], label = 'Class III')
        p5, = ax.plot(output['year'], output['unmetChildCarePerRecipient_4'], label = 'Class IV')
        p6, = ax.plot(output['year'], output['unmetChildCarePerRecipient_5'], label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours per week')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Unmet Child Care Need Per Recipient')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'UnmetChildCarePerRecipientChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 36: informal and formal care and unmet care need
        fig, ax = plt.subplots()
        p1, = ax.plot(output['year'], output['informalChildCarePerRecipient'], linewidth = 3, label = 'Informal Care')
        p2, = ax.plot(output['year'], output['formalChildCarePerRecipient'], linewidth = 3, label = 'Formal Care')
        p3, = ax.plot(output['year'], output['unmetChildCarePerRecipient'], linewidth = 3, label = 'Unmet Care')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours per week')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Delivered and Unmet Child Care Per Recipient')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        ax.set_ylim([0, 30])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'Delivered_UnmetChildCarePerRecipientChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 37
        n_groups = self.p['numberClasses']
        meanInformalCareReceived_1 = np.mean(output['informalChildCarePerRecipient_1'][-20:])
        meanFormalCareReceived_1 = np.mean(output['formalChildCarePerRecipient_1'][-20:])
        meanUnmetNeed_1 = np.mean(output['unmetChildCarePerRecipient_1'][-20:])
        meanInformalCareReceived_2 = np.mean(output['informalChildCarePerRecipient_2'][-20:])
        meanFormalCareReceived_2 = np.mean(output['formalChildCarePerRecipient_2'][-20:])
        meanUnmetNeed_2 = np.mean(output['unmetChildCarePerRecipient_2'][-20:])
        meanInformalCareReceived_3 = np.mean(output['informalChildCarePerRecipient_3'][-20:])
        meanFormalCareReceived_3 = np.mean(output['formalChildCarePerRecipient_3'][-20:])
        meanUnmetNeed_3 = np.mean(output['unmetChildCarePerRecipient_3'][-20:])
        meanInformalCareReceived_4 = np.mean(output['informalChildCarePerRecipient_4'][-20:])
        meanFormalCareReceived_4 = np.mean(output['formalChildCarePerRecipient_4'][-20:])
        meanUnmetNeed_4 = np.mean(output['unmetChildCarePerRecipient_4'][-20:])
        meanInformalCareReceived_5 = np.mean(output['informalChildCarePerRecipient_5'][-20:])
        meanFormalCareReceived_5 = np.mean(output['formalChildCarePerRecipient_5'][-20:])
        meanUnmetNeed_5 = np.mean(output['unmetChildCarePerRecipient_5'][-20:])
        informalCare = (meanInformalCareReceived_1, meanInformalCareReceived_2, meanInformalCareReceived_3,
                        meanInformalCareReceived_4, meanInformalCareReceived_5)
        formalCare = (meanFormalCareReceived_1, meanFormalCareReceived_2, meanFormalCareReceived_3,
                      meanFormalCareReceived_4, meanFormalCareReceived_5)
        sumInformalFormalCare = [x + y for x, y in zip(informalCare, formalCare)]
        totCare = [sum(x) for x in zip(informalCare, formalCare)]
        unmetNeeds = (meanUnmetNeed_1, meanUnmetNeed_2, meanUnmetNeed_3, meanUnmetNeed_4, meanUnmetNeed_5)
        ind = np.arange(n_groups)    # the x locations for the groups
        width = 0.4       # the width of the bars: can also be len(x) sequence
        
        fig, ax = plt.subplots()
        p1 = ax.bar(ind, informalCare, width, label = 'Informal Care')
        p2 = ax.bar(ind, formalCare, width, bottom = informalCare, label = 'Formal Care')
        p3 = ax.bar(ind, unmetNeeds, width, bottom = sumInformalFormalCare, label = 'Unmet Care Needs')
        ax.set_ylim([0, max(totCare)*1.1])
        ax.set_ylabel('Hours per week')
        ax.set_xticks(ind)
        plt.xticks(ind, ('I', 'II', 'III', 'IV', 'V'))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Informal, Formal and Unmet Child Care Need per Recipient')
        fig.tight_layout()
        path = os.path.join(folder, 'ChildCarePerRecipientByClassStackedBarChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 38: informal and formal care supplied per carer by social class (mean of last 20 years)
        
        n_groups = self.p['numberClasses']
        meanInformalCareSupplied_1 = np.mean(output['informalCarePerCarer_1'][-20:])
        meanFormalCareSupplied_1 = np.mean(output['formalCarePerCarer_1'][-20:])
        meanInformalCareSupplied_2 = np.mean(output['informalCarePerCarer_2'][-20:])
        meanFormalCareSupplied_2 = np.mean(output['formalCarePerCarer_2'][-20:])
        meanInformalCareSupplied_3 = np.mean(output['informalCarePerCarer_3'][-20:])
        meanFormalCareSupplied_3 = np.mean(output['formalCarePerCarer_3'][-20:])
        meanInformalCareSupplied_4 = np.mean(output['informalCarePerCarer_4'][-20:])
        meanFormalCareSupplied_4 = np.mean(output['formalCarePerCarer_4'][-20:])
        meanInformalCareSupplied_5 = np.mean(output['informalCarePerCarer_5'][-20:])
        meanFormalCareSupplied_5 = np.mean(output['formalCarePerCarer_5'][-20:])
        informalCare = (meanInformalCareSupplied_1, meanInformalCareSupplied_2, meanInformalCareSupplied_3,
                        meanInformalCareSupplied_4, meanInformalCareSupplied_5)
        formalCare = (meanFormalCareSupplied_1, meanFormalCareSupplied_2, meanFormalCareSupplied_3,
                      meanFormalCareSupplied_4, meanFormalCareSupplied_5)
        totCare = [sum(x) for x in zip(informalCare, formalCare)]
        ind = np.arange(n_groups)    # the x locations for the groups
        width = 0.4       # the width of the bars: can also be len(x) sequence
        fig, ax = plt.subplots()
        p1 = ax.bar(ind, informalCare, width, label = 'Informal Care')
        p2 = ax.bar(ind, formalCare, width, bottom = informalCare, label = 'Formal Care')
        ax.set_ylim([0, max(totCare)*1.1])
        ax.set_ylabel('Hours per week')
        ax.set_xticks(ind)
        plt.xticks(ind, ('I', 'II', 'III', 'IV', 'V'))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Informal and Formal Care per Carer')
        fig.tight_layout()
        path = os.path.join(folder, 'CarePerCarerByClassStackedBarChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 39: informal and formal care supplied by kinship network distance (mean of last 20 years) # Modified y lim
           
        n_groups = 4
        meanInformalCareHousehold = np.mean(output['sumNoK_informalSupplies[0]'][-20:])
        meanFormalCareHousehold = np.mean(output['sumNoK_formalSupplies[0]'][-20:])
        meanInformalCare_K1 = np.mean(output['sumNoK_informalSupplies[1]'][-20:])
        meanFormalCare_K1 = np.mean(output['sumNoK_formalSupplies[1]'][-20:])
        meanInformalCare_K2 = np.mean(output['sumNoK_informalSupplies[2]'][-20:])
        meanFormalCare_K2 = np.mean(output['sumNoK_formalSupplies[2]'][-20:])
        meanInformalCare_K3 = np.mean(output['sumNoK_informalSupplies[3]'][-20:])
        meanFormalCare_K3 = np.mean(output['sumNoK_formalSupplies[3]'][-20:])
        informalCare = (meanInformalCareHousehold, meanInformalCare_K1, meanInformalCare_K2, meanInformalCare_K3)
        formalCare = (meanFormalCareHousehold, meanFormalCare_K1, meanFormalCare_K2, meanFormalCare_K3)
        totCare = [sum(x) for x in zip(informalCare, formalCare)]
        ind = np.arange(n_groups)    # the x locations for the groups
        width = 0.4       # the width of the bars: can also be len(x) sequence
        fig, ax = plt.subplots()
        p1 = ax.bar(ind, informalCare, width, label = 'Informal Care')
        p2 = ax.bar(ind, formalCare, width, bottom = informalCare, label = 'Formal Care')
        ax.set_ylim([0, max(totCare)*1.1])
        ax.set_xticks(ind)
        plt.xticks(ind, ('Household', 'I', 'II', 'III'))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper right')
        ax.set_title('Informal and Formal Care per Kinship Level')
        fig.tight_layout()
        path = os.path.join(folder, 'InformalFormalCareByKinshipStackedBarChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 40: Share of Care supplied by Women, total and by social class (from 1960 to 2020)
       
        fig, ax = plt.subplots()
        p1, = ax.plot(output['year'], output['shareInformalCareSuppliedByFemales'], linewidth = 3)
#        p2, = ax.plot(output['year'], output['shareInformalCareSuppliedByFemales_1'], label = 'Class I')
#        p3, = ax.plot(output['year'], output['shareInformalCareSuppliedByFemales_2'], label = 'Class II')
#        p4, = ax.plot(output['year'], output['shareInformalCareSuppliedByFemales_3'], label = 'Class III')
#        p5, = ax.plot(output['year'], output['shareInformalCareSuppliedByFemales_4'], label = 'Class IV')
#        p6, = ax.plot(output['year'], output['shareInformalCareSuppliedByFemales_5'], label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Share of care')
        ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.legend_.remove()
        ax.set_title('Share of Informal Care supplied by Women')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        # ax.set_ylim([0, 0.8])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'ShareCareWomedChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 41: informal care provided by gender per social class (mean of last 20 years)
        
        n_groups = self.p['numberClasses']
        informalCareMales_1 = np.mean(output['informalCareSuppliedByMales_1'][-20:])
        informalCareMales_2 = np.mean(output['informalCareSuppliedByMales_2'][-20:])
        informalCareMales_3 = np.mean(output['informalCareSuppliedByMales_3'][-20:])
        informalCareMales_4 = np.mean(output['informalCareSuppliedByMales_4'][-20:])
        informalCareMales_5 = np.mean(output['informalCareSuppliedByMales_5'][-20:])
        informalCareFemales_1 = np.mean(output['informalCareSuppliedByFemales_1'][-20:])
        informalCareFemales_2 = np.mean(output['informalCareSuppliedByFemales_2'][-20:])
        informalCareFemales_3 = np.mean(output['informalCareSuppliedByFemales_3'][-20:])
        informalCareFemales_4 = np.mean(output['informalCareSuppliedByFemales_4'][-20:])
        informalCareFemales_5 = np.mean(output['informalCareSuppliedByFemales_5'][-20:])
        means_males = (informalCareMales_1, informalCareMales_2, informalCareMales_3, informalCareMales_4, informalCareMales_5)
        means_females = (informalCareFemales_1, informalCareFemales_2, informalCareFemales_3, informalCareFemales_4, informalCareFemales_5)
        fig, ax = plt.subplots()
        index = np.arange(n_groups)
        bar_width = 0.35
        opacity = 0.8
        rects1 = ax.bar(index, means_females, bar_width,
                         alpha=opacity,
                         color='b',
                         label='Female')
        rects2 = ax.bar(index + bar_width, means_males, bar_width,
                         alpha=opacity,
                         color='g',
                         label='Male')
        ax.set_ylabel('Hours per week')
        ax.set_xlabel('Socio-Economic Classes')
        ax.set_title('Informal Care Supplied by Gender')
        ax.set_xticks(ind + bar_width/2)
        plt.xticks(index + bar_width/2, ('I', 'II', 'III', 'IV', 'V'))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1])
        fig.tight_layout()
        path = os.path.join(folder, 'InformalCareByGenderAndClassGroupedBarChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
         # Chart 42: Ratio Women Income and Men Income, total and by social class (from 1960 to 2020)
       
        fig, ax = plt.subplots()
        p1, = ax.plot(output['year'], output['ratioWage'], linewidth = 3, label = 'Population')
        p2, = ax.plot(output['year'], output['ratioWage_1'], label = 'Class I')
        p3, = ax.plot(output['year'], output['ratioWage_2'], label = 'Class II')
        p4, = ax.plot(output['year'], output['ratioWage_3'], label = 'Class III')
        p5, = ax.plot(output['year'], output['ratioWage_4'], label = 'Class IV')
        p6, = ax.plot(output['year'], output['ratioWage_5'], label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Wage Ratio')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Women and Men Wage Ratio')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'WomenMenWageRatioChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 43: income by gender per social class (mean of last 20 years)
               
        n_groups = self.p['numberClasses']
        WageMales_1 = np.mean(output['averageMalesWage_1'][-20:])
        WageMales_2 = np.mean(output['averageMalesWage_2'][-20:])
        WageMales_3 = np.mean(output['averageMalesWage_3'][-20:])
        WageMales_4 = np.mean(output['averageMalesWage_4'][-20:])
        WageMales_5 = np.mean(output['averageMalesWage_5'][-20:])
        WageFemales_1 = np.mean(output['averageFemalesWage_1'][-20:])
        WageFemales_2 = np.mean(output['averageFemalesWage_2'][-20:])
        WageFemales_3 = np.mean(output['averageFemalesWage_3'][-20:])
        WageFemales_4 = np.mean(output['averageFemalesWage_4'][-20:])
        WageFemales_5 = np.mean(output['averageFemalesWage_5'][-20:])
        means_males = (WageMales_1, WageMales_2, WageMales_3, WageMales_4, WageMales_5)
        means_females = (WageFemales_1, WageFemales_2, WageFemales_3, WageFemales_4, WageFemales_5)
        fig, ax = plt.subplots()
        index = np.arange(n_groups)
        bar_width = 0.35
        opacity = 0.8
        rects3 = ax.bar(index, means_females, bar_width,
                         alpha=opacity,
                         color='b',
                         label='Female')
        rects4 = ax.bar(index + bar_width, means_males, bar_width,
                         alpha=opacity,
                         color='g',
                         label='Male')
        ax.set_ylabel('Average Wage')
        ax.set_xlabel('Socio-Economic Classes')
        ax.set_title('Female and Male Average Wage')
        ax.set_xticks(ind + bar_width/2)
        plt.xticks(index + bar_width/2, ('I', 'II', 'III', 'IV', 'V'))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1])
        plt.tight_layout()
        path = os.path.join(folder, 'WageByGenderAndClassGroupedBarChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 44: Ratio Women Income and Men Income, total and by social class (from 1960 to 2020)
       
        fig, ax = plt.subplots()
        p1, = ax.plot(output['year'], output['ratioIncome'], linewidth = 3, label = 'Population')
        p2, = ax.plot(output['year'], output['ratioIncome_1'], label = 'Class I')
        p3, = ax.plot(output['year'], output['ratioIncome_2'], label = 'Class II')
        p4, = ax.plot(output['year'], output['ratioIncome_3'], label = 'Class III')
        p5, = ax.plot(output['year'], output['ratioIncome_4'], label = 'Class IV')
        p6, = ax.plot(output['year'], output['ratioIncome_5'], label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Income Ratio')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Women and Men Income Ratio')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'WomenMenIncomeRatioChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 45: income by gender per social class (mean of last 20 years)
        
        n_groups = self.p['numberClasses']
        incomeMales_1 = np.mean(output['averageMalesIncome_1'][-20:])
        incomeMales_2 = np.mean(output['averageMalesIncome_2'][-20:])
        incomeMales_3 = np.mean(output['averageMalesIncome_3'][-20:])
        incomeMales_4 = np.mean(output['averageMalesIncome_4'][-20:])
        incomeMales_5 = np.mean(output['averageMalesIncome_5'][-20:])
        incomeFemales_1 = np.mean(output['averageFemalesIncome_1'][-20:])
        incomeFemales_2 = np.mean(output['averageFemalesIncome_2'][-20:])
        incomeFemales_3 = np.mean(output['averageFemalesIncome_3'][-20:])
        incomeFemales_4 = np.mean(output['averageFemalesIncome_4'][-20:])
        incomeFemales_5 = np.mean(output['averageFemalesIncome_5'][-20:])
        means_males = (incomeMales_1, incomeMales_2, incomeMales_3, incomeMales_4, incomeMales_5)
        means_females = (incomeFemales_1, incomeFemales_2, incomeFemales_3, incomeFemales_4, incomeFemales_5)
        fig, ax = plt.subplots()
        index = np.arange(n_groups)
        bar_width = 0.35
        opacity = 0.8
        rects3 = ax.bar(index, means_females, bar_width,
                         alpha=opacity,
                         color='b',
                         label='Female')
        rects4 = ax.bar(index + bar_width, means_males, bar_width,
                         alpha=opacity,
                         color='g',
                         label='Male')
        ax.set_ylabel('Income')
        ax.set_xlabel('Socio-Economic Classes')
        ax.set_title('Female and Male Average Income')
        ax.set_xticks(ind + bar_width/2)
        plt.xticks(index + bar_width/2, ('I', 'II', 'III', 'IV', 'V'))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1])
        plt.tight_layout()
        path = os.path.join(folder, 'IncomeByGenderAndClassGroupedBarChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        ################################################################## 
        # Chart 46: Population by social class and number of taxpayers (1960-2020)
       
        fig, ax = plt.subplots()
        ax.plot(output['year'], output['taxPayers'], linewidth = 3, label = 'Number of Taxpayers', color = 'yellow')
        ax.stackplot(output['year'], output['numUnskilled'], output['numSkilled'], output['numLowClass'],
                      output['numMidClass'], output['numUpClass'], 
                      labels = ['Unskilled Class (I)','Skilled Class (II)', 'Lower Class (III)', 'Middel Class (IV)', 'Upper Class (V)'])
        ax.set_xlim(left = self.p['statsCollectFrom'])
        # ax.set_ylabel('Hours of care')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Population and Number of Taxpayers')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'PopulationTaxPayersStackedChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 47: Average Household size (1960-2020)
        fig, ax = plt.subplots()
        p1, = ax.plot(output['year'], output['averageHouseholdSize_1'], label = 'Class I')
        p2, = ax.plot(output['year'], output['averageHouseholdSize_2'], label = 'Class II')
        p3, = ax.plot(output['year'], output['averageHouseholdSize_3'], label = 'Class III')
        p4, = ax.plot(output['year'], output['averageHouseholdSize_4'], label = 'Class IV')
        p5, = ax.plot(output['year'], output['averageHouseholdSize_5'], label = 'Class V')
        maxValue = max(output['averageHouseholdSize_1']+output['averageHouseholdSize_2']+output['averageHouseholdSize_3']+output['averageHouseholdSize_4']+output['averageHouseholdSize_5'])
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylim([0, maxValue*2.0])
        # ax.set_ylabel('Average Household Members')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Average Family Size')
        ax.set_ylim([0, 8])
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'AverageFamilySizeChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()         
                 
##        pylab.plot(years,self.numMarriages)
##        pylab.ylabel('Number of marriages')
##        pylab.xlabel('Year')
##        pylab.savefig('numMarriages.pdf')
##
##        pylab.plot(years,self.numDivorces)
##        pylab.ylabel('Number of divorces')
##        pylab.xlabel('Year')
##        pylab.savefig('numDivorces.pdf')
        
        # Chart 48: Average Tax Burden (1960-2020)
       
        fig, ax = plt.subplots()
        ax.plot(output['year'], output['taxBurden'], linewidth = 3, color = 'red')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Care costs per taxpayer per year')
        # ax.set_xlabel('Year')
        ax.set_title('Average Tax Burden in pounds')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'TaxBurdenChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()  
      
        # total Tax Refund
        
        fig, ax = plt.subplots()
        ax.plot(output['year'], output['totalTaxRefund'], linewidth = 3, color = 'red')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Tax Refund')
        # ax.set_xlabel('Year')
        ax.set_title('Total Tax Refund in pounds')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'totalTaxRefundChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()  
        
         # pension budget
        
        fig, ax = plt.subplots()
        ax.plot(output['year'], output['pensionExpenditure'], linewidth = 3, color = 'red')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Tax Refund')
        # ax.set_xlabel('Year')
        ax.set_title('Budget balance in pounds')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'pensionExpenditureChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()  
        
        # Chart 49: Proportion of married adult women (1960-2020)
        fig, ax = plt.subplots()
        ax.plot(output['year'], output['marriageProp'], linewidth = 3, color = 'red')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        # ax.set_ylabel('Proportion of married adult women')
        ax.set_title('Proportion of married adult women')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'MarriageRateChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 49: Proportion of lone parents (1960-2020)
        fig, ax = plt.subplots()
        ax.plot(output['year'], output['shareLoneParents'], linewidth = 3, color = 'red')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        # ax.set_ylabel('Proportion of married adult women')
        ax.set_title('Share of lone parents')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'LoneParentsShareChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 49-bis: Proportion of Distant parents (1960-2020)
        fig, ax = plt.subplots()
        ax.plot(output['year'], output['shareDistantParents'], linewidth = 3, color = 'red')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        # ax.set_ylabel('Proportion of married adult women')
        ax.set_title('Share of distant parents')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'DistantParentsShareChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 50: Health Care Cost (1960-2020)
        fig, ax = plt.subplots()
        ax.plot(output['year'], output['hospitalizationCost'], linewidth = 3, color = 'red')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Cost in Pounds')
        # ax.set_xlabel('Year')
        ax.set_title('Total Health Care Cost')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'TotalHealthCareCostChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 51: Per Capita Health Care Cost (1960-2020)
        fig, ax = plt.subplots()
        ax.plot(output['year'], output['perCapitaHospitalizationCost'], linewidth = 3, color = 'red')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Cost in Pounds')
        # ax.set_xlabel('Year')
        ax.set_title('Per Capita Health Care Cost')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'PerCapitaHealthCareCostChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 52: Gini Coefficient of Unmet Social Care (from 1960 to 2020)
      
        fig, ax = plt.subplots()
        p1, = ax.plot(output['year'], output['unmetSocialCareNeedGiniCoefficient'], linewidth = 3, label = 'Population')
        p2, = ax.plot(output['year'], output['unmetSocialCareNeedGiniCoefficient_1'], label = 'Class I')
        p3, = ax.plot(output['year'], output['unmetSocialCareNeedGiniCoefficient_2'], label = 'Class II')
        p4, = ax.plot(output['year'], output['unmetSocialCareNeedGiniCoefficient_3'], label = 'Class III')
        p5, = ax.plot(output['year'], output['unmetSocialCareNeedGiniCoefficient_4'], label = 'Class IV')
        p6, = ax.plot(output['year'], output['unmetSocialCareNeedGiniCoefficient_5'], label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Gini Coefficient')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Unmet Social Care Gini Coeffcient')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.ylim(0.5, 1.0)
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'UnmetSocialCareGiniCoefficientChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 53: Gini Coefficient of Share of Unmet Social Care (from 1960 to 2020)
        fig, ax = plt.subplots()
        p1, = ax.plot(output['year'], output['shareUnmetSocialCareNeedGiniCoefficient'], linewidth = 3, label = 'Population')
        p2, = ax.plot(output['year'], output['shareUnmetSocialCareNeedGiniCoefficient_1'], label = 'Class I')
        p3, = ax.plot(output['year'], output['shareUnmetSocialCareNeedGiniCoefficient_2'], label = 'Class II')
        p4, = ax.plot(output['year'], output['shareUnmetSocialCareNeedGiniCoefficient_3'], label = 'Class III')
        p5, = ax.plot(output['year'], output['shareUnmetSocialCareNeedGiniCoefficient_4'], label = 'Class IV')
        p6, = ax.plot(output['year'], output['shareUnmetSocialCareNeedGiniCoefficient_5'], label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Gini Coefficient')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.set_title('Share of Unmet Social Care Gini Coeffcient')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.ylim(0.5, 1.0)
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'ShareUnmetSocialCareGiniCoefficientChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 54: Public supply
        fig, ax = plt.subplots()
        ax.plot(output['year'], output['publicSupply'], linewidth = 3)
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours of per week')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.legend_.remove()
        ax.set_title('Public Social Care Supply')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'PublicSocialCareSupplyChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
      
        fig, ax = plt.subplots()
        ax.plot(output['year'], output['costDirectFunding'], linewidth = 3)
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Pounds per week')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.legend_.remove()
        ax.set_title('Cost of Public Social Care')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'CostDirectFundingChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # care credit charts 
        fig, ax = plt.subplots()
        p1, = ax.plot(output['year'], output['socialCareCredits'], linewidth = 3, label = 'Total Social Credit')
        p2, = ax.plot(output['year'], output['careCreditSupply'], linewidth = 3, label = 'Public Social Care Supply')
        p3, = ax.plot(output['year'], output['socialCreditSpent'], linewidth = 3, label = 'Social Credit Transferred')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Hours of per week')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        # ax.legend_.remove()
        ax.set_title('Credit Public Care Supply')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'CreditPublicSocialCareSupplyChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        fig, ax = plt.subplots()
        ax.plot(output['year'], output['shareCreditsSpent'], linewidth = 3)
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Share of total credit')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.legend_.remove()
        ax.set_title('Share of Social Credit Transferred')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'ShareSocialCreditTransferChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        fig, ax = plt.subplots()
        ax.plot(output['year'], output['careCreditCost'], linewidth = 3)
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Pounds per week')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.legend_.remove()
        ax.set_title('Cost of Credit Public Social Care')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'CostCreditSocialCareChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
        # Chart 55: Aggregate QALY
        fig, ax = plt.subplots()
        ax.plot(output['year'], output['totQALY'], linewidth = 3)
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('QALY Index')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.legend_.remove()
        ax.set_title('Aggregate QALY Index')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'AggregateQALYChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
         # Chart 56: Average QALY
        fig, ax = plt.subplots()
        ax.plot(output['year'], output['meanQALY'], linewidth = 3)
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('QALY Index')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'lower left')
        ax.legend_.remove()
        ax.set_title('Average QALY Index')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'AverageQALYChart.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()
        
#        self.qualityAdjustedLifeYears_M.append(np.mean(self.discountedQALY[-20:]))
#        self.qualityAdjustedLifeYears_SD.append(np.std(self.discountedQALY[-20:]))
#        
#        self.perCapitaQualityAdjustedLifeYears_M.append(np.mean(self.averageDiscountedQALY[-20:]))
#        self.perCapitaQualityAdjustedLifeYears_SD.append(np.std(self.averageDiscountedQALY[-20:]))

        # Chart 57: Ratio of Unmet Care Need and Total Supply (from 1960 to 2020)
        fig, ax = plt.subplots()
        p1, = ax.plot(output['year'], output['ratioUnmetNeed_CareSupply'], linewidth = 3, label = 'Population')
        p2, = ax.plot(output['year'], output['ratioUnmetNeed_CareSupply_1'], label = 'Class I')
        p3, = ax.plot(output['year'], output['ratioUnmetNeed_CareSupply_2'], label = 'Class II')
        p4, = ax.plot(output['year'], output['ratioUnmetNeed_CareSupply_3'], label = 'Class III')
        p5, = ax.plot(output['year'], output['ratioUnmetNeed_CareSupply_4'], label = 'Class IV')
        p6, = ax.plot(output['year'], output['ratioUnmetNeed_CareSupply_5'], label = 'Class V')
        ax.set_xlim(left = self.p['statsCollectFrom'])
        ax.set_ylabel('Share of total supply')
        # ax.set_xlabel('Year')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(loc = 'upper left')
        ax.set_title('Ratio of Unmet Care Need and Total Supply')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.xlim(self.p['statsCollectFrom'], self.p['endYear'])
        plt.xticks(range(self.p['statsCollectFrom'], self.p['endYear']+1, 10))
        fig.tight_layout()
        path = os.path.join(folder, 'RatioUnmetCareNeedTotalSupply.pdf')
        pp = PdfPages(path)
        pp.savefig(fig)
        pp.close()

class PopPyramid:
    """Builds a data object for storing population pyramid data in."""
    def __init__ (self, ageClasses, careLevels):
        self.maleData = pylab.zeros((ageClasses,careLevels),dtype=int)
        self.femaleData = pylab.zeros((ageClasses, careLevels),dtype=int)

    def update(self, year, ageClasses, careLevels, pixelFactor, people):
        ## zero the two arrays
        for a in range (ageClasses):
            for c in range (careLevels):
                self.maleData[a,c] = 0
                self.femaleData[a,c] = 0
        ## tally up who belongs in which category
        for i in people:
            ageClass = ( year - i.birthdate ) / 5
            if ageClass > ageClasses - 1:
                ageClass = ageClasses - 1
            careClass = i.careNeedLevel
            if i.sex == 'male':
                self.maleData[ageClass,careClass] += 1
            else:
                self.femaleData[ageClass,careClass] += 1

        ## normalize the totals into pixels
        total = len(people)        
        for a in range (ageClasses):
            for c in range (careLevels):
                self.maleData[a,c] = pixelFactor * self.maleData[a,c] / total
                self.femaleData[a,c] = pixelFactor * self.femaleData[a,c] / total