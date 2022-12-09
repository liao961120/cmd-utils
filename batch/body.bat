@ECHO OFF
:: body file.txt <#from> <#to>

IF "%2"=="" ( SET "from=1" ) ELSE ( SET "from=%2" )
IF "%3"=="" ( SET "to=$" ) ELSE ( SET "to=%3" )

REM ECHO FROM %from%
REM ECHO TO   %to%

C:\Users\rd\bin\unix\sed\bin\sed.exe  -n %from%,%to%p %1

ECHO:
:: PAUSE