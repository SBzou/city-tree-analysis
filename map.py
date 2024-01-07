import pandas as pd
import folium
import webbrowser
from html2image import Html2Image

#%%
def get_label(index) :
    return f"{df['CODE'][index]} {df['ESPECE'][index]}"

#%%
def show_map() :
    #Show a map of all the trees
    map = folium.Map(location=[locations['longitude'][0], locations['latitude'][0]], zoom_start=13)
    for index in range(1, len(locationlist)):
        color = 'green'
        folium.Marker(locationlist[index], popup=get_label(index), icon=folium.Icon(color=color, icon_color='white', icon='male', angle=0, prefix='fa')).add_to(map)
    map.save("map/map.html")
    webbrowser.open("map/map.html")

#%%
def show_only_defaut_map() :
    #Show a map of red dots for tree with a defaut and green dots for tree without defauts
    map = folium.Map(location=[locations['longitude'][0], locations['latitude'][0]], zoom_start=13)
    color = 'red'
    for index in range(1, len(locationlist)):
        if df['DEFAUT'][index] == 1:
            folium.Marker(locationlist[index], popup=get_label(index), icon=folium.Icon(color=color, icon_color='white', icon='male', angle=0, prefix='fa')).add_to(map)
    map.save("map/map_only_defaut.html")
    
#%%
def show_defaut_map() :
    #Show a map of red dots for tree with a defaut and green dots for tree without defauts
    map = folium.Map(location=[locations['longitude'][0]+0.008, locations['latitude'][0]], zoom_start=14)
    for index in range(1, len(locationlist)):
        if df['DEFAUT'][index] == 0 :
            color = 'green'
        else : 
            color = 'red'
        folium.Marker(locationlist[index], popup=get_label(index), icon=folium.Icon(color=color, icon_color='white', icon='male', angle=0, prefix='fa')).add_to(map)
    map.save("map/map_defaut.html")

#%%
def show_one_kind_defaut_map(defaut) :
    #Show a map of red dots for tree with a defaut and green dots for tree without defauts
    map = folium.Map(location=[locations['longitude'][0], locations['latitude'][0]], zoom_start=13)
    for index in range(1, len(locationlist)):
        if df[defaut][index] == 0 :
            color = 'green'
        else : 
            color = 'red'
        folium.Marker(locationlist[index], popup=get_label(index), icon=folium.Icon(color=color, icon_color='white', icon='male', angle=0, prefix='fa')).add_to(map)
    map.save(f"map/map_defaut_{defaut}.html")
    
#%%
def show_number_defaut_map() :
    #Show a map where each dot represent the number of defaut for one tree. Green represent zero defaut while black represent 4 defauts
    map = folium.Map(location=[locations['longitude'][0], locations['latitude'][0]], zoom_start=13)
    for index in range(1, len(locationlist)):
        numberDefaut = df['Collet'][index] + df['Houppier'][index] + df['Racine'][index] + df['Tronc'][index]
        if numberDefaut == 0 :
            color = 'green'
        elif numberDefaut == 1 :
            color = 'orange'
        elif numberDefaut == 2 :
            color = 'lightred'
        elif numberDefaut == 3 :
            color = 'red'
        else : 
            color = 'black'
        folium.Marker(locationlist[index], popup=get_label(index), icon=folium.Icon(color=color, icon_color='white', icon='male', angle=0, prefix='fa')).add_to(map)
    map.save("map/map_number_defaut.html")

#%%
def show_year_defaut_map(year) :
    #Show a map of all the trees with ANNEEDEPLANTATION < year
    map = folium.Map(location=[locations['longitude'][0], locations['latitude'][0]], zoom_start=13)
    color = 'green'
    for index in range(1, len(locationlist)):
        if df['ANNEEDEPLANTATION'][index] <= year :  
            folium.Marker(locationlist[index], popup=get_label(index), icon=folium.Icon(color=color, icon_color='white', icon='male', angle=0, prefix='fa')).add_to(map)
    map.save('map/map_year_' + str(year) + '.html')
    
#%%
hti = Html2Image() #To save html file as image

df = pd.read_csv('data/donnees-traitees.csv')
locations = df[['longitude', 'latitude']][0:1000]
locationlist = locations.values.tolist()

show_map()
show_defaut_map()
show_one_kind_defaut_map("Collet")
show_only_defaut_map()
show_number_defaut_map()
show_year_defaut_map(2005)