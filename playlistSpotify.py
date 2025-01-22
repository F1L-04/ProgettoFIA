import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

# Configura le credenziali di Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="7a8f41fa05dd4f98b30102a1b8e1f826",        # Sostituisci con il tuo Client ID
    client_secret="cf7cb59199c948ab83e76df023c6f559", # Sostituisci con il tuo Client Secret
    redirect_uri="http://localhost:8888/callback",  # URI configurato su Spotify Developer
    scope="playlist-modify-private playlist-modify-public"  # Permessi per la modifica di playlist pubbliche e private
))


# Ottieni l'URL di autorizzazione
#auth_url = sp.auth_manager.get_authorize_url()
#print(f"Visita questo link per autenticarti: {auth_url}")

# Dopo aver autorizzato, copia e incolla il codice qui
#authorization_code = input("Inserisci il codice di autorizzazione che ottieni dopo aver autorizzato l'accesso: ")

# Usa il codice per ottenere il token di accesso
#sp.auth_manager.get_access_token(authorization_code)

# Verifica se l'autenticazione è stata completata correttamente
#user_id = sp.me()['id']
#print(f"Autenticazione completata! ID utente: {user_id}")


# ID della playlist esistente (sostituisci con l'ID della playlist che vuoi modificare)
playlist_id = "1EDCrFThjnlM8eZx63FtqW"  # Playlist ID che vuoi usare

# Funzione per verificare se la playlist è vuota
def is_playlist_empty(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    return len(results['items']) == 0

# Funzione per svuotare la playlist
def clear_playlist(playlist_id):
    sp.playlist_replace_items(playlist_id, [])  # Rimuove tutte le tracce
    print("Playlist svuotata!")

# Funzione per cercare una traccia su Spotify usando nome e artista
def search_track(name, artist):
    query = f"track:{name} artist:{artist}"
    result = sp.search(query, type="track", limit=1)  # Limita la ricerca a 1 risultato
    tracks = result['tracks']['items']
    
    if tracks:
        track_uri = tracks[0]['uri']  # Prendi l'URI del primo risultato
        print(f"Trovata traccia: {tracks[0]['name']} - {tracks[0]['artists'][0]['name']}")
        return track_uri
    else:
        print(f"Traccia '{name}' di '{artist}' non trovata!")
        return None

# Funzione per aggiungere brani alla playlist
def add_tracks_to_playlist(playlist_id, track_uris):
  # Dividi le tracce in batch di 100
  for i in range(0, len(track_uris), 100):
      track_batch = track_uris[i:i + 100]
      try:
          # Aggiungi il batch di tracce alla playlist
          sp.playlist_add_items(playlist_id, track_batch)
          print(f"Aggiornamento della playlist con {len(track_batch)} tracce completato.")
      except Exception as e:
          print(f"Errore nell'aggiungere le tracce: {e}")

# Funzione per rimuovere brani specifici dalla playlist
def remove_tracks_from_playlist(playlist_id, track_uris):
    sp.playlist_remove_items(playlist_id, track_uris)
    print("Brani rimossi dalla playlist!")

# Funzione principale che gestisce la playlist
def manage_playlist(playlist):
    # Verifica se la playlist è vuota
    if not is_playlist_empty(playlist_id):
        print("La playlist non è vuota, svuotando...")
        clear_playlist(playlist_id)  # Svuota la playlist se non è vuota

    # Carica il CSV con i dati delle canzoni
    #df = pd.read_csv('Playlist_scelta.csv')  # Assicurati che il percorso del CSV sia corretto

    # Assicurati che il CSV abbia le colonne "Nome" e "Artista" (o i nomi delle colonne corretti)
    tracks_to_add = [(row['track_name'], row['artist(s)_name']) for _, row in playlist.iterrows()]

    # Cerca le tracce e ottieni gli URI
    track_uris_to_add = [search_track(name, artist) for name, artist in tracks_to_add]
    track_uris_to_add = [uri for uri in track_uris_to_add if uri is not None]

    # Aggiungi i brani alla playlist
    if track_uris_to_add:
        add_tracks_to_playlist(playlist_id, track_uris_to_add)
