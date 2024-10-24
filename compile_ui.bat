@ECHO OFF

set OSGEO4W_ROOT=C:\OSGeo4W
set PATH=%PATH%;%OSGEO4W_ROOT%\apps\qgis\bin;%OSGEO4W_ROOT%\bin


@echo off
call %OSGEO4W_ROOT%\bin\o4w_env.bat
@echo off


cd /d %~dp0

@ECHO ON      

::Resources
call pyrcc5 ui\resources.qrc -o ui\resources_rc.py
::call pyuic5 ui\ui_BaseDialog.ui -o gui\ui_BaseDialog.py 

@ECHO OFF
GOTO END

:ERROR
   echo "Failed!"
   set ERRORLEVEL=%ERRORLEVEL%
   pause

:END
@ECHO ON