import pylab as pl
import numpy as np
import scipy.integrate as si
import decimal as d
import math

# want one set of inputs for low and one set for high?
def get_input(s0, i0, r0, gamma, beta, lamb, control_start):
   if s0 is not None:
      try:
         s0+=0
      except TypeError:
         print('S0 must be an integer')
   if i0 is not None:
      try:
         i0+=0
      except TypeError:
         print('I0 must be an integer')
   if r0 is not None:
      try:
         r0+=0
      except TypeError:
         print('R0 must be an integer')
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
   if lamb is not None:
      try:
         lamb = float(str(lamb))
      except d.InvalidOpperation:
         print('Lambda is not a decimal')
   input_dict = {'s0': s0,
                'i0': i0,
                'r0': r0,
                'gamma':gamma,
                'beta':beta,
                'cs':control_start,
                'lamb':lamb,
                'pop': sum([s0,i0,r0])}
   return(input_dict)

### SIR Model:
# dSdt = - BSI/N
# dIdt = BSI/n - gI
# dRdt = gI
# B = beta
# g = gamma

## http://scipython.com/book/chapter-8-scipy/additional-examples/the-sir-epidemic-model/
def sir_deriv(y, t, N, beta, gamma):
   S, I, R = y
   dSdt = -beta * S * I/N
   dIdt = beta * S * I /N - gamma * I
   dRdt = gamma * I
   return dSdt, dIdt, dRdt


def sir_nocontrol(input_variables, end=100):
   # initialize
   s0 = input_variables['s0']
   i0 = input_variables['i0']
   r0 = input_variables['r0']
   N = input_variables['pop']
   beta = input_variables['beta']
   gamma = input_variables['gamma']
   init = s0, i0, r0
   # time points (days)
   t = np.linspace(0,end,end)
   # integrate over time
   sir = si.odeint(sir_deriv, init, t, args=(N, beta, gamma))
   return(sir.T)


# modify to include the control measure
def sir_cntl_deriv(y, t, N, beta, gamma, lamb, cs):
   if t < cs:
      S, I, R = y
      dSdt = -beta * S * I/N
      dIdt = beta * S * I /N - gamma * I
      dRdt = gamma * I
      return dSdt, dIdt, dRdt
   else:
      S, I, R = y
      dSdt = -beta * S * I/N - lamb * S
      dIdt = beta * S * I /N - gamma * I
      dRdt = gamma * I
      return dSdt, dIdt, dRdt



def sir_control(input_variables, end=100):
   # initialize
   s0 = input_variables['s0']
   i0 = input_variables['i0']
   r0 = input_variables['r0']
   N = input_variables['pop']
   beta = input_variables['beta']
   gamma = input_variables['gamma']
   cs = input_variables['cs']
   lamb = input_variables['lamb']
   init = s0, i0, r0
   # time points (days)
   t = np.linspace(0,end,end)
   # integrate over time
   sir = si.odeint(sir_cntl_deriv, init, t, args=(N, beta, gamma, lamb, cs))
   return(sir.T)

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


## Returns: Kappa (relative infected controlled: infected uncontrolled)
## Takes: Dictionary of values (from get_input)
def get_kappa(input_dict):
   I = input_dict['i0']
   sir_model = sir_nocontrol(input_dict)
   R = list(sir_model[2])
   R_end = max(R)
   SIR_cntl = sir_control(input_dict)
   R_ctl = list(SIR_cntl[2])
   R_ctl_end = max(R_ctl)
   # If the outbreak never happens, return 0
   if max(list(SIR_cntl[1])) <= 2 or max(list(sir_model[1]))<= 2:
      return(0)
   kappa = R_ctl_end/R_end
   kappa = min(kappa, 1)
   return(kappa)



