#Suddivido i mood in categorie.
#Felicità: Canzoni con valenza alta, energia medio-alta.
#Relax: Canzoni con valenza medio-alta, energia bassa, acousticness alta.
#Tristezza: Canzoni con valenza bassa, energia bassa.
#Carica: Canzoni con energia alta, bpm elevato. 
#Ballabile:Canzoni con danceability elevata.


#Assegno un Mood alle Canzoni
#derivo la variabile mood con la regola basate su soglie

def assign_mood(row):
    if row['valence_%'] >= 65 and row['energy_%'] >= 55 and row['danceability_%'] >= 60:
        return 'Felicità'  # Ridotte leggermente le soglie
    elif row['energy_%'] <= 60 and row['valence_%'] >= 20 and row['valence_%'] <= 70 and row['acousticness_%'] >= 35 and row['bpm'] <= 130:
        return 'Relax'  # Maggiore tolleranza su bpm e acousticness
    elif row['valence_%'] <= 40 and row['energy_%'] <= 50 and row['acousticness_%'] >= 25:
        return 'Tristezza'  # Soglie più ampie
    elif row['energy_%'] >= 60 and row['valence_%'] >= 25 and row['valence_%'] <= 80 and row['bpm'] >= 110:
        return 'Carica'  # Aumentato il range di valence
    elif row['danceability_%'] >= 60 and row['bpm'] >= 80 and row['bpm'] <= 160 and row['energy_%'] >= 35:
        return 'Ballabile'  # Maggiore flessibilità su energia e bpm
    else:
        # Logica di fallback per ridurre i Neutri
        if row['valence_%'] >= 50 or row['energy_%'] >= 50:
            return 'Felicità'
        elif row['acousticness_%'] >= 25 and row['bpm'] <= 110:
            return 'Relax'
        elif row['energy_%'] >= 55 and row['bpm'] >= 100:
            return 'Carica'
        elif row['danceability_%'] >= 50:
            return 'Ballabile'
        else:
            return 'Neutro'
