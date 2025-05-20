@echo on
set "sourcedir=.\INPUT"
set "outputdir=.\OUTPUT"

PUSHD "%sourcedir%"
for %%F in (*.mp4) DO ffmpeg -i "%%F" "..\OUTPUT\%%F"
POPD

pause
pause