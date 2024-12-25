import sys
from PyQt5.QtCore import QUrl, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply


class IconLoader(QThread):
    """Класс для асинхронной загрузки иконки из URL в отдельном потоке."""
    icon_loaded = pyqtSignal(QIcon)  # Сигнал для передачи иконки после загрузки

    def __init__(self, url, parent=None):
        super().__init__(parent)
        self.url = url

    def run(self):
        """Загружает иконку с URL в фоновом потоке."""
        manager = QNetworkAccessManager()
        request = QNetworkRequest(QUrl(self.url))
        reply = manager.get(request)

        # Подключаем сигнал, который будет вызван, когда загрузка завершится
        reply.finished.connect(lambda: self.handle_response(reply))

    def handle_response(self, reply):
        """Обрабатываем ответ после загрузки изображения."""
        if reply.error() == QNetworkReply.NoError:
            # Изображение загружено успешно
            image = QImage()
            image.loadFromData(reply.readAll())  # Читаем данные изображения
            icon = QIcon(QPixmap(image))

            # Отправляем иконку обратно в основной поток
            self.icon_loaded.emit(icon)
        else:
            print("Ошибка при загрузке иконки:", reply.errorString())


class MainWindow(QMainWindow):
    """Главное окно приложения с WebView и системным треем."""
    def __init__(self):
        super().__init__()

        # Настройка окна
        self.setWindowTitle('Ваше приложение')  # Название окна
        self.setGeometry(100, 100, 1200, 800)

        # Создаем WebEngineView для отображения сайта
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('https://bekbolsun-es.github.io/Americanpizzam.gibhub.io/'))  # Укажите свой URL

        # Создание вертикальной компоновки для окна
        layout = QVBoxLayout()
        layout.addWidget(self.browser)

        # Центральный виджет с компоновкой
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Запуск загрузки иконки
        self.icon_loader = IconLoader('https://replicate.delivery/pbxt/9XWrqbt53yohL9wtV1Azyds1yikGiNEat40ZNI28r59HfUcIA/out.png')
        self.icon_loader.icon_loaded.connect(self.set_icon)  # Подключаем сигнал для обработки иконки
        self.icon_loader.start()  # Запускаем загрузку иконки

        # Контекстное меню для иконки в трей
        tray_menu = QMenu(self)

        # Действие для открытия окна
        open_action = QAction('Открыть приложение', self)
        open_action.triggered.connect(self.show)
        tray_menu.addAction(open_action)

        # Действие для выхода
        quit_action = QAction('Выход', self)
        quit_action.triggered.connect(self.quit_application)
        tray_menu.addAction(quit_action)

        # Устанавливаем меню в системный трей
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setContextMenu(tray_menu)

        # Показываем иконку в системном трее
        self.tray_icon.show()

    def set_icon(self, icon):
        """Устанавливаем иконку для окна и трея."""
        self.setWindowIcon(icon)
        self.tray_icon.setIcon(icon)

    def quit_application(self):
        """Закрытие приложения"""
        QApplication.quit()


# Запуск приложения
if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()  # Показываем окно приложения
    sys.exit(app.exec_())
