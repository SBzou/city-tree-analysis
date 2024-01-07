import geopy.distance
import pandas as pd

#%%
def is_tree_near_school(tree, radius, school_list) :
    #Tree represent the coord of the tree
    #Return true if there is no school around the tree with distance < radius
    for pos in school_list:
        pos_coord = (float(pos[1]), float(pos[2]))
        if geopy.distance.distance(tree, pos_coord).km < radius:
            return True 
    return False  

#%%
def get_number_tree_near_schools() : 
    #Return [numberTreeGood, numberTreeDefaut] with :
    #numberTreeGood = the number of tree near a school that have no defaut 
    #numberTreeDefaut = the number of tree near a school that have a defaut
    school_df = pd.read_csv('data/positions_ecoles.csv')
    school_list = school_df.values.tolist()
    
    numberTreeDefaut = 0
    numberTreeGood = 0
    for index in range(1, len(locationlist)):
        coord = (df['longitude'][index], df['latitude'][index])
        if is_tree_near_school(coord, proximity_threshold, school_list) :
            if df['DEFAUT'][index] == 1:
                numberTreeDefaut = numberTreeDefaut + 1
            else :
                numberTreeGood = numberTreeGood + 1
    return [numberTreeGood, numberTreeDefaut]

#%%
def is_tree_in_park(tree, park_list) :
    #Tree represent the coord of the tree
    #Return true if the tree is in a park 
    for pos in park_list:
        pos_coord = (float(pos[1]), float(pos[2]))
        if geopy.distance.distance(tree, pos_coord).km < pos[3]:
            return True 
    return False

#%%
def get_number_tree_in_park() : 
    #Return [numberTreeGood, numberTreeDefaut] with :
    #numberTreeGood = the number of tree in a Park that have no defaut 
    #numberTreeDefaut = the number of tree in a Park that have a defaut
    park_df = pd.read_csv('data/positions_parcs.csv')
    park_list = park_df.values.tolist()

    numberTreeDefaut = 0
    numberTreeGood = 0
    for index in range(1, len(locationlist)):
        coord = (df['longitude'][index], df['latitude'][index])
        if is_tree_in_park(coord, park_list) :
            if df['DEFAUT'][index] == 1:
                numberTreeDefaut = numberTreeDefaut + 1
            else :
                numberTreeGood = numberTreeGood + 1
    return [numberTreeGood, numberTreeDefaut]

#%%
df = pd.read_csv("data/donnees-traitees.csv")
locations = df[['longitude', 'latitude']][0:1000]
locationlist = locations.values.tolist()
proximity_threshold = 0.3

def main():
    print(get_number_tree_near_schools())               #If proximity_threshold = 0.3 : [203, 93]
    print(get_number_tree_in_park())                    #                               [687, 312]

#%%
if __name__ == "__main__":
    main()
