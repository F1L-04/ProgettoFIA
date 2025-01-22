import funGrafica as OG

import gradio as gr
import pandas as pd
import random
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


# Interfaccia
interfaccia = gr.Interface(
    fn=OG.genera_playlist,
    inputs=gr.Dropdown(["Felicità", "Tristezza", "Relax", "Carica", "Ballabile", "Neutro"], label="Seleziona un mood"),
    outputs=[gr.DataFrame(label="Playlist generata"), gr.File(label="Scarica CSV")],
    title="Generatore di Playlist",
)

interfaccia.launch(share=True)