'''
Class to look at samples on a sphere and verify that they are a uniform
distribution.
'''
import numpy as np

class UniformAnalyzer(object):
  ''' 
  This object just takes samples on a sphere and analyzes their 
  distribution to determine if they are uniformly distributed.
  '''
  def __init__(self, samples):
    ''' 
    Just copy the reference to the list of samples.
    Each sample should be of the same length, and represent
    a point on the sphere.
    '''
    self.samples = samples
    self.dim = len(self.samples[0])

  def AnalyzeSamples(self):
    ''' Analyze samples by calculating means of spherical harmonics. '''
    statistics = [[] for _ in range(10)]
    n_xi_eta_pairs = 16
    for k in range(n_xi_eta_pairs):
      xi, eta = self.GenerateXiEta()
      for L in range(1, len(statistics) + 1):
        harmonics = []
        for sample in self.samples:
          u = np.inner(xi, sample)
          v = np.inner(eta, sample)
          # Numpy arctan is always between -pi/2 and pi/2.
          theta = np.arctan(v/u)  + (u < 0)*np.pi
          harmonics.append(np.cos(L*theta))
        statistics[L-1].append(np.mean(harmonics))
    for L in range(1, len(statistics) + 1):
      print ('Mean at L = %d is: %f +/- %f' % 
             (L, np.mean(statistics[L-1]), 
              np.std(statistics[L-1])/np.sqrt(n_xi_eta_pairs)))


  def GenerateXiEta(self):
    ''' Generate a random pair of orthonormal vectors. '''
    xi = np.random.normal(0, 1, self.dim)
    xi = xi/np.linalg.norm(xi)
    
    eta = np.random.normal(0, 1, self.dim)
    eta = eta - np.inner(eta, xi)*xi
    
    eta = eta/np.linalg.norm(eta)

    return xi, eta
    
    
    
    
    