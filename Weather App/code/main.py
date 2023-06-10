# Python libraries
import requests
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
# System libraries
import sys
# Custom-made libraries
from settings import *

class App:
    def __init__(self) -> None:
        # * General setup
        self.app = QApplication([])
        self.main_win = QWidget()
        self.font = "assets/fonts/Gotham-Font/Gotham-Light.otf"

        self.api_key = "60802247ca61d141c353d275e46921a3"
        self.cities = self._get_cities()

        # * Widgets
        search_btn_size = (WIDTH-(WIDTH-50), 50)
        self.search_btn = self._handle_button(None, self.main_win, search_btn_size, (WIDTH-search_btn_size[0], 0), "assets/graphics/search.png", 10)

        self.line_edit = self._handle_line_completer(self.main_win, (WIDTH-search_btn_size[0]-25, search_btn_size[0]), (10, 10))

        self.temp_label_pos = (WIDTH//2, HEIGHT//2)
        self.temp_label = self._handle_label(self.font, 50, None, self.main_win, "white")

        self.city_label = self._handle_label(self.font, 30, None, self.main_win, "white")

        self.humidity_num_label = QLabel(self.main_win)
        self.humidity_label = QLabel(self.main_win)
        self.humidity_image = QLabel(self.main_win)

        self.wind_speed_num = QLabel(self.main_win)
        self.wind_speed_label = QLabel(self.main_win)
        self.wind_speed_img = QLabel(self.main_win)

        self.image = QLabel(self.main_win)
        self.image.setPixmap(QPixmap())

    def _handle_label(self, font_path: str, font_size: int, text: str, win: QWidget, color: str) -> QLabel:
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        else:
            font_family = "Arial"

        font = QFont(font_family, font_size)
        label = QLabel(text, win)
        label.setFont(font)
        label.setStyleSheet(f"color: {color};")

        return label

    def _update_label(self, label: QLabel, text: str, offset: int = 35):
        label.setText(text)
        label.adjustSize()
        label.move(self.temp_label_pos[0] - label.width()//2, self.temp_label_pos[1] - label.height()//2 + offset)

    def _update_image(self, label: QLabel, image_path: str):
        pixmap = QPixmap(image_path).scaled(200, 200, aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        label.setPixmap(pixmap)
        label.setFixedSize(pixmap.size())
        label.move(WIDTH//2 - label.width()//2, 45)

        return label

    def _handle_city_info(self, hum, wind) -> None:
        # ! THIS WAS HARDCODED BECAUSE YESTERDAY I WAS TIRED
        self.humidity_label.setText("Humidity")
        self.humidity_label.setFont(QFont(self.font, 11))
        self.humidity_label.setStyleSheet("color: white;")
        self.humidity_label.adjustSize()
        self.humidity_label.move(90, HEIGHT-50)
        
        self.humidity_num_label.setText(hum)
        self.humidity_num_label.setFont(QFont(self.font, 17))
        self.humidity_num_label.setStyleSheet("color: white;")
        self.humidity_num_label.adjustSize()
        self.humidity_num_label.move(90, HEIGHT-82)
        
        self.humidity_image.setPixmap(QPixmap("assets/graphics/humidity.png").scaled(40, 40, aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))
        self.humidity_image.adjustSize()
        self.humidity_image.move(40, HEIGHT-80)

        self.wind_speed_num.setText("Wind Speed")
        self.wind_speed_num.setFont(QFont(self.font, 11))
        self.wind_speed_num.setStyleSheet("color: white;")
        self.wind_speed_num.adjustSize()
        self.wind_speed_num.move(WIDTH-105, HEIGHT-50)
        
        self.wind_speed_label.setText(wind)
        self.wind_speed_label.setFont(QFont(self.font, 17))
        self.wind_speed_label.setStyleSheet("color: white;")
        self.wind_speed_label.adjustSize()
        self.wind_speed_label.move(WIDTH-105, HEIGHT-82)
        
        self.wind_speed_img.setPixmap(QPixmap("assets/graphics/wind.png").scaled(40, 40, aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation))
        self.wind_speed_img.adjustSize()
        self.wind_speed_img.move(WIDTH-155, HEIGHT-80)

    def _handle_line_completer(self, win: QWidget, size: tuple, pos: tuple) -> QLineEdit:
        model = QStringListModel()
        model.setStringList(self.cities)

        completer = QCompleter()
        completer.setModel(model)

        font = QFont()
        font.setPointSize(18)

        line_edit = QLineEdit(win)
        line_edit.setFont(font)
        line_edit.setGeometry(pos[0], pos[1], size[0], size[1])
        line_edit.setCompleter(completer)
        line_edit.show()

        return line_edit
    
    def _get_cities(self) -> list:
        cities = [
            "New York City", "Los Angeles", "Chicago", "San Francisco", "Miami", "Las Vegas", "Washington, D.C.", "Boston", "Seattle", "New Orleans",
            "London", "Manchester", "Birmingham", "Edinburgh", "Glasgow", "Liverpool", "Bristol", "Oxford", "Cambridge", "York",
            "Paris", "Marseille", "Lyon", "Toulouse", "Nice", "Bordeaux", "Strasbourg", "Nantes", "Lille", "Cannes",
            "Berlin", "Munich", "Hamburg", "Frankfurt", "Cologne", "Dresden", "Stuttgart", "Leipzig", "Düsseldorf", "Nuremberg",
            "Beijing", "Shanghai", "Hong Kong", "Guangzhou", "Shenzhen", "Chengdu", "Xi'an", "Hangzhou", "Nanjing", "Chongqing",
            "Mumbai", "Delhi", "Bangalore", "Kolkata", "Chennai", "Hyderabad", "Jaipur", "Ahmedabad", "Pune", "Goa",
            "Tokyo", "Kyoto", "Osaka", "Yokohama", "Hiroshima", "Nagoya", "Sapporo", "Kobe", "Fukuoka", "Nara",
            "Sao Paulo", "Rio de Janeiro", "Brasilia", "Salvador", "Fortaleza", "Recife", "Manaus", "Curitiba", "Porto Alegre", "Belém",
            "Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Gold Coast", "Cairns", "Darwin", "Canberra", "Hobart",
            "Toronto", "Vancouver", "Montreal", "Calgary", "Edmonton", "Ottawa", "Quebec City", "Winnipeg", "Halifax", "Victoria",
            "Casablanca", "Rabat", "Tangier", "El Jadida", "Kenitra", "Agadir", "Laayoune", "Fez", "Safi", "Dakhla", "Nador"
        ]

        return cities

    def _handle_button(self, text: str, win: QWidget, size: tuple, pos: tuple, img_path: str, offset: int) -> QPushButton:
        btn = QPushButton(text, win)
        btn.setGeometry(pos[0]-offset, pos[1]+offset, size[0], size[1])
        btn.setIcon(QIcon(img_path))
        btn.setIconSize(QSize(btn.width()-offset*2, btn.height()-offset*2))
        return btn

    def _handle_win_colors(self, start_color: str, end_color: str):
        gradient = QLinearGradient(0, -20, 150, self.main_win.height())
        gradient.setColorAt(0, QColor(start_color))
        gradient.setColorAt(1, QColor(end_color))

        palette = QPalette()
        palette.setBrush(self.main_win.backgroundRole(), QBrush(gradient))
        self.main_win.setPalette(palette)

    def _main_win_propreties(self):
        self._handle_win_colors("#48e3b5", "#3f3c61")
        
        self.main_win.setWindowTitle("Weather App")
        self.main_win.setFixedSize(QSize(WIDTH, HEIGHT))
        self.main_win.show()

    def _get_weather(self):
        user_input = self.line_edit.text().lower()
        if user_input:
            weather_data = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=imperial&APPID={self.api_key}").json()

            print(weather_data)

            if weather_data["cod"] == "404":
                self.temp_label.setText("")
                self.image.setPixmap(QPixmap())
                self._update_label(self.city_label, weather_data["message"].capitalize(), 30)
            else:
                weather = weather_data["weather"][0]["main"]
                temp = round((round(weather_data["main"]["temp"]) - 32) * (5/9))
                humidity = weather_data["main"]["humidity"]
                wind_speed = round(weather_data["wind"]["speed"], 1)

                self._handle_city_info(f"{humidity}%", f"{wind_speed}Km/H")
                self._update_label(self.temp_label, f"{temp}°C")
                self._update_label(self.city_label, weather_data["name"], 90)
                self._update_image(self.image, f"assets/graphics/{weather.lower()}.png")

    def _handle_events(self):
        self.search_btn.clicked.connect(self._get_weather)

    def _run(self):
        self._handle_events()
        self._main_win_propreties()
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    app = App()
    app._run()


