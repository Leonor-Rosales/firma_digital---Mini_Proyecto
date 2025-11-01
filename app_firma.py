import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QFileDialog, QHBoxLayout, QFrame
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class DashboardFirma(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Firma Digital - Dashboard")
        self.setGeometry(100, 50, 1000, 600)
        self.setStyleSheet("background-color: #1b1b2f; color: #FFFFFF;")
        self.archivo_seleccionado = None
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(20)
        self.setLayout(main_layout)

        # Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("background-color: #1b1b2f;")
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(20, 20, 20, 20)
        sidebar_layout.setSpacing(15)
        sidebar.setLayout(sidebar_layout)

        # Botones turquesa/aqua con texto oscuro
        btn_style = """
            QPushButton {
                background-color: #40E0D0;
                color: #1b1b2f;
                border-radius: 12px;
                padding: 12px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #7FFFD4;
            }
            QPushButton:pressed {
                background-color: #00FFFF;
            }
        """

        self.btn_generar_claves = QPushButton("Generar claves RSA")
        self.btn_generar_claves.setStyleSheet(btn_style)
        self.btn_generar_claves.clicked.connect(self.generar_claves)
        sidebar_layout.addWidget(self.btn_generar_claves)

        self.btn_seleccionar_archivo = QPushButton("Seleccionar archivo")
        self.btn_seleccionar_archivo.setStyleSheet(btn_style)
        self.btn_seleccionar_archivo.clicked.connect(self.seleccionar_archivo)
        sidebar_layout.addWidget(self.btn_seleccionar_archivo)

        self.btn_firmar = QPushButton("Firmar archivo")
        self.btn_firmar.setStyleSheet(btn_style)
        self.btn_firmar.clicked.connect(self.firmar_archivo)
        sidebar_layout.addWidget(self.btn_firmar)

        self.btn_verificar = QPushButton("Verificar firma")
        self.btn_verificar.setStyleSheet(btn_style)
        self.btn_verificar.clicked.connect(self.verificar_firma)
        sidebar_layout.addWidget(self.btn_verificar)

        sidebar_layout.addStretch()

        # Panel principal sin borde, fondo oscuro
        panel = QFrame()
        panel.setStyleSheet("background-color: #1e1e2f; border-radius: 15px;")  # sin borde
        panel_layout = QVBoxLayout()
        panel_layout.setContentsMargins(20, 20, 20, 20)
        panel_layout.setSpacing(10)
        panel.setLayout(panel_layout)

        # Log / Consola
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setStyleSheet("""
            background-color: #1e1e2f;
            color: #40E0D0;
            border: none;
            font-family: Consolas;
            font-size: 14px;
            padding: 10px;
        """)
        panel_layout.addWidget(QLabel("Consola de resultados:"))
        panel_layout.addWidget(self.log)

        # Agregar sidebar y panel al layout principal
        main_layout.addWidget(sidebar)
        main_layout.addWidget(panel, stretch=1)

    # Funciones de prueba
    def generar_claves(self):
        self.log.append("Función generar_claves aún no implementada.")

    def seleccionar_archivo(self):
        opciones = QFileDialog.Options()
        archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo", "", "Todos los archivos (*)", options=opciones)
        if archivo:
            self.archivo_seleccionado = archivo
            self.log.append(f"Archivo seleccionado: {archivo}")

    def firmar_archivo(self):
        if self.archivo_seleccionado:
            self.log.append(f"Firmando archivo: {self.archivo_seleccionado}")
        else:
            self.log.append("No se ha seleccionado ningún archivo.")

    def verificar_firma(self):
        self.log.append("Función verificar_firma aún no implementada.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = DashboardFirma()
    ventana.show()
    sys.exit(app.exec_())
