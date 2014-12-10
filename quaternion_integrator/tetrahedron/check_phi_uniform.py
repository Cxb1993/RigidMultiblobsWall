''' 
Script to check that phi, the angle of rotation around the vertical axis, 
is uniformly distributed as it should be.
'''

import sys
import numpy as np
import math
from matplotlib import pyplot

import tetrahedron as tdn
from quaternion_integrator import QuaternionIntegrator
from quaternion import Quaternion

def bin_phi(orientation, bin_width, phi_hist):
  ''' Bin the angle phi given an orientation. '''
  phi = np.arcsin(orientation.p[2])
  idx = int(math.floor((phi + np.pi)/bin_width))
  phi_hist[idx] += 1

def plot_phis(phi_list, names, buckets):
  ''' 
  Plot phi distributions from a list of histograms. Each entry
  in the phi_list corresponds to one scheme.  The order of the entries
  should correspond to the order of names, a list of strings to label
  each scheme in the plot.
  '''
  for k in range(len(phi_list)):
    pyplot.plot(buckets, phi_list[k], label = names[k])

  pyplot.legend(loc='best', prop={'size': 9})
  pyplot.savefig('./plots/PhiDistribution.pdf')
    
    
  


  
if __name__ == "__main__":
  # Script to run the various integrators on the quaternion.
  initial_orientation = [Quaternion([1., 0., 0., 0.])]
  fixman_integrator = QuaternionIntegrator(tdn.tetrahedron_mobility,
                                           initial_orientation, 
                                           tdn.gravity_torque_calculator)
  rfd_integrator = QuaternionIntegrator(tdn.tetrahedron_mobility, 
                                        initial_orientation, 
                                        tdn.gravity_torque_calculator)
  em_integrator = QuaternionIntegrator(tdn.tetrahedron_mobility, 
                                       initial_orientation, 
                                       tdn.gravity_torque_calculator)
  # Get command line parameters
  dt = float(sys.argv[1])
  n_steps = int(sys.argv[2])
  print_increment = max(int(n_steps/10.), 1)

  bin_width = 1./5.
  fixman_phi = np.zeros(int(2.*np.pi/bin_width))
  rfd_phi = np.zeros(int(2.*np.pi/bin_width))
  em_phi = np.zeros(int(2.*np.pi/bin_width))

  for k in range(n_steps):
    # Fixman step and bin result.
    fixman_integrator.fixman_time_step(dt)
    bin_phi(fixman_integrator.orientation[0], 
            bin_width, 
            fixman_phi)
    # RFD step and bin result.
    rfd_integrator.rfd_time_step(dt)
    bin_phi(rfd_integrator.orientation[0],
            bin_width, 
            rfd_phi)    
    # EM step and bin result.
    em_integrator.additive_em_time_step(dt)
    bin_phi(em_integrator.orientation[0],
            bin_width, 
            em_phi)

    if k % print_increment == 0:
      print "At step:", k

  names = ['Fixman', 'RFD', 'EM']
  buckets  = np.linspace(-1.*np.pi, np.pi, len(fixman_phi))
  plot_phis([fixman_phi, rfd_phi, em_phi], names, buckets)
