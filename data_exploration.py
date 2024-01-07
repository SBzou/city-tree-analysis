import pandas as pd
import re
import warnings
import pyproj
warnings.simplefilter(action='ignore', category=FutureWarning)

#%%     
def remove_useless_values():
      #Removing columns that are very unlikely to be relevant
      df.drop(columns= ['CODE_PARENT','CODE_PARENT_DESC','RAISONDEPLANTATION','SOUS_CATEGORIE','TYPEIMPLANTATIONPLU','INTITULEPROTECTIONPLU','VARIETE'], inplace=True)
      #Remove FREQUENTATIONCIBLE column: Most values are the same
      df.drop(columns=['FREQUENTATIONCIBLE'], inplace=True)

#%%
def remove_missing_values(df):
      #Removal of values whose diameter is not entered (there are few)
      length = len(df)
      df.drop(df[df.DIAMETREARBREAUNMETRE == '?'].index, inplace=True)
      new_length = len(df)
      print(str(length-new_length) + ' rows dropped')

      #Removal of the unknown elements of NOTEDIAGNOSTIC in order to make an order relationship
      length = len(df)
      df.drop(df[df.NOTEDIAGNOSTIC == '?'].index, inplace=True)
      new_length = len(df)
      print(str(length-new_length) + ' rows dropped')

#%%
def replace_missing_values(df):
      #Conversion of diameters into numerized data. The order relationship is maintained
      df.DIAMETREARBREAUNMETRE = df.DIAMETREARBREAUNMETRE.apply(lambda x: int(x.split(' ')[0]))

      #It is assumed that trees with a PLU identifier are those placed under PLU protection. 
      #We then replace all PLU fields by a single 'PLU' field: 0 or 1
      df['IDENTIFIANTPLU'] = df['IDENTIFIANTPLU'].apply(lambda x: 0 if x == '?' else 1)
      df.rename(columns={'IDENTIFIANTPLU' : 'PLU'}, inplace=True)

      #Numerize the NOTEDIAGNOSTIC column (order relationship). 
      #Replace the column name NOTEDIAGNOSTIC by SEVERITEDIAGNOSTIC for clarity
      df.NOTEDIAGNOSTIC.unique() # 5 possibilités
      df['NOTEDIAGNOSTIC'] = df['NOTEDIAGNOSTIC'].apply(lambda x:
                                                        0 if x == 'Arbre davenir normal'
                                                        else (1 if x == 'Arbre davenir incertain'
                                                              else (2 if x == 'Arbre à abattre dans les 10 ans'
                                                                    else (3 if x== 'Arbre à abattre dans les 5 ans'
                                                                          else 4))))
      df.rename(columns={'NOTEDIAGNOSTIC' : 'SEVERITEDIAGNOSTIC'}, inplace=True)
      
      #The field PRIORITERENOUVELLEMENT has an order relationship that we want to keep and numerize,
      #however, there is missing values
      df.PRIORITEDERENOUVELLEMENT.unique()
      len(df[df.PRIORITEDERENOUVELLEMENT == '?'])
      """
      il y'a 104 valeurs manquantes. Avant de toutes les retirer, nous proposons une méthode pour les inclure dans une des 
      classes
      """
      #We first numerize filled in values
      df['PRIORITEDERENOUVELLEMENT'] = df['PRIORITEDERENOUVELLEMENT'].apply(lambda x:
                                                        0 if x == 'de 1 à 5 ans'
                                                        else (1 if x == 'de 6 à 10 ans'
                                                              else (2 if x == 'de 11 à 20 ans'
                                                                    else (3 if x== 'plus de 20 ans'
                                                                          else '?'))))
      #Note that the correlation between renewal priority and default is quite high
      df[df.PRIORITEDERENOUVELLEMENT != '?']['PRIORITEDERENOUVELLEMENT'].astype('float64').corr(df[df.PRIORITEDERENOUVELLEMENT != '?']['DEFAUT'].astype('float64'))
      
      #%% 
      #Rather than assigning an average/median value to missing values, we decide to keep the link with the defect
      #The proportion of trees with defects is calculated for each class
      for i in range(4) :
            prop_defaut = len(df[df.PRIORITEDERENOUVELLEMENT == i][df.DEFAUT == 1]) / len(df[df.PRIORITEDERENOUVELLEMENT == i])
            print(str(prop_defaut) + ' de proportion de défaut pour la classe ' + str(i))

            prop_defaut = len(df[df.PRIORITEDERENOUVELLEMENT == '?'][df.DEFAUT == 1]) / len(df[df.PRIORITEDERENOUVELLEMENT == '?'])
            print(str(prop_defaut) + ' de proportion de défaut pour les valeurs non renséignées')

      #%%
      #We notice that class 0 and 1 have a very close proportion of defects. since they all contain
      #the two a small number of elements, we propose to group it. In addition we add an intermediate class 
      #for values not specified, so that the lower the new PRIORITY, the higher the chance 
      #have a defect. We can try again later without this treatment.
      df['PRIORITEDERENOUVELLEMENT'] = df['PRIORITEDERENOUVELLEMENT'].apply(lambda x:
                                                                        0 if x == 0
                                                                        else (0 if x == 1
                                                                              else (1 if x == '?'
                                                                                    else (2 if x== 2
                                                                                          else 3))))
      #New proportions :
      for i in range(4) :
            prop_defaut = len(df[df.PRIORITEDERENOUVELLEMENT == i][df.DEFAUT == 1]) / len(df[df.PRIORITEDERENOUVELLEMENT == i])
            print(str(prop_defaut) + ' de proportion de défaut pour la classe ' + str(i))

      #%% 
      #For the SOUS_CATEGORIE_DESC field, we notice that the proportion of tree with default is much lower for
      #of road shafts: 0.23 versus approximately O.4 for each of the other classes (0.40, 0.41 and 0.44)
      #replace the column with a binary field indicating whether the tree is voirire or not. ( there are 7192 road trees)
      df['SOUS_CATEGORIE_DESC'] = df['SOUS_CATEGORIE_DESC'].apply(lambda x: 1 if x == 'Arbre de voirie' else 0)

      #Rename SOUS_CATEGORIE_DESC in ARBREDEVOIRIE
      df.rename(columns={'SOUS_CATEGORIE_DESC' : 'ARBREDEVOIRIE'}, inplace=True)
      return df

#%%
def process_data(df):
      #For tree development stages, we need to address missing values.
      #46 values for STADEDEDEVELOPPEMENT and only 4 for STADEDEVELOPPEMENTDIAG
      # We start by removing the missing values from STADEDEVELOPPEMENTDIAG:length = len(df)
      length = len(df)
      df.drop(df[df.STADEDEVELOPPEMENTDIAG == '?'].index, inplace=True)
      new_length = len(df)
      print(str(length-new_length) + ' rows dropped')

      #%%
      #We argue that for most elements, the values of STADEDEVELOPMENT and
      #STADEDEVELOPPEMENTDIAG are the same. Let’s test this hypothesis:
      valeurs_egales = 0
      df_without_missing_val = df[df.STADEDEDEVELOPPEMENT != '?'].reset_index(drop=True)

      for i in range(len(df_without_missing_val)):
            if df_without_missing_val.STADEDEDEVELOPPEMENT[i] == df_without_missing_val.STADEDEVELOPPEMENTDIAG[i] :
                  valeurs_egales +=1
      print(str(valeurs_egales) + ' valeurs égales sur ' + str(len(df_without_missing_val))) # 0.87 % de valeurs égales

      #%%We then decide to give the elements not specified the value of the STADEDEVELOPPEMENTDIAG:
      df.loc[df.STADEDEDEVELOPPEMENT == '?', 'STADEDEDEVELOPPEMENT'] = df[df.STADEDEDEVELOPPEMENT == '?']['STADEDEVELOPPEMENTDIAG']

      #%%We numerize both columns
      df.STADEDEVELOPPEMENTDIAG .unique()
      df['STADEDEDEVELOPPEMENT'] = df['STADEDEDEVELOPPEMENT'].apply(lambda x:
                                                                  0 if x == 'Arbre jeune'
                                                                  else (1 if x == 'Arbre adulte'
                                                                        else 2))

      df['STADEDEVELOPPEMENTDIAG'] = df['STADEDEVELOPPEMENTDIAG'].apply(lambda x:
                                                                  0 if x == 'Arbre jeune'
                                                                  else (1 if x == 'Arbre adulte'
                                                                        else 2))

      #%%
      # TRAITEMENTCHENILLES : The value '?' most likely indicates that the tree does not receive caterpillar treatment.
      # We therefore numerize according to the level of treatment: 0 = no treatment, 3 = high treatment
      df['TRAITEMENTCHENILLES'] = df['TRAITEMENTCHENILLES'].apply(lambda x:
                                                                        0 if x == '?'
                                                                        else (1 if x == 'Basse'
                                                                              else (2 if x == 'Moyenne'
                                                                                    else 3)))


      #%% TRAVAUXPRECONISESDIAG :
      for field in df.TRAVAUXPRECONISESDIAG.unique() :
            prop_defaut = len(df[df.TRAVAUXPRECONISESDIAG == field][df.DEFAUT == 1]) / len(df[df.TRAVAUXPRECONISESDIAG == field])
            print(str(round(prop_defaut,2)) + ' de proportion de défaut pour ' +  str(field))

      #We find that the proportions of defects are not balanced according to the recommended work:
      #With Haubannage, Abattage, Controle resistographe or Size secured, there is almost always a defect.
      #Hanging, Dead wood cut, Curtain cut: close to 0.53
      #Extension Height, Feet Layout Darbres, Size formation and sizing together with nearly 0.34
      #The rest together
      df['TRAVAUXPRECONISESDIAG'] = df['TRAVAUXPRECONISESDIAG'].apply(lambda x:
                                                                  1 if x in ['Taille de prolongement','Aménagement pieds darbres', 'Taille formation et mise au gabarit' ]
                                                                  else (2 if x in ['Emondage', 'Taille de bois mort', 'Taille rideau']
                                                                        else (3 if x in ['Haubannage','Controle résistographe','Taille mise en sécurité','Abattage']
                                                                              else 0)))
      #%%
      #TROTTOIR : Just have 0 or 1 rather than yes or no
      df['TROTTOIR'] = df['TROTTOIR'].apply(lambda x: 1 if x == 'oui' else 0)

      #VIGUEUR : Remove the two missing values, and count (order relationship)
      length = len(df)
      df.drop(df[df.VIGUEUR == '?'].index, inplace=True)
      new_length = len(df)
      print(str(length-new_length) + ' rows dropped')

      df['VIGUEUR'] = df['VIGUEUR'].apply(lambda x : 0 if x == 'vieillissement dépérissement' else
                                          1 if x == 'vigueur intermédiaire' else 3)
      return df 

#%%
def convert_coordinates(df):
    #Define coordinate conversion functions
    inProj = pyproj.Proj("+init=EPSG:3945")
    outProj = pyproj.Proj("+init=EPSG:4326")

    #Convert coordinates to latitude and longitude
    df[['latitude', 'longitude']] = df.apply(lambda row: pd.Series(pyproj.transform(inProj, outProj, float(row['coord_x']), float(row['coord_y']))), axis=1)

    #Drop the original coordinate columns
    df.drop(columns=['coord_x', 'coord_y'], inplace=True)

    # Process ADR_SECTEUR column
    secteur_mapping = {1: 0, 3: 1, 6: 2, 4: 3, 5: 4, 2: 5}
    df['ADR_SECTEUR'] = df['ADR_SECTEUR'].map(secteur_mapping)

    return df

#%%
def traitement_process(df):
      #%% ANNEEREALISATIONDIAGNOSTIC
      #We simply propose to remove values that have not been diagnosed, because there are few
      length = len(df)
      df.drop(df[df.ANNEEREALISATIONDIAGNOSTIC == '?'].index, inplace=True)
      new_length = len(df)
      print(str(length-new_length) + ' rows dropped')

      #%%
      #There are several values not entered in the ANNEETRAVAUXPRECONISESDIAG field. We cannot remove them
      #We must either assign them a value or remove the column

      #Let’s see if there is a clear link with the date of the previous diagnistic:
      df[df.ANNEETRAVAUXPRECONISESDIAG != '?']['ANNEETRAVAUXPRECONISESDIAG'].astype('float64').corr(df[df.ANNEETRAVAUXPRECONISESDIAG != '?']['ANNEEREALISATIONDIAGNOSTIC'].astype('float64'))
      df[df.ANNEETRAVAUXPRECONISESDIAG != '?']['ANNEETRAVAUXPRECONISESDIAG'].astype('float64').corr(df[df.ANNEETRAVAUXPRECONISESDIAG != '?']['DEFAUT'].astype('float64'))
      
      #The correlation is at 0.38 which is average
      

      diff = df[df.ANNEETRAVAUXPRECONISESDIAG != '?']['ANNEETRAVAUXPRECONISESDIAG'].astype('float64') - df[df.ANNEETRAVAUXPRECONISESDIAG != '?']['ANNEEREALISATIONDIAGNOSTIC'].astype('float64')
      diff.mean() # 2 year difference aproximatively

      #Let’s try to give to the missing values the date of the last daiagnostic + 2, after converting the values to int
      df.loc[df.ANNEETRAVAUXPRECONISESDIAG == '?', 'ANNEETRAVAUXPRECONISESDIAG'] = df[df.ANNEETRAVAUXPRECONISESDIAG == '?']['ANNEEREALISATIONDIAGNOSTIC'].astype('float64') + 2
      df = df.astype({"ANNEETRAVAUXPRECONISESDIAG": int , 'ANNEEREALISATIONDIAGNOSTIC' : int})

      #%%
      #Create a classe TETEDECHAT, LIERRE and CEPEE
      df['TETEDECHAT'] = df['REMARQUES'].apply(lambda x: 1 if bool(re.search(" chat", x)) else 0)
      df['LIERRE'] = df['REMARQUES'].apply(lambda x: 1 if bool(re.search("lierr*e", x, re.IGNORECASE)) else 0)
      df['CEPEE'] = df['REMARQUES'].apply(lambda x: 1 if bool(re.search("cépée", x, re.IGNORECASE)) else 0)

      #The REMARQUES column can now be removed and processing is complete.
      df.drop(columns=['REMARQUES'], inplace=True)

      df = df.reset_index()
      return df

#%%
def save_data(df):      
      df.to_csv('data/donnees-traitees.csv')

#%%
import time as time
start = time.time()
df = pd.read_csv("data/donnees-defi-egc.csv")
remove_useless_values()
remove_missing_values(df)
df = replace_missing_values(df)
df = process_data(df)
df = convert_coordinates(df)
df = traitement_process(df)
save_data(df)

print(time.time() - start)