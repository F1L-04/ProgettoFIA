import pandas as pd
import funzioni as f
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import random

from sklearn.model_selection import train_test_split
pd.__version__

spotify_dataset = pd.read_csv('spotify-2023.csv', encoding='latin1')

# Stampa le prime righe del DataFrame
spotify_dataset


# Rimuovere colonne specifiche (ad esempio, 'colonna1' e 'colonna2')
df = spotify_dataset.drop(['artist_count', 'in_spotify_charts', 'in_apple_charts', 'in_deezer_charts', 'in_shazam_charts', 'released_month', 'released_day'], axis=1)

#Controllo Valori nulli
nan_mask = df.isna()
nan_count = nan_mask.sum()


#Eliminazione righe con valori nulli
df.dropna(inplace= True)

#Verifica della corrette eliminazione delle righe nulle 
nan_mask = df.isna()
nan_count = nan_mask.sum()


# Applicato al dataset la funzione per aggiungere la colonna mood
df['mood'] = df.apply(f.assign_mood, axis=1)


#Visualizzo i Mood

#Scatter Plot: Confronta valence ed energy per vedere la distribuzione dei mood.
#sns.scatterplot(data=df, x='valence_%', y='energy_%', hue='mood')
#plt.title('Distribuzione dei Mood')
#plt.savefig('scatterplot.png')

#Grafico di distribuzione
#sns.countplot(x='mood', data=df)
#plt.title('Distribuzione dei Mood')
#plt.savefig('grafico.png')

#Stampa del conteggio dei mood
print(df['mood'].value_counts())

# Dividi il dataset in 70% training e 30% testing
train_set, test_set = train_test_split(df, test_size=0.3, random_state=42)

# Esporta i due dataset se necessario
train_set.to_csv('train_set.csv', encoding='utf-8', index=False)
test_set.to_csv('test_set.csv', encoding='utf-8', index=False)


#Stampa del conteggio dei mood
print(test_set['mood'].value_counts())

# Chiedi all'utente di scegliere un mood
user_mood = input("Scegli un mood (Felicità, Relax, Tristezza, Carica,Ballabile): ")

# Filtra il DataFrame per il mood selezionato
mood_set = test_set[test_set['mood'] == user_mood]

mood_st=mood_set.copy()

#Ballabilità vs Felicità:
#•    Quanto una canzone è ballabile rispetto a quanto è felice.
#Energia vs Acustica:
#•    Differenza tra energia e la componente acustica, che indica quanto una canzone è “potente” rispetto alla sua dolcezza.
#Energia × Ballabilità:
#•    Un indicatore che combina il livello di energia e la ballabilità.
#Acustica × Felicità:
#•    Indica tracce acustiche che mantengono una positività elevata.

mood_st['dance_valence_ratio'] = mood_st['danceability_%'] / (mood_st['valence_%'] + 1e-5)
mood_st['energy_acoustic_diff'] = mood_st['energy_%'] - mood_st['acousticness_%']
mood_st['energy_dance_combo'] = mood_st['energy_%'] * mood_st['danceability_%']
mood_st['acoustic_valence_combo'] = mood_st['acousticness_%'] * mood_st['valence_%']

print(mood_st)

# Preprocessing: Selezioniamo solo le colonne numeriche per il clustering
features = mood_st[['dance_valence_ratio', 'energy_acoustic_diff', 'energy_dance_combo', 'acoustic_valence_combo']]

# Normalizzazione delle caratteristiche
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Clustering: KMeans
n_clusters = f.dynamic_clusters(len(mood_st))
kmeans = KMeans(n_clusters, random_state=42)
mood_st['cluster'] = kmeans.fit_predict(scaled_features)

# Analisi dei cluster: Calcoliamo la media solo per le colonne numeriche
numeric_columns = mood_st.select_dtypes(include=['float64', 'int64']).columns
cluster_means = mood_st.groupby('cluster')[numeric_columns].mean()

# Stampa dei risultati
print(cluster_means)


# Visualizza tutte le canzoni per cluster
for i in range(n_clusters): 
    print(f"\nCluster {i}:")
    print(mood_st[mood_st['cluster'] == i][['track_name', 'artist(s)_name', 'cluster']])


# Riduzione delle dimensioni a 2 componenti principali usando PCA
pca = PCA(n_components=2, random_state=42)
reduced_features = pca.fit_transform(scaled_features)

# Aggiungere le componenti principali al DataFrame
mood_st['PCA1'] = reduced_features[:, 0]
mood_st['PCA2'] = reduced_features[:, 1]

# Visualizzazione dei cluster
plt.figure(figsize=(10, 7))
for cluster in mood_st['cluster'].unique():
    cluster_data = mood_st[mood_st['cluster'] == cluster]
    plt.scatter(cluster_data['PCA1'], cluster_data['PCA2'], label=f'Cluster {cluster}', s=50)

plt.title('Visualizzazione dei cluster (PCA)')
plt.xlabel('PCA1')
plt.ylabel('PCA2')
plt.legend()
plt.grid(True)
plt.savefig("cluster.png")

indice=random.randint(1,kmeans.n_clusters)-1
print(indice)
playlist_scelta=mood_st[mood_st['cluster']==indice][['track_name', 'artist(s)_name', 'cluster']]
print(playlist_scelta)

playlist_scelta.to_csv(f'Playlist_scelta.csv', encoding='utf-8', index=False)
print(f"Playlist_scelta salvata")
