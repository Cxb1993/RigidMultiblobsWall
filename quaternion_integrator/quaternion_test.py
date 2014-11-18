import unittest
import numpy as np
import random
from quaternion import Quaternion

class TestQuaternion(unittest.TestCase):

  def setUp(self):
    pass

  def test_quaternion_from_rotation(self):
    ''' Test that we correctly create a quaternion from an angle '''
    # Generate a random rotation vector
    phi = np.random.rand(3)
    phi_norm = np.linalg.norm(phi)
    theta = Quaternion.from_rotation(phi)
    
    self.assertAlmostEqual(theta.entries[0], np.cos(phi_norm/2.))
    self.assertAlmostEqual(theta.entries[1], np.sin(phi_norm/2.)*phi[0]/phi_norm)
    self.assertAlmostEqual(theta.entries[2], np.sin(phi_norm/2.)*phi[1]/phi_norm)
    self.assertAlmostEqual(theta.entries[3], np.sin(phi_norm/2.)*phi[2]/phi_norm)

  
  def test_multiply_quaternions(self):
    ''' Test that quaternion multiplication works '''
    # First construct any random unit quaternion. Not uniform.
    s = 2*random.random() - 1.
    p1 = (2. - 2*np.abs(s))*random.random() - (1. - np.abs(s))
    p2 = ((2. - 2.*np.abs(s) - 2.*np.abs(p1))*random.random() - 
          (1. - np.abs(s) - np.abs(p1)))
    p3 = np.sqrt(1. - s**2 - p1**2 - p2**2)
    theta1 = Quaternion(np.array([s, p1, p2, p3]))

    # Construct another quaternion.
    t = 2*random.random() - 1.
    q1 = (2. - 2*np.abs(s))*random.random() - (1. - np.abs(s))
    q2 = ((2. - 2.*np.abs(s) - 2.*np.abs(p1))*random.random() - 
          (1. - np.abs(s) - np.abs(p1)))
    q3 = np.sqrt(1. - s**2 - p1**2 - p2**2)
    theta2 = Quaternion(np.array([t, q1, q2, q3]))
    
    product = theta1*theta2
    
    self.assertAlmostEqual(product.s, t*s - p1*q1 - p2*q2 - p3*q3)
    self.assertAlmostEqual(product.entries[1], s*q1 + t*p1 + p2*q3 - p3*q2)
    self.assertAlmostEqual(product.entries[2], s*q2 + t*p2 + p3*q1 - p1*q3)
    self.assertAlmostEqual(product.entries[3], s*q3 + t*p3 + p1*q2 - p2*q1)

    
  def test_quaternion_rotation_matrix(self):
    ''' Test that we create the correct rotation matrix for a quaternion. '''
    # First construct any random unit quaternion. Not uniform.
    s = 2*random.random() - 1.
    p1 = (2. - 2*np.abs(s))*random.random() - (1. - np.abs(s))
    p2 = ((2. - 2.*np.abs(s) - 2.*np.abs(p1))*random.random() - 
          (1. - np.abs(s) - np.abs(p1)))
    p3 = np.sqrt(1. - s**2 - p1**2 - p2**2)
    theta = Quaternion(np.array([s, p1, p2, p3]))
    
    R = theta.rotation_matrix()

    self.assertAlmostEqual(R[0][0], 2.*(theta.s**2 + theta.p[0]**2 - 0.5))
    self.assertAlmostEqual(R[0][1], 2.*(theta.p[0]*theta.p[1] - 
                                        theta.s*theta.p[2]))
    self.assertAlmostEqual(R[1][0], 2.*(theta.p[0]*theta.p[1] +
                                        theta.s*theta.p[2]))
    self.assertAlmostEqual(R[1][1], 2.*(theta.s**2 + theta.p[1]**2 - 0.5))
    self.assertAlmostEqual(R[2][2], 2.*(theta.s**2 + theta.p[2]**2 - 0.5))
    
if __name__ == '__main__':
  unittest.main()