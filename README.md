## Thinker Modul x Fifa Sim
>[!NOTE]
>Ladet euch alles runter,
>(wenn ihr auf Windows seit ändert den namen von `thinker` zu `thinker.exe`)
>und führt die Datei aus

>[!WARNING]
>Führt diesen Befehl unbeding aus!
>```bash
>pip install -r requirements.txt
>```
    

>[!IMPORTANT]
>Alles muss in einem Ordner sein

>[!TIP]
>Öffnen sie die Datei `ergebnisse.db` mit dem [DB Browser für SQLight](https://sqlitebrowser.org/) damit sie die Ergebnisse der vorherigen Simulationen sehen können
>Wenn ihr eure eigene exe machen wollt, führt aus:
>```bash
>pip install pyinstaller
> 
>pyinstaller --onefile thinker-src-code.py
>```
>Nach dem es fertig ist, wird die datei hier sein: `/fifa-thinker-main/dist` . ihr müsst nur noch den suffix ".exe" anheften und ausführen
