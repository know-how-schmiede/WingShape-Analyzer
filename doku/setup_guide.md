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

## EXE erstellen (Windows)

Vorgehensweise:

1. Aktiviere deine virtuelle Umgebung (`.venv`).
2. Installiere PyInstaller:

```bash
pip install pyinstaller
```

3. Erstelle die EXE mit folgendem Befehl im Terminal:

```bash
pyinstaller --noconfirm --onedir --windowed --add-data "src;src" --collect-all customtkinter src/main.py
```

Erklaerung der Parameter:

- `--onedir`: Erstellt einen Ordner mit der EXE und allen notwendigen DLLs (stabiler fuer komplexe Bibliotheken wie Matplotlib).
- `--windowed`: Verhindert, dass beim Starten ein schwarzes Konsolen-Fenster im Hintergrund aufpoppt.
- `--collect-all customtkinter`: Wichtig! Stellt sicher, dass die Themes und Grafiken von CustomTkinter mit eingepackt werden.

## 2. Schritt: Eine Setup.exe (Installer) erstellen

Die erstellte EXE aus Schritt 1 laeuft zwar, besteht aber aus vielen Dateien in einem Ordner.
Um eine einzige Setup.exe zu erhalten, die das Programm unter Windows \"richtig\" installiert
(mit Desktop-Icon und Deinstallations-Eintrag), nutzt man externe Tools.

Empfehlung: Inno Setup (Klassiker)
Inno Setup ist kostenlos, extrem stabil und Industriestandard fuer Windows-Installer.

1. Lade Inno Setup herunter und installiere es.
2. Starte den Inno Setup Script Wizard.
3. Waehle deine `main.exe` (aus dem `dist`-Ordner von PyInstaller) als Hauptdatei aus.
4. Fuege den gesamten Ordner hinzu, in dem die EXE liegt, damit alle Abhaengigkeiten dabei sind.

Der Wizard generiert am Ende eine einzige Datei: `mysetup.exe`.

## Inno Setup Script (empfohlen)

Im Ordner `installer/inno/` liegt ein fertiges Script: `WingShape-Analyzer.iss`.

Schritte:

1. Erstelle die EXE (Ordner-Version) mit PyInstaller:

```bash
pyinstaller --noconfirm --onedir --windowed --name WingShape-Analyzer --add-data "src;src" --add-data "data;data" --add-data "doku;doku" --collect-all customtkinter src/main.py
```

Hinweis: Fuehre den Befehl im Projekt-Root aus (dort, wo `src/` liegt).
Falls du im Ordner `installer/` bist, zuerst: `cd ..`

2. Oeffne `installer/inno/WingShape-Analyzer.iss` in Inno Setup.
3. Aktualisiere die Versionsdatei fuer Inno Setup:

```bash
python installer/inno/update_version.py
```

4. Optional: Lege ein Icon unter `installer/assets/app.ico` ab.
5. Klicke auf **Compile**. Die fertige Setup-Datei liegt danach in `installer/output/`.

Optionaler Helper (Windows):

```bat
installer\\build_installer.bat
```

Dieses Skript aktualisiert zuerst die Version und startet dann den Inno Setup Compiler.
