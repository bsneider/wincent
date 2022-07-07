import json
import os

# import transitivity_disjoint_set as soln

def test_readinput():
    #read file
    cwd = os.getcwd()

    # Print the current working directory
    print("Current working directory: {0}".format(cwd))
    f = open('../inputs/example.in')