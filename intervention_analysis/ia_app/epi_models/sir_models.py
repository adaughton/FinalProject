#import mathplotlib
import pylab as pl
import numpy as np
import decimal as d
import math

## Returns: dictionary of inputs for other functions
## Takes: values to run model
# S0 = susceptible at t=0
# I0 = infected at t=0
# R0 = recovered at t=0
# t = time, currently always set to 0. Maybe remove?
# gamma = 1/ infectious period (days)
# beta = gamma * R_0
# control_start = when control measure starts
# _lambda = control effectiveness
def get_input(S0, I0, R0, t, gamma, beta, control_start, _lambda):
   if S0 is not None:
      try:
         S0+=0
      except TypeError:
         print('S0 must be an integer')
   if I0 is not None:
      try:
         I0+=0
      except TypeError:
         print('I0 must be an integer')
   if R0 is not None:
      try:
         R0+=0
      except TypeError:
         print('R0 must be an integer')
   if t is not None:
      try:
         t+=0
      except TypeError:
         print('t must be an integer')
   if control_start is not None:
      try:
         control_start+=0
      except TypeError:
         print('control_start must be an integer')
   if gamma is not None:
      try:
         # strs added to stop many decimal places being added beyond
         # what user puts in
         gamma = float(str(gamma))
      except d.InvalidOpperation:
         print('Gamma is not a decimal')
   if beta is not None:
      try:
         beta = float(str(beta))
      except d.InvalidOpperation:
         print('Beta is not a decimal')
   if _lambda is not None:
      try:
         _lambda = float(str(_lambda))
      except d.InvalidOpperation:
         print('Lambda is not a decimal')
   input_dict = {'S0': S0,
                'I0': I0,
                'R0': R0,
                'time': t,
                'gamma':gamma,
                'beta':beta,
                'cs':control_start,
                'lambda':_lambda,
                'pop': sum([S0,I0,R0])}
   return(input_dict)

## Returns: new list with value added to it
## Takes: number, current list
def add_timestep(num, list):
   list.append(num)
   return(list)

## Returns :Number of new infections at each time point
## Important bc I(t) does not describe new infections (shows prevalence)
## Takes: Output from SIR or SIR_withcnlt
def newly_infected(sir_series):
   susceptible_series = sir_series[0]
   infected_series = sir_series[1]
   newly_infected = []
   for i in range(0, len(infected_series)-1):
      if i == 0:
         newly_infected.append(infected_series[0])
      else:
         new_infections = susceptible_series[i-1] - susceptible_series[i]
         if new_infections > 0:
            newly_infected.append(new_infections)
         else:
            newly_infected.append(0)
   return(newly_infected)

## Returns: Susceptible, infected, recovered and time at the end
## Takes: Dictionary of values (from get_input) and an option end (for control)

# Note to self: arbitrarily default end to 100 days (after 100 days)
# for now, 1/3 year should be fine b/c we focus on acute infectious dis.
def SIR(input_dict, end=100):
   S = input_dict['S0']
   I = input_dict['I0']
   R = input_dict['R0']
   S_list = add_timestep(S, [])
   I_list = add_timestep(I, [])
   R_list = add_timestep(R, [])
   time = 0
   beta = input_dict['beta']
   gamma = input_dict['gamma']
   pop = input_dict['pop']
   while time <= end:
      dS = - beta*S*I/pop
      # if R0 is large, can result in no S, but still I to R
      # so, we add this:
      if S + dS < 0:
         S = 0
      else:
         S = S + dS
      dI = beta*S*I/pop - gamma*I
      dR = gamma*I
      I = I + dI
      R = R + dR
      S_list = add_timestep(S, S_list)
      I_list = add_timestep(I, I_list)
      R_list = add_timestep(R, R_list)
      time = time +1
   return(S_list, I_list, R_list, end)

## Returns: Susceptible, infected, recovered and time at the end of controlled
## Takes: Dictionary of values (from get_input)
def SIR_withcntl(input_dict):
   c = input_dict['cs']
   beta = input_dict['beta']
   gamma = input_dict['gamma']
   pop = input_dict['pop']
   _lambda = input_dict['lambda']
   sir_before_control = SIR(input_dict, c)
   S = sir_before_control[0][len(sir_before_control[0])-1]
   I = sir_before_control[1][len(sir_before_control[1])-1]
   R = sir_before_control[2][len(sir_before_control[2])-1]
   time = sir_before_control[3]
   S_list = sir_before_control[0]
   I_list = sir_before_control[1]
   R_list = sir_before_control[2]
   while time <= 100:
      # Because we remove people from the susceptible population
      # the num. in the potential outbreak changes
      pop = S + I + R
      dS = - beta*S*I/pop - _lambda * S
      if S + dS < 0:
         S = 0
      else:
         S = S + dS
      dI = beta*S*I/pop - gamma*I
      dR = gamma*I
      I = I + dI
      R = R + dR
      S_list = add_timestep(S, S_list)
      I_list = add_timestep(I, I_list)
      R_list = add_timestep(R, R_list)
      time = time + 1
   return(S_list, I_list, R_list, time)

## Returns: Kappa (relative infected controlled: infected uncontrolled)
## Takes: Dictionary of values (from get_input)
def get_kappa(input_dict):
   I = input_dict['I0']
   sir_model = SIR(input_dict)
   R = sir_model[2]
   # Remove inf and nan
   R_c = [x for x
          in R
          if str(x)!='nan' and str(x)!='-inf' and str(x) !='inf']
   R_end = R_c[len(R_c)-1]
   SIR_cntl = SIR_withcntl(input_dict)
   R_ctl = SIR_cntl[2]
   # If the outbreak never happens, return 0
   if max(SIR_cntl[1]) <= 2 or max(sir_model[1])<= 2:
      return(0)
   # Remove inf and nan
   R_c_cln = [x for x
              in R_ctl
              if str(x)!='nan' and str(x)!='-inf' and str(x)!='inf']
   R_c_end = R_c_cln[len(R_c_cln)-1]
   kappa = R_c_end/R_end
   # This happens occasionally and is caused by weird rounding in tiny obs
   # Perhaps a thing to investigate further
   if kappa > 1:
      kappa = 1
   return(kappa)

## Returns: peak intensity (see Dave's thesis info)
## Takes: Dictionary of values (from get_input)
def peak_intensity(input_dict):
   rho = input_dict['gamma']/input_dict['beta']
   I0 = input_dict['I0']/input_dict['pop']
   S0 = input_dict['S0']/input_dict['pop']
   peak_intensity = I0 + S0 - rho * (math.log(S0)+1 - math.log(rho))
   return(peak_intensity)