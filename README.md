#  Persönliche Finanzverwaltung (Python)

Ein Konsolenprogramm zur Verwaltung persönlicher Finanzen.  
Mit diesem Tool kannst du **Einnahmen und Ausgaben erfassen, analysieren, visualisieren und speichern**.  
Die Anwendung unterstützt **JSON- und CSV-Speicherung** sowie grafische Auswertungen mit Matplotlib.  

---

##  Funktionen

- **Transaktionen hinzufügen**  
  Erfasse Einnahmen oder Ausgaben mit Datum, Betrag, Kategorie und optionaler Beschreibung.

- **Transaktionen anzeigen**  
  Gibt eine Übersicht aller Transaktionen aus.

- **Finanzbilanz berechnen**  
  Summiert alle Einnahmen und Ausgaben und zeigt die aktuelle Bilanz an.

- **Ausgabenanalyse nach Kategorien**  
  Gruppiert Ausgaben nach Kategorien (z. B. Lebensmittel, Miete, Transport).

- **Diagramme erstellen**  
  - Balkendiagramm: Einnahmen, Ausgaben, Bilanz  
  - Kuchendiagramm: Ausgaben nach Kategorien  
  Speichert Diagramme als `finanzbericht.png`.

- **Daten speichern**  
  Speichert alle Transaktionen in einer **JSON-Datei** (`finanzdaten.json`).  

- **Export als CSV**  
  Speichert alle Transaktionen zusätzlich als **CSV-Datei** (`finanzdaten.csv`).  

- **Daten laden**  
  Lädt beim Start automatisch gespeicherte Transaktionen aus `finanzdaten.json`.  

---

##  Installation

1. Python (>=3.8) installieren.  
2. Repository/Datei herunterladen.  
3. Abhängigkeiten installieren:

```bash
pip install matplotlib pandas
```
