import sys
import os
import rsa
import subprocess
import platform
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QFileDialog, QHBoxLayout, QFrame, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class DashboardFirma(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Firma Digital - Dashboard")
        self.setGeometry(100, 50, 1000, 600)
        self.setStyleSheet("background-color: #1b1b2f; color: #FFFFFF;")
        self.archivo_seleccionado = None
        self.clave_privada = None
        self.clave_publica = None
        
        # Crear carpeta /out si no existe
        if not os.path.exists("out"):
            os.makedirs("out")
        
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
        panel.setStyleSheet("background-color: #1e1e2f; border-radius: 15px;")
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
            font-size: 18px;
            padding: 10px;
        """)
        panel_layout.addWidget(QLabel("Consola de resultados:"))
        panel_layout.addWidget(self.log)

        # Agregar sidebar y panel al layout principal
        main_layout.addWidget(sidebar)
        main_layout.addWidget(panel, stretch=1)

    def generar_claves(self):
        try:
            self.log.clear()
            self.log.append("🔄 Generando claves RSA (512 bits)...")
            self.clave_publica, self.clave_privada = rsa.newkeys(512)
            
            # Guardar claves en archivos
            with open("clave_publica.pem", "wb") as f:
                f.write(self.clave_publica.save_pkcs1("PEM"))
            
            with open("clave_privada.pem", "wb") as f:
                f.write(self.clave_privada.save_pkcs1("PEM"))
            
            self.log.append("✅ Claves generadas y guardadas correctamente.")
            self.log.append("📄 Archivos creados: clave_publica.pem, clave_privada.pem\n")
        except Exception as e:
            self.log.append(f"❌ Error al generar claves: {str(e)}\n")

    def seleccionar_archivo(self):
        opciones = QFileDialog.Options()
        archivo, _ = QFileDialog.getOpenFileName(
            self, 
            "Seleccionar archivo", 
            "", 
            "Archivos soportados (*.txt *.pdf *.docx);;Texto (*.txt);;PDF (*.pdf);;Word (*.docx)", 
            options=opciones
        )
        if archivo:
            # Validar extensión
            ext = os.path.splitext(archivo)[1].lower()
            if ext not in ['.txt', '.pdf', '.docx']:
                self.log.clear()
                self.log.append("❌ Tipo de archivo no permitido.")
                self.log.append("✅ Solo se aceptan: .txt, .pdf, .docx\n")
                self.archivo_seleccionado = None
                return
            
            self.archivo_seleccionado = archivo
            self.log.clear()
            self.log.append(f"📁 Archivo seleccionado: {archivo}\n")
            
            # Mostrar contenido del archivo
            try:
                with open(archivo, "rb") as f:
                    contenido = f.read()
                
                if ext == '.txt':
                    contenido_decodificado = contenido.decode('utf-8', errors='ignore')
                    self.log.append("📄 Contenido del archivo:\n")
                    self.log.append(contenido_decodificado + "\n")
                else:
                    self.log.append(f"📄 Archivo binario detectado: {ext}\n")
                    self.log.append(f"📊 Tamaño: {len(contenido)} bytes\n")
            except Exception as e:
                self.log.append(f"⚠️ No se pudo mostrar el contenido: {str(e)}\n")

    def firmar_archivo(self):
        if not self.archivo_seleccionado:
            self.log.clear()
            self.log.append("❌ No se ha seleccionado ningún archivo.\n")
            return
        
        if self.clave_privada is None:
            self.log.clear()
            self.log.append("❌ Primero debes generar las claves RSA.\n")
            return
        
        try:
            self.log.clear()
            nombre_archivo = os.path.basename(self.archivo_seleccionado)
            self.log.append(f"🔏 Firmando archivo: {nombre_archivo}...")
            
            # Leer archivo
            with open(self.archivo_seleccionado, "rb") as f:
                contenido = f.read()
            
            # Firmar con clave privada
            firma = rsa.sign(contenido, self.clave_privada, "SHA-256")
            
            # Guardar firma en carpeta /out
            nombre_sin_ext = os.path.splitext(nombre_archivo)[0]
            nombre_firma = os.path.join("out", f"{nombre_sin_ext}.firma")
            with open(nombre_firma, "wb") as f:
                f.write(firma)
            
            self.log.append(f"✅ Archivo firmado correctamente.")
            self.log.append(f"📝 Firma guardada en: {nombre_firma}\n")
            self.log.append(f"🔐 Tamaño de la firma: {len(firma)} bytes\n")
            
            # Abrir carpeta /out
            self.abrir_carpeta_out()
            
        except Exception as e:
            self.log.clear()
            self.log.append(f"❌ Error al firmar archivo: {str(e)}\n")

    def verificar_firma(self):
        if not self.archivo_seleccionado:
            self.log.clear()
            self.log.append("❌ No se ha seleccionado ningún archivo.\n")
            return
        
        nombre_archivo = os.path.basename(self.archivo_seleccionado)
        nombre_sin_ext = os.path.splitext(nombre_archivo)[0]
        nombre_firma = os.path.join("out", f"{nombre_sin_ext}.firma")
        
        if not os.path.exists(nombre_firma):
            self.log.clear()
            self.log.append(f"❌ Archivo de firma no encontrado: {nombre_firma}\n")
            return
        
        # Cargar clave pública
        if not os.path.exists("clave_publica.pem"):
            self.log.clear()
            self.log.append("❌ Archivo de clave pública no encontrado.\n")
            return
        
        try:
            self.log.clear()
            self.log.append("🔍 Verificando firma digital...")
            
            # Cargar clave pública
            with open("clave_publica.pem", "rb") as f:
                clave_publica = rsa.PublicKey.load_pkcs1(f.read())
            
            # Leer mensaje y firma
            with open(self.archivo_seleccionado, "rb") as f:
                mensaje = f.read()
            
            with open(nombre_firma, "rb") as f:
                firma = f.read()
            
            # Verificar firma
            rsa.verify(mensaje, firma, clave_publica)
            self.log.append("✅ Firma válida. El archivo no fue alterado.")
            self.log.append("🔐 El archivo proviene del remitente auténtico.\n")
            
        except rsa.VerificationError:
            self.log.clear()
            self.log.append("❌ Firma no válida.")
            self.log.append("⚠️  El archivo pudo haber sido alterado o no coincide con la firma.\n")
        except Exception as e:
            self.log.clear()
            self.log.append(f"❌ Error al verificar firma: {str(e)}\n")
    
    def abrir_carpeta_out(self):
        ruta_out = os.path.abspath("out")
        try:
            if platform.system() == "Windows":
                os.startfile(ruta_out)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", ruta_out])
            else:
                subprocess.Popen(["xdg-open", ruta_out])
        except Exception as e:
            self.log.append(f"⚠️ No se pudo abrir la carpeta: {str(e)}\n")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = DashboardFirma()
    ventana.show()
    sys.exit(app.exec_())