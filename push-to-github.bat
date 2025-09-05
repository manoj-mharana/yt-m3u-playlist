@echo off
REM ===== GitHub Repo Auto Push Script =====

REM 🔹 अपने project folder में जाएँ
cd /d "D:\YouTube Live News Channels\New folder"

REM 🔹 Repo initialize करें (अगर पहले से init नहीं है तो)
git init

REM 🔹 Remote set करें (अगर पहले से add है तो error ignore कर दें)
git remote remove origin
git remote add origin https://github.com/manoj-mharana/yt-m3u-playlist.git

REM 🔹 Files add और commit करें
git add .
git commit -m "Initial commit"

REM 🔹 Branch को main पर set करें
git branch -M main

REM 🔹 GitHub पर push करें
git push -u origin main

pause