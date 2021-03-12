# Befehle zum Bespaßen des pis

Denk dran, dass du mit Pfeiltasten nach oben und unten die letzten Befehle durchsuchen kannst.

Die Tab-Taste ist die Autovervollständigung im Terminal.

## Befehle auf deinem MacBook

* ssh pi@192.168.178.116 - auf dem Pi anmelden um dort ein Skript ausführen zu können. Danach kannst du ein neues Terminal aufmachen um auf deinem Macbook weiter zu arbeiten
* ls - zeigt alle Dateien an die sich im Pfad befinden wo du gerade bist
* cd "Verzeichnis" - wechselt in das Verzeichnis
* cd .. - wechselt in das Verzeichnis wieder eine Ebene höher
* scp Menschaergeredichnicht.py pi@192.168.178.116:/home/pi - kopiert dein Skript auf den Pi

## Befehle auf dem Pi

* python3 Menschaergeredichnicht.py - führt dein Python Script aus