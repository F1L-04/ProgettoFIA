import funGrafica as OG
import gradio as gr
import pandas as pd


# Funzione che genera la playlist, il link Spotify e il file CSV
def genera_playlist_e_link(mood):
    # Genera la playlist e ottieni il link Spotify
    playlist_df,filePath, spotify_link = OG.genera_playlist(mood)
    
    # Crea il link Spotify come HTML
    spotify_html = f'<a href="{spotify_link}" target="_blank">Ascolta su Spotify</a>'
    
    # Restituisce la playlist come DataFrame, il link HTML e il file CSV
    return playlist_df, spotify_html, filePath

# Interfaccia
interfaccia = gr.Interface(
    fn=genera_playlist_e_link,
    inputs=gr.Dropdown(["Felicità", "Tristezza", "Relax", "Carica", "Ballabile"], label="Seleziona un mood"),
    outputs=[gr.DataFrame(label="Playlist generata"), 
             gr.HTML(label="Link Spotify"),
             gr.File(label="Scarica CSV")], 
    title="Generatore di Playlist",
)

interfaccia.launch(share=True)