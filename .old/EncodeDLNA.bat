@echo on
set "sourcedir=.\INPUT"
set "outputdir=.\OUTPUT"

PUSHD "%outputdir%"
for %%F in (*.mp4) DO ffmpeg -i "%%F" -vf scale=-1:1080 -c:a aac -c:v libx264 -profile:v high -level:v 4.2 -r 60 "%%F.mkv"
POPD

pause
pause