# -*- coding: utf-8 -*-

from docplex.mp.model import Model
import numpy as np
import pandas as pd
import os
import json

# Movendo para pasta corrente
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
from inpdat import inpdat


# Power balance rule
def rule_eq_power_bal(ibus):
    flow_out = []
    for ilin in set_L:
        if psys.SB[ilin] == ibus:
            flow_out.append(flow[ilin])
        elif psys.EB[ilin] == ibus:
            flow_out.append(-flow[ilin])
    return m.linear_constraint(lhs = pg[ibus]+pr[ibus]-m.sum(flow_out),
                               rhs = psys.PD[ibus],
                               ctsense = 'eq',
                               name = 'eq_power_bal')


# Power flow calc
def rule_eq_flow(ilin):
    i = psys.SB[ilin]
    j = psys.EB[ilin]
    return m.linear_constraint(lhs = flow[ilin]-psys.Bor[ilin]*(teta[i]-teta[j]),
                               rhs = 0,
                               ctsense = 'eq',
                               name = 'eq_flow')


# Escolhendo sistema
file = open(dir_path+'\\Casos\\data_3b.json')

# Lendo dados
datasys = json.load(file)
file.close
    
    
# Transformando dados em numpy.ndarray
for key in datasys:
    datasys[key] = np.array(datasys[key])

# Leitura do systema
psys = inpdat(datasys)

# Modelo do DOcplex
m = Model(name='OPF')

# Sets
set_B = np.array([ibus for ibus in range(psys.NB)])  # All buses
set_L = np.array([ilin for ilin in range(psys.NL)])  # All branches

# Variáveis
teta = m.continuous_var_dict(keys = set_B,
                             lb = -psys.teta_max,
                             ub = +psys.teta_max,
                             name = 'teta')

flow = m.continuous_var_dict(keys = set_L,
                            lb = -psys.Fmax,
                            ub = +psys.Fmax,
                            name = 'flow')

pg = m.continuous_var_dict(keys = set_B,
                           lb = 0,
                           ub = psys.PGmax,
                           name = 'pg')

pr = m.continuous_var_dict(keys = set_B,
                           lb = 0,
                           ub = psys.PD,
                           name = 'pr')

# Objetivo
m.minimize(m.sum([1000*pr[ibus] for ibus in set_B]))

# Creating constraints
eq_bal = [rule_eq_power_bal(ibus) for ibus in set_B]

eq_ref_teta = m.linear_constraint(lhs = teta[0],
                                  rhs = 0,
                                  ctsense = 'eq',
                                  name = 'eq_ref_teta')

eq_flow = [rule_eq_flow(ilin) for ilin in set_L]

# Adding constraints
m.add_constraints(eq_bal)
m.add_constraint(eq_ref_teta)
m.add_constraints(eq_flow)

# Solucionando model
s = m.solve()
# m.print_solution()


# Exibindo resultados
SBAR = {'NB': set_B+1,
        'pg': [pg[ibus].solution_value for ibus in set_B],
        'pr': [pr[ibus].solution_value for ibus in set_B],
        'teta': [teta[ibus].solution_value for ibus in set_B],
        'LM': [eq_bal[ibus].dual_value for ibus in set_B],
        }
print(pd.DataFrame(SBAR))

SLIN = {'NL': set_L+1,
        'de': [psys.SB[ilin]+1 for ilin in set_L],
        'para': [psys.EB[ilin]+1 for ilin in set_L],
        'flow': [flow[ilin].solution_value for ilin in set_L],
        }
print(pd.DataFrame(SLIN))
