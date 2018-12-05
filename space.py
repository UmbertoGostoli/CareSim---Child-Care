# -*- coding: utf-8 -*-
"""
Created on Thu Nov 02 15:01:53 2017

@author: ug4d
"""
import random
import numpy as np
import networkx as nx

class Map:
    """Contains a collection of towns to make up the whole country being simulated."""
    def __init__ (self, gridXDimension, gridYDimension, townGridDimension, 
                  cdfHouseClasses, ukMap, ukClassBias, densityModifier, rs):
        self.towns = []
        self.allHouses = []
        self.occupiedHouses = []
        
        random.seed(rs)
        np.random.seed(rs)
        ukMap = np.array(ukMap)
        ukMap.resize(int(gridYDimension), int(gridXDimension))
        ukClassBias = np.array(ukClassBias)
        ukClassBias.resize(int(gridYDimension), int(gridXDimension))
        for y in range(int(gridYDimension)):
            for x in range(int(gridXDimension)):
                newTown = Town(townGridDimension, x, y,
                               cdfHouseClasses, ukMap[y][x],
                               ukClassBias[y][x], densityModifier, rs)
                self.towns.append(newTown)

        for t in self.towns:
            for h in t.houses:
                self.allHouses.append(h)
                
class Town:
    counter = 1
    """Contains a collection of houses."""
    def __init__ (self, townGridDimension, tx, ty,
                  cdfHouseClasses, density, classBias, densityModifier, rs):
        
        random.seed(rs)
        np.random.seed(rs)
        
        self.id = Town.counter
        Town.counter += 1
        self.x = tx
        self.y = ty
        self.houses = []
        self.name = str(tx) + "-" + str(ty)
        if density > 0.0:
            adjustedDensity = density * densityModifier
            for hy in range(int(townGridDimension)):
                for hx in range(int(townGridDimension)):
                    if random.random() < adjustedDensity:
                        newHouse = House(self,cdfHouseClasses,
                                         classBias,hx,hy, rs)
                        self.houses.append(newHouse)
                        
class House:
    counter = 1
    """The house class stores information about a distinct house in the sim."""
    def __init__ (self, town, cdfHouseClasses, classBias, hx, hy, rs):
        
        random.seed(rs)
        np.random.seed(rs)
        r = random.random()
        
        i = 0
        c = cdfHouseClasses[i] - classBias
        while r > c:
            i += 1
            c = cdfHouseClasses[i] - classBias
        self.size = i
        
        self.careNetwork = nx.Graph()
        self.incomeBrackets = []
        self.childCareNeeds = []
        self.childCarePrices = []
        self.socialCareNeedsByPrice = []
        self.socialCarePrices = []
        self.totalSocialCareNeed = 0
        self.totalChildCareNeed = 0
        self.childCareNeedShare = 0
        self.informalChildCareReceived = 0
        self.formalChildCareReceived = 0
        self.informalSocialCareReceived = 0
        self.formalSocialCareReceived = 0
        self.residualChildCare = []
        self.residualSocialCare = 0
        self.careNeedIndex = 0
        self.networkSupply = 0
        self.householdInformalSupply = []
        
        self.householdFormalChildCareSupply = []
        self.householdFormalSocialCareSupply = []
        
        self.householdFormalSupplyCost = 0
        self.networkTotalSupplies = []
        self.networkInformalSupply = []
        self.residualIncomeForCare = []
        self.suppliers = []
        self.incomeByTaxBand = []
        self.availableIncomeByTaxBand = []
        
        self.initialOccupants = 0
        self.occupants = []
        self.town = town
        self.x = hx
        self.y = hy
        self.rank = None
        self.icon = None
        self.id = House.counter
        House.counter += 1
        self.name = self.town.name + "-" + str(hx) + "-" + str(hy)
        