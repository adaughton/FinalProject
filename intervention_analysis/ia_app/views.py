from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from palettable.colorbrewer.diverging import BrBG_6 as bg6
import matplotlib as mpl
import numpy as np
import json
import pandas as pd

from ia_app.forms import forms as f
from ia_app.epi_models import sir as sm
from ia_app.epi_models import sir_contour_plots as sc
# helper functions to make view more readable


# Create your views here.
# TODO: break into multiple functions so logic not so concentrated
# TODO check minimum amount of info
def index(req):
   sir_series = []
   kappa_series = []
   lambda_series = []
   ia_series = []
   pcp_series = []
   form = f.SIR_Model_Form(req.GET)
   message = 'Put in some data'
   S0=None
   I0 = None
   g_low = None
   b_low = None
   cs = None
   _lambda=None
   # see what data is in the url
   # modify from days to gamma and R0 to beta
   if req.method == 'GET':
      if form.is_valid():
         S0 = form.cleaned_data['S0']
         I0 = form.cleaned_data['I0']
         g_high = 1/int(form.cleaned_data['days_low'])
         g_low = 1/int(form.cleaned_data['days_high'])
         _lambda = form.cleaned_data['lamb']
         cs = form.cleaned_data['control_start']
         r0_low = float(form.cleaned_data['r0_low'])
         r0_high = float(form.cleaned_data['r0_high'])
         if g_low and r0_low:
            b_low = r0_low * g_low
         if g_high and r0_high:
            b_high = r0_high * g_high
   # if S0 and I0 and g_low and b_low, we want to run SIR models and
   # include in first graph
   if S0 and I0 and g_low and b_low:
      message = ()
      chartID = 'sir_line'
      chart_height = 375
      background_color = '#F8F7F8'
      sir_chart = {"renderTo": chartID,
                   "type": "line",
                   "height": chart_height,
                   "backgroundColor": background_color,
                   "borderWidth": 0}
      sir_title = {"text": 'Outbreak curves (SIR model)'}
      sir_xAxis = {"title":
                     {"text": 'Time steps into outbreak (e.g., Days)'}}
      sir_yAxis = {"title": {"text": 'Cases'}}
      input_dictionary_low = sm.get_input(S0, I0, 0, g_low, b_low, 0, 100)
      sir_low = list(sm.sir_nocontrol(input_dictionary_low)[1])
      # round to 2 decimal places
      sir_low = [round(s, 2) for s in sir_low]
      sir_series.append({"name": 'Low estimate',
                         "data": sir_low,
                         "color": '#955b92',
                       })

   if S0 and I0 and g_high and b_high:
      input_dictionary_high = sm.get_input(S0, I0, 0, g_high, b_high, 0, 100)
      sir_high = list(sm.sir_nocontrol(input_dictionary_high)[1])
      # round to 2 decimal places
      sir_high = [round(s, 2) for s in sir_high]
      sir_series.append({"name": 'High estimate',
                        "data": sir_high,
                        "color": '#F7B745',
                      })

   # if we have all the fields and control info, add to sir graph
   if cs and _lambda and S0 and I0 and g_high and b_high and g_low and b_low:
      # add a horizontal line in red where the control starts
      the_max = max(sir_series[1]['data'])
      sir_series.append({"name": "Control start",
                         "data": [[cs,0], [cs,the_max+100]],
                         "color":"#A19891",
                         "dashStyle":"dot",
                        })
      # add modified SIR lines to the graph
      control_low = sm.get_input(S0, I0, 0, g_low, b_low, _lambda, cs)
      sir_controlled_low = list(sm.sir_control(control_low)[1])
      sir_controlled_low = [round(s, 2) for s in sir_controlled_low]
      sir_series.append({"name": 'Low estimate (with control)',
                        "data": sir_controlled_low,
                        "dashStyle": 'dot',
                        "color": '#955b92',
                       })
      control_high = sm.get_input(S0, I0, 0, g_high, b_high, _lambda, cs)
      sir_controlled_high = list(sm.sir_control(control_high)[1])
      sir_controlled_high = [round(s, 2) for s in sir_controlled_high]
      sir_series.append({"name": 'High estimate (with control)',
                        "data": sir_controlled_high,
                        "dashStyle": 'dot',
                        "color": '#F7B745',
                      })
      # if all data, also generate the parallel coordinates plot
      # empty lists for parallel coordinates plot
      pcp_series_g = []
      pcp_series_r0 = []
      pcp_series_l = []
      pcp_series_cs = []
      pcp_series_k = []
      contour_x = []
      contour_y = []
      contour_z = []
      # get ranges of parameters
      g_range = np.arange(g_low, g_high, 0.1)
      b_range = np.arange(b_low, b_high, 0.1)
      ## modify the cs and effectiveness slightly in both directions
      cs_low = max(cs-4, 2)
      cs_high = cs+7
      lambda_low = round(max(_lambda-0.1, 0.001), 2)
      lambda_high = round(_lambda+0.3, 2)
      cs_range = np.arange(cs_low, cs_high, 1)
      l_range = np.arange(lambda_low, lambda_high, 0.05)
      for g in g_range:
         for b in b_range:
            contour_x.append(round(1/g, 2))
            contour_y.append(round(b/g, 2))
            input = sm.get_input(S0,I0, 0, g,b,_lambda, cs)
            contour_z.append(round(sm.get_kappa(input),2))
            for c in cs_range:
               for l in l_range:
                  input = sm.get_input(S0,I0, 0, g,b,l,c)
                  k = sm.get_kappa(input)
                  pcp_series_g.append(round(1/g, 2))
                  pcp_series_cs.append(round(c, 2))
                  pcp_series_l.append(round(l, 2))
                  pcp_series_k.append(round(k, 3))
                  pcp_series_r0.append(round(b/g,2))
   return render(req, 'index.html', locals())


def contact(req):
   return render(req, 'contact.html')

def help(req):
   return render(req, 'Explanation.html')
