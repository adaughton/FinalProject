import getpass
import re
import sys
import unittest

import django.test as dt
import ia_app

## This is to make sure the interface & all graphs work in the app

client = dt.Client()


class View_Tests(dt.TestCase):
   def test_root(self):
      response = self.client.get('/')
      self.assertEqual(response.status_code, 200)
      self.assertContains(response, 'show me an example!')
      self.assertNotContains(response, 'There is an error')
      graph_response = self.client.get('/?S0=10000&I0=1&days_low=5&days_high=7&r0_low=1.8&r0_high=2.5&lambd=0.1&control_start=5')
      self.assertEqual(graph_response.status_code, 200)
      self.assertContains(graph_response, 'SIR Simulated')
      self.assertNotContains(graph_response, 'There is an error')
      self.assertNotContains(graph_response, 'show me an example!')

   def test_contact(self):
      response = self.client.get('/contact/')
      self.assertEqual(response.status_code, 200)
      self.assertContains(response, 'adaughton@lanl.gov')
      self.assertNotContains(response, 'There is an error')
