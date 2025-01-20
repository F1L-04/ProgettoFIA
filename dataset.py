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


#print( nan_count)

#Stampa tutte le righe
#pd.set_option("display.max_rows", None)


#Eliminazione righe con valori nulli
df.dropna(inplace= True)

#Verifica della corrette eliminazione delle righe nulle 
nan_mask = df.isna()
nan_count = nan_mask.sum()


#print( nan_count)

#print(df.describe)

# Applicato al dataset la funzione per aggiungere la colonna mood
df['mood'] = df.apply(f.assign_mood, axis=1)
 
#print(df)

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

# Verifica le dimensioni dei dataset
#print(f"Dimensioni train_set: {train_set.shape}")
#print(f"Dimensioni test_set: {test_set.shape}")


# Esporta i due dataset se necessario
train_set.to_csv('train_set.csv', index=False)
test_set.to_csv('test_set.csv', index=False)


#Stampa del conteggio dei mood
print(train_set['mood'].value_counts())

#print(train_set)
#print(test_set)

# Chiedi all'utente di scegliere un mood
user_mood = input("Scegli un mood (Felicità, Relax, Tristezza, Carica,Ballabile): ")

# Filtra il DataFrame per il mood selezionato
mood_set = train_set[train_set['mood'] == user_mood]

mood_st=mood_set


# Preprocessing: Selezioniamo solo le colonne numeriche per il clustering
features = mood_st[['valence_%', 'energy_%', 'danceability_%', 'bpm', 'acousticness_%']]

# Normalizzazione delle caratteristiche
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Creare una copia esplicita di mood_st per evitare il problema del SettingWithCopyWarning
mood_st = mood_st.copy()

# Clustering: KMeans
kmeans = KMeans(n_clusters=2, random_state=42)
mood_st['cluster'] = kmeans.fit_predict(scaled_features)

# Analisi dei cluster: Calcoliamo la media solo per le colonne numeriche
numeric_columns = mood_st.select_dtypes(include=['float64', 'int64']).columns
cluster_means = mood_st.groupby('cluster')[numeric_columns].mean()

# Stampa dei risultati
print(cluster_means)


# Visualizza tutte le canzoni per cluster
for i in range(2): 
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
