from this import d
import pandas as pd
from scipy.spatial import distance    #To calculate cosinus_similarity
import os

#%%   
def get_all_values_repartition() :
  #Build all the files in the folder stats/value_count/
  #Each file represent the repartition of the different values for one column
  colList = df.columns.values   #List of column name
  
  for colName in colList : 
    table = df[colName].value_counts().rename_axis('class').reset_index(name='count')
    text_file = open("stats/value_count/" + colName + '.txt', "w")
    text_file.write(table.to_string())
    text_file.close()

#%%        
def get_columns_cosinus_similarities(col1, col2) :
  #Return the similarity between col1 and col2
  #Requirement : col1 and col2 must contain numeric values
  return 1 - distance.cosine(df[col1], df[col2])

#%%
def get_columns_cosinus_similarities_stade_developpement() :
  #Return the similarity between STADEDEDEVELOPPEMENT and STADEDEVELOPPEMENTDIAG
  #We first numerize both column before returning the cosinus similarity between them
  df['STADEDEDEVELOPPEMENT'] = df['STADEDEDEVELOPPEMENT'].apply(lambda x:
                                                              0 if x == 'Arbre jeune'
                                                              else (1 if x == 'Arbre adulte' 
                                                                else(2 if x =='Arbre vieillissant' 
                                                                  else 3)))
  df['STADEDEVELOPPEMENTDIAG'] = df['STADEDEVELOPPEMENTDIAG'].apply(lambda x:
                                                              0 if x == 'Arbre jeune'
                                                              else (1 if x == 'Arbre adulte' 
                                                                else(2 if x =='Arbre vieillissant' 
                                                                  else 3)))
  return get_columns_cosinus_similarities('STADEDEDEVELOPPEMENT', 'STADEDEVELOPPEMENTDIAG')

#%%  
def get_matrix_similarities() :
  #Build the file stats/similarities/defaut.txt
  #This file contains all similarities combination for the columns : DEFAUT, Collet, Houppier, Racine, Tronc
  table = {'': ['DEFAUT', 'Collet', 'Houppier', 'Racine'], 
          'Collet': [get_columns_cosinus_similarities('DEFAUT', 'Collet'), 'X', 'X', 'X'],
          'Houppier': [get_columns_cosinus_similarities('DEFAUT', 'Houppier'), get_columns_cosinus_similarities('Collet', 'Houppier'), 'X', 'X'],
          'Racine': [get_columns_cosinus_similarities('DEFAUT', 'Racine'), get_columns_cosinus_similarities('Collet', 'Racine'), get_columns_cosinus_similarities('Houppier', 'Racine'), 'X'],
          'Tronc': [get_columns_cosinus_similarities('DEFAUT', 'Tronc'), get_columns_cosinus_similarities('Collet', 'Tronc'), get_columns_cosinus_similarities('Houppier', 'Tronc'), get_columns_cosinus_similarities('Racine', 'Tronc')]
    }
  table_df = pd.DataFrame(data=table)

  text_file = open("stats/similarities/" + 'defaut.txt', "w")
  text_file.write(table_df.to_string())
  text_file.close()

#%%    
def get_defaut_proportion_for_stade_developpement_difference() :
  #First, build a set of row where STADEDEDEVELOPPEMENT and STADEDEVELOPPEMENTDIAG have different values
  #Then, use this set to calculate the percentages of value 1 in the columns : DEFAUT, Collet, Houppier, Racine, Tronc
  #Finally, build the file stats/similarities/stadeDeveloppementDifferences.txt
  df_temp = df.loc[~(df['STADEDEDEVELOPPEMENT'] == df['STADEDEVELOPPEMENTDIAG'])]
  lenght = len(df_temp)
  table = {'': ['DEFAUT', 'Collet', 'Houppier', 'Racine', 'Tronc'], 
    'percentages': [value_count(df_temp, 'DEFAUT', 1, lenght), value_count(df_temp, 'Collet', 1, lenght), value_count(df_temp, 'Houppier', 1, lenght), value_count(df_temp, 'Racine', 1, lenght), value_count(df_temp, 'Tronc', 1, lenght)]}
  
  table_df = pd.DataFrame(data=table)
  text_file = open("stats/percentages/" + 'stadeDeveloppementDifferences.txt', "w")
  text_file.write(table_df.to_string())
  text_file.close()
  #Conclusion : Collet = 7% and Racine = 3%
  #We can consider that if STADEDEDEVELOPPEMENT != STADEDEDEVELOPPEMENTDIAG, then Collet == 0 and Racine == 0 and so keeping STADEDEDEVELOPPEMENT and STADEDEVELOPPEMENTDIAG differences is irrelevant for these fields
  #We could merge both columns STADEDEVELOPPEMENT and STADEDEVELOPPEMENTDIAG if we only want to study Collet and Racine
  #Warning, DEFAUT = 29.7%, Houppier = 17.9% and Tronc = 14.5%, a merge of columns STADEDEVELOPPEMENT and STADEDEVELOPPEMENTDIAG could lead to a loss of usefull information

#%%  
def get_defaut_proportion_for_year() :
  #For each year between 2004 and 2015, build a set of row where ANNEEDEPLANTATION == year
  #Then, use this set to calculate the percentages of value 1 in the columns : DEFAUT, Collet, Houppier, Racine, Tronc
  #Finally, build the file 'stats/percentages/anneeDePlantation' + year + '.txt'
  #Then we do the same methode with ANNEEREALISATIONDIAGNOSTIC and ANNEETRAVAUXPRECONISESDIAG
  minValue = df['ANNEEDEPLANTATION'].min()
  maxValue = df['ANNEEDEPLANTATION'].max()

  for year in range(minValue, maxValue+1) :
    df_temp = df.loc[df['ANNEEDEPLANTATION'] == year]
    lenght = len(df_temp)
    if (lenght > 0) :
      table = {'': ['DEFAUT', 'Collet', 'Houppier', 'Racine', 'Tronc'], 
        'percentages': [value_count(df_temp, 'DEFAUT', 1, lenght), value_count(df_temp, 'Collet', 1, lenght), value_count(df_temp, 'Houppier', 1, lenght), value_count(df_temp, 'Racine', 1, lenght), value_count(df_temp, 'Tronc', 1, lenght)]}
      table_df = pd.DataFrame(data=table)
      text_file = open("stats/percentages/annee_de_plantation/" + str(year) + '.txt', "w")
      text_file.write(table_df.to_string())
      text_file.close()
  #Conclusion : The older ANNEEDEPLANTATION is, the more DEFAUTS are which is logical. 
  #From 2012 to 2015, the percentages are from 0 to 8%. We could consider making a cut in this column with "Recent" and "Old" values
  #And so, if ANNEEDEPLANTATION is "Recent", then there is a really high chance that there is no default

  for year in range(minValue, maxValue+1) :
    df_temp = df.loc[df['ANNEEREALISATIONDIAGNOSTIC'] == str(year)]
    lenght = len(df_temp)
    if (lenght > 0) :
      table = {'': ['DEFAUT', 'Collet', 'Houppier', 'Racine', 'Tronc'], 
        'percentages': [value_count(df_temp, 'DEFAUT', 1, lenght), value_count(df_temp, 'Collet', 1, lenght), value_count(df_temp, 'Houppier', 1, lenght), value_count(df_temp, 'Racine', 1, lenght), value_count(df_temp, 'Tronc', 1, lenght)]}
      table_df = pd.DataFrame(data=table)
      text_file = open("stats/percentages/annee_realisation_diagnostic/" + str(year) + '.txt', "w")
      text_file.write(table_df.to_string())
      text_file.close()

  for year in range(minValue, maxValue+1) :
    df_temp = df.loc[df['ANNEETRAVAUXPRECONISESDIAG'] == str(year)]
    lenght = len(df_temp)
    if (lenght > 0) :
      table = {'': ['DEFAUT', 'Collet', 'Houppier', 'Racine', 'Tronc'], 
        'percentages': [value_count(df_temp, 'DEFAUT', 1, lenght), value_count(df_temp, 'Collet', 1, lenght), value_count(df_temp, 'Houppier', 1, lenght), value_count(df_temp, 'Racine', 1, lenght), value_count(df_temp, 'Tronc', 1, lenght)]}
      table_df = pd.DataFrame(data=table)
      text_file = open("stats/percentages/annee_travaux_preconises_diag/" + str(year) + '.txt', "w")
      text_file.write(table_df.to_string())
      text_file.close()
  #Conclusion : ANNEEREALISATIONDIAGNOSTIC and ANNEETRAVAUXPRECONISEDIAG value doesn't seem to be enough to predict if there is a default or not

#%%
def get_defaut_proportionF_for_adr_secteur() :
  minValue = df['ADR_SECTEUR'].min()
  maxValue = df['ADR_SECTEUR'].max()

  for adr in range(minValue, maxValue+1) :
    df_temp = df.loc[df['ADR_SECTEUR'] == adr]
    lenght = len(df_temp)
    if (lenght > 0) :
      table = {'': ['DEFAUT', 'Collet', 'Houppier', 'Racine', 'Tronc'], 
        'percentages': [value_count(df_temp, 'DEFAUT', 1, lenght), value_count(df_temp, 'Collet', 1, lenght), value_count(df_temp, 'Houppier', 1, lenght), value_count(df_temp, 'Racine', 1, lenght), value_count(df_temp, 'Tronc', 1, lenght)]}
      table_df = pd.DataFrame(data=table)
      text_file = open("stats/percentages/adr_secteur/" + str(adr) + '.txt', "w")
      text_file.write(table_df.to_string())
      text_file.close()
  #Conclusion : ADR_SECTEUR value doesn't seem to be enough to predict if there is a default or not

#%%
def value_count(dataFrame, colName, value, lenght) :
  #Return the percent of occurences of value in the column colName of dataFrame
  if value in dataFrame[colName].values :
    percent = dataFrame[colName].value_counts()[value]
    return percent/lenght
  return 0

#%%
def build_all_stats() :
  path = "stats"
  if not os.path.exists(path) : os.makedirs(path)
  path = "stats/percentages"
  if not os.path.exists(path) : os.makedirs(path)
  path = "stats/percentages/adr_secteur"
  if not os.path.exists(path) : os.makedirs(path)
  path = "stats/percentages/annee_de_plantation"
  if not os.path.exists(path) : os.makedirs(path)
  path = "stats/percentages/annee_realisation_diagnostic"
  if not os.path.exists(path) : os.makedirs(path)
  path = "stats/percentages/annee_travaux_preconises_diag"
  if not os.path.exists(path) : os.makedirs(path)
  path = "stats/similarities"
  if not os.path.exists(path) : os.makedirs(path)
  path = "stats/value_count"
  if not os.path.exists(path) : os.makedirs(path)
  get_matrix_similarities()
  get_defaut_proportion_for_stade_developpement_difference()
  get_defaut_proportion_for_year()
  get_defaut_proportionF_for_adr_secteur()

#%%
def get_defaut_proportion_for_traitement_chenilles() :
  #For each value in values, calculate the percentages of value 1 in the columns : DEFAUT, Collet, Houppier, Racine, Tronc
  values = ['?', 'Basse', 'Moyenne', 'Haute']
  for value in values :
    df_temp = df.loc[df['TRAITEMENTCHENILLES'] == value]
    lenght = len(df_temp)
    print(lenght)
    table = {'': ['DEFAUT', 'Collet', 'Houppier', 'Racine', 'Tronc'], 
      'percentages': [value_count(df_temp, 'DEFAUT', 1, lenght), value_count(df_temp, 'Collet', 1, lenght), value_count(df_temp, 'Houppier', 1, lenght), value_count(df_temp, 'Racine', 1, lenght), value_count(df_temp, 'Tronc', 1, lenght)]}
    table_df = pd.DataFrame(data=table)
    print(table_df)
  #Conclusion : Quite surprising but there is no difference of defaut proportion between high, medium, low or ? priority
  #We could expect that high priority would have more defauts but no
 
#%%
def get_defaut_proportion_for_trottoir() :
  values = ['oui', 'non']
  for value in values :
    df_temp = df.loc[df['TROTTOIR'] == value]
    lenght = len(df_temp)
    print(lenght)
    table = {'': ['DEFAUT', 'Collet', 'Houppier', 'Racine', 'Tronc'], 
      'percentages': [value_count(df_temp, 'DEFAUT', 1, lenght), value_count(df_temp, 'Collet', 1, lenght), value_count(df_temp, 'Houppier', 1, lenght), value_count(df_temp, 'Racine', 1, lenght), value_count(df_temp, 'Tronc', 1, lenght)]}
    table_df = pd.DataFrame(data=table)
    print(table_df)
  #Conclusion : Each defaut proportion is a bit higher if TROTTOIR value == 'non' (around +3%). This is not relevant
 
#%% 
def get_defaut_proportion_for_type_implantation_plu() :
  values = ['?', 'Alignement', 'Groupé']
  for value in values :
    df_temp = df.loc[df['TYPEIMPLANTATIONPLU'] == value]
    lenght = len(df_temp)
    print(lenght)
    table = {'': ['DEFAUT', 'Collet', 'Houppier', 'Racine', 'Tronc'], 
      'percentages': [value_count(df_temp, 'DEFAUT', 1, lenght), value_count(df_temp, 'Collet', 1, lenght), value_count(df_temp, 'Houppier', 1, lenght), value_count(df_temp, 'Racine', 1, lenght), value_count(df_temp, 'Tronc', 1, lenght)]}
    table_df = pd.DataFrame(data=table)
    print(table_df)
 

#%%
df = pd.read_csv('data/donnees-defi-egc.csv')

def main():
  get_all_values_repartition()
  print(get_columns_cosinus_similarities_stade_developpement())    #We have a similary of 92% between 'STADEDEDEVELOPPEMENT' and 'STADEDEVELOPPEMENTDIAG'
  build_all_stats()
  get_defaut_proportion_for_traitement_chenilles()
  get_defaut_proportion_for_trottoir()
  get_defaut_proportion_for_type_implantation_plu()

#%%
if __name__ == "__main__":
    main()