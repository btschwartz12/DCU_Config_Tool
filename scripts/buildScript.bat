@echo off
:: Installation instructions and script for SRFN Config Tool
::
:: Aclara 2022
::
::
::=============================================================================
:: Step 1: Install required packages/software
::
:: Required:
::      - python (3+)
::      - pip 
::          python -m pip install --upgrade pip
::          pip install get-pip.py
::      - tkinter 
::          pip install tk
::      - xmlschema 
::          pip install xmlschema
::      - xlwings
::          pip install xlwings
:: 
:: Optional:
::      - auto-py-to-exe (if build needs to be modified in future)
::          pip install auto-py-to-exe
::=============================================================================
:: Step 2: Initialize environment variables
::
    set "ScriptName=app.py"
::      - name of the python file that will be executed (has root window tk.tK())
    set "BasePathPython=C:/Users/70060/AppData/Local/Programs/Python/Python310"
::      - where python.exe and the 'lib/' directory is stored
    set "Source=C:\Users\70060\Documents\DCU_Config_Tool\"
::      - where source code and script is stored
    set "Python=%BasePathPython%/python.exe"
::      - python executable, not required for now
    set "PackageSource=%BasePathPython%/lib/site-packages"
::      - where packages are located to be loaded into the executable
::=============================================================================
:: Step 3: Add required packages
::
    set "XMLSCHEMA_pkg=%PackageSource%/xmlschema;xmlschema/"
    set "OPENPYXL_pkg=%PackageSource%/openpyxl;openpyxl/"
    set "icon=data/misc;aclara.png"
::      - This will imported using pyinstaller --add-data
::
:: For future packages that need to be included, follow the same 
:: format as above, and just add another --add-data to the 
:: pyinstaller command below
::      - ex. 'pyinstaller ... --add-data %A_pkg% --add-data %B_pkg% ...' 
::=============================================================================

:: pyinstaller converts python source to an executable
pyinstaller --noconfirm --onefile --console --add-data "%XMLSCHEMA_pkg%" --add-data "%OPENPYXL_pkg%" --add-data "%icon%" "%Source%%ScriptName%"

::=============================================================================
:: Step 4: Initialize executable's directory
::
::      - For the app to function, there must exist a directory 'config/' in
::          the same directory as the executable, and this 'config/' 
::          directory MUST have:
::              - options.json 
::              - wkst_config.json
::      - For now....
            mkdir dist\config
            echo f | xcopy /i /y /f config\options.json dist\config\options.json
            echo f | xcopy /i /y /f config\wkst_config.json dist\config\wkst_config.json
::=============================================================================
