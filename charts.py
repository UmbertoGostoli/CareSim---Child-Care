# -*- coding: utf-8 -*-
"""
Created on Thu Sep 06 12:05:05 2018

@author: Umberto Gostoli
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_pdf import PdfPages
import os
import pandas as pd



def init_params(params):
    """Set up the simulation parameters."""
    p = {}

    p['endYear'] = int(params['endYear'].values[0])
    p['statsCollectFrom'] = int(params['statsCollectFrom'].values[0])
    p['numberPolicies'] = int(params['numberPolicies'].values[0])
    p['numberScenarios'] = int(params['numberScenarios'].values[0])
    p['numRepeats'] = int(params['numRepeats'].values[0])
    p['implementPoliciesFromYear'] = int(params['implementPoliciesFromYear'].values[0])
    p['timeDiscountingFactor'] = params['timeDiscountingFactor'].values[0]
    p['numberClasses'] = int(params['numberClasses'].values[0])
    p['numCareLevels'] = int(params['numCareLevels'].values[0])
    p['outputYear'] = int(params['outputYear'].values[0])
    
    return p


def doGraphs():
    """Plot the graphs needed at the end of one run."""
    
    filename = 'generalParameters.csv' 
    genParams = pd.read_csv(filename, sep=',',header=0)
    p = init_params(genParams)
    
    multipleScenarios = []
    for s in range(int(p['numberScenarios'])):
        scenarioFolder = 'Results/Scenario_' + str(s)
        multiplePolicies = []
        for n in range(int(p['numberPolicies'])):
            policyFolder = scenarioFolder + '/Policy_' + str(n)
            multipleOutputs = []
            for r in range(int(p['numRepeats'])):
                runFolder = policyFolder + '/Run_' + str(r)
                filename = runFolder + '/Dataset/outputSim.csv'
                outputSim = pd.read_csv(filename, sep=',',header=0)
                singleRunCharts(outputSim, p, runFolder)
                multipleOutputs.append(outputSim)
            multipleRunsCharts(multipleOutputs, p, policyFolder)
            multiplePolicies.append(multipleOutputs)
            if n == 0:
                multipleScenarios.append(multiplePolicies)
        multiplePoliciesCharts(multiplePolicies, p, scenarioFolder)
    sensitivityCharts(multipleScenarios, p)

def sensitivityCharts(outputs, p):
    
    folder = 'sensitivityCharts'
    if not os.path.exists(folder):
        os.makedirs(folder)
    # Compare outputs for n scenarios (at policy 0).
    # Choose the outputs to compare
    
    
def multipleRunsCharts(outputs, p, policyFolder):
    
    folder = policyFolder + '/Charts'
    if not os.path.exists(folder):
        os.makedirs(folder)
        
    # Add barcharts with multiple outputs and standard deviations

    fig, ax = plt.subplots()
    chart = [None]*p['numRepeats']
    for i in range(p['numRepeats']):
        if p['numRepeats'] > 1:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['shareUnmetCareDemand'], label = 'Run ' + str(i+1))
        else:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['shareUnmetCareDemand'])

    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Share of Care Need')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    if p['numRepeats'] < 2:
        ax.legend().set_visible(False)
    ax.set_title('Share of Unmet Care Need')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'ShareUnmetCareNeedChart_MR.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 2: Average unmet care need
    fig, ax = plt.subplots()
    chart = [None]*p['numRepeats']
    for i in range(p['numRepeats']):
        if p['numRepeats'] > 1:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['unmetCarePerRecipient'], label = 'Run ' + str(i+1))
        else:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['unmetCarePerRecipient'])

    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours of Unmet Care Need')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    if p['numRepeats'] < 2:
        ax.legend().set_visible(False)
    ax.set_title('Average Unmet Care Need')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'AverageUnmetCareNeedChart_MR.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    ### Add charts with not discounted aggregate and average QALY
    # Chart 3: Aggregate Quality-adjusted Life outputs[i]['year']
    fig, ax = plt.subplots()
    chart = [None]*p['numRepeats']
    for i in range(p['numRepeats']):
        if p['numRepeats'] > 1:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['totQALY'], label = 'Run ' + str(i+1))
        else:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['totQALY'])

    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Aggregate QALY')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    if p['numRepeats'] < 2:
        ax.legend().set_visible(False)
    ax.set_title('Aggregate Quality-adjusted Life Year')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'AggregateQALYChart_MR.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 4: Average Quality-adjusted Life outputs[i]['year']
    fig, ax = plt.subplots()
    chart = [None]*p['numRepeats']
    for i in range(p['numRepeats']):
        if p['numRepeats'] > 1:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['meanQALY'], label = 'Run ' + str(i+1))
        else:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['meanQALY'])

    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Average QALY')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    if p['numRepeats'] < 2:
        ax.legend().set_visible(False)
    ax.set_title('Average Quality-adjusted Life Year')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'AverageQALYChart_MR.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 5: Aggregate Discounted Quality-adjusted Life outputs[i]['year']
    fig, ax = plt.subplots()
    chart = [None]*p['numRepeats']
    for i in range(p['numRepeats']):
        if p['numRepeats'] > 1:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['discountedQALY'], label = 'Run ' + str(i+1))
        else:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['discountedQALY'])

    ax.set_xlim(left = p['implementPoliciesFromYear'])
    ax.set_ylabel('Discounted QALY')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    if p['numRepeats'] < 2:
        ax.legend().set_visible(False)
    ax.set_title('Discounted Quality-adjusted Life Year')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['implementPoliciesFromYear'], p['endYear'])
    plt.xticks(range(p['implementPoliciesFromYear'], p['endYear']+1, 5))
    fig.tight_layout()
    path = os.path.join(folder, 'DiscountedAggregateQALYChart_MR.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 6: Average Discounted Quality-adjusted Life outputs[i]['year']
    fig, ax = plt.subplots()
    chart = [None]*p['numRepeats']
    for i in range(p['numRepeats']):
        if p['numRepeats'] > 1:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['averageDiscountedQALY'], label = 'Run ' + str(i+1))
        else:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['averageDiscountedQALY'])

    ax.set_xlim(left = p['implementPoliciesFromYear'])
    ax.set_ylabel('Discounted Average QALY')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    if p['numRepeats'] < 2:
        ax.legend().set_visible(False)
    ax.set_title('Discounted Average Quality-adjusted Life Year')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['implementPoliciesFromYear'], p['endYear'])
    plt.xticks(range(p['implementPoliciesFromYear'], p['endYear']+1, 5))
    fig.tight_layout()
    path = os.path.join(folder, 'DiscountedAverageQALYChart_MR.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 7: per-capita Hospitalization Costs 
    fig, ax = plt.subplots()
    chart = [None]*p['numRepeats']
    for i in range(p['numRepeats']):
        if p['numRepeats'] > 1:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['perCapitaHospitalizationCost'], label = 'Run ' + str(i+1))
        else:
            chart[i], = ax.plot(outputs[i]['year'], outputs[i]['perCapitaHospitalizationCost'])

    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Per-capita Yearly Cost')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    if p['numRepeats'] < 2:
        ax.legend().set_visible(False)
    ax.set_title('Per-Capita Hospitalization Costs')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'PerCapitaHospitalizationCostsChart_MR.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    ## Bar Chart with multiple outputs across many runs
    
    # Shares
    fig, ax = plt.subplots()
    objects = ('shareInformalSocialCare', 'shareUnmetSocialCareDemand', 'ratioUnmetNeed_CareSupply',
               'shareCareGivers', 'shareInformalCareSuppliedByFemales', 'ratioIncome')
    y_pos = np.arange(len(objects))
    shareInformalSocialCare = []
    shareUnmetSocialCareDemand = []
    ratioUnmetNeed_CareSupply = []
    shareCareGivers = []
    shareInformalCareSuppliedByFemales = []
    ratioIncome = []
    for i in range(p['numRepeats']):
        shareInformalSocialCare.append(outputs[i].loc[outputs[i]['year'] == p['outputYear'], 'shareInformalSocialCare'].values[0])
        shareUnmetSocialCareDemand.append(outputs[i].loc[outputs[i]['year'] == p['outputYear'], 'shareUnmetSocialCareDemand'].values[0])
        ratioUnmetNeed_CareSupply.append(outputs[i].loc[outputs[i]['year'] == p['outputYear'], 'ratioUnmetNeed_CareSupply'].values[0])
        shareCareGivers.append(outputs[i].loc[outputs[i]['year'] == p['outputYear'], 'shareCareGivers'].values[0])
        shareInformalCareSuppliedByFemales.append(outputs[i].loc[outputs[i]['year'] == p['outputYear'], 'shareInformalCareSuppliedByFemales'].values[0])
        ratioIncome.append(outputs[i].loc[outputs[i]['year'] == p['outputYear'], 'ratioIncome'].values[0])
    outcomes = [shareInformalSocialCare, shareUnmetSocialCareDemand, ratioUnmetNeed_CareSupply,
                shareCareGivers, shareInformalCareSuppliedByFemales, ratioIncome]
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('Shares')
    ax.set_title('Values and variance across runs')
    fig.tight_layout()
    path = os.path.join(folder, 'sharesValuesVariancesBarPlot.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Hours (total)
    fig, ax = plt.subplots()
    objects = ('totalCareSupply', 'socialCareNeed', 'informalSocialCareReceived',
               'formalSocialCareReceived', 'unmetSocialCareNeed')
    y_pos = np.arange(len(objects))
    totalCareSupply = []
    socialCareNeed = []
    informalSocialCareReceived = []
    formalSocialCareReceived = []
    unmetSocialCareNeed = []
    for i in range(p['numRepeats']):
        totalCareSupply.append(outputs[i].loc[outputs[i]['year'] == p['outputYear'], 'totalCareSupply'].values[0])
        socialCareNeed.append(outputs[i].loc[outputs[i]['year'] == p['outputYear'], 'socialCareNeed'].values[0])
        informalSocialCareReceived.append(outputs[i].loc[outputs[i]['year'] == p['outputYear'], 'informalSocialCareReceived'].values[0])
        formalSocialCareReceived.append(outputs[i].loc[outputs[i]['year'] == p['outputYear'], 'formalSocialCareReceived'].values[0])
        unmetSocialCareNeed.append(outputs[i].loc[outputs[i]['year'] == p['outputYear'], 'unmetSocialCareNeed'].values[0])
    outcomes = [totalCareSupply, socialCareNeed, informalSocialCareReceived,
                formalSocialCareReceived, unmetSocialCareNeed]
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('Total Hours')
    ax.set_title('Values and variance across runs')
    fig.tight_layout()
    path = os.path.join(folder, 'totalHoursValuesVariancesBarPlot.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Hours (per capita)
    fig, ax = plt.subplots()
    objects = ('perCapitaSocialCareReceived', 'perCapitaUnmetSocialCareDemand', 'informalSocialCarePerRecipient',
               'formalSocialCarePerRecipient', 'unmetSocialCarePerRecipient')
    y_pos = np.arange(len(objects))
    perCapitaSocialCareReceived = []
    perCapitaUnmetSocialCareDemand = []
    informalSocialCarePerRecipient = []
    formalSocialCarePerRecipient = []
    unmetSocialCarePerRecipient = []
    for i in range(p['numRepeats']):
        perCapitaSocialCareReceived.append(outputs[i].loc[outputs[i]['year'] == p['outputYear'], 'perCapitaSocialCareReceived'].values[0])
        perCapitaUnmetSocialCareDemand.append(outputs[i].loc[outputs[i]['year'] == p['outputYear'], 'perCapitaUnmetSocialCareDemand'].values[0])
        informalSocialCarePerRecipient.append(outputs[i].loc[outputs[i]['year'] == p['outputYear'], 'informalSocialCarePerRecipient'].values[0])
        formalSocialCarePerRecipient.append(outputs[i].loc[outputs[i]['year'] == p['outputYear'], 'formalSocialCarePerRecipient'].values[0])
        unmetSocialCarePerRecipient.append(outputs[i].loc[outputs[i]['year'] == p['outputYear'], 'unmetSocialCarePerRecipient'].values[0])
    outcomes = [perCapitaSocialCareReceived, perCapitaUnmetSocialCareDemand, informalSocialCarePerRecipient,
                formalSocialCarePerRecipient, unmetSocialCarePerRecipient]
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('Average Hours')
    ax.set_title('Values and variance across runs')
    fig.tight_layout()
    path = os.path.join(folder, 'averageHoursValuesVariancesBarPlot.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
def multiplePoliciesCharts(outputs, p, scenarioFolder):
    
    folder = scenarioFolder + '/Charts'
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Bar charts of share of unmet care demand 
    fig, ax = plt.subplots()
    
    policyYears = (p['endYear']-p['implementPoliciesFromYear']) + 1
    
    objects = ('Benchmark',)
    outcomes = []
    for j in range(p['numberPolicies']):
        policyOutcome = []
        for i in range(p['numRepeats']): 
            policyOutcome.append(outputs[j][i].loc[outputs[j][i]['year'] == p['outputYear'], 'shareUnmetCareDemand'].values[0])
        outcomes.append(policyOutcome)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    y_pos = np.arange(len(objects))
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('Share of Total Demand')
    ax.set_title('Share of Unmet Care Demand')
    fig.tight_layout()
    path = os.path.join(folder, 'SharesUnmetCareDemandBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Bar charts of total unmet care need
    fig, ax = plt.subplots()
    objects = ('Benchmark',)
    outcomes = []
    for j in range(p['numberPolicies']):
        policyOutcome = []
        for i in range(p['numRepeats']):
            policyOutcome.append(np.sum(outputs[j][i]['totalUnnmetCareNeed'][-policyYears:]))
        outcomes.append(policyOutcome)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    y_pos = np.arange(len(objects))
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('Hours of Unmet Care')
    ax.set_title('Total Unmet Social Care Need')
    fig.tight_layout()
    path = os.path.join(folder, 'TotalsUnmetCareNeedBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Bar charts of unmet Care Per Recipient
    fig, ax = plt.subplots()
    objects = ('Benchmark',)
    outcomes = []
    for j in range(p['numberPolicies']):
        policyOutcome = []
        for i in range(p['numRepeats']):
            policyOutcome.append(np.mean(outputs[j][i]['perCapitaUnmetCareDemand'][-policyYears:]))
        outcomes.append(policyOutcome)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    y_pos = np.arange(len(objects))
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('Hours of Unmet Care')
    ax.set_title('Per capita Unmet Social Care')
    fig.tight_layout()
    path = os.path.join(folder, 'perCapitaUnmetCareBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # QALY barcharts
    # Bar charts of total qualy (not discounted)
    fig, ax = plt.subplots()
    objects = ('Benchmark',)
    outcomes = []
    for j in range(p['numberPolicies']):
        policyOutcome = []
        for i in range(p['numRepeats']):
            policyOutcome.append(np.sum(outputs[j][i]['totQALY'][-policyYears:]))
        outcomes.append(policyOutcome)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    y_pos = np.arange(len(objects))
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('QALY')
    ax.set_title('Total QALY')
    fig.tight_layout()
    path = os.path.join(folder, 'totalQALYsBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Bar charts of average qualy (not discounted)
    fig, ax = plt.subplots()
    objects = ('Benchmark',)
    outcomes = []
    for j in range(p['numberPolicies']):
        policyOutcome = []
        for i in range(p['numRepeats']):
            policyOutcome.append(np.mean(outputs[j][i]['meanQALY'][-policyYears:]))
        outcomes.append(policyOutcome)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    y_pos = np.arange(len(objects))
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('QALY')
    ax.set_title('Average QALY')
    fig.tight_layout()
    path = os.path.join(folder, 'averageQALYsBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Bar charts of total qualy (discounted)
    fig, ax = plt.subplots()
    objects = ('Benchmark',)
    outcomes = []
    for j in range(p['numberPolicies']):
        policyOutcome = []
        for i in range(p['numRepeats']):
            policyOutcome.append(discountedSum(outputs[j][i]['totQALY'][-policyYears:], p))
        outcomes.append(policyOutcome)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    y_pos = np.arange(len(objects))
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('QALY')
    ax.set_title('Total Discounted QALY')
    fig.tight_layout()
    path = os.path.join(folder, 'totalDiscountedQALYsBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Hospitalisation Costs Barcharts
    # Bar charts of total hospitalization Cost (not discounted)
    fig, ax = plt.subplots()
    objects = ('Benchmark',)
    outcomes = []
    for j in range(p['numberPolicies']):
        policyOutcome = []
        for i in range(p['numRepeats']):
            policyOutcome.append(np.sum(outputs[j][i]['hospitalizationCost'][-policyYears:])*52)
        outcomes.append(policyOutcome)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    y_pos = np.arange(len(objects))
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('Hospitalization Cost')
    ax.set_title('Total Hospitalization Cost')
    fig.tight_layout()
    path = os.path.join(folder, 'totalHospitalizationCostsBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Bar charts of average hospitalization Cost (not discounted)
    fig, ax = plt.subplots()
    objects = ('Benchmark',)
    outcomes = []
    for j in range(p['numberPolicies']):
        policyOutcome = []
        for i in range(p['numRepeats']):
            policyOutcome.append(np.mean(outputs[j][i]['perCapitaHospitalizationCost'][-policyYears:]))
        outcomes.append(policyOutcome)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    y_pos = np.arange(len(objects))
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('Hospitalization Cost')
    ax.set_title('Total Hospitalization Cost')
    fig.tight_layout()
    path = os.path.join(folder, 'averageHospitalizationCostsBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Bar charts of total hospitalization Cost (discounted)
    fig, ax = plt.subplots()
    objects = ('Benchmark',)
    outcomes = []
    for j in range(p['numberPolicies']):
        policyOutcome = []
        for i in range(p['numRepeats']):
            policyOutcome.append(discountedSum(outputs[j][i]['hospitalizationCost'][-policyYears:], p))
        outcomes.append(policyOutcome)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    y_pos = np.arange(len(objects))
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('Hospitalization Cost')
    ax.set_title('Total Discounted Hospitalization Cost')
    fig.tight_layout()
    path = os.path.join(folder, 'totalDiscountedHospitalizationCostsBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Bar charts of direct policy costs (total)
    
    fig, ax = plt.subplots()
    objects = ('Benchmark',)
    outcomes = []
    for j in range(p['numberPolicies']):
        policyOutcome = []
        for i in range(p['numRepeats']):
            policyOutcome.append(np.sum(outputs[j][i]['totalPolicyCost'][-policyYears:])*52)
        outcomes.append(policyOutcome)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    y_pos = np.arange(len(objects))
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('Pounds')
    ax.set_title('Total public expenditure')
    fig.tight_layout()
    path = os.path.join(folder, 'totalPolicyCostsBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Bar charts of direct policy costs (discounted)
    
    fig, ax = plt.subplots()
    objects = ('Benchmark',)
    outcomes = []
    for j in range(p['numberPolicies']):
        policyOutcome = []
        for i in range(p['numRepeats']):
            policyOutcome.append(discountedSum(52*np.array(outputs[j][i]['totalPolicyCost'][-policyYears:]), p))
        outcomes.append(policyOutcome)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    y_pos = np.arange(len(objects))
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('Pounds')
    ax.set_title('Present Cost of Public expenditure')
    fig.tight_layout()
    path = os.path.join(folder, 'discountedPolicyCostBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Bar charts of policy costs per capita
    fig, ax = plt.subplots()
    objects = ('Benchmark',)
    outcomes = []
    for j in range(p['numberPolicies']):
        policyOutcome = []
        for i in range(p['numRepeats']):
            policyOutcome.append(np.mean(outputs[j][i]['perCapitaPolicyCost'][-policyYears:]))
        outcomes.append(policyOutcome)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    y_pos = np.arange(len(objects))
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('Pounds per week')
    ax.set_title('Per Capita Public Expenditure')
    fig.tight_layout()
    path = os.path.join(folder, 'perCapitaPolicyCostsBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Total cost Stacked Bar Chart
    objects = ('Benchmark',)
    n_groups = p['numberPolicies']
    means = []
    outcomes_1 = []
    outcomes_2 = []
    outcomes_3 = []
    for j in range(p['numberPolicies']):
        policyOutcome_1 = []
        policyOutcome_2 = []
        policyOutcome_3 = []
        for i in range(p['numRepeats']):
            policyOutcome_1.append(np.sum(outputs[j][i]['totalTaxRefund'][-policyYears:])*52)
            policyOutcome_2.append(np.sum(outputs[j][i]['costDirectFunding'][-policyYears:])*52)
            policyOutcome_3.append(np.sum(outputs[j][i]['careCreditCost'][-policyYears:])*52)
        outcomes_1.append(policyOutcome_1)
        outcomes_2.append(policyOutcome_1)
        outcomes_3.append(policyOutcome_1)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means.append([np.mean(x) for x in outcomes_1])
    means.append([np.mean(x) for x in outcomes_2])
    means.append([np.mean(x) for x in outcomes_3])
    totCare = [sum(x) for x in zip(means[0], means[1], means[2])]
    ind = np.arange(n_groups)    # the x locations for the groups
    width = 0.4       # the width of the bars: can also be len(x) sequence
    fig, ax = plt.subplots()
    chart = [None]*3
    labels = ['Tax deduction', 'Direct funding', 'Care credit']
    bottom = [0]*p['numberPolicies']
    for i in range(3):
        chart[i], = ax.bar(ind, means[i], width, bottom = bottom, label = labels[i])
        bottom = [sum(x) for x in zip(bottom, means[i])]
    ax.set_ylim([0, max(totCare)*1.1])
    ax.set_ylabel('Pounds')
    ax.set_xticks(ind)
    plt.xticks(ind, objects)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper right')
    ax.set_title('Public expenditure by policy lever')
    fig.tight_layout()
    path = os.path.join(folder, 'expenditureByPolicyLeverSBC.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()        
   
    # Per capita policy costs Stacked Bar Chart
    objects = ('Benchmark',)
    n_groups = p['numberPolicies']
    means = []
    outcomes_1 = []
    outcomes_2 = []
    outcomes_3 = []
    for j in range(p['numberPolicies']):
        policyOutcome_1 = []
        policyOutcome_2 = []
        policyOutcome_3 = []
        for i in range(p['numRepeats']):
            policyOutcome_1.append(np.sum(outputs[j][i]['perCapitaTaxRefund'][-policyYears:])*52)
            policyOutcome_2.append(np.sum(outputs[j][i]['perCapitaCostDirectFunding'][-policyYears:])*52)
            policyOutcome_3.append(np.sum(outputs[j][i]['perCapitaCareCreditCost'][-policyYears:])*52)
        outcomes_1.append(policyOutcome_1)
        outcomes_2.append(policyOutcome_1)
        outcomes_3.append(policyOutcome_1)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means.append([np.mean(x) for x in outcomes_1])
    means.append([np.mean(x) for x in outcomes_2])
    means.append([np.mean(x) for x in outcomes_3])
    totCare = [sum(x) for x in zip(means[0], means[1], means[2])]
    ind = np.arange(n_groups)    # the x locations for the groups
    width = 0.4       # the width of the bars: can also be len(x) sequence
    fig, ax = plt.subplots()
    chart = [None]*3
    labels = ['Tax deduction', 'Direct funding', 'Care credit']
    bottom = [0]*p['numberPolicies']
    for i in range(3):
        chart[i], = ax.bar(ind, means[i], width, bottom = bottom, label = labels[i])
        bottom = [sum(x) for x in zip(bottom, means[i])]
    ax.set_ylim([0, max(totCare)*1.1])
    ax.set_ylabel('Pounds')
    ax.set_xticks(ind)
    plt.xticks(ind, objects)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper right')
    ax.set_title('Per capita expenditure by policy lever')
    fig.tight_layout()
    path = os.path.join(folder, 'perCapitaExpenditureByPolicyLeverSBC.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()        
    
    # Repeat previous 5 charts with costs including hospitalization costs
    
    # Bar charts of direct policy costs (total)
    
    fig, ax = plt.subplots()
    objects = ('Benchmark',)
    outcomes = []
    for j in range(p['numberPolicies']):
        policyOutcome = []
        for i in range(p['numRepeats']):
            policyOutcome.append(np.sum(outputs[j][i]['policyCostWithHC'][-policyYears:]))
        outcomes.append(policyOutcome)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    y_pos = np.arange(len(objects))
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('Pounds')
    ax.set_title('Public expenditure with hospitalization costs')
    fig.tight_layout()
    path = os.path.join(folder, 'totalCostsWithHospitalBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Bar charts of direct policy costs (discounted)
    
    fig, ax = plt.subplots()
    objects = ('Benchmark',)
    outcomes = []
    for j in range(p['numberPolicies']):
        policyOutcome = []
        for i in range(p['numRepeats']):
            policyOutcome.append(discountedSum(outputs[j][i]['policyCostWithHC'][-policyYears:], p))
        outcomes.append(policyOutcome)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    y_pos = np.arange(len(objects))
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('Pounds')
    ax.set_title('Present Cost with hospitalisation costs')
    fig.tight_layout()
    path = os.path.join(folder, 'discountedCostWithHospitalBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Bar charts of policy costs per capita
    fig, ax = plt.subplots()
    objects = ('Benchmark',)
    outcomes = []
    for j in range(p['numberPolicies']):
        policyOutcome = []
        for i in range(p['numRepeats']):
            policyOutcome.append(np.mean(outputs[j][i]['perCapitaPolicyCostWithHC'][-policyYears:]))
        outcomes.append(policyOutcome)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    y_pos = np.arange(len(objects))
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('Pounds per week')
    ax.set_title('Per capita costs with hospitalisation costs')
    fig.tight_layout()
    path = os.path.join(folder, 'perCapitaCostsWithHospitalBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Total cost Stacked Bar Chart
    objects = ('Benchmark',)
    n_groups = p['numberPolicies']
    means = []
    outcomes_1 = []
    outcomes_2 = []
    outcomes_3 = []
    outcomes_4 = []
    for j in range(p['numberPolicies']):
        policyOutcome_1 = []
        policyOutcome_2 = []
        policyOutcome_3 = []
        policyOutcome_4 = []
        for i in range(p['numRepeats']):
            policyOutcome_1.append(np.sum(outputs[j][i]['totalTaxRefund'][-policyYears:])*52)
            policyOutcome_2.append(np.sum(outputs[j][i]['costDirectFunding'][-policyYears:])*52)
            policyOutcome_3.append(np.sum(outputs[j][i]['careCreditCost'][-policyYears:])*52)
            policyOutcome_4.append(np.sum(outputs[j][i]['policyCostWithHC'][-policyYears:]))
        outcomes_1.append(policyOutcome_1)
        outcomes_2.append(policyOutcome_2)
        outcomes_3.append(policyOutcome_3)
        outcomes_4.append(policyOutcome_4)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means.append([np.mean(x) for x in outcomes_1])
    means.append([np.mean(x) for x in outcomes_2])
    means.append([np.mean(x) for x in outcomes_3])
    means.append([np.mean(x) for x in outcomes_4])
    totCare = [sum(x) for x in zip(means[0], means[1], means[2], means[3])]
    ind = np.arange(n_groups)    # the x locations for the groups
    width = 0.4       # the width of the bars: can also be len(x) sequence
    fig, ax = plt.subplots()
    chart = [None]*4
    labels = ['Tax deduction', 'Direct funding', 'Care credit', 'Hospitalization Costs']
    bottom = [0]*p['numberPolicies']
    for i in range(4):
        chart[i], = ax.bar(ind, means[i], width, bottom = bottom, label = labels[i])
        bottom = [sum(x) for x in zip(bottom, means[i])]
    ax.set_ylim([0, max(totCare)*1.1])
    ax.set_ylabel('Pounds')
    ax.set_xticks(ind)
    plt.xticks(ind, objects)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper right')
    ax.set_title('Public expenditures with Hospitalisation Costs')
    fig.tight_layout()
    path = os.path.join(folder, 'totalCostsWithHospitalSBC.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()        
   
    # Per capita policy costs Stacked Bar Chart
    objects = ('Benchmark',)
    n_groups = p['numberPolicies']
    means = []
    outcomes_1 = []
    outcomes_2 = []
    outcomes_3 = []
    outcomes_4 = []
    for j in range(p['numberPolicies']):
        policyOutcome_1 = []
        policyOutcome_2 = []
        policyOutcome_3 = []
        policyOutcome_4 = []
        for i in range(p['numRepeats']):
            policyOutcome_1.append(np.sum(outputs[j][i]['perCapitaTaxRefund'][-policyYears:])*52)
            policyOutcome_2.append(np.sum(outputs[j][i]['perCapitaCostDirectFunding'][-policyYears:])*52)
            policyOutcome_3.append(np.sum(outputs[j][i]['perCapitaCareCreditCost'][-policyYears:])*52)
            policyOutcome_4.append(np.sum(outputs[j][i]['perCapitaPolicyCostWithHC'][-policyYears:]))
        outcomes_1.append(policyOutcome_1)
        outcomes_2.append(policyOutcome_2)
        outcomes_3.append(policyOutcome_3)
        outcomes_4.append(policyOutcome_4)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means.append([np.mean(x) for x in outcomes_1])
    means.append([np.mean(x) for x in outcomes_2])
    means.append([np.mean(x) for x in outcomes_3])
    means.append([np.mean(x) for x in outcomes_4])
    totCare = [sum(x) for x in zip(means[0], means[1], means[2], means[3])]
    ind = np.arange(n_groups)    # the x locations for the groups
    width = 0.4       # the width of the bars: can also be len(x) sequence
    fig, ax = plt.subplots()
    chart = [None]*4
    labels = ['Tax deduction', 'Direct funding', 'Care credit', 'Hospitalization Costs']
    bottom = [0]*p['numberPolicies']
    for i in range(4):
        chart[i], = ax.bar(ind, means[i], width, bottom = bottom, label = labels[i])
        bottom = [sum(x) for x in zip(bottom, means[i])]
    ax.set_ylim([0, max(totCare)*1.1])
    ax.set_ylabel('Pounds')
    ax.set_xticks(ind)
    plt.xticks(ind, objects)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper right')
    ax.set_title('Per capita expenditures with Hospitalisation Costs')
    fig.tight_layout()
    path = os.path.join(folder, 'perCapitaCostsWithHospitalSBC.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Charts of total costs (including budget differences)
    
    fig, ax = plt.subplots()
    objects = ('Benchmark',)
    outcomes = []
    for j in range(p['numberPolicies']):
        policyOutcome = []
        for i in range(p['numRepeats']):
            policyOutcome.append(np.sum(outputs[j][i]['totalCost'][-policyYears:]))
        outcomes.append(policyOutcome)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    y_pos = np.arange(len(objects))
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('Pounds')
    ax.set_title('Total Financial Cost')
    fig.tight_layout()
    path = os.path.join(folder, 'totalFinancialCostBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Bar charts of direct policy costs (discounted)
    
    fig, ax = plt.subplots()
    objects = ('Benchmark',)
    outcomes = []
    for j in range(p['numberPolicies']):
        policyOutcome = []
        for i in range(p['numRepeats']):
            policyOutcome.append(discountedSum(outputs[j][i]['totalCost'][-policyYears:], p))
        outcomes.append(policyOutcome)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    y_pos = np.arange(len(objects))
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('Pounds')
    ax.set_title('Present Cost of Financial Cost')
    fig.tight_layout()
    path = os.path.join(folder, 'discountedFinancialCostBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Bar charts of policy costs per capita
    fig, ax = plt.subplots()
    objects = ('Benchmark',)
    outcomes = []
    for j in range(p['numberPolicies']):
        policyOutcome = []
        for i in range(p['numRepeats']):
            policyOutcome.append(np.mean(outputs[j][i]['perCapitaCost'][-policyYears:]))
        outcomes.append(policyOutcome)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    y_pos = np.arange(len(objects))
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('Pounds per week')
    ax.set_title('Per capita financial cost')
    fig.tight_layout()
    path = os.path.join(folder, 'perCapitaFinancialCostBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    ################### Cost effectiveness charts #################
    
    #########  Policy-only Incremental Cost Effectiveness Ratios
    #### A - Denominator: Unmet care need 
    
    # 1 - Total not discounted
    fig, ax = plt.subplots()
    objects = ()
    outcomes = []
    for j in range(1, p['numberPolicies']):
        policyOutcome = []
        for i in range(p['numRepeats']):
            costPolicy = np.sum(outputs[j][i]['totalPolicyCost'][-policyYears:])
            effectPolicy = np.sum(outputs[j][i]['totalUnnmetCareNeed'][-policyYears:])
            for k in range(p['numRepeats']):
                costBenchmark = np.sum(outputs[0][k]['totalPolicyCost'][-policyYears:])
                effectBenchmark = np.sum(outputs[0][k]['totalUnnmetCareNeed'][-policyYears:])
                icer = (costPolicy-costBenchmark)/(effectBenchmark-effectPolicy)
                policyOutcome.append(icer)
        outcomes.append(policyOutcome)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    y_pos = np.arange(len(objects))
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('ICER')
    ax.set_title('ICER based on unmet care need')
    fig.tight_layout()
    path = os.path.join(folder, 'totalUnmetCareNeedICER_BarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # 2 - Total discounted
    fig, ax = plt.subplots()
    objects = ()
    outcomes = []
    for j in range(1, p['numberPolicies']):
        policyOutcome = []
        for i in range(p['numRepeats']):
            costPolicy = discountedSum(outputs[j][i]['totalPolicyCost'][-policyYears:], p)
            effectPolicy = discountedSum(outputs[j][i]['totalUnnmetCareNeed'][-policyYears:], p)
            for k in range(p['numRepeats']):
                costBenchmark = discountedSum(outputs[0][k]['totalPolicyCost'][-policyYears:], p)
                effectBenchmark = discountedSum(outputs[0][k]['totalUnnmetCareNeed'][-policyYears:], p)
                icer = (costPolicy-costBenchmark)/(effectBenchmark-effectPolicy)
                policyOutcome.append(icer)
        outcomes.append(policyOutcome)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    y_pos = np.arange(len(objects))
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('ICER')
    ax.set_title('ICER based on discounted unmet care need')
    fig.tight_layout()
    path = os.path.join(folder, 'discountedUnmetCareNeedICER_BarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # 3 - Per capita
    fig, ax = plt.subplots()
    objects = ()
    outcomes = []
    for j in range(1, p['numberPolicies']):
        policyOutcome = []
        for i in range(p['numRepeats']):
            costPolicy = np.sum(outputs[j][i]['perCapitaPolicyCost'][-policyYears:])
            effectPolicy = np.sum(outputs[j][i]['perCapitaUnmetCareDemand'][-policyYears:])
            for k in range(p['numRepeats']):
                costBenchmark = np.sum(outputs[0][k]['perCapitaPolicyCost'][-policyYears:])
                effectBenchmark = np.sum(outputs[0][k]['perCapitaUnmetCareDemand'][-policyYears:])
                icer = (costPolicy-costBenchmark)/(effectBenchmark-effectPolicy)
                policyOutcome.append(icer)
        outcomes.append(policyOutcome)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    y_pos = np.arange(len(objects))
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('ICER')
    ax.set_title('ICER based on per capita unmet care need')
    fig.tight_layout()
    path = os.path.join(folder, 'perCapitaUnmetCareNeedICER_BarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    
    #### B - Denominator: QALY
    
    # 1 - Total not discounted
    fig, ax = plt.subplots()
    objects = ()
    outcomes = []
    for j in range(1, p['numberPolicies']):
        policyOutcome = []
        for i in range(p['numRepeats']):
            costPolicy = np.sum(outputs[j][i]['totalPolicyCost'][-policyYears:])
            effectPolicy = np.sum(outputs[j][i]['totQALY'][-policyYears:])
            for k in range(p['numRepeats']):
                costBenchmark = np.sum(outputs[0][k]['totalPolicyCost'][-policyYears:])
                effectBenchmark = np.sum(outputs[0][k]['totQALY'][-policyYears:])
                icer = (costPolicy-costBenchmark)/(effectPolicy-effectBenchmark)
                policyOutcome.append(icer)
        outcomes.append(policyOutcome)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    y_pos = np.arange(len(objects))
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('ICER')
    ax.set_title('ICER based on aggregate QALY')
    fig.tight_layout()
    path = os.path.join(folder, 'aggregateQalyICER_BarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # 2 - Total discounted
    fig, ax = plt.subplots()
    objects = ()
    outcomes = []
    for j in range(1, p['numberPolicies']):
        policyOutcome = []
        for i in range(p['numRepeats']):
            costPolicy = discountedSum(outputs[j][i]['totalPolicyCost'][-policyYears:], p)
            effectPolicy = discountedSum(outputs[j][i]['totQALY'][-policyYears:], p)
            for k in range(p['numRepeats']):
                costBenchmark = discountedSum(outputs[0][k]['totalPolicyCost'][-policyYears:], p)
                effectBenchmark = discountedSum(outputs[0][k]['totQALY'][-policyYears:], p)
                icer = (costPolicy-costBenchmark)/(effectPolicy-effectBenchmark)
                policyOutcome.append(icer)
        outcomes.append(policyOutcome)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    y_pos = np.arange(len(objects))
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('ICER')
    ax.set_title('ICER based on discounted QALY')
    fig.tight_layout()
    path = os.path.join(folder, 'discountedQalyICER_BarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # 3 - Per capita
    fig, ax = plt.subplots()
    objects = ()
    outcomes = []
    for j in range(1, p['numberPolicies']):
        policyOutcome = []
        for i in range(p['numRepeats']):
            costPolicy = np.sum(outputs[j][i]['perCapitaPolicyCost'][-policyYears:])
            effectPolicy = np.sum(outputs[j][i]['meanQALY'][-policyYears:])
            for k in range(p['numRepeats']):
                costBenchmark = np.sum(outputs[0][k]['perCapitaPolicyCost'][-policyYears:])
                effectBenchmark = np.sum(outputs[0][k]['meanQALY'][-policyYears:])
                icer = (costPolicy-costBenchmark)/(effectPolicy-effectBenchmark)
                policyOutcome.append(icer)
        outcomes.append(policyOutcome)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    y_pos = np.arange(len(objects))
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('ICER')
    ax.set_title('ICER based on average QALY')
    fig.tight_layout()
    path = os.path.join(folder, 'averageQalyICER_BarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    
    #########  Policy plus Hospistalisation Expenses Incremental Cost Effectiveness Ratios
    ##### Unmet Care Need
    # 1 - Total not discounted
    fig, ax = plt.subplots()
    objects = ()
    outcomes = []
    for j in range(1, p['numberPolicies']):
        policyOutcome = []
        for i in range(p['numRepeats']):
            costPolicy = np.sum(outputs[j][i]['policyCostWithHC'][-policyYears:])
            effectPolicy = np.sum(outputs[j][i]['totalUnnmetCareNeed'][-policyYears:])
            for k in range(p['numRepeats']):
                costBenchmark = np.sum(outputs[0][k]['policyCostWithHC'][-policyYears:])
                effectBenchmark = np.sum(outputs[0][k]['totalUnnmetCareNeed'][-policyYears:])
                icer = (costPolicy-costBenchmark)/(effectBenchmark-effectPolicy)
                policyOutcome.append(icer)
        outcomes.append(policyOutcome)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    y_pos = np.arange(len(objects))
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('ICER')
    ax.set_title('ICER based on unmet care need')
    fig.tight_layout()
    path = os.path.join(folder, 'totalUnmetCareNeedICER_HC_BarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # 2 - Total discounted
    fig, ax = plt.subplots()
    objects = ()
    outcomes = []
    for j in range(1, p['numberPolicies']):
        policyOutcome = []
        for i in range(p['numRepeats']):
            costPolicy = discountedSum(outputs[j][i]['policyCostWithHC'][-policyYears:], p)
            effectPolicy = discountedSum(outputs[j][i]['totalUnnmetCareNeed'][-policyYears:], p)
            for k in range(p['numRepeats']):
                costBenchmark = discountedSum(outputs[0][k]['policyCostWithHC'][-policyYears:], p)
                effectBenchmark = discountedSum(outputs[0][k]['totalUnnmetCareNeed'][-policyYears:], p)
                icer = (costPolicy-costBenchmark)/(effectBenchmark-effectPolicy)
                policyOutcome.append(icer)
        outcomes.append(policyOutcome)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    y_pos = np.arange(len(objects))
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('ICER')
    ax.set_title('ICER based on discounted unmet care need')
    fig.tight_layout()
    path = os.path.join(folder, 'discountedUnmetCareNeedICER_HC_BarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # 3 - Per capita
    fig, ax = plt.subplots()
    objects = ()
    outcomes = []
    for j in range(1, p['numberPolicies']):
        policyOutcome = []
        for i in range(p['numRepeats']):
            costPolicy = np.sum(outputs[j][i]['perCapitaPolicyCostWithHC'][-policyYears:])
            effectPolicy = np.sum(outputs[j][i]['perCapitaUnmetCareDemand'][-policyYears:])
            for k in range(p['numRepeats']):
                costBenchmark = np.sum(outputs[0][k]['perCapitaPolicyCostWithHC'][-policyYears:])
                effectBenchmark = np.sum(outputs[0][k]['perCapitaUnmetCareDemand'][-policyYears:])
                icer = (costPolicy-costBenchmark)/(effectBenchmark-effectPolicy)
                policyOutcome.append(icer)
        outcomes.append(policyOutcome)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    y_pos = np.arange(len(objects))
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('ICER')
    ax.set_title('ICER based on per capita unmet care need')
    fig.tight_layout()
    path = os.path.join(folder, 'perCapitaUnmetCareNeedICER_HC_BarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    ##### QALY
    # 1 - Total not discounted
    fig, ax = plt.subplots()
    objects = ()
    outcomes = []
    for j in range(1, p['numberPolicies']):
        policyOutcome = []
        for i in range(p['numRepeats']):
            costPolicy = np.sum(outputs[j][i]['policyCostWithHC'][-policyYears:])
            effectPolicy = np.sum(outputs[j][i]['totQALY'][-policyYears:])
            for k in range(p['numRepeats']):
                costBenchmark = np.sum(outputs[0][k]['policyCostWithHC'][-policyYears:])
                effectBenchmark = np.sum(outputs[0][k]['totQALY'][-policyYears:])
                icer = (costPolicy-costBenchmark)/(effectPolicy-effectBenchmark)
                policyOutcome.append(icer)
        outcomes.append(policyOutcome)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    y_pos = np.arange(len(objects))
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('ICER')
    ax.set_title('ICER based on QALY')
    fig.tight_layout()
    path = os.path.join(folder, 'totalQalyICER_HC_BarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # 2 - Total discounted
    fig, ax = plt.subplots()
    objects = ()
    outcomes = []
    for j in range(1, p['numberPolicies']):
        policyOutcome = []
        for i in range(p['numRepeats']):
            costPolicy = discountedSum(outputs[j][i]['policyCostWithHC'][-policyYears:], p)
            effectPolicy = discountedSum(outputs[j][i]['totQALY'][-policyYears:], p)
            for k in range(p['numRepeats']):
                costBenchmark = discountedSum(outputs[0][k]['policyCostWithHC'][-policyYears:], p)
                effectBenchmark = discountedSum(outputs[0][k]['totQALY'][-policyYears:], p)
                icer = (costPolicy-costBenchmark)/(effectPolicy-effectBenchmark)
                policyOutcome.append(icer)
        outcomes.append(policyOutcome)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    y_pos = np.arange(len(objects))
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('ICER')
    ax.set_title('ICER based on discounted QALY')
    fig.tight_layout()
    path = os.path.join(folder, 'discountedQalyICER_HC_BarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # 3 - Per capita
    fig, ax = plt.subplots()
    objects = ()
    outcomes = []
    for j in range(1, p['numberPolicies']):
        policyOutcome = []
        for i in range(p['numRepeats']):
            costPolicy = np.sum(outputs[j][i]['perCapitaPolicyCostWithHC'][-policyYears:])
            effectPolicy = np.sum(outputs[j][i]['meanQALY'][-policyYears:])
            for k in range(p['numRepeats']):
                costBenchmark = np.sum(outputs[0][k]['perCapitaPolicyCostWithHC'][-policyYears:])
                effectBenchmark = np.sum(outputs[0][k]['meanQALY'][-policyYears:])
                icer = (costPolicy-costBenchmark)/(effectPolicy-effectBenchmark)
                policyOutcome.append(icer)
        outcomes.append(policyOutcome)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    y_pos = np.arange(len(objects))
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('ICER')
    ax.set_title('ICER based on average QALY')
    fig.tight_layout()
    path = os.path.join(folder, 'averageQalyICER_HC_BarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    #########  Policy plus Hospistalisation Expenses plus Budget Balance Incremental Cost Effectiveness Ratios
    ##### Unmet Care Need
    # 1 - Total not discounted
    fig, ax = plt.subplots()
    objects = ()
    outcomes = []
    for j in range(1, p['numberPolicies']):
        policyOutcome = []
        for i in range(p['numRepeats']):
            costPolicy = np.sum(outputs[j][i]['totalCost'][-policyYears:])
            effectPolicy = np.sum(outputs[j][i]['totalUnnmetCareNeed'][-policyYears:])
            for k in range(p['numRepeats']):
                costBenchmark = np.sum(outputs[0][k]['totalCost'][-policyYears:])
                effectBenchmark = np.sum(outputs[0][k]['totalUnnmetCareNeed'][-policyYears:])
                icer = (costPolicy-costBenchmark)/(effectBenchmark-effectPolicy)
                policyOutcome.append(icer)
        outcomes.append(policyOutcome)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    y_pos = np.arange(len(objects))
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('ICER')
    ax.set_title('ICER based on unmet care need')
    fig.tight_layout()
    path = os.path.join(folder, 'totalUnmetCareNeedICER_BB_BarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # 2 - Total discounted
    fig, ax = plt.subplots()
    objects = ()
    outcomes = []
    for j in range(1, p['numberPolicies']):
        policyOutcome = []
        for i in range(p['numRepeats']):
            costPolicy = discountedSum(outputs[j][i]['totalCost'][-policyYears:], p)
            effectPolicy = discountedSum(outputs[j][i]['totalUnnmetCareNeed'][-policyYears:], p)
            for k in range(p['numRepeats']):
                costBenchmark = discountedSum(outputs[0][k]['totalCost'][-policyYears:], p)
                effectBenchmark = discountedSum(outputs[0][k]['totalUnnmetCareNeed'][-policyYears:], p)
                icer = (costPolicy-costBenchmark)/(effectBenchmark-effectPolicy)
                policyOutcome.append(icer)
        outcomes.append(policyOutcome)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    y_pos = np.arange(len(objects))
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('ICER')
    ax.set_title('ICER based on discounted unmet care need')
    fig.tight_layout()
    path = os.path.join(folder, 'discountedUnmetCareNeedICER_BB_BarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # 3 - Per capita
    fig, ax = plt.subplots()
    objects = ()
    outcomes = []
    for j in range(1, p['numberPolicies']):
        policyOutcome = []
        for i in range(p['numRepeats']):
            costPolicy = np.sum(outputs[j][i]['perCapitaCost'][-policyYears:])
            effectPolicy = np.sum(outputs[j][i]['perCapitaUnmetCareDemand'][-policyYears:])
            for k in range(p['numRepeats']):
                costBenchmark = np.sum(outputs[0][k]['perCapitaCost'][-policyYears:])
                effectBenchmark = np.sum(outputs[0][k]['perCapitaUnmetCareDemand'][-policyYears:])
                icer = (costPolicy-costBenchmark)/(effectBenchmark-effectPolicy)
                policyOutcome.append(icer)
        outcomes.append(policyOutcome)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    y_pos = np.arange(len(objects))
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('ICER')
    ax.set_title('ICER based on per capita unmet care need')
    fig.tight_layout()
    path = os.path.join(folder, 'perCapitaUnmetCareNeedICER_BB_BarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    ######  QALY
    # 1 - Total not discounted
    fig, ax = plt.subplots()
    objects = ()
    outcomes = []
    for j in range(1, p['numberPolicies']):
        policyOutcome = []
        for i in range(p['numRepeats']):
            costPolicy = np.sum(outputs[j][i]['totalCost'][-policyYears:])
            effectPolicy = np.sum(outputs[j][i]['totQALY'][-policyYears:])
            for k in range(p['numRepeats']):
                costBenchmark = np.sum(outputs[0][k]['totalCost'][-policyYears:])
                effectBenchmark = np.sum(outputs[0][k]['totQALY'][-policyYears:])
                icer = (costPolicy-costBenchmark)/(effectPolicy-effectBenchmark)
                policyOutcome.append(icer)
        outcomes.append(policyOutcome)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    y_pos = np.arange(len(objects))
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('ICER')
    ax.set_title('ICER based on QALY')
    fig.tight_layout()
    path = os.path.join(folder, 'totalQalyICER_BB_BarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # 2 - Total discounted
    fig, ax = plt.subplots()
    objects = ()
    outcomes = []
    for j in range(1, p['numberPolicies']):
        policyOutcome = []
        for i in range(p['numRepeats']):
            costPolicy = discountedSum(outputs[j][i]['totalCost'][-policyYears:], p)
            effectPolicy = discountedSum(outputs[j][i]['totQALY'][-policyYears:], p)
            for k in range(p['numRepeats']):
                costBenchmark = discountedSum(outputs[0][k]['totalCost'][-policyYears:], p)
                effectBenchmark = discountedSum(outputs[0][k]['totQALY'][-policyYears:], p)
                icer = (costPolicy-costBenchmark)/(effectPolicy-effectBenchmark)
                policyOutcome.append(icer)
        outcomes.append(policyOutcome)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    y_pos = np.arange(len(objects))
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('ICER')
    ax.set_title('ICER based on discounted QALY')
    fig.tight_layout()
    path = os.path.join(folder, 'discountedQalyICER_BB_BarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # 3 - Per capita
    fig, ax = plt.subplots()
    objects = ()
    outcomes = []
    for j in range(1, p['numberPolicies']):
        policyOutcome = []
        for i in range(p['numRepeats']):
            costPolicy = np.sum(outputs[j][i]['perCapitaCost'][-policyYears:])
            effectPolicy = np.sum(outputs[j][i]['meanQALY'][-policyYears:])
            for k in range(p['numRepeats']):
                costBenchmark = np.sum(outputs[0][k]['perCapitaCost'][-policyYears:])
                effectBenchmark = np.sum(outputs[0][k]['meanQALY'][-policyYears:])
                icer = (costPolicy-costBenchmark)/(effectPolicy-effectBenchmark)
                policyOutcome.append(icer)
        outcomes.append(policyOutcome)
        if j > 0:
            policyID = 'Policy ' + str(j)
            objects += (policyID,)
    means = [np.mean(x) for x in outcomes]
    sd = [np.std(x) for x in outcomes]
    y_pos = np.arange(len(objects))
    ax.bar(y_pos, means, yerr = sd, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    ax.xaxis.set_ticks_position('none')
    ax.set_ylabel('ICER')
    ax.set_title('ICER based on average QALY')
    fig.tight_layout()
    path = os.path.join(folder, 'averageQalyICER_BB_BarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
def discountedSum(timeSeries, p):
    discountedSum = 0
    ts = np.array(timeSeries)
    for i in range(len(ts)):
        discountedSum += ts[i]/pow((1.0 + p['timeDiscountingFactor']), float(i))
    return discountedSum

def singleRunCharts(output, p, runFolder):
    
    folder = runFolder + '/Charts'
    if not os.path.exists(folder):
        os.makedirs(folder)

    policyYears = (p['endYear']-p['implementPoliciesFromYear']) + 1

    # Chart 1: total social and child care demand and potential supply (from 1960 to 2020)
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['totalCareSupply'], linewidth=2, label = 'Potential Supply', color = 'green')
    ax.stackplot(output['year'], output['socialCareNeed'], output['childCareNeed'], labels = ['Social Care Need','Child Care Need'])
    # ax.plot(years, totalSocialCareDemand, linewidth=2, label = 'Social Care Need', color = 'red')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    # ax.set_xlabel('Year')
    ax.set_title('Care Needs and Potential Supply')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
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
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Share of population')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Share of Care Givers')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
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
    ax.set_xlim(left = p['statsCollectFrom'])
    # ax.set_ylabel('Share of Care Takers')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Share of Care Takers by Care Need Level')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.ylim(0, 1)
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
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
    ax.set_xlim(left = p['statsCollectFrom'])
    # ax.set_ylabel('Share of Care Need')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Share of Social Care Need')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'ShareSocialCareNeedsChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 5: Per Capita total care demand and unmet care demand (1960-2020)    , 
    fig, ax = plt.subplots()
    ax.stackplot(output['year'], output['perCapitaCareReceived'], output['perCapitaUnmetCareDemand'], labels = ['Care Received','Unmet Care Need'])
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Per Capita Received Care and Unmet Care Need')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'PerCapitaCareUnmetCareChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 6: Per Capita total social care demand and unmet social care demand (1960-2020) 
    fig, ax = plt.subplots()
    ax.stackplot(output['year'], output['perCapitaSocialCareReceived'], output['perCapitaUnmetSocialCareDemand'], labels = ['Care Received','Unmet Care Need'])
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Per Capita Demand and Unmet Social Care Need')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'PerCapitaDemandUnmetSocialCareChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 7: Per Capita total child care demand and unmet child care demand (1960-2020)
    
    fig, ax = plt.subplots()
    ax.stackplot(output['year'], output['perCapitaChildCareReceived'], output['perCapitaUnmetChildCareDemand'], labels = ['Care Received','Unmet Care Need'])
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Per Capita Demand and Unmet Child Care Need')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'PerCapitaDemandUnmetChildCareChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 8: total informal and formal care received and unmet care needs (from 1960 to 2020)
               
    fig, ax = plt.subplots()
    ax.stackplot(output['year'], output['informalCareReceived'], output['formalCareReceived'], output['totalUnnmetCareNeed'], 
                 labels = ['Informal Care','Formal Care', 'Unmet Care Needs'])
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Care by Type and Unmet Care Needs')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'CareReceivedStackedChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 9: Shares informal care received (from 1960 to 2020)
    
    #sharesInformalCare_M.append(np.mean(shareInformalCareReceived[-20:]))
    #sharesInformalCare_SD.append(np.std(shareInformalCareReceived[-20:]))
    
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['shareInformalCareReceived'], linewidth = 3, label = 'Population')
    p2, = ax.plot(output['year'], output['shareInformalCareReceived_1'], label = 'Class I')
    p3, = ax.plot(output['year'], output['shareInformalCareReceived_2'], label = 'Class II')
    p4, = ax.plot(output['year'], output['shareInformalCareReceived_3'], label = 'Class III')
    p5, = ax.plot(output['year'], output['shareInformalCareReceived_4'], label = 'Class IV')
    p6, = ax.plot(output['year'], output['shareInformalCareReceived_5'], label = 'Class V')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Share of care received')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Share of Informal Care Received')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
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
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Share of care received')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Share of Informal Social Care Received')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
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
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Share of care received')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Share of Informal Child Care Received')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'ShareInformalChildCareReceivedChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 12: total informal and formal social care received and unmet social care needs (from 1960 to 2020)
    
    fig, ax = plt.subplots()
    ax.stackplot(output['year'], output['informalSocialCareReceived'], output['formalSocialCareReceived'], output['unmetSocialCareNeed'], 
                 labels = ['Informal Care','Formal Care', 'Unmet Care Needs'])
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Social Care by Type and Unmet Care Needs')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'SocialCareReceivedStackedChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Informal and formal care and unmet care need per receiver by care need level.
    
    n_groups = p['numCareLevels']-1
    meanInformalCareReceived_1 = output.loc[output['year'] == p['outputYear'], 'meanInformalSocialCareReceived_N1'].values[0]
    meanFormalCareReceived_1 = output.loc[output['year'] == p['outputYear'], 'meanFormalSocialCareReceived_N1'].values[0]
    meanUnmetNeed_1 = output.loc[output['year'] == p['outputYear'], 'meanUnmetSocialCareNeed_N1'].values[0]
    meanInformalCareReceived_2 = output.loc[output['year'] == p['outputYear'], 'meanInformalSocialCareReceived_N2'].values[0]
    meanFormalCareReceived_2 = output.loc[output['year'] == p['outputYear'], 'meanFormalSocialCareReceived_N2'].values[0]
    meanUnmetNeed_2 = output.loc[output['year'] == p['outputYear'], 'meanUnmetSocialCareNeed_N2'].values[0]
    meanInformalCareReceived_3 = output.loc[output['year'] == p['outputYear'], 'meanInformalSocialCareReceived_N3'].values[0]
    meanFormalCareReceived_3 = output.loc[output['year'] == p['outputYear'], 'meanFormalSocialCareReceived_N3'].values[0]
    meanUnmetNeed_3 = output.loc[output['year'] == p['outputYear'], 'meanUnmetSocialCareNeed_N3'].values[0]
    meanInformalCareReceived_4 = output.loc[output['year'] == p['outputYear'], 'meanInformalSocialCareReceived_N4'].values[0]
    meanFormalCareReceived_4 = output.loc[output['year'] == p['outputYear'], 'meanFormalSocialCareReceived_N4'].values[0]
    meanUnmetNeed_4 = output.loc[output['year'] == p['outputYear'], 'meanUnmetSocialCareNeed_N4'].values[0]
    informalCare = (meanInformalCareReceived_1, meanInformalCareReceived_2, meanInformalCareReceived_3,
                    meanInformalCareReceived_4)
    formalCare = (meanFormalCareReceived_1, meanFormalCareReceived_2, meanFormalCareReceived_3,
                  meanFormalCareReceived_4)
    sumInformalFormalCare = [x + y for x, y in zip(informalCare, formalCare)]
    unmetNeeds = (meanUnmetNeed_1, meanUnmetNeed_2, meanUnmetNeed_3, meanUnmetNeed_4)
    ind = np.arange(n_groups)    # the x locations for the groups
    width = 0.4       # the width of the bars: can also be len(x) sequence
    fig, ax = plt.subplots()
    p1 = ax.bar(ind, informalCare, width, label = 'Informal Care')
    p2 = ax.bar(ind, formalCare, width, bottom = informalCare, label = 'Formal Care')
    p3 = ax.bar(ind, unmetNeeds, width, bottom = sumInformalFormalCare, label = 'Unmet Care Needs')
    ax.set_ylabel('Hours per week')
    ax.set_xticks(ind)
    plt.xticks(ind, ('NL 1', 'NL 2', 'NL 3', 'NL 4'))
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Informal, Formal and Unmet Social Care by Care Need Level')
    fig.tight_layout()
    path = os.path.join(folder, 'SocialCarePerRecipientByNeedLevelStackedBarChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 13: total informal and formal child care received and unmet child care needs (from 1960 to 2020)
    
    fig, ax = plt.subplots()
    ax.stackplot(output['year'], output['informalChildCareReceived'], output['formalChildCareReceived'], output['unmetChildCareNeed'], 
                 labels = ['Informal Care','Formal Care', 'Unmet Care Needs'])
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Child Care by Type and Unmet Care Needs')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
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
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Share of care need')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Share of Unmet Care Need')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
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
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Share of care need')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Share of Unmet Social Care Need')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
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
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Share of care need')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Share of Unmet Child Care Need')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
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
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Per Capita Unmet Care Need')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
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
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Average Unmet Care Need')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'AverageUnmetCareNeedChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 19 
   
    n_groups = p['numberClasses']
    meanInformalCareReceived_1 = output.loc[output['year'] == p['outputYear'], 'informalCareReceived_1'].values[0]
    meanFormalCareReceived_1 = output.loc[output['year'] == p['outputYear'], 'formalCareReceived_1'].values[0]
    meanUnmetNeed_1 = output.loc[output['year'] == p['outputYear'], 'unmetCareNeed_1'].values[0]
    meanInformalCareReceived_2 = output.loc[output['year'] == p['outputYear'], 'informalCareReceived_2'].values[0]
    meanFormalCareReceived_2 = output.loc[output['year'] == p['outputYear'], 'formalCareReceived_2'].values[0]
    meanUnmetNeed_2 = output.loc[output['year'] == p['outputYear'], 'unmetCareNeed_2'].values[0]
    meanInformalCareReceived_3 = output.loc[output['year'] == p['outputYear'], 'informalCareReceived_3'].values[0]
    meanFormalCareReceived_3 = output.loc[output['year'] == p['outputYear'], 'formalCareReceived_3'].values[0]
    meanUnmetNeed_3 = output.loc[output['year'] == p['outputYear'], 'unmetCareNeed_3'].values[0]
    meanInformalCareReceived_4 = output.loc[output['year'] == p['outputYear'], 'informalCareReceived_4'].values[0]
    meanFormalCareReceived_4 = output.loc[output['year'] == p['outputYear'], 'formalCareReceived_4'].values[0]
    meanUnmetNeed_4 = output.loc[output['year'] == p['outputYear'], 'unmetCareNeed_4'].values[0]
    meanInformalCareReceived_5 = output.loc[output['year'] == p['outputYear'], 'informalCareReceived_5'].values[0]
    meanFormalCareReceived_5 = output.loc[output['year'] == p['outputYear'], 'formalCareReceived_5'].values[0]
    meanUnmetNeed_5 = output.loc[output['year'] == p['outputYear'], 'unmetCareNeed_5'].values[0]
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
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Informal Care Per Recipient')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    ax.set_ylim([0, 50])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
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
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Formal Care Per Recipient')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
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
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Unmet Care Need Per Recipient')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
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
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Delivered and Unmet Care Per Recipient')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    ax.set_ylim([0, 50])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'Delivered_UnmetCarePerRecipientChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 24: informal and formal care received and unmet care needs per recipient by social class (mean of last 20 years)
   
    n_groups = p['numberClasses']
    meanInformalCareReceived_1 = output.loc[output['year'] == p['outputYear'], 'informalCarePerRecipient_1'].values[0]
    meanFormalCareReceived_1 = output.loc[output['year'] == p['outputYear'], 'formalCarePerRecipient_1'].values[0]
    meanUnmetNeed_1 = output.loc[output['year'] == p['outputYear'], 'unmetCarePerRecipient_1'].values[0]
    meanInformalCareReceived_2 = output.loc[output['year'] == p['outputYear'], 'informalCarePerRecipient_2'].values[0]
    meanFormalCareReceived_2 = output.loc[output['year'] == p['outputYear'], 'formalCarePerRecipient_2'].values[0]
    meanUnmetNeed_2 = output.loc[output['year'] == p['outputYear'], 'unmetCarePerRecipient_2'].values[0]
    meanInformalCareReceived_3 = output.loc[output['year'] == p['outputYear'], 'informalCarePerRecipient_3'].values[0]
    meanFormalCareReceived_3 = output.loc[output['year'] == p['outputYear'], 'formalCarePerRecipient_3'].values[0]
    meanUnmetNeed_3 = output.loc[output['year'] == p['outputYear'], 'unmetCarePerRecipient_3'].values[0]
    meanInformalCareReceived_4 = output.loc[output['year'] == p['outputYear'], 'informalCarePerRecipient_4'].values[0]
    meanFormalCareReceived_4 = output.loc[output['year'] == p['outputYear'], 'formalCarePerRecipient_4'].values[0]
    meanUnmetNeed_4 = output.loc[output['year'] == p['outputYear'], 'unmetCarePerRecipient_4'].values[0]
    meanInformalCareReceived_5 = output.loc[output['year'] == p['outputYear'], 'informalCarePerRecipient_5'].values[0]
    meanFormalCareReceived_5 = output.loc[output['year'] == p['outputYear'], 'formalCarePerRecipient_5'].values[0]
    meanUnmetNeed_5 = output.loc[output['year'] == p['outputYear'], 'unmetCarePerRecipient_5'].values[0]
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
   
    n_groups = p['numberClasses']
    meanInformalCareReceived_1 = output.loc[output['year'] == p['outputYear'], 'informalSocialCareReceived_1'].values[0]
    meanFormalCareReceived_1 = output.loc[output['year'] == p['outputYear'], 'formalSocialCareReceived_1'].values[0]
    meanUnmetNeed_1 = output.loc[output['year'] == p['outputYear'], 'unmetSocialCareNeed_1'].values[0]
    meanInformalCareReceived_2 = output.loc[output['year'] == p['outputYear'], 'informalSocialCareReceived_2'].values[0]
    meanFormalCareReceived_2 = output.loc[output['year'] == p['outputYear'], 'formalSocialCareReceived_2'].values[0]
    meanUnmetNeed_2 = output.loc[output['year'] == p['outputYear'], 'unmetSocialCareNeed_2'].values[0]
    meanInformalCareReceived_3 = output.loc[output['year'] == p['outputYear'], 'informalSocialCareReceived_3'].values[0]
    meanFormalCareReceived_3 = output.loc[output['year'] == p['outputYear'], 'formalSocialCareReceived_3'].values[0]
    meanUnmetNeed_3 = output.loc[output['year'] == p['outputYear'], 'unmetSocialCareNeed_3'].values[0]
    meanInformalCareReceived_4 = output.loc[output['year'] == p['outputYear'], 'informalSocialCareReceived_4'].values[0]
    meanFormalCareReceived_4 = output.loc[output['year'] == p['outputYear'], 'formalSocialCareReceived_4'].values[0]
    meanUnmetNeed_4 = output.loc[output['year'] == p['outputYear'], 'unmetSocialCareNeed_4'].values[0]
    meanInformalCareReceived_5 = output.loc[output['year'] == p['outputYear'], 'informalSocialCareReceived_5'].values[0]
    meanFormalCareReceived_5 = output.loc[output['year'] == p['outputYear'], 'formalSocialCareReceived_5'].values[0]
    meanUnmetNeed_5 = output.loc[output['year'] == p['outputYear'], 'unmetSocialCareNeed_5'].values[0]
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
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Informal Social Care Per Recipient')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
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
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Formal Social Care Per Recipient')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
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
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Unmet Social Care Need Per Recipient')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
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
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Delivered and Unmet Care Per Recipient')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'Delivered_UnmetSocialCarePerRecipientChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 30

    n_groups = p['numberClasses']
    meanInformalCareReceived_1 = output.loc[output['year'] == p['outputYear'], 'informalSocialCarePerRecipient_1'].values[0]
    meanFormalCareReceived_1 = output.loc[output['year'] == p['outputYear'], 'formalSocialCarePerRecipient_1'].values[0]
    meanUnmetNeed_1 = output.loc[output['year'] == p['outputYear'], 'unmetSocialCarePerRecipient_1'].values[0]
    meanInformalCareReceived_2 = output.loc[output['year'] == p['outputYear'], 'informalSocialCarePerRecipient_2'].values[0]
    meanFormalCareReceived_2 = output.loc[output['year'] == p['outputYear'], 'formalSocialCarePerRecipient_2'].values[0]
    meanUnmetNeed_2 = output.loc[output['year'] == p['outputYear'], 'unmetSocialCarePerRecipient_2'].values[0]
    meanInformalCareReceived_3 = output.loc[output['year'] == p['outputYear'], 'informalSocialCarePerRecipient_3'].values[0]
    meanFormalCareReceived_3 = output.loc[output['year'] == p['outputYear'], 'formalSocialCarePerRecipient_3'].values[0]
    meanUnmetNeed_3 = output.loc[output['year'] == p['outputYear'], 'unmetSocialCarePerRecipient_3'].values[0]
    meanInformalCareReceived_4 = output.loc[output['year'] == p['outputYear'], 'informalSocialCarePerRecipient_4'].values[0]
    meanFormalCareReceived_4 = output.loc[output['year'] == p['outputYear'], 'formalSocialCarePerRecipient_4'].values[0]
    meanUnmetNeed_4 = output.loc[output['year'] == p['outputYear'], 'unmetSocialCarePerRecipient_4'].values[0]
    meanInformalCareReceived_5 = output.loc[output['year'] == p['outputYear'], 'informalSocialCarePerRecipient_5'].values[0]
    meanFormalCareReceived_5 = output.loc[output['year'] == p['outputYear'], 'formalSocialCarePerRecipient_5'].values[0]
    meanUnmetNeed_5 = output.loc[output['year'] == p['outputYear'], 'unmetSocialCarePerRecipient_5'].values[0]
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
   
    n_groups = p['numberClasses']
    meanInformalCareReceived_1 = output.loc[output['year'] == p['outputYear'], 'informalChildCareReceived_1'].values[0]
    meanFormalCareReceived_1 = output.loc[output['year'] == p['outputYear'], 'formalChildCareReceived_1'].values[0]
    meanUnmetNeed_1 = output.loc[output['year'] == p['outputYear'], 'unmetChildCareNeed_1'].values[0]
    meanInformalCareReceived_2 = output.loc[output['year'] == p['outputYear'], 'informalChildCareReceived_2'].values[0]
    meanFormalCareReceived_2 = output.loc[output['year'] == p['outputYear'], 'formalChildCareReceived_2'].values[0]
    meanUnmetNeed_2 = output.loc[output['year'] == p['outputYear'], 'unmetChildCareNeed_2'].values[0]
    meanInformalCareReceived_3 = output.loc[output['year'] == p['outputYear'], 'informalChildCareReceived_3'].values[0]
    meanFormalCareReceived_3 = output.loc[output['year'] == p['outputYear'], 'formalChildCareReceived_3'].values[0]
    meanUnmetNeed_3 = output.loc[output['year'] == p['outputYear'], 'unmetChildCareNeed_3'].values[0]
    meanInformalCareReceived_4 = output.loc[output['year'] == p['outputYear'], 'informalChildCareReceived_4'].values[0]
    meanFormalCareReceived_4 = output.loc[output['year'] == p['outputYear'], 'formalChildCareReceived_4'].values[0]
    meanUnmetNeed_4 = output.loc[output['year'] == p['outputYear'], 'unmetChildCareNeed_4'].values[0]
    meanInformalCareReceived_5 = output.loc[output['year'] == p['outputYear'], 'informalChildCareReceived_5'].values[0]
    meanFormalCareReceived_5 = output.loc[output['year'] == p['outputYear'], 'formalChildCareReceived_5'].values[0]
    meanUnmetNeed_5 = output.loc[output['year'] == p['outputYear'], 'unmetChildCareNeed_5'].values[0]
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
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Informal Child Care Per Recipient')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
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
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Formal Child Care Per Recipient')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
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
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylim([0, maxValue*2.0])
    ax.set_ylabel('Hours per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Average Hours of Care By Class')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_ylim([0, 60])
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
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
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Unmet Child Care Need Per Recipient')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
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
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Delivered and Unmet Child Care Per Recipient')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    ax.set_ylim([0, 30])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'Delivered_UnmetChildCarePerRecipientChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 37
    n_groups = p['numberClasses']
    meanInformalCareReceived_1 = output.loc[output['year'] == p['outputYear'], 'informalChildCarePerRecipient_1'].values[0]
    meanFormalCareReceived_1 = output.loc[output['year'] == p['outputYear'], 'formalChildCarePerRecipient_1'].values[0]
    meanUnmetNeed_1 = output.loc[output['year'] == p['outputYear'], 'unmetChildCarePerRecipient_1'].values[0]
    meanInformalCareReceived_2 = output.loc[output['year'] == p['outputYear'], 'informalChildCarePerRecipient_2'].values[0]
    meanFormalCareReceived_2 = output.loc[output['year'] == p['outputYear'], 'formalChildCarePerRecipient_2'].values[0]
    meanUnmetNeed_2 = output.loc[output['year'] == p['outputYear'], 'unmetChildCarePerRecipient_2'].values[0]
    meanInformalCareReceived_3 = output.loc[output['year'] == p['outputYear'], 'informalChildCarePerRecipient_3'].values[0]
    meanFormalCareReceived_3 = output.loc[output['year'] == p['outputYear'], 'formalChildCarePerRecipient_3'].values[0]
    meanUnmetNeed_3 = output.loc[output['year'] == p['outputYear'], 'unmetChildCarePerRecipient_3'].values[0]
    meanInformalCareReceived_4 = output.loc[output['year'] == p['outputYear'], 'informalChildCarePerRecipient_4'].values[0]
    meanFormalCareReceived_4 = output.loc[output['year'] == p['outputYear'], 'formalChildCarePerRecipient_4'].values[0]
    meanUnmetNeed_4 = output.loc[output['year'] == p['outputYear'], 'unmetChildCarePerRecipient_4'].values[0]
    meanInformalCareReceived_5 = output.loc[output['year'] == p['outputYear'], 'informalChildCarePerRecipient_5'].values[0]
    meanFormalCareReceived_5 = output.loc[output['year'] == p['outputYear'], 'formalChildCarePerRecipient_5'].values[0]
    meanUnmetNeed_5 = output.loc[output['year'] == p['outputYear'], 'unmetChildCarePerRecipient_5'].values[0]
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
    
    n_groups = p['numberClasses']
    meanInformalCareSupplied_1 = output.loc[output['year'] == p['outputYear'], 'informalCarePerCarer_1'].values[0]
    meanFormalCareSupplied_1 = output.loc[output['year'] == p['outputYear'], 'formalCarePerCarer_1'].values[0]
    meanInformalCareSupplied_2 = output.loc[output['year'] == p['outputYear'], 'informalCarePerCarer_2'].values[0]
    meanFormalCareSupplied_2 = output.loc[output['year'] == p['outputYear'], 'formalCarePerCarer_2'].values[0]
    meanInformalCareSupplied_3 = output.loc[output['year'] == p['outputYear'], 'informalCarePerCarer_3'].values[0]
    meanFormalCareSupplied_3 = output.loc[output['year'] == p['outputYear'], 'formalCarePerCarer_3'].values[0]
    meanInformalCareSupplied_4 = output.loc[output['year'] == p['outputYear'], 'informalCarePerCarer_4'].values[0]
    meanFormalCareSupplied_4 = output.loc[output['year'] == p['outputYear'], 'formalCarePerCarer_4'].values[0]
    meanInformalCareSupplied_5 = output.loc[output['year'] == p['outputYear'], 'informalCarePerCarer_5'].values[0]
    meanFormalCareSupplied_5 = output.loc[output['year'] == p['outputYear'], 'formalCarePerCarer_5'].values[0]
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
    meanInformalCareHousehold = output.loc[output['year'] == p['outputYear'], 'sumNoK_informalSupplies[0]'].values[0]
    meanFormalCareHousehold = output.loc[output['year'] == p['outputYear'], 'sumNoK_formalSupplies[0]'].values[0]
    meanInformalCare_K1 = output.loc[output['year'] == p['outputYear'], 'sumNoK_informalSupplies[1]'].values[0]
    meanFormalCare_K1 = output.loc[output['year'] == p['outputYear'], 'sumNoK_formalSupplies[1]'].values[0]
    meanInformalCare_K2 = output.loc[output['year'] == p['outputYear'], 'sumNoK_informalSupplies[2]'].values[0]
    meanFormalCare_K2 = output.loc[output['year'] == p['outputYear'], 'sumNoK_formalSupplies[2]'].values[0]
    meanInformalCare_K3 = output.loc[output['year'] == p['outputYear'], 'sumNoK_informalSupplies[3]'].values[0]
    meanFormalCare_K3 = output.loc[output['year'] == p['outputYear'], 'sumNoK_formalSupplies[3]'].values[0]
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
    
    # Shares of carers
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['shareCarers'], linewidth = 3, label = 'Population')
    p2, = ax.plot(output['year'], output['shareWomenCarers'], label = 'Women')
    p3, = ax.plot(output['year'], output['shareMenCarers'], label = 'Man')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Share')
    ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    # ax.legend_.remove()
    ax.set_title('Share of Informal Carers')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    # ax.set_ylim([0, 0.8])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'ShareInformalCarersChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    
    # Chart 40: Share of Care supplied by Women, total and by social class (from 1960 to 2020)
   
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['shareInformalCareSuppliedByFemales'], linewidth = 3, label = 'Population')
    p2, = ax.plot(output['year'], output['shareInformalCareSuppliedByFemales_1'], label = 'Class I')
    p3, = ax.plot(output['year'], output['shareInformalCareSuppliedByFemales_2'], label = 'Class II')
    p4, = ax.plot(output['year'], output['shareInformalCareSuppliedByFemales_3'], label = 'Class III')
    p5, = ax.plot(output['year'], output['shareInformalCareSuppliedByFemales_4'], label = 'Class IV')
    p6, = ax.plot(output['year'], output['shareInformalCareSuppliedByFemales_5'], label = 'Class V')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Share of care')
    ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    # ax.legend_.remove()
    ax.set_title('Share of Informal Care supplied by Women')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    # ax.set_ylim([0, 0.8])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'ShareCareWomedChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 41: informal care provided by gender per social class (mean of last 20 years)
    
    n_groups = p['numberClasses']
    informalCareMales_1 = output.loc[output['year'] == p['outputYear'], 'informalCareSuppliedByMales_1'].values[0]
    informalCareFemales_1 = output.loc[output['year'] == p['outputYear'], 'informalCareSuppliedByFemales_1'].values[0]
    informalCareMales_2 = output.loc[output['year'] == p['outputYear'], 'informalCareSuppliedByMales_2'].values[0]
    informalCareFemales_2 = output.loc[output['year'] == p['outputYear'], 'informalCareSuppliedByFemales_2'].values[0]
    informalCareMales_3 = output.loc[output['year'] == p['outputYear'], 'informalCareSuppliedByMales_3'].values[0]
    informalCareFemales_3 = output.loc[output['year'] == p['outputYear'], 'informalCareSuppliedByFemales_3'].values[0]
    informalCareMales_4 = output.loc[output['year'] == p['outputYear'], 'informalCareSuppliedByMales_4'].values[0]
    informalCareFemales_4 = output.loc[output['year'] == p['outputYear'], 'informalCareSuppliedByFemales_4'].values[0]
    informalCareMales_5 = output.loc[output['year'] == p['outputYear'], 'informalCareSuppliedByMales_5'].values[0]
    informalCareFemales_5 = output.loc[output['year'] == p['outputYear'], 'informalCareSuppliedByFemales_5'].values[0]
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
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Wage Ratio')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Women and Men Wage Ratio')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'WomenMenWageRatioChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 43: income by gender per social class (mean of last 20 years)
           
    n_groups = p['numberClasses']
    WageMales_1 = output.loc[output['year'] == p['outputYear'], 'averageMalesWage_1'].values[0]
    WageFemales_1 = output.loc[output['year'] == p['outputYear'], 'averageFemalesWage_1'].values[0]
    WageMales_2 = output.loc[output['year'] == p['outputYear'], 'averageMalesWage_2'].values[0]
    WageFemales_2 = output.loc[output['year'] == p['outputYear'], 'averageFemalesWage_2'].values[0]
    WageMales_3 = output.loc[output['year'] == p['outputYear'], 'averageMalesWage_3'].values[0]
    WageFemales_3 = output.loc[output['year'] == p['outputYear'], 'averageFemalesWage_3'].values[0]
    WageMales_4 = output.loc[output['year'] == p['outputYear'], 'averageMalesWage_4'].values[0]
    WageFemales_4 = output.loc[output['year'] == p['outputYear'], 'averageFemalesWage_4'].values[0]
    WageMales_5 = output.loc[output['year'] == p['outputYear'], 'averageMalesWage_5'].values[0]
    WageFemales_5 = output.loc[output['year'] == p['outputYear'], 'averageFemalesWage_5'].values[0]
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
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Income Ratio')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Women and Men Income Ratio')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'WomenMenIncomeRatioChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 45: income by gender per social class (mean of last 20 years)
    
    n_groups = p['numberClasses']
    incomeMales_1 = output.loc[output['year'] == p['outputYear'], 'averageMalesIncome_1'].values[0]
    incomeFemales_1 = output.loc[output['year'] == p['outputYear'], 'averageFemalesIncome_1'].values[0]
    incomeMales_2 = output.loc[output['year'] == p['outputYear'], 'averageMalesIncome_2'].values[0]
    incomeFemales_2 = output.loc[output['year'] == p['outputYear'], 'averageFemalesIncome_2'].values[0]
    incomeMales_3 = output.loc[output['year'] == p['outputYear'], 'averageMalesIncome_3'].values[0]
    incomeFemales_3 = output.loc[output['year'] == p['outputYear'], 'averageFemalesIncome_3'].values[0]
    incomeMales_4 = output.loc[output['year'] == p['outputYear'], 'averageMalesIncome_4'].values[0]
    incomeFemales_4 = output.loc[output['year'] == p['outputYear'], 'averageFemalesIncome_4'].values[0]
    incomeMales_5 = output.loc[output['year'] == p['outputYear'], 'averageMalesIncome_5'].values[0]
    incomeFemales_5 = output.loc[output['year'] == p['outputYear'], 'averageFemalesIncome_5'].values[0]
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
    ax.set_xlim(left = p['statsCollectFrom'])
    # ax.set_ylabel('Hours of care')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Population and Number of Taxpayers')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
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
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylim([0, maxValue*1.5])
    # ax.set_ylabel('Average Household Members')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Average Family Size')
    # ax.set_ylim([0, 8])
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'AverageFamilySizeChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()         
    
    # Chart 48: Average Tax Burden (1960-2020)
   
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['taxBurden'], linewidth = 3, color = 'red')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Care costs per taxpayer per year')
    # ax.set_xlabel('Year')
    ax.set_title('Average Tax Burden in pounds')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'TaxBurdenChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()  
  
    # total Tax Refund
    
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['totalTaxRefund'], linewidth = 3, color = 'red')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Tax Refund')
    # ax.set_xlabel('Year')
    ax.set_title('Total Tax Refund in pounds')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'totalTaxRefundChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()  
    
     # pension budget
    
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['govBudget'], linewidth = 3, color = 'red')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Tax Refund')
    # ax.set_xlabel('Year')
    ax.set_title('Budget balance in pounds')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'govBudgetChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()  
    
    # Chart 49: Proportion of married adult women (1960-2020)
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['marriageProp'], linewidth = 3, color = 'red')
    ax.set_xlim(left = p['statsCollectFrom'])
    # ax.set_ylabel('Proportion of married adult women')
    ax.set_title('Proportion of married adult women')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'MarriageRateChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 49: Proportion of lone parents (1960-2020)
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['shareLoneParents'], linewidth = 3, color = 'red')
    ax.set_xlim(left = p['statsCollectFrom'])
    # ax.set_ylabel('Proportion of married adult women')
    ax.set_title('Share of lone parents')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'LoneParentsShareChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 49-bis: Proportion of Distant parents (1960-2020)
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['shareDistantParents'], linewidth = 3, color = 'red')
    ax.set_xlim(left = p['statsCollectFrom'])
    # ax.set_ylabel('Proportion of married adult women')
    ax.set_title('Share of distant parents')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'DistantParentsShareChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 50: Health Care Cost (1960-2020)
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['hospitalizationCost'], linewidth = 3, color = 'red')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Cost in Pounds')
    # ax.set_xlabel('Year')
    ax.set_title('Total Health Care Cost')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'TotalHealthCareCostChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 51: Per Capita Health Care Cost (1960-2020)
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['perCapitaHospitalizationCost'], linewidth = 3, color = 'red')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Cost in Pounds')
    # ax.set_xlabel('Year')
    ax.set_title('Per Capita Health Care Cost')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
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
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Gini Coefficient')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Unmet Social Care Gini Coeffcient')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.ylim(0.5, 1.0)
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
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
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Gini Coefficient')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.set_title('Share of Unmet Social Care Gini Coeffcient')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.ylim(0.5, 1.0)
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'ShareUnmetSocialCareGiniCoefficientChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 54: Public supply
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['publicSupply'], linewidth = 3)
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours of per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.legend_.remove()
    ax.set_title('Public Social Care Supply')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'PublicSocialCareSupplyChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
  
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['costDirectFunding'], linewidth = 3)
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Pounds per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.legend_.remove()
    ax.set_title('Cost of Public Social Care')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
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
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Hours of per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    # ax.legend_.remove()
    ax.set_title('Credit Public Care Supply')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'CreditPublicSocialCareSupplyChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['shareCreditsSpent'], linewidth = 3)
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Share of total credit')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.legend_.remove()
    ax.set_title('Share of Social Credit Transferred')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'ShareSocialCreditTransferChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['careCreditCost'], linewidth = 3)
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Pounds per week')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.legend_.remove()
    ax.set_title('Cost of Credit Public Social Care')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'CostCreditSocialCareChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
    # Chart 55: Aggregate QALY
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['totQALY'], linewidth = 3)
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('QALY Index')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.legend_.remove()
    ax.set_title('Aggregate QALY Index')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'AggregateQALYChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
     # Chart 56: Average QALY
    fig, ax = plt.subplots()
    ax.plot(output['year'], output['meanQALY'], linewidth = 3)
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('QALY Index')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'lower left')
    ax.legend_.remove()
    ax.set_title('Average QALY Index')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'AverageQALYChart.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
#        qualityAdjustedLifeYears_M.append(np.mean(discountedQALY[-20:]))
#        qualityAdjustedLifeYears_SD.append(np.std(discountedQALY[-20:]))
#        
#        perCapitaQualityAdjustedLifeYears_M.append(np.mean(averageDiscountedQALY[-20:]))
#        perCapitaQualityAdjustedLifeYears_SD.append(np.std(averageDiscountedQALY[-20:]))

    # Chart 57: Ratio of Unmet Care Need and Total Supply (from 1960 to 2020)
    fig, ax = plt.subplots()
    p1, = ax.plot(output['year'], output['ratioUnmetNeed_CareSupply'], linewidth = 3, label = 'Population')
    p2, = ax.plot(output['year'], output['ratioUnmetNeed_CareSupply_1'], label = 'Class I')
    p3, = ax.plot(output['year'], output['ratioUnmetNeed_CareSupply_2'], label = 'Class II')
    p4, = ax.plot(output['year'], output['ratioUnmetNeed_CareSupply_3'], label = 'Class III')
    p5, = ax.plot(output['year'], output['ratioUnmetNeed_CareSupply_4'], label = 'Class IV')
    p6, = ax.plot(output['year'], output['ratioUnmetNeed_CareSupply_5'], label = 'Class V')
    ax.set_xlim(left = p['statsCollectFrom'])
    ax.set_ylabel('Share of total supply')
    # ax.set_xlabel('Year')
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(loc = 'upper left')
    ax.set_title('Ratio of Unmet Care Need and Total Supply')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlim(p['statsCollectFrom'], p['endYear'])
    plt.xticks(range(p['statsCollectFrom'], p['endYear']+1, 10))
    fig.tight_layout()
    path = os.path.join(folder, 'RatioUnmetCareNeedTotalSupply.pdf')
    pp = PdfPages(path)
    pp.savefig(fig)
    pp.close()
    
doGraphs()