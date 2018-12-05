 
#from simulation import Sim
from simulation import Sim
import cProfile
import pylab
import math
import matplotlib.pyplot as plt
import random
import numpy as np
import multiprocessing
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_pdf import PdfPages
import time
import os
import pandas as pd
from itertools import izip_longest
import itertools
import csv
from collections import OrderedDict


def init_params():
    """Set up the simulation parameters."""
    p = {}
    
    p['numRepeats'] = 1
    
    p['loadFromFile'] = False
    p['verboseDebugging'] = False
    p['doGraphs'] = False
    p['saveChecks'] = True
    p['getCheckVariablesAtYear'] = 2015
    
    p['numberPolicyParameters'] = 2
    p['valuesPerParam'] = 1
    p['numberScenarios'] = 3
    
    p['multiprocessing'] = False
    p['numberProcessors'] = 3
    
    p['favouriteSeed'] = 123
    p['startYear'] = 1860
    p['endYear'] = 2040
    p['thePresent'] = 2012
    p['statsCollectFrom'] = 1990
    p['regressionCollectFrom'] = 1960 
    p['implementPoliciesFromYear'] = 2020

    # Multiple runs parameters (to delete)

    #############################################
    
    ### Initialization Variables
    p['initialPop'] = 600   
    p['minStartAge'] = 24
    p['maxStartAge'] = 45
    p['numberClasses'] = 5
    p['initialClassShares'] = [0.2, 0.25, 0.3, 0.2, 0.05]
    
    ### Income
    p['weeklyHours'] = 40.0
    p['pensionWage'] = [5.0, 7.0, 10.0, 13.0, 18.0] # [0.64, 0.89, 1.27, 1.66, 2.29] #  
    p['incomeInitialLevels'] = [5.0, 7.0, 9.0, 11.0, 14.0] #[0.64, 0.89, 1.15, 1.40, 1.78] #  
    p['incomeFinalLevels'] = [10.0, 15.0, 22.0, 33.0, 50.0] #[1.27, 1.91, 2.80, 4.21, 6.37] # 
    
    p['savings_SES_I'] = [0.0, 0.0, 1000, 2000, 3000, 2500, 2000, 1500]
    p['savings_SES_II'] = [0.0, 1500, 2500, 5000, 8000, 6000, 5000, 4000]
    p['savings_SES_III'] = [0.0, 2500, 6000, 8000, 14000, 12000, 10000, 8000]
    p['savings_SES_IV'] = [0.0, 6000, 15000, 20000, 35000, 30000, 25000, 20000]
    p['savings_SES_V'] = [0.0, 12000, 35000, 50000, 90000, 75000, 60000, 50000]
    
    
    p['incomeGrowthRate'] = [0.4, 0.35, 0.35, 0.3, 0.25]
    p['workDiscountingTime'] = 0.8
    p['wageGrowthRate'] = 1.0 # 1.01338 # 
    p['stateSupport'] = 200
    
    ### Budget and public cost
    p['pensionContributionRate'] = 0.05
    p['pricePublicSocialCare'] = 20.0 # [2.55] # 20
    
    ###  Marriages
    p['deltaAgeProb'] =  [0.0, 0.1, 0.25, 0.4, 0.2, 0.05]
    p['studentFactorParam'] = 0.5
    p['betaGeoExp'] = 2.0 #[1.0 - 4.0]
    p['betaSocExp'] = 2.0
    p['rankGenderBias'] = 0.5
    p['basicMaleMarriageProb'] =  0.85
    p['maleMarriageModifierByDecade'] = [0.0, 0.16, 0.5, 1.0, 0.8, 0.7, 0.66, 0.5, 0.4, 0.2, 0.1, 0.05, 0.01, 0.0]
    # p['incomeMarriageParam'] = 0.025
    
    ### Births
    p['minPregnancyAge'] = 17
    p['maxPregnancyAge'] = 42
    p['growingPopBirthProb'] = 0.215
    p['fertilityBias'] = 0.9
    # p['fertilityCorrector'] = 1.0
    
    ### Allocate Care
    # # # # # # # # # # 
    # main function
    p['unmetCareNeedDiscountParam'] = 0.5
    p['shareUnmetNeedDiscountParam'] = 0.5
    p['socialCareBankingAge'] = 65
    
    # - network size parameters
    p['networkDistanceParam'] = 2.0
    
    # care credits allocation function
    p['absoluteCreditQuantity'] = False
    p['quantityYearlyIncrease'] = 0.0
    p['socialCareCreditQuantity'] = 0
    p['kinshipNetworkCarePropension'] = 0.5
    p['volunteersCarePropensionCoefficient'] = 0.01
    
    # - careDemand function
    p['numCareLevels'] = 5
    p['careLevelNames'] = ['none','low','moderate','substantial','critical']
    p['careDemandInHours'] = [0.0, 8.0, 16.0, 32.0, 80.0]
    p['childCareDemand'] = 68
    p['maxFormalChildcareHours'] = 48
    p['zeroYearCare'] = 80.0
    
    p['childCareTaxFreeRate'] = 0.2
    p['childcareTaxFreeCap'] = 40
    p['maxHouseholdIncomeChildCareSupport'] = 300
    p['freeChildCareHoursToddlers'] = 12
    p['freeChildCareHoursPreSchool'] = 20
    p['freeChildCareHoursSchool'] = 32
    
    # - Childcare
    # p['childcareDecreaseRate'] = 0.25
    # p['priceChildCare'] = 0.76 # 6 
    # p['schoolAge'] = 5
    # p['maxFormalChildcareHours'] = 48
    # p['schoolHours'] = 30
    # p['freeChildcareHours'] = 15
    # p['workingParentsFreeChildcareHours'] = 30
    # p['minAgeStartChildCareSupport'] = 3
    # p['minAgeStartChildCareSupportByIncome'] =  2
    # p['maxHouseholdIncomeChildCareSupport'] = 40 # 320
    
    # - careSupplies function
    p['incomeCareParam'] = 0.0005 #[0.00025 - 0.001]
    p['taxBreakRate'] = 0.0
       ### Policy Lever
    p['socialSupportLevel'] = 4   ### Policy lever
    p['maxSavingsMeansTest'] = 23000
    p['minAgeForSupport'] = 0
    
    p['quantumCare'] = 4.0
    p['retiredHours'] = [48.0, 24.0, 12.0, 8.0]
    p['employedHours'] = [24.0, 16.0, 8.0, 4.0]
    p['studentHours'] = [24.0, 16.0, 8.0, 4.0]
    p['teenAgersHours'] = [12.0, 0.0, 0.0, 0.0]
    p['formalCareDiscountFactor'] = 0.5
    p['priceSocialCare'] = 17.0 
    p['priceChildCare'] = 6.0
    p['taxBrackets'] = [663, 228, 0] 
    p['taxBandsNumber'] = 3
    p['bandsTaxationRates'] = [0.4, 0.2, 0.0] 
    
    # - social care banking
    p['socialCareCreditShare'] = 0.0 ### Policy Lever
    
    ### Health Care Cost
    p['hospitalizationParam'] = 0.5
    p['needLevelParam'] = 2.0
    p['unmetSocialCareParam'] = 2.0
    p['costHospitalizationPerDay'] = 400
    
    ### Transitions
    # # # # # # # # # # # 
    # - age transition function 
    p['ageOfRetirement'] = 65
    p['ageTeenagers'] = 12
    p['minWorkingAge'] = 16
    p['qalyBeta'] = 0.18
    p['qalyAlpha'] = 1.5
    
    # - social transition
    p['educationCosts'] = [0.0, 100.0, 150.0, 200.0] #[0.0, 12.74, 19.12, 25.49] # 
    p['leaveHomeStudentProb'] = 0.5
    p['eduWageSensitivity'] = 0.2 # 0.5
    p['eduRankSensitivity'] = 3.0 # 5.0
    p['costantIncomeParam'] = 80.0 # 20.0
    p['costantEduParam'] = 10.0 #  10.0
    p['careEducationParam'] = 0.005 
    p['workingAge'] = [16, 18, 20, 22, 24]
    
    # - care transition function
    p['personCareProb'] = 0.0008
    p['maleAgeCareScaling'] = 18.0 # p['maleAgeCareProb'] = 0.0008
    p['femaleAgeCareScaling'] = 19.0 # p['femaleAgeCareProb'] = 0.0008
    p['baseCareProb'] = 0.0002
    p['careBias'] = 0.9
    p['careTransitionRate'] = 0.7
    p['unmetNeedExponent'] = 1.0 # 0.005 #[0.005 - 0.02]
    p['hillHealthLevelThreshold'] = 3
    p['seriouslyHillSupportRate'] = 0.5
    
    ### Divorce
    p['basicDivorceRate'] = 0.06
    p['variableDivorce'] = 0.06
    p['divorceModifierByDecade'] = [ 0.0, 1.0, 0.9, 0.5, 0.4, 0.2, 0.1, 0.03, 0.01, 0.001, 0.001, 0.001, 0.0, 0.0, 0.0, 0.0, 0.0 ]
    p['divorceBias'] = 1.0
    
    ### Death
    p['mortalityBias'] = 0.85 # After 1950
    p['careNeedBias'] = 0.9
    p['unmetCareNeedBias'] = 0.5
    p['baseDieProb'] = 0.0001
    p['babyDieProb'] = 0.005
    p['maleAgeScaling'] = 14.0
    p['maleAgeDieProb'] = 0.00021
    p['femaleAgeScaling'] = 15.5
    p['femaleAgeDieProb'] = 0.00019
    
    ### Relocations
    # # # # # # # # # # # #
    # - job relocations
    p['relocationDecisionParam'] = 1.0
    p['shareHouseholdRelocation'] = 0.03
    p['networkBetaParam'] = 4.0
    p['socialBetaParam'] = 1.0
    p['townWeightExp'] = 2.0
    p['townAttractionParam'] = 0.5
    p['apprenticesRelocationProb'] = 0.5
    
    # - spouse relocations
    p['relocationCostBetaParam'] = 1.0
    p['yearsInTownSensitivityParam'] = 0.5
    p['relocationCostParam'] = 0.5 # [1 -4]
        
    # - pensioners relocation
    p['retiredRelocationParam'] = 0.00005 # 0.01
    
    ### Stats and chart parameters
    p['maxWtWChildAge'] = 5
    p['discountingFactor'] = 0.03
    p['qalyDiscountRate'] = 0.035
    
    #################################################################
    
     ## Description of the map, towns, and houses
    p['mapGridXDimension'] = 8
    p['mapGridYDimension'] = 12    
    p['townGridDimension'] = 70
    p['cdfHouseClasses'] = [ 0.6, 0.9, 5.0 ]
    p['ukMap'] = [[ 0.0, 0.1, 0.2, 0.1, 0.0, 0.0, 0.0, 0.0 ],
                  [ 0.1, 0.1, 0.2, 0.2, 0.3, 0.0, 0.0, 0.0 ],
                  [ 0.0, 0.2, 0.2, 0.3, 0.0, 0.0, 0.0, 0.0 ],
                  [ 0.0, 0.2, 1.0, 0.5, 0.0, 0.0, 0.0, 0.0 ],
                  [ 0.4, 0.0, 0.2, 0.2, 0.4, 0.0, 0.0, 0.0 ],
                  [ 0.6, 0.0, 0.0, 0.3, 0.8, 0.2, 0.0, 0.0 ],
                  [ 0.0, 0.0, 0.0, 0.6, 0.8, 0.4, 0.0, 0.0 ],
                  [ 0.0, 0.0, 0.2, 1.0, 0.8, 0.6, 0.1, 0.0 ],
                  [ 0.0, 0.0, 0.1, 0.2, 1.0, 0.6, 0.3, 0.4 ],
                  [ 0.0, 0.0, 0.5, 0.7, 0.5, 1.0, 1.0, 0.0 ],
                  [ 0.0, 0.0, 0.2, 0.4, 0.6, 1.0, 1.0, 0.0 ],
                  [ 0.0, 0.2, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0 ]]
    p['ukClassBias'] = [[ 0.0, -0.05, -0.05, -0.05, 0.0, 0.0, 0.0, 0.0 ],
                        [ -0.05, -0.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ],
                        [ 0.0, -0.05, -0.05, 0.0, 0.0, 0.0, 0.0, 0.0 ],
                        [ 0.0, -0.05, -0.05, 0.05, 0.0, 0.0, 0.0, 0.0 ],
                        [ -0.05, 0.0, -0.05, -0.05, 0.0, 0.0, 0.0, 0.0 ],
                        [ -0.05, 0.0, 0.0, -0.05, -0.05, -0.05, 0.0, 0.0 ],
                        [ 0.0, 0.0, 0.0, -0.05, -0.05, -0.05, 0.0, 0.0 ],
                        [ 0.0, 0.0, -0.05, -0.05, 0.0, 0.0, 0.0, 0.0 ],
                        [ 0.0, 0.0, -0.05, 0.0, -0.05, 0.0, 0.0, 0.0 ],
                        [ 0.0, 0.0, 0.0, -0.05, 0.0, 0.2, 0.15, 0.0 ],
                        [ 0.0, 0.0, 0.0, 0.0, 0.1, 0.2, 0.15, 0.0 ],
                        [ 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0 ] ]
    p['mapDensityModifier'] = 0.6
    
    ## Graphical interface details
    p['interactiveGraphics'] = False #True
    p['delayTime'] = 0.0
    p['screenWidth'] = 1300
    p['screenHeight'] = 700
    p['bgColour'] = 'black'
    p['mainFont'] = 'Helvetica 18'
    p['fontColour'] = 'white'
    p['dateX'] = 70
    p['dateY'] = 20
    p['popX'] = 70
    p['popY'] = 50
    p['pixelsInPopPyramid'] = 2000
    p['num5YearAgeClasses'] = 28
    p['careLevelColour'] = ['blue','green','yellow','orange','red']
    p['houseSizeColour'] = ['brown','purple','yellow']
    p['pixelsPerTown'] = 56
    p['maxTextUpdateList'] = 22
    
    return p

def importParameters():
    
    filename = 'generalParameters.csv' 
    genParams = pd.read_csv(filename, sep=',',header=0)
    col = genParams.columns

    filename = 'initialParameters.csv' 
    params = pd.read_csv(filename, sep=',',header=0)
    
    for i in col:
        params[i] = genParams[i]
            
    params.to_csv(filename, index=False)
    
    numberRows = params.shape[0]
    keys = list(params.columns.values)
    values = []
    for column in params:
        colValues = []
        for i in range(numberRows):
            if pd.isnull(params.loc[i, column]):
                break
            colValues.append(params[column][i])
        values.append(colValues)
    p = dict(zip(keys, values))
    for key, value in p.iteritems():
        if len(value) < 2:
            p[key] = value[0]
    return p

def scenariosParams():
    
    
    
    # Copy some params from generalParameters to params

    filename = 'initialParameters.csv'
    params = pd.read_csv(filename, sep=',',header=0)
    
    filename = 'sensitivityParameters.csv' 
    sensitivityParams = pd.read_csv(filename, sep=',',header=0)
    names = sensitivityParams.columns
    numberRows = sensitivityParams.shape[0]
    
    runsParameters = []
    
    params['runNumber'] = np.nan
    params['paramIndex'] = np.nan
    numberRuns = params['numRepeats'][0]
    numberScenarios = 0
    
    for r in range(int(params['numRepeats'][0])):
        
        if sensitivityParams['combinationKey'][0] == 0:
            numberScenarios = 1
            params['runNumber'][0] = r
            params['paramIndex'][0] = 0
            runsParameters.append(params)
        
        else:
            if sensitivityParams['combinationKey'][0] == 1:
                numberScenarios = sensitivityParams.shape[0]
                index = 0
                for n in range(numberRows):
                    newRun = params.copy()
                    for i in names[1:]:
                        if pd.isnull(sensitivityParams[i][n]):
                            newRun[i][0] = params[i][0]
                        else:
                            newRun[i][0] = sensitivityParams[i][n]
                    newRun['runNumber'][0] = r
                    newRun['paramIndex'][0] = index
                    index += 1
                    runsParameters.append(newRun)
                    
            elif sensitivityParams['combinationKey'][0] == 2:
                numberScenarios = sensitivityParams.count().sum()
                index = 0
                for n in range(numberRows):
                    for i in names[1:]:
                        newRun = params.copy()
                        if not pd.isnull(sensitivityParams[i][n]):
                            newRun[i][0] = sensitivityParams[i][n]
                        else:
                            continue
                        newRun['runNumber'][0] = r
                        newRun['paramIndex'][0] = index
                        index += 1
                        runsParameters.append(newRun)
                        
            else:
                runList = []
                runNames = []
                for i in names[1:]:
                    if pd.isnull(sensitivityParams[i][0]):
                        continue
                    runNames.append(i)
                    runList.append([x for x in sensitivityParams[i] if pd.isnull(x) == False])
                combinations = list(itertools.product(*runList))
                numberScenarios = len(combinations)
                index = 0
                for c in combinations:
                    newRun = params.copy()
                    for n in c:
                        newRun[runNames[c.index(n)]][0] = n
                    newRun['runNumber'][0] = r
                    newRun['paramIndex'][0] = index
                    index += 1
                    runsParameters.append(newRun)
            
    filename = 'policyParameters.csv' 
    policies = pd.read_csv(filename, sep=',',header=0)
    names = policies.columns
    numberRows = policies.shape[0]
    for n in runsParameters:
        n['policyIndex'] = np.nan
        n['policyIndex'][0] = policies['combinationKey'][0]
    
    policyScenarios = [[] for i in range(len(runsParameters))]
    
    numberPolicies = 0
    
    for j in range(len(runsParameters)):
        index = 0
        numberPolicies = 1
        policyCombination = pd.DataFrame()
        policyCombination['policyIndex'] = [index]
        for i in names[1:]:
            policyCombination[i] = runsParameters[j][i]
        policyScenarios[j].append(policyCombination)
        index += 1
        
        if policies['combinationKey'][0] != 0:
            if policies['combinationKey'][0] == 1:
                numberPolicies = policies.shape[0] + 1
                for n in range(numberRows):
                    newPolicy = policyCombination.copy()
                    for i in names[1:]:
                        if pd.isnull(policies[i][n]):
                            newPolicy[i][0] = policyCombination[i][0]
                        else:
                            newPolicy[i][0] = policies[i][n]
                    newPolicy['policyIndex'] = index
                    index += 1
                    policyScenarios[j].append(newPolicy)
                
            elif policies['combinationKey'][0] == 2:
                numberPolicies = policies.count().sum()
                for n in range(numberRows):
                    for i in names[1:]:
                        newPolicy = policyCombination.copy()
                        if not pd.isnull(policies[i][n]):
                            newPolicy[i][0] = policies[i][n]
                        else:
                            continue
                        newPolicy['policyIndex'] = index
                        index += 1
                        policyScenarios[j].append(newPolicy)
            
            else:
                policyList = []
                policyNames = []
                for i in names[1:]:
                    if pd.isnull(policies[i][0]):
                        continue
                    policyNames.append(i)
                    policyList.append([x for x in policies[i] if pd.isnull(x) == False])
                combinations = list(itertools.product(*policyList))
                numberPolicies = len(combinations)
                for c in combinations:
                    newScenario = policyCombination.copy()
                    for n in c:
                        newScenario[policyNames[c.index(n)]][0] = n
                    newScenario['policyIndex'] = index
                    index += 1
                    policyScenarios[j].append(newScenario)
    
    # Add number combinations to generalPArameters and save new csv
    filename = 'generalParameters.csv' 
    genParams = pd.read_csv(filename, sep=',',header=0)
    genParams['numberScenarios'] = [numberScenarios]
    genParams['numberRuns'] = [numberRuns]
    genParams['numberPolicies'] = [numberPolicies]
    genParams.to_csv(filename, index=False)
    
    rearrangedScenarios = []
    for i in range(len(runsParameters)):
        for j in policyScenarios[i]:
            rearrangedScenarios.append([runsParameters[i], j])
    
    runsParameters = []
    
    for i in range(len(rearrangedScenarios)):
        scenariosParameters = []
        for scenario in rearrangedScenarios[i]:
            numberRows = scenario.shape[0]
            keys = list(scenario.columns.values)
            values = []
            for column in scenario:
                colValues = []
                for i in range(numberRows):
                    if pd.isnull(scenario.loc[i, column]):
                        break
                    colValues.append(scenario[column][i])
                values.append(colValues)
            p = OrderedDict(zip(keys, values))
            for key, value in p.iteritems():
                if len(value) < 2:
                    p[key] = value[0]
            scenariosParameters.append(p)
        runsParameters.append(scenariosParameters)

    return runsParameters

def simulation(params):
    p = params[0] # init_params()
    bs = Sim(p)
    bs.run(params[1])


if __name__ == "__main__":

    import_parameters = False # True
    
    if import_parameters == True:
        p = importParameters()
    else:
        p = init_params()
    
    if p['multiprocessing'] == True:
        random.seed(p['favouriteSeed'])
        np.random.seed(p['favouriteSeed'])
        
        processors = p['numberProcessors']
        if processors > multiprocessing.cpu_count():
            processors = multiprocessing.cpu_count()
        
        pool = multiprocessing.Pool(processors)
        
        params = scenariosParams()

        pool.map(simulation, params)
        pool.close()
        pool.join()
            
    else:
        random.seed(int(p['favouriteSeed']))
        np.random.seed(int(p['favouriteSeed']))
        
        params = scenariosParams()
        
        for n in params:
            b = Sim(n[0])
            b.run(n[1])
