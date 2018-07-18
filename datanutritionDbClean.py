# Ce programme prend en entrée la base de données nutrionnelle complète et génère en sortie la base nettoyée pour permettre l'analyse exploratoire des données
# nom du fichier entrée : fr.openfoodfacts.org.products.csv
# nom du ficher sortie : fr.openfoodfacts.org.products-cleaned.csv
# Les fichers doivent être dans le même répertoire que le programme


# Importation des librairies
import numpy as np
import pandas as pd

# variables 

# nom du fichier input
in_file='fr.openfoodfacts.org.products.csv'
# nom du fichier sortie
out_file='fr.openfoodfacts.org.products-cleaned.csv'

# Chargement de fichier de données
# on utilise le paramètre low_memory=false pour éviter le warning
print("Reading input file : " + in_file)
data = pd.read_csv(in_file,sep='\t',low_memory=False)
print("Dataset successfully loaded")

###############
# Data cleaning
###############
print("Starting data cleaning")

# Suppression des colonnes avec plus de 40% de valeur NaN
data=data[data.columns[data.isnull().mean() < 0.4]]


# Filtre les produits uniquement disponible en France
data = data[data['countries_fr'] == "France"]
# on supprime la colonne countries_fr qui ne sert plus car données filtrées
del data['countries_fr']

# Suppression des produits dont le nom de produit est vide car inutile pour notre analyse
data = data.dropna(subset=['product_name'])

# Suppression des lignes avec plus de 70% de valeurs vides
t = len(data.columns)*0.7
data = data.dropna(thresh=t)


####################
# Feature selection
####################

# On ne conserve que les features qui nous paraissent pertinentes pour l'analyse
data = data[['product_name' , 'brands_tags' , 'nutrition_grade_fr' , 'energy_100g' , 'fat_100g' , 
             'saturated-fat_100g' , 'carbohydrates_100g' , 'sugars_100g' , 'fiber_100g' , 'proteins_100g' , 
             'salt_100g' , 'nutrition-score-fr_100g' , 'nutrition-score-uk_100g']]

print("Data successfully cleaned.")

# Génération du fichier de sortie correspondant au fichier nettoyé
data.to_csv(out_file,sep="\t", index=False)
print("Output file generated : " + out_file)
