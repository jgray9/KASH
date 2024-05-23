pyinstaller --onefile --distpath . ^
--add-data "text.json:." ^
--add-data "images\back.png:." ^
--add-data "images\pin.png:." ^
--add-data "images\road.png:." ^
kash.py
rmdir /s /q build
del kash.spec