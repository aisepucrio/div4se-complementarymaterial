import pandas as pd
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
file_path = 'I&D4SE.xlsx'
df = pd.read_excel(file_path, usecols=['Como você se identifica em relação à sua orientação sexual?  ', 
                                       'Qual(is) dos tipos de discriminação você acha que são mais recorrentes dentro da área de desenvolvimento de software?'])

# Rename columns for simplicity
df.columns = ['sexuality', 'discrimination']

# Drop rows with missing 'sexuality' values
df = df.dropna(subset=['sexuality'])

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
sexuality_mapping = {
    'Heterossexual': 'Heterosexual',
    'Homossexual': 'LGBTQ+',
    'Bissexual': 'LGBTQ+',
    'Pansexual': 'LGBTQ+',
    'Prefiro não responder': 'Id rather not answer',
    'Não sei': 'Id rather not answer'
}

# Map the sexualities to the new categories
df['sexuality_english'] = df['sexuality'].map(sexuality_mapping)

# Ensure there are no null values in the 'sexuality_english' column
df['sexuality_english'] = df['sexuality_english'].fillna('Id rather not answer')

# Re-encode 'sexuality_english' to ensure 'Id rather not answer' is the last category
df['sexuality_english'] = pd.Categorical(df['sexuality_english'], 
                                         categories=[cat for cat in df['sexuality_english'].unique() if cat != 'Id rather not answer'] + ['Id rather not answer'], 
                                         ordered=True)

df['sexuality_english_codificado'] = df['sexuality_english'].cat.codes

# Create a matrix of the sum of discrimination types grouped by the new encoded sexuality with adjusted order
matriz_english = df.groupby('sexuality_english_codificado')[list(discrimination_mapping.keys())].sum().T

# Plot the heatmap with the new categories in the desired order
plt.figure(figsize=(10, 7))
sns.heatmap(matriz_english, annot=True, cmap='Blues', xticklabels=df['sexuality_english'].cat.categories, yticklabels=list(discrimination_mapping.keys()))
plt.xlabel('Sexual orientation')
plt.ylabel('Types of discrimination')
plt.show()
