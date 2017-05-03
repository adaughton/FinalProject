# This pulls data from the large matrix generated from running many SIR models
# and generates the information needed to produce contour plots

import pandas as pd
from ia_app.epi_models import sir as sm
import numpy as np


def get_contour_lambda(df, _lambda):
   data_list = []
   df = df[df['kappa']<= 0.1][df['lamb']<=_lambda]
   unique_gammas = df['gamma'].unique()
   unique_betas = df['beta'].unique()
   for g in unique_gammas:
      for b in unique_betas:
         sub = df[df['gamma']==g][df['beta']==b]
         data_list.append([b,g, sub['control_start'].max()])
   return(data_list)


## Returns:relative kappa (controlled:uncontrolled) for all gamma and beta
## Takes two outbreak dictionaries. Uses control measures in first dictionary
## Second dictionary is to get gamma and beta ranges
def kappa_heat_map(input_dict_low, input_dict_high):
   data_list = []
   unique_gammas = list(np.arange(input_dict_high['gamma'], input_dict_low['gamma'], -0.05))
   unique_betas = list(np.arange(input_dict_low['beta'], input_dict_high['beta'], 0.05))
   for g in unique_gammas:
      for b in unique_betas:
         S0 = input_dict_low['s0']
         I0 = input_dict_low['i0']
         R0 = input_dict_low['r0']
         t = input_dict_low['time']
         cs = input_dict_low['cs']
         _lambda = input_dict_low['lamb']
         input_dict = sm.get_input(S0, I0, R0, t, g, b, cs, _lambda)
         # commented out original get_kappa and renamed get_kappa2
         kappa = sm.get_kappa(input_dict)
         data_list.append([unique_gammas.index(g),
                           unique_betas.index(b),
                           round(kappa,2)])
   unique_days = [round(1/g,2) for g in unique_gammas]
   unique_betas_rounded = [round(b, 2) for b in unique_betas]
   return(data_list, unique_days, unique_betas_rounded)


# This needs to be what the min lambda is to get a kappa <= 0.1
# maybe just try by categories for now??
# lambda is 1-5% 5-10% 10-20% 20-30% 30-40%

def lambda_cutoffs(input_dict, unique_lambdas):
   for l in unique_lambdas:
      input_dict['lamb']=l
      if sm.get_kappa(input_dict) <= 0.1 and sm.get_kappa(input_dict) > 0:
         return l
   return 0

def get_contour_lambda2(input_dict_low, input_dict_high):
   data_list = []
   unique_gammas = list(np.arange(input_dict_high['gamma'], input_dict_low['gamma'], -0.05))
   unique_betas = list(np.arange(input_dict_low['beta'], input_dict_high['beta'], 0.05))
   unique_lambdas = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, .9]
   for g in unique_gammas:
      for b in unique_betas:
         S0 = input_dict_low['s0']
         I0 = input_dict_low['i0']
         R0 = input_dict_low['r0']
         t = input_dict_low['time']
         cs = input_dict_low['cs']
         input_dict = sm.get_input(S0, I0, R0, t, g, b, cs, None)
         try:
            l = lambda_cutoffs(input_dict, unique_lambdas)
            data_list.append([unique_gammas.index(g),
                              unique_betas.index(b),
                              l])
         except:
            data_list.append([unique_gammas.index(g),
                              unique_betas.index(b),
                              0])
   #unique_gammas_rounded = [round(g, 2) for g in unique_gammas]
   unique_days = [round(1/g,2) for g in unique_gammas]
   unique_betas_rounded = [round(b, 2) for b in unique_betas]
   return(data_list, unique_days, unique_betas_rounded)

def cs_cutoffs(input_dict, unique_cs):
   for c in unique_cs:
      input_dict['cs']=c
      if sm.get_kappa(input_dict) <= 0.1 and sm.get_kappa(input_dict) > 0:
         return c

# This needs to be what the min cs is to get a kappa <= 0.1
def get_control_start(input_dict_low, input_dict_high):
   data_list = []
   unique_gammas = list(np.arange(input_dict_high['gamma'], input_dict_low['gamma'], -0.05))
   unique_betas = list(np.arange(input_dict_low['beta'], input_dict_high['beta'], 0.05))
   unique_cs = list(np.arange(max(input_dict_high['cs'], input_dict_low['cs'])+14, 1, -1))
   #print(unique_cs)
   for g in unique_gammas:
      for b in unique_betas:
         S0 = input_dict_low['s0']
         I0 = input_dict_low['i0']
         R0 = input_dict_low['r0']
         t = input_dict_low['time']
         _lambda = input_dict_low['lamb']
         #cs = input_dict_low['cs']
         input_dict = sm.get_input(S0, I0, R0, t, g, b, 100, _lambda)
         try:
            c = cs_cutoffs(input_dict, unique_cs)
            data_list.append([unique_gammas.index(g),
                              unique_betas.index(b),
                              c])
         except:
            data_list.append([unique_gammas.index(g),
                              unique_betas.index(b),
                              None])
   unique_days = [round(1/g,2) for g in unique_gammas]
   unique_betas_rounded = [round(b, 2) for b in unique_betas]
   return(data_list, unique_days, unique_betas_rounded)

