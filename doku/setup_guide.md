# Setup Guide (Einsteiger)

Dieses Projekt nutzt eine lokale virtuelle Umgebung (venv). Die Schritte unten funktionieren auf
Windows sowie auf Mac/Linux.

1. Stelle sicher, dass Python 3.10 oder neuer installiert ist.
2. Oeffne ein Terminal und wechsle in den Projektordner.
3. Erstelle die virtuelle Umgebung und installiere die Abhaengigkeiten.
Windows: `setup_env.bat`
Mac/Linux: `bash setup_env.sh`
4. Falls die Umgebung nach dem Skript nicht aktiv ist, aktiviere sie manuell.
Windows: `.venv\Scripts\activate`
Mac/Linux: `source .venv/bin/activate`
5. Starte die Anwendung.
Windows: `python src\main.py`
Mac/Linux: `python src/main.py`

Wenn alles korrekt eingerichtet ist, erscheint ein Fenster mit der GUI. Dort kannst du eine
Airfoil-Datei laden und die Kurve sofort anzeigen lassen.
