# -*- coding: utf-8 -*-
"""
Created on Thu Nov 02 15:40:07 2017

@author: ug4d
"""
import random
import numpy as np
import math
import networkx as nx

class Population:
    """The population class stores a collection of persons."""
    def __init__ (self, initialPop, startYear, minStartAge, maxStartAge,
                  nc, ics, wa, il, fl, gr, wdt, rs):
        self.allPeople = []
        self.livingPeople = []
        
        random.seed(rs)
        np.random.seed(rs)
        
        ranks = []
        for n in range(int(nc)):
            ranks.extend([n]*(int)(ics[n]*(initialPop/2)))
        
        for i in range(int(initialPop/2)):
            
            ageMale = random.randint(minStartAge, maxStartAge)
            ageFemale = ageMale - random.randint(-2,5)
            if ( ageFemale < 24 ):
                ageFemale = 24
            maleBirthYear = startYear - ageMale
            femaleBirthYear = startYear - ageFemale
            classeRanks = range(int(nc))
            numClass = ranks[i] #np.random.choice(classeRanks, p = ics)
            classRank = numClass
            
            workingTimeMale = 0
            numClass = int(numClass)
            for i in range(int(ageMale-wa[numClass])):
                workingTimeMale *= wdt
                workingTimeMale += 1
            workingTimeFemale = 0
            for i in range(int(ageFemale-wa[numClass])):
                workingTimeFemale *= wdt
                workingTimeFemale += 1
            newK = fl[numClass]    
            c = np.math.log(il[numClass]/newK)
            maleWage = newK*np.math.exp(c*np.math.exp(-1*gr[numClass]*workingTimeMale))
            femaleWage = newK*np.math.exp(c*np.math.exp(-1*gr[numClass]*workingTimeFemale))
            maleIncome = maleWage*40.0
            femaleIncome = femaleWage*40.0
            manStatus = 'employed'
            finalIncome = fl[numClass]
            yearsInTown = random.randint(0, 10)
            tenure = 1.0
            newMan = Person(None, None, ageMale, maleBirthYear, 'male', manStatus, 
                            None, classRank, maleWage, 
                            maleIncome, finalIncome, workingTimeMale, yearsInTown)
            status = 'employed'
            finalIncome = fl[numClass]
            yearsInTown = random.randint(0, 10)
            newWoman = Person(None, None, ageFemale, femaleBirthYear, 'female', 
                              status, None, classRank, femaleWage, femaleIncome, 
                              finalIncome, workingTimeFemale, yearsInTown)
            
            newMan.independentStatus = True
            newWoman.independentStatus = True

            newMan.partner = newWoman
            newWoman.partner = newMan

            self.allPeople.append(newMan)
            self.livingPeople.append(newMan)
            self.allPeople.append(newWoman)
            self.livingPeople.append(newWoman)

class Person:
    """The person class stores information about a person in the sim."""
    counter = 1

    def __init__(self, mother, father, age, birthYear, sex, status, house,
                 classRank, wage, income, finalIncome, workingTime, yit):

        self.mother = mother
        self.father = father
        self.children = []
        self.household = []
        self.age = age
        self.yearAfterPolicy = 0
        self.birthdate = birthYear
        self.visitedCarer = False
        self.careNeedLevel = 0
        
        self.hoursDemand = 0
        self.residualNeed = 0
        
        
        
        self.hoursSocialCareDemand = 0
        self.residualSocialCareNeed = 0
        self.hoursChildCareDemand = 0
        self.residualChildCareNeed = 0
        self.informalChildCareReceived = 0
        self.formalChildCareReceived = 0
        
        self.informalSocialCareReceived = 0
        self.formalSocialCareReceived = 0
        
        self.netHouseholdCare = 0
        self.netIndividualCare = 0
        
        self.hoursSupply = 0
        
        
        self.socialWork = 0
        self.childWork = 0
        self.workToCare = 0
        
        self.socialCareCredits = 0
        self.volunteerCareSupply = 0
        self.creditNeedRatio = 0
        self.maxNokSupply = 0
        self.residualNetNeed = 0
        self.potentialVolunteer = False
        
        self.cumulativeUnmetNeed = 0
        self.totalDiscountedShareUnmetNeed = 0
        self.totalDiscountedTime = 0
        self.averageShareUnmetNeed = 0
        self.informalSupplyByKinship = []
        self.formalSupplyByKinship = []
        self.networkSupply = 0
        
        self.maxInformalSupply = 0
        self.residualInformalSupplies = []
        self.hoursInformalSupplies = []
        self.residualInformalSupply = 0
        
        self.residualFormalSupply = []
        
        self.hoursFormalSupply = []
        self.residualExtraworkCare = []
        self.residualIncomeCare = 0
        self.offWorkCare = 0

        self.hoursCareSupply = 0
        self.mortalityRate = 0
        self.fertilityRate = 0
        
        self.residualWorkingHours = 0
        self.incomeByTaxBands = []
        self.maxFormalCareSupply = 0
        self.qaly = 0
        self.residualSupply = 0
        self.formalCare = 0
        self.informalCare = 0
        self.careReceived = 0
        self.socialNetwork = []
        
        self.careNetwork = nx.Graph()
        self.numSuppliers = 0
        self.supplyNetwork = nx.Graph()
        
        self.householdSupply = 0
        
        self.householdTotalSupply = 0
        
        self.careReceivers = []
        self.totalCareSupplied = []
        
        self.totalSupply = 0
        
        self.totalInformalSupply = 0
        self.socialCareProvider = False
        self.babyCarer = False
        self.yearOfSchoolLeft = 0
        self.dead = False
        self.partner = None
        self.previousPartners = []
        self.numberPartner = 0
        if sex == 'random':
            self.sex = random.choice(['male', 'female'])
        else:
            self.sex = sex
        if self.sex == 'female':
            self.sexIndex = 1
        else:
            self.sexIndex = 0
        self.house = house
        self.socialCareMap = []
        self.classRank = classRank
        self.temporaryClassRank = 0
        self.ageStartWorking = -1
        self.yearMarried = -1
        self.yearsSeparated = 0
        self.wage = wage
        self.hourlyWage = wage
        self.income = income
        self.wealth = 0
        self.netIncome = income
        self.disposableIncome = income

        self.workingTime = workingTime
        self.status = status
        self.socialCareReceiver = False
        self.independentStatus = False
        self.elderlyWithFamily = False
        self.yearIndependent = 0

        self.newTown = None

        self.yearsInTown = yit
        self.justMarried = None
        # Introducing care needs of babies
        if age < 1:
            self.careRequired = 80
        self.careAvailable = 0
        self.movedThisYear = False
        self.id = Person.counter
        Person.counter += 1
        

        
        
        
        
        