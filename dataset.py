import pandas as pd
import funzioni as f
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

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


#print(train_set)
#print(test_set)

# Chiedi all'utente di scegliere un mood
user_mood = input("Scegli un mood (Felicità, Relax, Tristezza, Carica,Ballabile): ")

# Filtra il DataFrame per il mood selezionato
playlist = train_set[train_set['mood'] == user_mood]

# Controlla se ci sono almeno 50 canzoni nel mood selezionato
if len(playlist) >= 50:
    # Seleziona 50 canzoni randomiche
    random_playlist = playlist.sample(n=50, random_state=42)  # random_state garantisce risultati ripetibili
else:
    # Se ci sono meno di 30 canzoni, usa tutte le canzoni disponibili
    random_playlist = playlist
    print(f"Attenzione: ci sono solo {len(playlist)} canzoni disponibili per il mood selezionato.")

# Mostra alcune canzoni
print(random_playlist[['track_name', 'artist(s)_name']].head())

# Salva la playlist personalizzata
random_playlist.to_csv(f'{user_mood}_playlist.csv', index=False)
print(f"Playlist salvata in {user_mood}_playlist.csv")

assert random_playlist.duplicated(subset=['track_name', 'artist(s)_name']).sum() == 0, "Ci sono duplicati nella playlist!"

Playlist=pd.read_csv(f'{user_mood}_playlist.csv',encoding="latin1")


# Preprocessing: Selezioniamo solo le colonne numeriche per il clustering
features = Playlist[['valence_%', 'energy_%', 'danceability_%', 'bpm', 'acousticness_%']]

# Normalizzazione delle caratteristiche
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Clustering: KMeans
kmeans = KMeans(n_clusters=2, random_state=42)
Playlist['cluster'] = kmeans.fit_predict(scaled_features)

# Analisi dei cluster: Calcoliamo la media solo per le colonne numeriche
numeric_columns = Playlist.select_dtypes(include=['float64', 'int64']).columns
cluster_means = Playlist.groupby('cluster')[numeric_columns].mean()

# Stampa dei risultati
print(cluster_means)


# Visualizza tutte le canzoni per cluster
for i in range(2): 
    print(f"\nCluster {i}:")
    print(Playlist[Playlist['cluster'] == i][['track_name', 'artist(s)_name', 'cluster']])



#PCA per ridurre la dimensionalità
pca = PCA(n_components=2)  # Riduciamo a 2 dimensioni
pca_components = pca.fit_transform(scaled_features)

# Aggiungiamo i componenti PCA al dataset
Playlist['pca1'] = pca_components[:, 0]
Playlist['pca2'] = pca_components[:, 1]

# Visualizzazione dei cluster con PCA
plt.figure(figsize=(10, 8))
sns.scatterplot(x='pca1', y='pca2', hue='cluster', palette='Set1', data=Playlist, s=100, alpha=0.7, edgecolor='k')

# Aggiungi titoli e altre etichette
plt.title('Visualizzazione dei Cluster con PCA')
plt.xlabel('Componente Principale 1')
plt.ylabel('Componente Principale 2')
plt.legend(title='Cluster')
plt.savefig('cluster.png')










