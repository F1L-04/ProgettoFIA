import pandas as pd

from sklearn.model_selection import train_test_split
pd.__version__

spotify_dataset = pd.read_csv('spotify-2023.csv', encoding='latin1')

# Stampa le prime righe del DataFrame
spotify_dataset


# Rimuovere colonne specifiche (ad esempio, 'colonna1' e 'colonna2')
df = spotify_dataset.drop(['artist_count', 'in_spotify_charts', 'in_apple_charts', 'in_deezer_charts', 'in_shazam_charts', 'released_month', 'released_day', 'key', 'mode'], axis=1)

# Dividi il dataset in 70% training e 30% testing
train_set, test_set = train_test_split(df, test_size=0.3, random_state=42)

# Verifica le dimensioni dei dataset
print(f"Dimensioni train_set: {train_set.shape}")
print(f"Dimensioni test_set: {test_set.shape}")

# Esporta i due dataset se necessario
train_set.to_csv('train_set.csv', index=False)
test_set.to_csv('test_set.csv', index=False)

train_set
test_set
