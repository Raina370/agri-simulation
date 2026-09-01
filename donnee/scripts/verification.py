import pandas as pd

df = pd.read_csv("donnee/csv_extraits/cultures.csv")

print("Aperçu des données :")
print(df)

print("\nValeurs manquantes par colonne :")
print(df.isna().sum())