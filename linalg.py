import numpy as np
from gensim import matutils
import scipy.sparse as ss

def norm(vec, ord=None):
    return np.linalg.norm(vec, ord=ord)

def to_unit(vec, norm='l2'):
    """
    Scale a vector to unit length.

    Notes: input vector can be numpy.ndarray,
    scipy.sparse or Gensim BoW
    """
    return matutils.unitvec(vec, norm=norm)

# def is_unit(vec, ord=None):
#     return abs(norm(vec, ord=ord) - 1) <= 1e-12

def to_sparse(vec):
    """
    Converts numpy.ndarray to scipy.sparse
    """
    return ss.csc_matrix(vec)

def zero_vec(len):
    return np.zeros(len)

def dot(vec1, vec2):
    return np.dot(vec1, vec2)
