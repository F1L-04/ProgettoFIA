#Suddivido i mood in categorie.
#Felicità: Canzoni con valenza alta, energia medio-alta.
#Relax: Canzoni con valenza medio-alta, energia bassa, acousticness alta.
#Tristezza: Canzoni con valenza bassa, energia bassa.
#Carica: Canzoni con energia alta, bpm elevato. 
#Ballabile:Canzoni con danceability elevata.


#Assegno un Mood alle Canzoni
#derivo la variabile mood con la regola basate su soglie

def assign_mood(row):
    if row['valence_%'] >= 70 and row['energy_%'] >= 60:
        return 'Felicità'
    elif row['acousticness_%'] >= 80 and row['energy_%'] < 40:
        return 'Relax'
    elif row['valence_%'] <= 30 and row['energy_%'] <= 40:
        return 'Tristezza'
    elif row['energy_%'] >= 70 and row['bpm'] >= 120:
        return 'Carica'
    elif row['danceability_%'] >= 80:
        return 'Ballabile'
    else:
        return 'Neutro'