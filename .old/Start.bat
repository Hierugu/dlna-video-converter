@echo on
set "sourcedir=.\INPUT"
set "outputdir=.\OUTPUT"

PUSHD "%sourcedir%"
for %%F in (*.mp4) DO ffmpeg -i "%%F" ..\OUTPUT\%%F
POPD

PUSHD "%outputdir%"
for %%F in (*.mp4) DO ffmpeg -i "%%F" -acodec copy -vcodec copy -f mpegts %%F.ts
for %%F in (*.ts) DO echo file %%F >> list.txt
ffmpeg -f concat -i list.txt -vf scale=-1:1080 -c:a aac -c:v libx264 -profile:v high -level:v 4.2 -r 60 ..\Result.mkv
del list.txt
del *.ts
POPD
pause
pause
