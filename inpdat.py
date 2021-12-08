# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 16:07:30 2021

@author: arthu
"""

import numpy as np

class inpdat:
    def __init__(self, datasys):
        teta_max = np.pi
        PB = 100  # Base Power (MW)
        CO2_TAX = 26  # Carbon tax [$/ton]
        
        #DBAR
        NB = datasys['DBAR'].shape[0]  # Number of buses
        BPD = np.where(datasys['DBAR'][:, 9] != 0)[0]  # Buses with demand
        ND = BPD.size  # Number of demand buses
        PD = datasys['DBAR'][:, 9]/PB  # Demand
        
        # DGER
        NG = datasys['DGER'].shape[0]  # Number of non-renewable generators
        PGmax = datasys['DGER'][:,2]/PB  # Non-renewable capacity
        BPG = datasys['DGER'][:,1]  # Buses with non-renewable generators
        CPG = PB*(datasys['DGER'][:,4]+CO2_TAX*datasys['DGER'][:,5])  # Operational cost of non-renewable generators [$/MWh] -> [$/puh]
        PGramp = datasys['DGER'][:,6]/100  # Non-renewable ramp-rate limits [#]
        PGtype = datasys['DGER'][:,7]  # type: 1 - gas | 2 - coal | 3 - wind | 4 - solar
        PGser = datasys['DGER'][:,8]  # type: 1 - gas | 2 - coal
        
        # DLIN
        NL = datasys['DLIN'].shape[0]
        SB = datasys['DLIN'][:,0]-1  # sending bus
        EB = datasys['DLIN'][:,1]-1  # ending bus
        EP0 = datasys['DLIN'][:,12]  # number of circuits in corridors
        X = datasys['DLIN'][:,3]/(EP0*100)  # reactance
        Bor = 1/X  # susceptance
        Fmax = datasys['DLIN'][:,9]*EP0/PB  # Circuit power flow capacity
        
        self.teta_max = teta_max
        self.PB = PB
        self.NB = NB
        #
        self.ND = ND
        self.PD = PD
        self.BPD = BPD
        #
        self.NG = NG
        self.BPG = BPG
        self.PGmax = PGmax
        self.CPG = CPG
        self.PGramp = PGramp
        self.PGtype = PGtype
        self.PGser = PGser
        #
        self.NL = NL
        self.SB = SB
        self.EB = EB
        self.EP0 = EP0
        self.Bor = Bor
        self.Fmax = Fmax
