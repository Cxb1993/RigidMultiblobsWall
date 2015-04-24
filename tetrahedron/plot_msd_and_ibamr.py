''' 
Script to compare free tetrahedron translational MSD to 
that generated by using IBAMR with stiff springs.
'''

import cPickle
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
import os
import sys
sys.path.append('..')

import tetrahedron_free as tf
from translational_diffusion_coefficient import calculate_average_mu_parallel_and_perpendicular
from utils import MSDStatistics
from utils import plot_time_dependent_msd


# IBAMR data taken from Floren's .agr file
IBAMR_TIME = np.arange(0., 1200., 20.)

IBAMR_PARALLEL = np.array(
  [0.0, 0.31387986, 0.61932061, 0.92558214, 1.2323787, 1.5363076, 1.8333141, 2.1351591, 2.4306246, 2.7233928, 3.0128003, 3.2984048, 3.5817992, 3.8758074, 4.1740698, 4.4770331, 4.7824102, 5.0884229, 5.395501, 5.707325, 6.0191544, 6.3245403, 6.618314, 6.9127493, 7.2072074, 7.5064569, 7.8064613, 8.1082906, 8.4080401, 8.7100983, 9.0083495, 9.3011976, 9.5928211, 9.8756846, 10.156134, 10.438258, 10.726745, 11.020214, 11.308653, 11.592833, 11.870325, 12.137984, 12.39645, 12.648749, 12.89393, 13.137412, 13.378526, 13.618359, 13.859778, 14.107134, 14.36192, 14.621232, 14.887143, 15.155475, 15.421278, 15.689851, 15.958944, 16.226829, 16.489455, 16.748454])

# OLD DATA, COM
  # [0., 0.23030084, 0.46050293, 0.69003878,
  #  0.91991073, 1.1500172, 1.3800153, 1.6088495, 1.8364486,
  #  2.0640567, 2.2921163, 2.5206239, 2.7501723, 2.979825,
  #  3.2094257, 3.4390972, 3.6691305, 3.9003276, 4.1311499,  
  #  4.3611359])

IBAMR_PARALLEL_STD = np.array(
  [0., 0.007922184, 0.021165123, 0.039936091, 0.064833262, 0.092595274, 0.12291567, 0.154386, 0.18920445, 0.22750933, 0.26745547, 0.31255077, 0.36059012, 0.40946914, 0.45795286, 0.50661798, 0.55427674, 0.60257379, 0.65161055, 0.70169291, 0.75130049, 0.80377758, 0.85593371, 0.90988944, 0.96580046, 1.0197725, 1.0727919, 1.1274379, 1.1822783, 1.2339925, 1.2856881, 1.3394988, 1.3924697, 1.4430575, 1.4952869, 1.5482621, 1.6030242, 1.659566, 1.7163531, 1.7740243, 1.8320686, 1.8919511, 1.9548058, 2.0191084, 2.084018, 2.1498994, 2.2172136, 2.2854789, 2.3569592, 2.4299621, 2.5022892, 2.5756872, 2.6488403, 2.7237399, 2.7984008, 2.8715145, 2.9449472, 3.0205673, 3.0979506, 3.1746681])


  # OLD STD DEV, COM
  # [0., 0.001477575, 0.003386016, 0.006319060, 0.010594295, 0.015719995,
  #  0.022184539, 0.029280662, 0.037885666, 0.045756387, 0.053230181,
  #  0.060988031, 0.068676815, 0.077319251, 0.086739617, 0.096781223,
  #  0.10675642, 0.11709404, 0.12807461, 0.1388481])


IBAMR_PERP = np.array(
  [0., 0.2022592, 0.35871055, 0.49051806, 0.60639776, 0.70471013, 0.78958025, 0.86181461, 0.92644596, 0.97793565, 1.0227378, 1.0591931, 1.0922352, 1.1201694, 1.1466463, 1.1685141, 1.192555, 1.2141156, 1.2331648, 1.2530412, 1.2692351, 1.2904508, 1.3033252, 1.3084962, 1.3140598, 1.3181057, 1.325151, 1.3341507, 1.346556, 1.3632568, 1.3750952, 1.3877728, 1.3975885, 1.4093132, 1.4247537, 1.4420902, 1.4547237, 1.4712008, 1.4907958, 1.5030571, 1.5229727, 1.53799, 1.5502683, 1.5630861, 1.5748583, 1.5823976, 1.5871277, 1.5879492, 1.5929505, 1.6048788, 1.6196219, 1.6291006, 1.6295151, 1.629291, 1.6235891, 1.6214796, 1.6216434, 1.6166553, 1.6148601, 1.6126036])


# OLD IBAMR PERP, COM
  # [0., 0.15078125, 0.27641909, 0.38550696, 0.481194, 0.56581186, 
  #  0.64170116, 0.71043655, 0.77321308, 0.82912696, 0.88002487, 
  #  0.92730235, 0.97134252, 1.0123946, 1.0509769, 1.0867704, 
  #  1.1207078, 1.152183, 1.1801148, 1.2056205])


IBAMR_PERP_STD = np.array(
  [0., 0.0068622868, 0.017801266, 0.029084112, 0.041471853, 0.055735769, 0.071051029, 0.085061356, 0.096595325, 0.10711713, 0.11802163, 0.12959921, 0.14070727, 0.15128752, 0.16139152, 0.17099472, 0.18145212, 0.19123962, 0.20157935, 0.2120522, 0.22115233, 0.22883895, 0.2359286, 0.24413393, 0.25111609, 0.25744989, 0.26274637, 0.26955845, 0.27741448, 0.28651548, 0.29518805, 0.30371155, 0.31466824, 0.32669779, 0.33751316, 0.34699114, 0.35731289, 0.36621035, 0.37641652, 0.38559788, 0.39519421, 0.40708557, 0.4181306, 0.42996755, 0.43911255, 0.4451679, 0.45145334, 0.45956998, 0.4708407, 0.48195419, 0.49472112, 0.50834703, 0.52071405, 0.53272826, 0.5441094, 0.55369583, 0.56347026, 0.57399728, 0.58701458, 0.60129831])

   # OLD PERP STD, COM.
  # [0., 0.001645053, 0.003407508, 0.005898420, 0.009283213, 0.013286326, 
  #  0.017028906, 0.020202788, 0.023350492, 0.026647023, 0.030101367, 
  #  0.033308575, 0.036714922, 0.039723968, 0.043054832, 0.046361506, 
  #  0.049286502, 0.052712193, 0.055929978, 0.059303183])

IBAMR_ROT_TIME = np.arange(0., 600., 8.)

IBAMR_ROT = np.array([0., 0.064968634, 0.11242956, 0.14855103, 0.17608518, 0.1967525, 0.21174524, 0.22252755, 0.23028701, 0.23453516, 0.23664138, 0.23733369, 0.23698804, 0.23598845, 0.2340496, 0.23191143, 0.22961686, 0.2271307, 0.22447612, 0.22145438, 0.21835336, 0.21523291, 0.21199147, 0.20903391, 0.20661029, 0.20482289, 0.20307446, 0.20127967, 0.19930859, 0.19696935, 0.19457457, 0.19251087, 0.19064572, 0.18897675, 0.18757275, 0.18652663, 0.18572594, 0.18499797, 0.18398326, 0.18271197, 0.18117685, 0.17990317, 0.17845548, 0.1768307, 0.17573837, 0.175209, 0.17471226, 0.17442775, 0.17426407, 0.17417899, 0.17396842, 0.17382137, 0.17373203, 0.17369497, 0.17393277, 0.17435629, 0.17459901, 0.17468773, 0.17457733, 0.17438013, 0.17406574, 0.17393546, 0.17381298, 0.17360129, 0.1731181, 0.1733729, 0.17363977, 0.17359317, 0.17305367, 0.17247337, 0.17188284, 0.17091212, 0.17004631, 0.16946134, 0.16908142])

IBAMR_ROT_STD = np.array([0., 0.00098840642, 0.0022415845, 0.0035705491, 0.0048107123, 0.005733684, 0.0065484562, 0.0073007529, 0.0078438709, 0.0085108099, 0.0089435596, 0.0092730393, 0.0093895957, 0.0093410608, 0.0092802161, 0.0092224487, 0.0091750132, 0.0090571134, 0.0088133663, 0.0086274333, 0.0084979276, 0.0085789065, 0.0087117416, 0.0088859529, 0.0090406066, 0.0091430137, 0.0091994095, 0.0090917761, 0.0089132271, 0.0087698068, 0.0085996897, 0.0085290295, 0.0083130971, 0.0079654469, 0.0076403542, 0.0075915472, 0.0075940918, 0.0077160098, 0.0079151115, 0.0080255885, 0.0081788753, 0.0081757167, 0.0081921602, 0.0080805169, 0.0079616324, 0.0079199344, 0.0079759865, 0.0082457133, 0.0084580943, 0.0085318877, 0.0085390706, 0.0086251133, 0.0086731951, 0.0085887348, 0.0085719202, 0.0087118781, 0.0087793578, 0.0086298678, 0.0084474905, 0.008217252, 0.0079486356, 0.0077753114, 0.0076376896, 0.0076584045, 0.0077514998, 0.0079849516, 0.0083105032, 0.0088572279, 0.009424059, 0.0098512161, 0.010285253, 0.010551646, 0.01069163, 0.010796125, 0.010757463])




if __name__ == '__main__':

  print "length of time", len(IBAMR_ROT_TIME)
  print "length of data", len(IBAMR_ROT)
  print "length of std", len(IBAMR_ROT_STD)

  rfd_data_name = ('tetrahedron-msd-dt-1.6-N-300000-end-1000.0-scheme-RFD-runs-4-final-geom-center.pkl')
  fixman_data_name = ('tetrahedron-msd-dt-1.6-N-300000-end-1000.0-scheme-FIXMAN-runs-4-final-geom-center.pkl')

  rfd_data_file = os.path.join('.', 'data', 
                               rfd_data_name)
  
  with open(rfd_data_file, 'rb') as f:
    rfd_msd_statistics = cPickle.load(f)
    rfd_msd_statistics.print_params()

  # Combine 0,0 and 1,1 into msd_parallel
  for scheme in rfd_msd_statistics.data:
    for dt in rfd_msd_statistics.data[scheme]:
      num_obs = len(rfd_msd_statistics.data[scheme][dt][1])
      rfd_msd_statistics.data[scheme][dt][0] = (
        rfd_msd_statistics.data[scheme][dt][0][0:num_obs])
      for k in range(len(rfd_msd_statistics.data[scheme][dt][1])):
        rfd_msd_statistics.data[scheme][dt][1][k][0][0] = (
          rfd_msd_statistics.data[scheme][dt][1][k][0][0] +
          rfd_msd_statistics.data[scheme][dt][1][k][1][1])
        rfd_msd_statistics.data[scheme][dt][2][k][0][0] = np.sqrt(
          rfd_msd_statistics.data[scheme][dt][2][k][0][0]**2 +
          rfd_msd_statistics.data[scheme][dt][2][k][1][1]**2)


  fixman_data_file = os.path.join('.', 'data', 
                                  fixman_data_name)
  
  with open(fixman_data_file, 'rb') as f:
    fixman_msd_statistics = cPickle.load(f)
    fixman_msd_statistics.print_params()

  # Combine 0,0 and 1,1 into msd_parallel
  for scheme in fixman_msd_statistics.data:
    for dt in fixman_msd_statistics.data[scheme]:
      num_obs = len(fixman_msd_statistics.data[scheme][dt][1])
      fixman_msd_statistics.data[scheme][dt][0] = (
        fixman_msd_statistics.data[scheme][dt][0][0:num_obs])
      for k in range(len(fixman_msd_statistics.data[scheme][dt][1])):
        fixman_msd_statistics.data[scheme][dt][1][k][0][0] = (
          fixman_msd_statistics.data[scheme][dt][1][k][0][0] +
          fixman_msd_statistics.data[scheme][dt][1][k][1][1])
        fixman_msd_statistics.data[scheme][dt][2][k][0][0] = np.sqrt(
          fixman_msd_statistics.data[scheme][dt][2][k][0][0]**2 +
          fixman_msd_statistics.data[scheme][dt][2][k][1][1]**2)


  average_mob_and_friction = calculate_average_mu_parallel_and_perpendicular(500)
  mu_parallel_com =  average_mob_and_friction[0] # 0.0711/2.

  # PRE COMPUTED VALUES:
  # These use parameters:
  # ETA = 1.0   # Fluid viscosity.
  # A = 0.5     # Particle Radius.
  # H = 3.5     # Initial Distance to wall.
  # KT = 0.2    # Temperature
  # M4 = 0.005*4.
  # M1 = 0.015*4.
  # M2 = 0.01*4.
  # M3 = 0.03*4.
  # REPULSION_STRENGTH = 2.0
  # DEBYE_LENGTH = 0.25 

  mu_perp_com = 0.0263
  zz_msd_com = 1.633
  rot_msd_com = 0.167
    
  mu_parallel_center = 0.0711/2.
  mu_perp_center = 0.0263
  zz_msd_center = 1.52
  rot_msd_center = 0.169

  mu_parallel_vertex = 0.117/2.
  mu_perp_vertex = 0.0487
  zz_msd_vertex = 2.517
  rot_msd_vertex = 0.167956760304

  figure_numbers = [1, 5, 1, 2, 3, 4]
  labels= [' parallel MSD', ' yy-MSD', ' perpendicular MSD', ' rotational MSD', ' rotational MSD', ' rotational MSD']
  styles = ['o', '^', 's', 'o', '.', '.']
  translation_end = 1000.
  fib_skip = 2
  fib_end = 28

  
  print "mu_parallel: ", mu_parallel_center
  print "msd_rot", rot_msd_center
  print "zz_msd", zz_msd_center
  

  for l in range(6):
    ind = [l, l]
    plot_time_dependent_msd(rfd_msd_statistics, ind, figure_numbers[l],
                            error_indices=[0, 2, 3], label=labels[l], symbol=styles[l],
                            num_err_bars=40)
    plot_time_dependent_msd(fixman_msd_statistics, ind, figure_numbers[l],
                            error_indices=[0, 2, 3], label=labels[l], symbol=styles[l],
                            num_err_bars=40, data_name='FixmanMSDComponent-%s.txt' % l)
    plt.figure(figure_numbers[l])
    if l in [0]:

      plt.errorbar(IBAMR_TIME[:fib_end:fib_skip], 
                   2.*IBAMR_PARALLEL[:fib_end:fib_skip], 
                   yerr = 2.*IBAMR_PARALLEL_STD[:fib_end:fib_skip],
                   c='red', marker='o', linestyle='--', label='FIB parallel')
      plt.plot([0.0, translation_end], 
               [0.0, translation_end*4.*tf.KT*mu_parallel_com], 'k-',
               lw=2, label=r'parallel theory')
    elif l == 2:
      plt.errorbar(IBAMR_TIME[:fib_end:fib_skip], 
                   IBAMR_PERP[:fib_end:fib_skip], 
                   yerr = IBAMR_PERP_STD[:fib_end:fib_skip],
                   c='red', marker='s', linestyle='--', label='FIB perpendicular')
      if translation_end > 200.:
        plt.plot([0.0, translation_end],
                 [zz_msd_center, zz_msd_center], 'k--',
                 lw=2, label='asymptotic perpendicular theory')
      plt.xlim([0., translation_end])
      plt.ylim([0., translation_end*4.*tf.KT*mu_parallel_com])

    if l == 3:
      plt.errorbar(IBAMR_ROT_TIME[0::3], IBAMR_ROT[0::3], yerr=IBAMR_ROT_STD[0::3], 
                   c='red', marker='s', label='FIB rotation')
      plt.plot([0.0, 550.],
                  [rot_msd_com, rot_msd_com], 'k--', lw=2, 
                  label='asymptotic rotational MSD')
      plt.xlim([0., 550.])

    plt.title('MSD(t) for Tetrahedron')
    plt.legend(loc='best', prop={'size': 11})
    plt.savefig('./figures/TimeDependentRotationalMSD-Component-%s-%s.pdf' % 
                   (l, l))
