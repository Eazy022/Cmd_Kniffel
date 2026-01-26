[README.txt](https://github.com/user-attachments/files/24857312/README.txt)
Dokumentation Fuer Cmd-Kniffel

Kniffel  Konsolenbasiertes Multiplayer-Spiel mit Login-System
Überblick:
Dieses Python-Projekt implementiert das Wuerfelspiel Kniffel fuer 2-4 Spieler in der Konsole.
Es enthält ein vollständiges Login- und Registrierungssystem über SQLite, eine lokale Punktetabelle und alle typischen Kniffel-Kategorien.
Das Spiel wird rundenbasiert gespielt, jeder Spieler würfelt bis zu dreimal pro Runde und wählt anschließend eine Kategorie, in der die Punkte eingetragen werden.

Setup und Ausführung
Voraussetzungen
     Python 3.8 oder höher
     SQLite (in Python-Standardbibliothek enthalten)
Installation & Start
    1. Den Code als kniffel.py speichern
    2. Script ausführen:

Struktur der Hauptfunktionen

1. Datenbank & Login (init_db,register,login,login_screen)

Diese Funktionen verwalten Benutzerkonten:

     init_db() erstellt die SQLite-Datenbank mit einer Tabelle users.
     register() fügt neue Benutzer mit gehashtem Passwort hinzu.
     login() überprüft Benutzername und Passwort.
     login_screen() bietet ein Menü zur Anmeldung oder Registrierung.
      
Die Passwörter werden sicher mit SHA-256 gehasht

2. Würfelfunktionen (roll_dice)

     roll_dice(num_dice=5) gibt eine Liste mit fünf Zufallswerten (1-6) zurück.
     In jeder Runde kann der Spieler bis zu dreimal würfeln, wobei bestimmte Würfel gezielt neu geworfen werden können.

3. Punktelogik & Kategorien
Jede Bewertungsfunktion entspricht einer Kniffel-Kategorie:

    pips_sum(n, dice)  Summe aller Würfel mit der Zahl n
    three_of_a_kind(dice)  mind. drei gleiche: Summe aller Augen
    four_of_a_kind(dice)  mind. vier gleiche: Summe aller Augen
    full_house(dice)  3+2 Kombination: 25 Punkte
    small_straight(dice)  Sequenz von 4 Zahlen: 30 Punkte
    large_straight(dice)  Sequenz von 5 Zahlen: 40 Punkte
    kniffel(dice)  alle fünf gleich: 50 Punkte
    chance(dice)  Summe aller Würfel
      
Die Kategorien sind in CATEGORIES definiert und werden dynamisch angezeigt.

4. Spieler- und Punktetabellen (create_empty_scoreboard, show_player_table)

     create_empty_scoreboard() üerzeugt eine leere Punkteliste mit None-Werten.
     show_player_table() zeigt den aktuellen Punktestand eines Spielers nach Oberem und Unterem Block an.
     total_score() summiert alle Punkte für die Gesamtauswertung.


5. Spielablauf (welcome_menu, play_game_complete)
     welcome_menu() erstellt Spielerliste, führt Login durch und startet das Spiel.
     play_game_complete() enthält die Hauptspiellogik:
        ? Rundenschleifen über alle Spieler
        ? Würfeln mit bis zu drei Würfen
        ? Kategorieauswahl & Punkteberechnung
        ? Beenden über Ctrl+C mit Sicherheitsabfrage
        ? Am Ende: Finales Ranking mit Medallienanzeige

6. Sicherheitsmechanismus (safe_exit)

Bei Abbruch (q oder Ctrl+C) wird nach Bestätigung der Zwischenstand aller Spieler ausgegeben, um Fortschritt nicht zu verlieren.

Designüberlegungen

     Konsolenbedienung: Einfach und interaktiv mit klaren Symbolen .
     Datensicherheit: Passwörter niemals im Klartext gespeichert.
     Robustheit: Fehlerabfang bei SQLite-Operationen und Benutzereingaben.
     Erweiterbarkeit: Neue Kategorien oder Features (z.?B. Boni, Highscore-Tabelle) können leicht ergänzt werden.

 Mögliche Erweiterungen

     Speicherung und Fortsetzung laufender Spiele.
     Grafische Benutzeroberfläche (z.?B. mit Tkinter oder Pygame).
     Online-Multiplayer-Modus über Socket-Kommunikation.
     Highscore-Liste der Spieler in der Datenbank.


