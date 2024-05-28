pyinstaller --onefile --distpath . ^
--add-data "text.json:." ^
--add-data "images\back.png:." ^
--add-data "images\background.png:." ^
--add-data "images\building.png:." ^
kash.py
rmdir /s /q build
del kash.spec