import os

#Remove dll file otherwise it will be injected on start up
try:
    files_to_remove = ["d3d11.dll", "powrprof.dll"]

    for file_name in files_to_remove:
        file_path = os.path.join(os.getcwd(), file_name)

        if os.path.exists(file_path):
            os.remove(file_path)
except Exception as e:
    print(f"Error while removing dll files: {e}")

from PyQt5.QtWidgets import QProgressBar, QApplication, QMessageBox, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QDialog, QStyle, QCheckBox, QSlider, QSizePolicy, QComboBox, QStyledItemDelegate
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QPixmap, QIcon, QMovie, QPalette
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl, QTimer, QSize
from PyQt5 import QtCore
import multiprocessing
import configparser
import subprocess
import threading
import requests
import zipfile
import shutil
import random
import json
import time
import sys

import socket
import urllib

global done
done = False

GITHUB_REPO = "bodnjenie14/Project_-bo4_Launcher"
GITHUB_REPO = "unknown43253252352352/Project-BO4-Launcher"

def update_settings(key, value):
    config = configparser.ConfigParser()
    print("settings")
    if not os.path.exists(os.path.join(os.getcwd(), "files", "settings.ini")):
        config.add_section('Launcher Settings')
        config.set('Launcher Settings', 'volume', '30')
        config.set('Launcher Settings', 'reshade', 'False')
        config.set('Launcher Settings', 'link', '')

        with open(os.path.join(os.getcwd(), "files", "settings.ini"), 'w') as configfile:
            config.write(configfile)

        print("Default INI file 'settings.ini' has been created.")
        return
    
    if(key is None or value is None):
        print("returned update settings")
        return

    config.read(os.path.join(os.getcwd(), "files", "settings.ini"))
    print("settings updated")

    config.set('Launcher Settings', key, value)

    with open(os.path.join(os.getcwd(), "files", "settings.ini"), 'w') as configfile:
        config.write(configfile)

def get_settings(key):
    update_settings(None, None)

    print("settings " + key)
    config = configparser.ConfigParser()
    config.read(os.path.join(os.getcwd(), "files", "settings.ini"))
    value = config.get('Launcher Settings', key)
    print(value)
    return value

global reshade
reshade = bool(get_settings("reshade"))

def get_json_item(json_path, spot, name):
    try:
        if os.path.exists(json_path):
            with open(json_path, "r") as json_file:
                data = json.load(json_file)
                print(data[spot][name])
        else:
            print("Creating default json")

            try:
                name = f'{os.getlogin()}'
            except Exception as e:
                print(f"Error aquiring username: {e}")
                name = "Unknown Soldier" 

            data = {
                "demonware":
                {
                    "ipv4": "78.157.42.107" #bods server
                },
                "identity":
                {
                    "name":  name,
                }
            }
            json_data = json.dumps(data, indent=4) 

            with open(json_path, "w") as json_file:
                json_file.write(json_data)

            return get_json_item(json_path, spot, name)

        return data[spot][name]
    except Exception as e:
        print(f"Something went wrong while reading json file: {e}")
        
class change_name(QDialog):
    def __init__(self, parent=None):
        super(change_name, self).__init__(parent)
        
        self.setWindowTitle("Set Name")
        self.setWindowIcon(self.style().standardIcon(getattr(QStyle, 'SP_MessageBoxInformation')))
        
        layout = QVBoxLayout()

        self.title = QLabel(f"Enter new name (Current name: {get_json_item('project-bo4.json', 'identity', 'name')})")
        layout.addWidget(self.title)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText(f"Enter Name: ")
        
        input_field_width = 300
        self.input_field.setFixedWidth(input_field_width)
        layout.addWidget(self.input_field)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

        self.setLayout(layout)

        self.setStyleSheet("""
            QDialog {
                background-color: #333;
                color: white;
            }
            QLabel {
                color: white;
            }
            QLineEdit {
                background-color: #555;
                color: white;
                border: 1px solid #444;
            }
            QPushButton {
                background-color: #555;
                color: white;
                border: 1px solid #444;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """)

class change_ip(QDialog):
    def __init__(self, parent=None):
        super(change_ip, self).__init__(parent)
        
        self.setWindowTitle("Set IP address")
        self.setWindowIcon(self.style().standardIcon(getattr(QStyle, 'SP_MessageBoxInformation')))
        
        layout = QVBoxLayout()
        ip_address = get_json_item('project-bo4.json', 'demonware', 'ipv4')
        if ip_address == "":
            ip_address = "None"

        self.title = QLabel(f"Select server IP address (Current IP Address: {ip_address})")

        layout.addWidget(self.title)

        input_layout = QHBoxLayout()
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Add new IP address to list")
        input_field_width = 300
        self.input_field.setFixedWidth(input_field_width)
        input_layout.addWidget(self.input_field) 

        self.add_button = QPushButton("Add") 
        self.add_button.clicked.connect(self.add_value) 
        input_layout.addWidget(self.add_button) 
        
        layout.addLayout(input_layout)  

        self.comboBox = QComboBox(self)
        layout.addWidget(self.comboBox)
        self.comboBox.setStyleSheet("background-color: #555; color: white;")

        self.generade_dropdown_menu()

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

        self.setLayout(layout)

        self.setStyleSheet("""
            QDialog {
                background-color: #333;
                color: white;
            }
            QLabel {
                color: white;
            }
            QLineEdit {
                background-color: #555;
                color: white;
                border: 1px solid #444;
            }
            QPushButton {
                background-color: #555;
                color: white;
                border: 1px solid #444;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """)

    def add_value(self):
        print(f"input {self.input_field.text()}")

        empty = False
        file_path = os.path.join(os.getcwd(), 'files', 'Ip_address.txt') 

        if not os.path.exists( file_path ):
            with open(file_path, 'w') as file:
                file.write(f"Empty\n")

        input_text = file_path.rstrip('\n')

        if self.input_field.text() != "":

            with open(file_path, 'r') as file:
                lines = file.readlines()
                if lines[0].strip() == "Empty":
                    empty = True

            if empty:
                with open(file_path, 'w') as file:
                    file.write(f"{self.input_field.text()}\n")
            else:
                with open(file_path, 'a') as file:
                    file.write(f"{self.input_field.text()}\n")
            
            self.generade_dropdown_menu()

    def generade_dropdown_menu(self):
        self.comboBox.clear()
        file_path = os.path.join(os.getcwd(), 'files', 'Ip_address.txt')

        if not os.path.exists( file_path ):
            with open(file_path, 'w') as file:
                file.write(f"Empty\n")

        with open(file_path, 'r') as file:
            for line in file:
                print(line, end='')
                self.comboBox.addItem( line.strip() )

def replace_json_value(json_file_path, value, spot, key):
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
            data[spot][key] = value

        with open(json_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
    except Exception as e:
        print(f"Something went wrong while modifying Json file: {e}")

class launcher(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setWindowTitle('Project-BO4')
        self.setWindowIcon(QIcon(os.path.join('files', 'images', 'exe_icon_bo4.ico')))
        title_layout = QVBoxLayout()

        try:
            images_folder = os.path.join(os.getcwd(), 'files', 'images')
            files = [f for f in os.listdir(images_folder) if f.lower().endswith(('.gif', '.jpg', '.jpeg', '.jfif', '.pjpeg', '.pjp', '.png'))]
            random_background = random.choice(files)

            if random_background.lower().endswith(('.gif')):
                self.movie = QMovie(os.path.join(os.getcwd(), 'files', 'images', random_background))
                background_label = QLabel(self)
                layout.addWidget(background_label)
                background_label.setMovie(self.movie)
                self.movie.start()

                self.setStyleSheet("background-color: #333;")

                buttons_layout = QHBoxLayout()
                checkbox = QCheckBox("DXVK / Reshade compatibility")
                buttons_layout.addWidget(checkbox)
                checkbox.setChecked(bool(get_settings("reshade")))
                checkbox.stateChanged.connect(self.checkbox_state_change)

            elif random_background.lower().endswith(('.jpg', '.jpeg', '.jfif', '.pjpeg', '.pjp', '.png')):
                background_label = QLabel(self)
                background_image = QPixmap(os.path.join(os.getcwd(), 'files', 'images', random_background))
                background_label.setPixmap(background_image)
                background_label.setGeometry(0, 0, background_image.width(), background_image.height())
                self.setFixedSize(background_image.width(), background_image.height())

                self.title = QLabel("")
                title_layout.addWidget(self.title)
                layout.addLayout(title_layout)

                check_box = QVBoxLayout()

                checkbox = QCheckBox("DXVK / Reshade compatibility")
                check_box.addWidget(checkbox)

                bool_value = get_settings("reshade")
                if bool_value == "True":
                    bool_value = True
                else:
                    bool_value = False
                checkbox.setChecked(bool_value)

                checkbox.stateChanged.connect(self.checkbox_state_change)
                layout.addLayout(check_box)

            try:
                sound_folder = os.path.join(os.getcwd(), 'files', 'sounds')
                sound_files = [f for f in os.listdir(sound_folder) if f.lower().endswith('.mp3')]
                random_sound_file = random.choice(sound_files)

                sound_path = os.path.join(sound_folder, random_sound_file)

                self.player = QMediaPlayer()
                sound_url = QUrl.fromLocalFile(sound_path)
                content = QMediaContent(sound_url)
                self.player.setMedia(content)
                self.player.setVolume(int(get_settings("volume")))
                self.player.play()

            except Exception as e:
                print(f"Something went wrong with start-up sound files: {e}")

        except Exception as e:
            print(f"Something went wrong with start up image, gif, or sound files: {e}")

        try:
            if not random_background.lower().endswith(('.gif')):
                buttons_layout = QHBoxLayout()

            self.volume_slider = QSlider(Qt.Horizontal)
            self.volume_slider.setMinimum(0)
            self.volume_slider.setMaximum(100)
            self.volume_slider.setValue(int(get_settings("volume")))
            self.volume_slider.valueChanged.connect(self.change_volume)
            self.volume_slider.setFixedWidth(50)
            buttons_layout.addWidget(self.volume_slider)

            self.name = QPushButton("Change Name")
            self.name.clicked.connect(self.set_name)
            self.name.setStyleSheet("background-color: #555; color: white;")
            buttons_layout.addWidget(self.name)

            self.change_ip = QPushButton("Change IP Address")
            self.change_ip.clicked.connect(self.set_ip)
            self.change_ip.setStyleSheet("background-color: #555; color: white;")
            buttons_layout.addWidget(self.change_ip)
            
            self.solo_button = QPushButton("Offline")
            self.solo_button.clicked.connect(lambda: self.start_game(which="solo"))
            self.solo_button.setStyleSheet("background-color: #555; color: white;")
            buttons_layout.addWidget(self.solo_button)

            self.Multiplayer = QPushButton("Online")
            self.Multiplayer.clicked.connect(lambda: self.start_game(which="multi"))
            self.Multiplayer.setStyleSheet("background-color: #555; color: white;")
            buttons_layout.addWidget(self.Multiplayer)

            layout.addLayout(buttons_layout)

            self.setLayout(layout)
        except Exception as e:
            print(f"Something went wrong with start up image, gif, or sound files: {e}")

    def open_new_window(self):
        if str(self.comboBox.currentText()) == "Add new IP Address":
            self.new_window = self.set_ip()

    def checkbox_state_change(self, state):
        global reshade
        if state == 2:
            reshade = True
            print("DXVK / Reshade compatibility checked")
        else:
            print("DXVK / Reshade compatibility unchecked")
            reshade = False

        update_settings("reshade", str(reshade))

    def set_ip(self):
        dialog = change_ip()
        result = dialog.exec_()

        print(f"current ip to set {dialog.comboBox.currentText()}")

        if result == QDialog.Accepted:
            ip_address = dialog.comboBox.currentText()
            if ip_address == "" or ip_address == "Empty":
                print("return")
                return

            if " " in ip_address:
                ip_address = ip_address.replace(" ", "")

            print(f"Entered IP Address: {ip_address}")
            if ip_address != "":
                replace_json_value("project-bo4.json", ip_address, 'demonware', 'ipv4')

    def set_name(self):
        dialog = change_name()
        if dialog.exec_() == QDialog.Accepted:
            name = dialog.input_field.text()
            print(f"Entered Name: {name}")
            if name != "":
                replace_json_value("project-bo4.json", name, 'identity', 'name')

    def start_game(self, which):
        global reshade
        
        if not os.path.exists(os.path.join("Players", "Mp.cfg")):
            if not os.path.exists("Players"):
                os.mkdir("Players")
            
            try:
                path_to_cfg = os.path.join(os.getcwd(), "files", "Players", "Mp.cfg")
                shutil.copy(path_to_cfg, os.getcwd())
            except Exception as e:
                print(e)

        if not os.path.exists(os.path.join(os.getcwd(), "LPC", ".manifest")) or not os.path.exists(os.path.join(os.getcwd(), "LPC", "core_ffotd_tu23_639_cf92ecf4a75d3f79.ff")) or not os.path.exists(os.path.join(os.getcwd(), "LPC", "core_playlists_tu23_639_cf92ecf4a75d3f79.ff")):
            if os.path.exists(os.path.join(os.getcwd(), "LPC")):
                try:
                    shutil.rmtree(os.path.join(os.getcwd(), "LPC"))
                except Exception as e:
                    print(e)
            
            path_to_lpc = os.path.join(os.getcwd(), "files", "LPC")
            try:
                shutil.copytree(path_to_lpc, os.path.join(os.getcwd(), "LPC"))
            except Exception as E:
                print(f"Error copying files: {E}")

        if which == "solo":
            try:
                if reshade == True:
                    path_to_dll = os.path.join(os.getcwd(), "files", "reshade_solo", "powrprof.dll")
                else:
                    path_to_dll = os.path.join(os.getcwd(), "files", "solo", "d3d11.dll")

                if os.path.exists(path_to_dll):
                    shutil.copy(path_to_dll, os.getcwd()) 
            except Exception as e:
                print(f"Error while copying dll files: {e}")

        elif which == "multi":
            try:
                if reshade == True:
                    path_to_dll = os.path.join(os.getcwd(), "files", "reshade_mp", "powrprof.dll")
                else:
                    path_to_dll = os.path.join(os.getcwd(), "files", "mp", "d3d11.dll")

                if os.path.exists(path_to_dll):
                    shutil.copy(path_to_dll, os.getcwd())
            except Exception as e:
                print(f"Error while copying dll files: {e}")

            ip_address = get_json_item('project-bo4.json', 'demonware', 'ipv4')
            if ip_address == "":
                click = set_ip()

                if click == 0:
                    return

                if ip_address == "" and click == QDialog.Accepted:
                    start_game("multi")
                    return
                else:
                    return
        try:
            window.hide()

            try:
                window.player.stop()
            except Exception as e:
                print(f"Error: {e}")

            try:
                process = subprocess.Popen(["BlackOps4.exe"])
                process.wait()
            except Exception as e:
                print(f"Error: {e}")

            sys.exit()
        except Exception as e:
            print(f"Error: {e}")

    def change_volume(self):
        volume = self.volume_slider.value()
        self.player.setVolume(volume)
        print(volume)
        update_settings("volume", str(volume))

class CustomComboBoxDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        text = index.data()
        print(text)
        palette = option.palette
        text_color = QPalette().color(QPalette.Text)
        
        if text != "Change IP Address" and text != "Add new IP Address":
            
            if self.check_server_online( text ):
                text_color = Qt.green
            else:
                text_color = Qt.red

        painter.save()
        painter.setPen(text_color)
        painter.drawText(option.rect, Qt.AlignCenter, text)
        painter.restore()

    def check_server_online(self, hostname):
        try:
            ip_address = socket.gethostbyname(hostname)
            print(f"{hostname} with IP address {ip_address} is online.")
            return True
        except (socket.gaierror, socket.herror):
            print(f"{hostname} could not be resolved or is offline.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        return False

def get_last_release_version():
    try:
        release_api_url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
        response = requests.get(release_api_url)
        response.raise_for_status()
        data = response.json()
        print(f"download link: {data['assets'][0]['browser_download_url']}")
        return data["assets"][0]["browser_download_url"]
    except requests.exceptions.RequestException as e:
        print(e)
        return None

def create_update_script(current_folder, updater_folder, program_name):
    script_content = f"""
    @echo off

    set source_folder={updater_folder}
    set destination_folder={current_folder}

    echo Terminating project-bo4.exe...
    taskkill /im "{program_name}" /t /f

    xcopy /y /e "%source_folder%" "%destination_folder%\"

    start "" "{program_name}"
    
    echo Exiting!
    exit
    """

    script_path = os.path.join(updater_folder, "project-bo4_updater.bat")
    with open(script_path, "w") as script_file:
        script_file.write(script_content)

    return script_path

def download_file(url, destination):
    if os.path.exists(destination):
        resume_byte_pos = os.path.getsize(destination)
    else:
        resume_byte_pos = 0

    headers = {'Range': f'bytes={resume_byte_pos}-'}

    while True:
        try:
            response = requests.get(url, headers=headers, stream=True, timeout=5)
            response.raise_for_status()

            with open(destination, 'ab') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"File downloaded to {destination}")
            return
        except (requests.RequestException, ConnectionError) as e:
            print(f"Error occurred during download: {e}")
            if os.path.exists(destination):
                resume_byte_pos = os.path.getsize(destination)
                headers = {'Range': f'bytes={resume_byte_pos}-'}
                print(f"Resuming download from byte position {resume_byte_pos}...")
            else:
                return

def get_download_size(url):
    try:
        d = urllib.request.urlopen( url )
        return d.info()['Content-Length']
    except Exception as E:
        print(f"Error getting file size: {E}")
    
    return None

def set_progress_bar(progressbar, file_size, output_size):
    print("progress bar started")
    progressbar.setValue(0)
    while not done:
        try:
            current_size = os.path.getsize( output_size )

            progress = int((int(current_size) / int(file_size)) * 100)
            progressbar.setValue(progress)

            if progress == 100:
                progressbar.setValue(100)
                print("break")
                break

        except Exception as e:
            print(f"Error with download bar while downloading: {e}")
        
        time.sleep(.1)
    
    progressbar.setValue(100)


def do_update(progressbar):

    global done
    done = False

    print("started")
    try:
        last = get_last_release_version()

        file_size = get_download_size(last)

        download_path = os.path.join(os.getcwd(), last.split("/")[-1] )
        absolute_path = os.path.abspath(download_path)

        progress_bar = threading.Thread(target=set_progress_bar, args=(progressbar, file_size, download_path))
        progress_bar.daemon = True
        progress_bar.start()

        try:
            download_file(last, download_path)
            done = True

            update_folder = os.path.join(os.getcwd(), "update_folder")
            if os.path.exists( update_folder ):
                try:
                    shutil.rmtree( update_folder )
                except Exception as e:
                    print(f"Error with update_folder: {e}")

            os.makedirs( update_folder )
            
            if download_path.endswith(".zip"):
                with zipfile.ZipFile(absolute_path, "r") as zip_ref:
                    done = False
                    uncompress_size = sum((file.file_size for file in zip_ref.infolist()))
                    progress_bar = threading.Thread(target=set_progress_bar, args=(progressbar, uncompress_size, update_folder))
                    progress_bar.daemon = True
                    progress_bar.start()

                    zip_ref.extractall(update_folder)
                    done = True
                    progressbar.setValue(100)
                    print("Extracted")

            if os.path.exists(absolute_path):
                os.remove(absolute_path)
                print("cleaned")

        except Exception as e:
            print(f"General Error: {e}")

        update_script = create_update_script(os.getcwd(), update_folder, "project-bo4.exe")
        
        try:
            subprocess.run(['cmd', '/C', 'start', '', fr'{update_script}'], shell=True)
        except Exception as e:
            print(f"Something went wrong with update script: {e}")

    except Exception as e:
        print(f"Something went wrong while updating: {e}")

    sys.exit(0)

    
class updater(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setWindowTitle('Project-bo4 updater')
        self.setWindowIcon(QIcon(os.path.join('files', 'images', 'exe_icon_bo4.ico')))

        background_label = QLabel(self)
        background_image = QPixmap(os.path.join(os.getcwd(), 'files', 'images', 'update', "updater_image.jpg"))
        background_label.setPixmap(background_image)
        background_label.setGeometry(0, 0, background_image.width(), background_image.height())
        self.setFixedSize(background_image.width(), background_image.height())

        layout = QVBoxLayout()
        title_layout = QHBoxLayout()

        self.title = QLabel("")
        title_layout.addWidget(self.title)
        layout.addLayout(title_layout)

        layout.addLayout(title_layout)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet('QProgressBar { background-color: #1C1C1C; border: 1px solid #333333; border-radius: 5px; text-align: center; color: white; } QProgressBar::chunk { background-color: #333333; }')
        
        layout.addWidget(self.progress_bar, 75)
        self.progress_bar.setValue(0)

        self.setLayout(layout)

        self.downloader = threading.Thread(target=do_update, args=(self.progress_bar,))
        self.downloader.daemon = True
        self.downloader.start()


def check_updates():
    last = get_last_release_version()
    current = get_settings("link")

    if current == last:
        print("software is uptodate")
        return
    
    update_settings("link", last)

    app = QApplication(sys.argv)
    window = updater()
    window.show()
    sys.exit(app.exec_())
        
if __name__ == "__main__":

    update_settings(None, None)
    try:
        check_updates()
    except Exception as e:
        print(f"Something went wrong while cheching updates: {e}")
    
    #generade default name if not found
    get_json_item('project-bo4.json', 'identity', 'name')
    
    app = QApplication(sys.argv)

    app.setStyle("Fusion")
    palette = app.palette()
    palette.setColor(QPalette.WindowText, Qt.white)
    app.setPalette(palette)

    window = launcher()
    window.show()
    sys.exit(app.exec_())
    
