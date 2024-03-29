# run in your local directory where the github repository is copied
#$ python3 -m test_cpa

from src.chem_pathway_analysis import cpa

# this is a stupid way to test the package but it works
# Next line is the example of lehmann 2004
# cpa.run_cpa(timestep=100.0,rate_threshold=1e-12,t_min=1.0e4,filename_model='user_model_example.txt',filename_concentration='user_concentration_example.txt',chronicle_writing=True)

# test article to see if P4 is deleted!
# cpa.run_cpa(timestep=100.0,rate_threshold=0.3e-9,t_min=1.0e4,filename_model='user_model_example.txt',filename_concentration='user_concentration_example.txt',chronicle_writing=True)

# Test for another simple chemical model that includes Cl and ClO O3 destruction catalysis
# This model is under dev since I have no clue of the real rates and proper concentration fo Cl and ClO
cpa.run_cpa(timestep=100.0,rate_threshold=1e-11,t_min=1.0e4,filename_model='user_model_O3destruction_example.txt',filename_concentration='user_concentration_O3destruction_example.txt',chronicle_writing=True)
