'''
This module compute the blob-blob forces using pycuda.
'''

import numpy as np
import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule


mod = SourceModule("""
#include <stdio.h>

/*
  This function compute the force between two blobs
  with vector between blob centers r.

  In this example the force is derived from a Yukawa potential
  
  U = eps * exp(-r_norm / b) / r_norm
  
  with
  eps = potential strength
  r_norm = distance between blobs
  b = Debey length
*/
__device__ void blob_blob_force(const double rx, 
                                const double ry, 
                                const double rz, 
                                double &fx, 
                                double &fy, 
                                double &fz, 
                                const double eps, 
                                const double b){

  double r = sqrt(rx*rx + ry*ry + rz*rz);
  double f = ((eps / b) + (eps / r)) * exp(-r / b) / (r*r);
  fx += f * rx;
  fy += f * ry;
  fz += f * rz;
}

/*
 This function computes the blob-blob force for all blobs.
*/
__global__ void calc_blob_blob_force(const double *x, 
                                     double *f, 
                                     const double repulsion_strength, 
                                     const double debey_length,
                                     const int number_of_blobs){
  int i = blockDim.x * blockIdx.x + threadIdx.x;
  if(i >= number_of_blobs) return;   

  int offset_i = i * 3;
  int offset_j;
  double rx, ry, rz;
  double fx = 0;
  double fy = 0;
  double fz = 0;

  // Loop over blobs to add interanctions
  for(int j=0; j<number_of_blobs; j++){
    offset_j = j * 3;

    // Compute blob to blob vector
    rx = x[offset_j]     - x[offset_i];
    ry = x[offset_j + 1] - x[offset_i + 1];
    rz = x[offset_j + 2] - x[offset_i + 2];

    // Compute force between blobs i and j
    if(i != j){
      blob_blob_force(rx, ry, rz, fx, fy, fz, repulsion_strength, debey_length);
    }
  }
  
  // Return forces
  f[offset_i]     = fx;
  f[offset_i + 1] = fy;
  f[offset_i + 2] = fz;
}
""")


def set_number_of_threads_and_blocks(num_elements):
  '''
  This functions uses a heuristic method to determine
  the number of blocks and threads per block to be
  used in CUDA kernels.
  '''
  threads_per_block=512
  if((num_elements/threads_per_block) < 512):
    threads_per_block = 256
  if((num_elements/threads_per_block) < 256):
    threads_per_block = 128
  if((num_elements/threads_per_block) < 128):
    threads_per_block = 64
  if((num_elements/threads_per_block) < 128):
    threads_per_block = 32
  num_blocks = (num_elements-1)/threads_per_block + 1

  return (threads_per_block, num_blocks)


def calc_blob_blob_forces_pycuda(r_vectors, *args, **kwargs):
   
  # Determine number of threads and blocks for the GPU
  number_of_blobs = np.int32(len(r_vectors))
  threads_per_block, num_blocks = set_number_of_threads_and_blocks(number_of_blobs)

  # Get parameters from arguments
  eps = kwargs.get('repulsion_strength')
  b = kwargs.get('debey_length')

  # Reshape arrays
  x = np.reshape(r_vectors, number_of_blobs * 3)
  f = np.empty_like(x)
        
  # Allocate GPU memory
  x_gpu = cuda.mem_alloc(x.nbytes)
  f_gpu = cuda.mem_alloc(f.nbytes)
    
  # Copy data to the GPU (host to device)
  cuda.memcpy_htod(x_gpu, x)
    
  # Get blob-blob force function
  force = mod.get_function("calc_blob_blob_force")

  # Compute mobility force product
  force(x_gpu, f_gpu, np.float64(eps), np.float64(b), number_of_blobs, block=(threads_per_block, 1, 1), grid=(num_blocks, 1)) 
   
  # Copy data from GPU to CPU (device to host)
  cuda.memcpy_dtoh(f, f_gpu)

  return np.reshape(f, (number_of_blobs, 3))
