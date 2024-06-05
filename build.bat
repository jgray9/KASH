pyinstaller --onefile --distpath . ^
--add-data "departments.json:." ^
--add-data "images\back.png:." ^
--add-data "images\background.png:." ^
--add-data "images\background_2.png:." ^
--add-data "images\info_board.png:." ^
--add-data "images\sign.png:." ^
kash.py
rmdir /s /q build
del kash.spec