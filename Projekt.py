import matplotlib.pyplot as plt
from datetime import datetime
import json
import os
import pandas as pd

# Globale Variablen
transaktionen = []
kategorien = {
    'Einnahmen': ['Gehalt',  'Kindergeld', 'Geschenke'],
    'Ausgaben': ['Lebensmittel', 'Miete', 'Transport', 'Unterhaltung', 'Sparbuch', 'Kleidung', 'Gesundheit']
}

# Funktionen
def transaktion_hinzufügen():
    """Fügt eine neue Transaktion hinzu"""
    print("\n--- Neue Transaktion hinzufügen ---")
    
    # Datum eingeben
    while True:
        try:
            datum_str = input("Datum (TT.MM.JJJJ) oder heute: ")
            if datum_str.lower() == 'heute' or datum_str == '':
                datum = datetime.now().date()
            else:
                datum = datetime.strptime(datum_str, "%d.%m.%Y").date()
            break
        except ValueError:
            print("Ungültiges Datum! Bitte im Format TT.MM.JJJJ eingeben.")
    
    # Betrag eingeben
    while True:
        try:
            betrag = float(input("Betrag: "))
            break
        except ValueError:
            print("Ungültiger Betrag! Bitte Zahl eingeben.")
    
    # Typ auswählen
    print("\nTyp auswählen:")
    print("1. Einnahme")
    print("2. Ausgabe")
    while True:
        typ_wahl = input("Wahl (1-2): ")
        if typ_wahl in ['1', '2']:
            typ = 'Einnahme' if typ_wahl == '1' else 'Ausgabe'
            break
        print("Ungültige Wahl!")
    
    # Kategorie auswählen
    print(f"\nVerfügbare {typ} Kategorien:")
    kategorie_liste = kategorien['Einnahmen'] if typ == 'Einnahme' else kategorien['Ausgaben']
    
    for i, kat in enumerate(kategorie_liste, 1):
        print(f"{i}. {kat}")
    
    while True:
        try:
            kat_wahl = int(input(f"Kategorie wählen (1-{len(kategorie_liste)}): "))
            if 1 <= kat_wahl <= len(kategorie_liste):
                kategorie = kategorie_liste[kat_wahl - 1]
                break
            print("Ungültige Wahl!")
        except ValueError:
            print("Bitte Zahl eingeben!")
    
    # Beschreibung
    beschreibung = input("Beschreibung (optional): ")
    
    # Transaktion speichern
    transaktion = {
        'id': len(transaktionen) + 1,
        'datum': datum.strftime("%d.%m.%Y"),
        'betrag': betrag,
        'typ': typ,
        'kategorie': kategorie,
        'beschreibung': beschreibung
    }
    
    transaktionen.append(transaktion)
    print(f"\nTransaktion erfolgreich hinzugefügt! (ID: {transaktion['id']})")

def transaktionen_anzeigen():
    """Zeigt alle Transaktionen an"""
    if not transaktionen:
        print("\nKeine Transaktionen vorhanden.")
        return
    
    print(f"\n--- Alle Transaktionen ({len(transaktionen)}) ---")
    for trans in transaktionen:
        vorzeichen = "+" if trans['typ'] == 'Einnahme' else "-"
        print(f"ID: {trans['id']} | {trans['datum']} | {vorzeichen}{abs(trans['betrag']):.2f}€ | "
              f"{trans['kategorie']} | {trans['beschreibung']}")

def bilanz_berechnen():
    """Berechnet die aktuelle Bilanz"""
    einnahmen = sum(t['betrag'] for t in transaktionen if t['typ'] == 'Einnahme')
    ausgaben = sum(t['betrag'] for t in transaktionen if t['typ'] == 'Ausgabe')
    bilanz = einnahmen - ausgaben
    
    print("\n--- Finanzbilanz ---")
    print(f"Einnahmen gesamt: +{einnahmen:.2f}€")
    print(f"Ausgaben gesamt: -{ausgaben:.2f}€")
    print(f"Bilanz: {bilanz:+.2f}€")
    
    return einnahmen, ausgaben, bilanz

def kategorie_analyse():
    """Analysiert Ausgaben nach Kategorien"""
    if not transaktionen:
        print("\nKeine Transaktionen für Analyse vorhanden.")
        return
    
    print("\n--- Ausgabenanalyse nach Kategorien ---")
    
    # Dictionary für Kategorieausgaben
    kategorie_ausgaben = {kat: 0 for kat in kategorien['Ausgaben']}
    
    for trans in transaktionen:
        if trans['typ'] == 'Ausgabe' and trans['kategorie'] in kategorie_ausgaben:
            kategorie_ausgaben[trans['kategorie']] += trans['betrag']
    
    # Ausgaben nach Kategorie anzeigen
    for kategorie, betrag in kategorie_ausgaben.items():
        if betrag > 0:
            print(f"{kategorie}: {betrag:.2f}€")

def diagramm_erstellen():
    """Erstellt Diagramme zur Visualisierung"""
    if not transaktionen:
        print("\nKeine Transaktionen für Diagramme vorhanden.")
        return
    
    # Daten für Diagramme vorbereiten
    einnahmen, ausgaben, bilanz = bilanz_berechnen()
    
    # Ausgaben nach Kategorie
    ausgaben_kategorien = {}
    for trans in transaktionen:
        if trans['typ'] == 'Ausgabe':
            if trans['kategorie'] not in ausgaben_kategorien:
                ausgaben_kategorien[trans['kategorie']] = 0
            ausgaben_kategorien[trans['kategorie']] += trans['betrag']
    
    # Diagramm erstellen
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Balkendiagramm für Einnahmen/Ausgaben
    labels = ['Einnahmen', 'Ausgaben', 'Bilanz']
    werte = [einnahmen, ausgaben, bilanz]
    farben = ['green', 'red', 'blue' if bilanz >= 0 else 'red']
    
    ax1.bar(labels, werte, color=farben)
    ax1.set_title('Finanzübersicht')
    ax1.set_ylabel('Betrag (€)')
    
    # Kuchendiagramm für Ausgabenkategorien
    if ausgaben_kategorien:
        kategorien = list(ausgaben_kategorien.keys())
        betraege = list(ausgaben_kategorien.values())
        
        ax2.pie(betraege, labels=kategorien, autopct='%1.1f%%')
        ax2.set_title('Ausgaben nach Kategorien')
    
    plt.tight_layout()
    plt.savefig('finanzbericht.png')
    print("\nDiagramm wurde als 'finanzbericht.png' gespeichert!")
    plt.show()

def daten_speichern():
    """Speichert Transaktionen in JSON-Datei"""
    with open('finanzdaten.json', 'w', encoding='utf-8') as f:
        json.dump(transaktionen, f, ensure_ascii=False, indent=2)
    print("Daten erfolgreich gespeichert!")

def daten_laden():
    """Lädt Transaktionen aus JSON-Datei"""
    global transaktionen
    try:
        if os.path.exists('finanzdaten.json'):
            with open('finanzdaten.json', 'r', encoding='utf-8') as f:
                transaktionen = json.load(f)
            print("Daten erfolgreich geladen!")
        else:
            print("Keine gespeicherten Daten gefunden.")
    except Exception as e:
        print(f"Fehler beim Laden: {e}")

def daten_speichern_csv():
    """Speichert Transaktionen in CSV-Datei"""
    df = pd.DataFrame(transaktionen)
    df.to_csv('finanzdaten.csv', index=False, sep=',', encoding='utf-8')
    print("Daten erfolgreich als 'finanzdaten.csv' gespeichert!")

def hauptmenü():
    # Daten laden
    daten_laden()
    """Hauptmenü der Anwendung"""
    while True:
        print("\n" + "="*50)
        print(" PERSÖNLICHE FINANZVERWALTUNG")
        print("="*50)
        print("1. Neue Transaktion hinzufügen")
        print("2. Alle Transaktionen anzeigen")
        print("3. Finanzbilanz berechnen")
        print("4. Ausgabenanalyse nach Kategorien")
        print("5. Diagramme erstellen")
        print("6. Daten speichern")
        print("7. als csv speichern")
        print("8. Beenden")
        print("="*50)

        wahl = input("Ihre Wahl (1-8): ")

        if wahl == '1':
            transaktion_hinzufügen()
        elif wahl == '2':
            transaktionen_anzeigen()
        elif wahl == '3':
            bilanz_berechnen()
        elif wahl == '4':
            kategorie_analyse()
        elif wahl == '5':
            diagramm_erstellen()
        elif wahl == '6':
            daten_speichern()
        elif wahl == '7':
            daten_speichern_csv()
        elif wahl == '8':
            print("Auf Wiedersehen!")
            break
        else:
            print("Ungültige Eingabe! Bitte 1-8 wählen.")

# Hauptprogramm
if __name__ == "__main__":
    print("Willkommen beim Finanzverwaltungs-Tool!")
    hauptmenü()

