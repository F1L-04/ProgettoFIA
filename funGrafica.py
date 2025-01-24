import pandas as pd
import funzioni as f
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import random
import playlistSpotify as spotify

from sklearn.model_selection import train_test_split
pd.__version__

def genera_playlist(user_mood):
  train_set=pd.read_csv('test_set.csv', encoding='utf-8')
  print(train_set.head()['mood']) 
  print("USER_MOOD "+user_mood)
  train_set['mood'] = train_set['mood'].str.strip()  # Rimuove gli spazi extra
  # Filtra il DataFrame per il mood selezionato
  mood_set = train_set[train_set['mood'] == user_mood]#user_mood]

  mood_st=mood_set.copy()

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

  # Creare una copia esplicita di mood_st per evitare il problema del SettingWithCopyWarning
  #mood_st = mood_st.copy()

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

  playlist_scelta.to_csv(f'Playlist_scelta.csv', index=False)
  filePath='Playlist_scelta.csv'
  print(f"Playlist_scelta salvata")

  link_playlist=spotify.manage_playlist(playlist_scelta)

  return playlist_scelta,filePath,link_playlist
