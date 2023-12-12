# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 21:39:44 2023

@author: Byron
"""
import itertools
import numpy as np
import pandas as pd

#Lattice parameter list
a = []

#Error parameter
error = 0.0035
decimal_places = 5

#Variables
h = [0,1,2,3,4,5]
l = [0,1,2,3,4,5]
k = [0,1,2,3,4,5]
n = [1]
lambda_ = [1.54056] #wavelength values
theta = [31.7505,45.5654,66.3084] #angles of peaks


#Loop through hlk permutations
hlk_combined = list(itertools.product(*[h,l,k]))
hlk_multiplied =[]

#combine hlk permutations
for list_ in hlk_combined:
    hlk_multiplied.append(list_[0]**2 + list_[1]**2 + list_[2]**2)
    
#list of hlk permutations with no duplicates
non_duplicated_hlk_multiplied = []
non_duplicated_hlk = []
for indx, value in enumerate(hlk_multiplied):
    if hlk_multiplied[indx] not in non_duplicated_hlk_multiplied:
        non_duplicated_hlk_multiplied.append(value)
        non_duplicated_hlk.append(hlk_combined[indx])

#Calculate d value for all variables
def d_function(en,lamb,the):
    '''function to calculate spaceing, d'''
    d = en*lamb/(2*np.sin((np.pi/180)*the/2))
    return d

#combine lists of variables to calculate spacing
d_adder = [n, lambda_, theta]
d_list = list(itertools.product(*d_adder))
d_calculated = []
variables = []

for value in d_list:
    t_d =d_function(value[0],value[1],value[2])
    d_calculated.append(t_d)
    variables.append([t_d] + [value[0], value[1], value[2]])
    

#equation to calculate a
def equation_function(de, multiple):
    '''function for lattice parameter equation'''
    function = de*np.sqrt(multiple)
    return function

#Combine lists of variables and calculate all permutations
list_adder = [d_calculated, non_duplicated_hlk_multiplied]
variables_list = list(itertools.product(*list_adder))
a_with_variables = []

#Calculate Lattice parameter for all permutations
for index,result in enumerate(variables_list):
    #find corresponding d_lambda values
    for i,x in enumerate(variables):
        if x[0] == result[0]:
            other_vs = x
        
    a_ = equation_function(result[0], result[1])
    a.append(round(a_,decimal_places))
    a_with_variables.append(sum([[round(a_,decimal_places)], other_vs],[]))

#Rounding values with error parameter
duplicate_number = 0
def compare_function(index, value, input_list, error_value, output_list, 
                     output_indices, dup_number):
    '''function comparing input values with list and applying error'''
    temporary_index_dict = {value:None}
    temporary_index = []
    for i,v in enumerate(input_list):
        
        upper = value + error_value
        lower = value - error_value
        if (upper >= v >= lower and value != v):
            dup_number += 1
            temporary_index.append(i)
    if dup_number > len(theta) - 2:
        output_list.append(value)
        output_indices.append(index)
        temporary_index_dict[value] = temporary_index
    return output_list, temporary_index_dict

duplicate_values = []
duplicate_indices = []
for i,v in enumerate(a):
    result = compare_function(i, v, a, error, duplicate_values, 
                     duplicate_indices, duplicate_number)
    if result[1][v] is not None:
        for x in result[1][v]:
            if duplicate_indices.count(x) == 0:
                duplicate_indices.append(x)
    

#Combine all final calculated values
temp = []
for i,v in enumerate(a_with_variables):
    index = i % 45
    temp.append(v + [non_duplicated_hlk[index]])
    
final = []
[final.append(temp[i]) for i in duplicate_indices]
    
df = pd.DataFrame(final, columns=['a','d','n', 'lambda','theta','(hkl)'])
print(df)



