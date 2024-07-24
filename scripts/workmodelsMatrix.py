import pandas as pd
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
file_path = 'I&D4SE.xlsx'
df = pd.read_excel(file_path, usecols=['Qual seu modelo de trabalho?', 
                                       'Qual(is) dos tipos de discriminação você acha que são mais recorrentes dentro da área de desenvolvimento de software?'])

# Rename columns for simplicity
df.columns = ['wm', 'discrimination']

# Drop rows with missing 'wm' values
df = df.dropna(subset=['wm'])

# Fill missing 'discrimination' values with empty strings
df['discrimination'] = df['discrimination'].fillna('')

# Define the list of discrimination types with their Portuguese equivalents
discrimination_mapping = {
    'Sexism': 'Machismo',
    'Racism': 'Racismo',
    'Elitism': 'Elitismo',
    'Ageism': 'Etarismo',
    'Ableism': 'Capacitismo'
}

# Create a column for each discrimination type
for disc, term in discrimination_mapping.items():
    df[disc] = df['discrimination'].apply(lambda x: 1 if isinstance(x, str) and term.lower() in x.lower() else 0)

# Define mapping for sexualities to English and create new unified categories
wm_mapping = {
    'Remoto': 'Remote',
    'Hibrido': 'Hybrid',
    'Presencial': 'On-site',
}

# Map the sexualities to the new categories
df['wm_english'] = df['wm'].map(wm_mapping)

# Ensure there are no null values in the 'wm_english' column
df['wm_english'] = df['wm_english'].fillna('Id rather not answer')

# Re-encode 'wm_english' to ensure 'Id rather not answer' is the last category
df['wm_english'] = pd.Categorical(df['wm_english'], 
                                         categories=[cat for cat in df['wm_english'].unique() if cat != 'Id rather not answer'], 
                                         ordered=True)

df['wm_english_codificado'] = df['wm_english'].cat.codes

# Create a matrix of the sum of discrimination types grouped by the new encoded wm with adjusted order
matriz_english = df.groupby('wm_english_codificado')[list(discrimination_mapping.keys())].sum().T

# Plot the heatmap with the new categories in the desired order
plt.figure(figsize=(10, 7))
sns.heatmap(matriz_english, annot=True, cmap='Blues', xticklabels=df['wm_english'].cat.categories, yticklabels=list(discrimination_mapping.keys()))
plt.xlabel('Work Models')
plt.ylabel('Types of discrimination')
plt.show()
