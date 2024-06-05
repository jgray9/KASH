pyinstaller --onefile --distpath . ^
--add-data "departments.json:." ^
--add-data "images\back.png:." ^
--add-data "images\back_highlighted.png:." ^
--add-data "images\background.png:." ^
--add-data "images\background_2.png:." ^
--add-data "images\info_board.png:." ^
--add-data "images\sign.png:." ^
--add-data "images\sign_highlighted.png:." ^
--add-data "images\search_bar.png:." ^
kash.py
rmdir /s /q build
del kash.spec