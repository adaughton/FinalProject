from unittest import TestCase

import sir as sm

# first lets test each function and just make sure it returns what we expect
class test_sir_models(TestCase):
   def test_get_input(self):
      input = sm.get_input(10, 1, 0, 0, 0.5, 0.5, 2, 0.5)
      test_dict = {'I0': 1,
                   'time': 0,
                   'lambda': 0.5,
                   'gamma': 0.5,
                   'cs': 2,
                   'pop': 11,
                   'S0': 10,
                   'R0': 0,
                   'beta': 0.5}
      self.assertDictEqual(input, test_dict)
   def test_add_timestep(self):
      test_list = [1, 2, 3]
      add = 4
      test_list.append(add)
      test_add_timestep_list = sm.add_timestep(add, [1,2,3])
      self.assertEqual(test_list, test_add_timestep_list)
   def test_get_kappa(self):
      # if lambda = 0 then no one should be saved
      test_dict = {'I0': 1,
                   'time': 0,
                   'lambda': 0,
                   'gamma': 0.5,
                   'cs': 1,
                   'pop': 100001,
                   'S0': 100000,
                   'R0': 0,
                   'beta': 0.8}
      kappa = sm.get_kappa(test_dict)
      # have to include int around kappa b/c of rounding stuff
      self.assertEqual(int(kappa), 1)
   def test_SIR(self):
      # At the end of the outbreak the num recovered == sum(infected)
      test_dict = {'I0': 1,
                   'time': 0,
                   'lambda': 0,
                   'gamma': 0.5,
                   'cs': 10,
                   'pop': 100001,
                   'S0': 100000,
                   'R0': 0,
                   'beta': 0.8}
      sir = sm.sir_nocontrol(test_dict)
      # sum S + I + R at each time point should equal the population num
      for s in range(0, len(sir[1])-1):
         sum_sir = sir[0][s]+sir[1][s]+sir[2][s]
         self.assertEqual(round(sum_sir, 1), test_dict['pop'])
      # sum of newly infected at end should equal num recovered at end
      newly_infected = sm.newly_infected(sir)
      sum_infected = sum(newly_infected)
      num_recovered = sir[2][len(sir[2])-1]
      self.assertEqual(round(sum_infected, 0), round(num_recovered,0))
   def test_SIRcntl(self):
      # At the end of the outbreak the num recovered == sum(infectd)
      test_dict = {'I0': 1,
                   'time': 0,
                   'lambda': 0,
                   'gamma': 0.5,
                   'cs': 10,
                   'pop': 100001,
                   'S0': 100000,
                   'R0': 0,
                   'beta': 0.8}
      # sum of newly infected at end should equal num recovered at end
      sir_withcntl = sm.sir_control(test_dict)
      newly_infected = sm.newly_infected(sir_withcntl)
      sum_infected = sum(newly_infected)
      num_recovered = sir_withcntl[2][len(sir_withcntl[2])-1]
      self.assertEqual(round(sum_infected, 0), round(num_recovered,0))

if __name__ == '__main__':
    unittest.main()


# next, we'll test the SIR with and without control in various scenarios
# where we know what the output ought to be

# test SIR_with control, time<1

# test SIR_with control, control eff = 0
# test SIR_with control controll eff = 1, cs = 1
# test SIR_with control controll eff = 1, cs > end
# test get kapp with some of the above combos

## how to test peak intensity?!
