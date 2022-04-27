#import libraries
import pandas as pd
import math as m

#read csv of data of other houses using read_csv
readcsv = pd.read_csv('houses.csv')

#a function to pull attributes from a specific key
def pull(dataframe, key):
    list = []
    for var in dataframe[key]:
         list.append(var)
    return list

#a function to find minimum value from list of attributes
def min(list_of_data):
    minimum = 9999
    for datum in list_of_data:
        if datum < minimum:
            minimum = datum
    return minimum

#a function to find maximum value from list of attributes
def max(list_of_data):
    maximum = -9999
    for datum in list_of_data:
        if datum > maximum:
            maximum = datum
    return maximum

#function to transform an attribute
def transform_attr(attr, max_attr, min_attr):
    transformed = 0
    transformed = (attr - min_attr)/(max_attr - min_attr)
    return transformed

#function to transform numbers of specified keys from a pandas dataframe format
def transform_data(dataframe, list_of_keys):
    attr_info = {}
    for key in list_of_keys:
        min_attr = min(pull(dataframe,key))
        max_attr = max(pull(dataframe,key))
        attr_info[key] = {'max':max_attr,'min':min_attr}
        i = 0
        while i < len(dataframe):
            dataframe[key][i]=transform_attr(dataframe[key][i], max_attr, min_attr)
            i += 1
    return dataframe , attr_info

#function to transform attributes from a dictionary format
def transform_list(data, attr_info):
    for key in data.keys():
        data[key] = transform_attr(data[key], attr_info[key]['max'], attr_info[key]['min'])
    return data

#function to predict a price of a house
#from a reference of list of data of 
#land area, building area, distance from center of the city, and prices from other houses from a csv file
def price_predict(new_data, old_datas, list_of_keys):
    smallest_difference = 9999
    price_predict = 0
    i = 0
    olddata_trans, attr_info = transform_data(old_datas, list_of_keys)
    newdata_trans = transform_list(new_data, attr_info)
    while i < len(old_datas):
        difference = 0
        for key in list_of_keys:
            difference += m.fabs(newdata_trans[key] - olddata_trans[key][i])
        if difference < smallest_difference:
            smallest_difference = difference
            price_predict = old_datas['price'][i]
        i += 1
    return price_predict

#input new data in a dictionary format
data = {'land' : 110, 'building' : 80, 'distance_to_center' : 35}

#predict the price of the house using price_predict() function
price = price_predict(data,readcsv,['land', 'building', 'distance_to_center'])
print(price)
