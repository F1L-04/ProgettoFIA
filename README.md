Moodify - Playlist Generator

Questo progetto nasce dall’idea di sfruttare tecniche avanzate di intelligenza artificiale per trasformare il modo in cui gli utenti interagiscono 
con la musica, basandosi sulle loro emozioni. Alla base del sistema vi è un’analisi dettagliata delle caratteristiche musicali di ciascun brano, 
come energia, ballabilità, positività, tempo.
Tali informazioni vengono poi utilizzate per associare ogni canzone a un determinato stato emotivo (o “mood”), come gioia, malinconia, 
rilassatezza o adrenalina.
Il cuore del progetto è rappresentato da un algoritmo di clustering, che raggruppa i brani con mood simili in playlist coerenti. 
Ad esempio, un mood “energico” potrebbe generare una playlist perfetta per un allenamento, mentre un mood “rilassato” potrebbe offrire 
una collezione di brani ideali per un momento di calma.

All'interno di questo repository sono presenti:
 - Dataset di partenza (spotify-2023.csv);
 - Documentazione - Presentazione del progetto;
 - File contenenti le operazioni di lettura, pulizia del dataset iniziale e la suddivisione in test_set e train_set (dataset.py);
 - I dataset di training e di testing;
 - File contenenti i metodi per la grafica dell'interfaccia utente (mainGrafica.py) e per l'implementazione di spotify (PlaylistSpotify.py);
 - Il dataset contenete l'elenco di tutte le canzoni della playlist generata (Playlist_scelta.csv);
 - File contenten le funzioni per l'assegnazione del mood alle canzoni (funzioni.py).

Procedimento

1-Caricamento del dataset:
Il dataset spotify-2023.csv viene caricato e alcune colonne non necessarie vengono rimosse per ottimizzare l'analisi.

2-Pulizia dei dati:
Sono stati rimossi i valori nulli per garantire l'integrità dei dati durante l'analisi.

3-Assegnazione del mood:
Utilizzando una funzione personalizzata (assign_mood), a ciascun brano viene assegnato un mood basato sui parametri delle canzoni.
I mood includono: Felicità, Relax, Tristezza, Carica e Ballabile.

4-Visualizzazione dei dati:
Sono stati creati grafici di distribuzione e scatter plot per visualizzare i mood e la distribuzione delle canzoni nei diversi gruppi.

5-Suddivisione del dataset:
Il dataset è stato diviso in due parti: 70% per il training e 30% per il testing. Entrambi i dataset sono stati esportati in formato CSV (train_set.csv e test_set.csv).

6-Filtro basato sul mood dell'utente:
È stato chiesto all'utente di selezionare un mood tra i seguenti: Felicità, Relax, Tristezza, Carica o Ballabile.
I brani del dataset di test sono stati filtrati in base al mood selezionato dall'utente.

7-Calcolo di nuove metriche personalizzate:
Sono state calcolate quattro nuove metriche per analizzare ulteriormente i brani:
Dance-Valence Ratio: Rapporto tra ballabilità e felicità.
Energy-Acoustic Difference: Differenza tra energia e componente acustica.
Energy-Dance Combo: Prodotto tra energia e ballabilità.
Acoustic-Valence Combo: Prodotto tra componente acustica e felicità.

8-Clustering con KMeans:
Utilizzando il numero dinamico di cluster (calcolato in base alla dimensione del dataset filtrato), i brani sono stati raggruppati in cluster omogenei.
È stata calcolata la media delle metriche numeriche per ogni cluster.

9-Visualizzazione dei cluster:
Le componenti principali dei dati sono state ridotte a due dimensioni tramite PCA.
È stato generato un grafico scatter per visualizzare i cluster.

10-Generazione di playlist personalizzate:
È stata selezionata casualmente una playlist da uno dei cluster generati.
La playlist scelta è stata esportata in formato CSV con il nome Playlist_scelta.csv.

11-Caricamento playlist su spotify
La playlist generata è stata caricata all'interno di spotify, attraverso le funzioni della libreria spotipy.

Output generato
Grafici di visualizzazione dei mood e dei cluster.
File CSV:
train_set.csv e test_set.csv: Dataset suddivisi per training e testing.
Playlist_scelta.csv: Playlist basata sul mood dell'utente e sul clustering.
Informazioni sui cluster e sulle canzoni presenti in ciascun gruppo.
