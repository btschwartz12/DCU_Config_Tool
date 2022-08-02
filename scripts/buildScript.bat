@echo off
:: Installation script for the DCU Config Tool
::
:: Ben Schwartz
:: Aclara 2022
::
::
::=============================================================================
:: Step 1: Initialize environment variables
::
    set "Source=C:\Users\70060\Documents\DCU_Config_Tool\"
::      - where source code and script is stored
    set "SpecPath=%Source%/app.spec"
::      - where packages are located to be loaded into the executable
::=============================================================================
:: Step 2: Create the executable using the .spec file
    pyinstaller "%SpecPath%"
::=============================================================================
:: Step 3: Initialize executable's directory
::
::      - For the app to work properly, there must exist a directory 'config/' in
::          the same directory as the executable, and this 'config/' 
::          directory MUST have:
::              - options.json 
::              - wkst_config.json
::      - For now....
            mkdir dist\config
            echo f | xcopy /i /y /f config\options.json dist\config\options.json
            echo f | xcopy /i /y /f config\wkst_config.json dist\config\wkst_config.json
::=============================================================================
