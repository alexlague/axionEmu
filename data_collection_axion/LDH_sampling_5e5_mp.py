import numpy as np
import pyDOE as pyDOE
import pickle

# number of parameters and samples

n_params = 9
n_samples = 120000 

# parameter ranges

obh2 =      np.linspace(0.0174, 0.0274, n_samples)
omaxh2 =     np.linspace(1e-32, 0.01   ,   n_samples)
H_0 =         np.linspace(55.0,    82.0,    n_samples) 
ns =        np.linspace(0.86, 1.07,    n_samples)
As =      np.linspace(5e-10,    2.6e-9,    n_samples)
tau_reio = np.linspace(0.01, 0.26,    n_samples)
z = np.linspace(2.51,5.0, n_samples)
ma = np.linspace(-29.30103, -26.30103, n_samples)
sum_omega = np.linspace(0.16, 0.36, n_samples) # sum of omaxh2 and omlambda in dark-energy region

# LHS grid

AllParams = np.vstack([obh2, omaxh2, H_0, ns, As, tau_reio, z, ma, sum_omega])
lhd = pyDOE.lhs(n_params, samples=n_samples, criterion=None)
idx = (lhd * n_samples).astype(int)

AllCombinations = np.zeros((n_samples, n_params))
for i in range(n_params):
    AllCombinations[:, i] = AllParams[i][idx[:, i]]

# saving

params = {'omega_b': AllCombinations[:, 0],
          'omega_ax': AllCombinations[:, 1],
          'H_0': AllCombinations[:, 2],
          'n_s': AllCombinations[:, 3],
          'A_s': AllCombinations[:, 4],
          'tau_reio': AllCombinations[:, 5],
          'z': AllCombinations[:, 6],
          'ma':10**(AllCombinations[:, 7]),
           }

sum_o = AllCombinations[:, 8]
omega_cdm = params['H_0']*params['H_0']*((0.01)**2)-(sum_o+params['omega_b']+0.0006) #default omega_nutrino_h2 is 0.0006  
omega_cdm = np.where(omega_cdm >0, omega_cdm, np.ones(len(omega_cdm))*1e-32)
params['omega_cdm'] = omega_cdm
data_pkl = 'LHD_parameters_5e5_mp.pkl' #the .pkl that stores all input parameters
f = open(data_pkl, 'wb')
pickle.dump(params, f)
f.close()
num_subfile = 60 # this number should be in consistent with number_cores variable in the 9parameters_data_collection_mp.py file
num_samples_per_subfile = int(n_samples/num_subfile)
for i in range(num_subfile):
    start = int(i*num_samples_per_subfile)
    print(start, start+num_samples_per_subfile)
    params_1 = {'omega_b': params['omega_b'][start:start+num_samples_per_subfile],
          'omega_cdm': params['omega_cdm'][start:start+num_samples_per_subfile],
          'H_0': params['H_0'][start:start+num_samples_per_subfile],
          'n_s': params['n_s'][start:start+num_samples_per_subfile],
          'A_s': params['A_s'][start:start+num_samples_per_subfile],
          'tau_reio': params['tau_reio'][start:start+num_samples_per_subfile],
          'z': params['z'][start:start+num_samples_per_subfile],
          'ma': params['ma'][start:start+num_samples_per_subfile],
          'omega_ax': params['omega_ax'][start:start+num_samples_per_subfile]
           }
    data_pkl = 'LHD_parameters_5e5_mp' +str(i) +'.pkl'
    f = open(data_pkl, 'wb')
    pickle.dump(params_1, f)
    f.close()
