import pandas as pd
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
file_path = 'I&D4SE.xlsx'
df = pd.read_excel(file_path, usecols=['Como você se identifica em relação à sua identidade de gênero?', 
                                       'Qual(is) dos tipos de discriminação você acha que são mais recorrentes dentro da área de desenvolvimento de software?'])

# Rename columns for simplicity
df.columns = ['gender', 'discrimination']

# Drop rows with missing 'gender' values
df = df.dropna(subset=['gender'])

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
gender_mapping = {
    'Homem Cisgênero': 'Cis/Trans Man',
    'Homem trans': 'Cis/Trans Man',
    'Mulher Cisgênero': 'Cis/Trans Woman',
    'Mulher trans': 'Cis/Trans Woman',
    'Não-binário': 'Others',
    'Bigênero': 'Others',
    'Prefiro não responder': 'Others'
}

# Map the sexualities to the new categories
df['gender_english'] = df['gender'].map(gender_mapping)

# Ensure there are no null values in the 'gender_english' column
df['gender_english'] = df['gender_english'].fillna('Others')

# Re-encode 'gender_english' to ensure 'Others' is the last category
df['gender_english'] = pd.Categorical(df['gender_english'], 
                                         categories=[cat for cat in df['gender_english'].unique() if cat != 'Others'] + ['Others'], 
                                         ordered=True)

df['gender_english_codificado'] = df['gender_english'].cat.codes

# Create a matrix of the sum of discrimination types grouped by the new encoded gender with adjusted order
matriz_english = df.groupby('gender_english_codificado')[list(discrimination_mapping.keys())].sum().T

# Plot the heatmap with the new categories in the desired order
plt.figure(figsize=(10, 7))
sns.heatmap(matriz_english, annot=True, cmap='Blues', xticklabels=df['gender_english'].cat.categories, yticklabels=list(discrimination_mapping.keys()))
plt.xlabel('Gender Identity')
plt.ylabel('Types of discrimination')
plt.show()