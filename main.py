import sys
import cv2
from PyQt5.QtWidgets import QComboBox, QVBoxLayout, QHBoxLayout,QStackedWidget,QApplication,QDesktopWidget, QWidget, QPushButton, QFormLayout, QLabel, QLineEdit, QDateEdit, QGridLayout, QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QMessageBox
from PyQt5.QtCore import Qt, QDate, QTimer
from PyQt5.QtGui import QFont, QPixmap, QImage
import datetime


import sqlite3



conn = sqlite3.connect("powerhousegym.db")
cursor = conn.cursor()

# Base class for centering functionality
class CenteredWindow(QWidget):
    def center(self):
        # Center the window on the screen
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        font = QFont()
        font.setPointSize(12)  # Adjust the point size as needed
        self.setFont(font)
        

# Clase para la pantalla de login
class Login(CenteredWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Login')
        self.setGeometry(180, 180, 450, 200)
        self.center()

        
        layout = QFormLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        self.setLayout(layout)
        

        self.usuario_input = QLineEdit()
        self.usuario_input.setFixedWidth(250)

        self.contrasena_input = QLineEdit()
        self.contrasena_input.setFixedWidth(250)
        self.contrasena_input.setEchoMode(QLineEdit.Password)

        layout.addRow('Usuario:', self.usuario_input)
        layout.addRow('Contraseña:', self.contrasena_input)

        self.login_button = QPushButton('Iniciar sesión')
        self.login_button.setFixedWidth(250)
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)



    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.login()

    def login(self):
        usuario = self.usuario_input.text()
        contrasena = self.contrasena_input.text()

        # Verificar credenciales (en este ejemplo, solo hay un usuario administrador)
        if usuario == 'admin' and contrasena == 'pass':
            self.close()
            self.menu = Menu()
            self.menu.show()
            print("Credenciales correctas")
            
        else:
            QMessageBox.warning(self, 'Error', 'Credenciales incorrectas')


# Clase para la pantalla de menú
class Menu(CenteredWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Menú')
        self.setGeometry(300, 300, 1000, 600)
        self.center()

         # Main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(main_layout)

        # Left section for buttons
        button_layout = QVBoxLayout()
        button_layout.setAlignment(Qt.AlignTop)  # Align buttons to the top
        main_layout.addLayout(button_layout)

        self.agregar_button = QPushButton('Agregar nuevo usuario')
        self.agregar_button.clicked.connect(self.show_agregar_usuario)
        button_layout.addWidget(self.agregar_button)

        self.listar_button = QPushButton('Listar usuarios')
        self.listar_button.clicked.connect(self.show_listar_usuarios)
        button_layout.addWidget(self.listar_button)

        
        self.acceso_button = QPushButton('Ingreso de usuarios')
        self.acceso_button.clicked.connect(self.show_acceso_usuarios)
        button_layout.addWidget(self.acceso_button)

        self.asistencia_button = QPushButton('Asistencia')
        self.asistencia_button.clicked.connect(self.show_asistencia_usuarios)
        button_layout.addWidget(self.asistencia_button)

        # Right section for displaying content
        self.content_area = QStackedWidget()
        main_layout.addWidget(self.content_area)

        # Add the sub-windows (content widgets) to the QStackedWidget
        self.agregar_widget = AgregarUsuario()
        self.listar_widget = ListarUsuarios()
        self.acceso_widget = AccesoUsuarios()
        self.asistencia_widget = AsistenciaUsuarios()


        self.content_area.addWidget(self.agregar_widget)
        self.content_area.addWidget(self.listar_widget)


        # Show the initial widget (optional)
        self.content_area.setCurrentWidget(self.listar_widget)


    def show_agregar_usuario(self):
        self.content_area.setCurrentWidget(self.agregar_widget)

    def show_listar_usuarios(self):
        self.content_area.setCurrentWidget(self.listar_widget)

    def show_acceso_usuarios(self):
        self.acceso_window = AccesoUsuarios()
        self.acceso_window.show()
    
    def show_asistencia_usuarios(self):
        self.asistencia_window = AsistenciaUsuarios()
        self.asistencia_window.show()

    def show_editar_usuarios(self):
        self.editar_window = EditarUsuario()
        self.editar_window.show()



# Clase para la pantalla de agregar usuario
class AgregarUsuario(CenteredWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Agregar usuario')
        self.setGeometry(100, 100, 300, 200)
        self.center()

        layout = QFormLayout()
        self.setLayout(layout)

        self.nombre_input = QLineEdit()

        # Input for membership (QComboBox)
        self.membresia_input = QComboBox()
        

        # Fetch membership types from the database and populate the QComboBox
        self.populate_membresia()

        self.fecha_ingreso_input = QDateEdit()
        self.fecha_ingreso_input.setDate(QDate.currentDate())  # Establece la fecha actual

        self.fecha_vencimiento_input = QDateEdit()
        self.fecha_vencimiento_input.setDate(QDate.currentDate().addMonths(1))  # Suma un mes a la fecha actual

        layout.addRow('Nombre:', self.nombre_input)
        layout.addRow('Membresia:', self.membresia_input)
        layout.addRow('Fecha de ingreso:', self.fecha_ingreso_input)
        layout.addRow('Fecha de vencimiento:', self.fecha_vencimiento_input)


        self.foto_label = QLabel()
        self.foto_label.setFixedSize(200, 200)

        self.tomar_foto_button = QPushButton('Tomar foto')
        self.tomar_foto_button.clicked.connect(self.tomar_foto)

        layout.addWidget(self.foto_label)
        layout.addWidget(self.tomar_foto_button)


        self.guardar_button = QPushButton('Guardar')
        self.guardar_button.clicked.connect(self.guardar_usuario)
        layout.addWidget(self.guardar_button)

        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.mostrar_frame)
        self.timer.start(30)

    def populate_membresia(self):
        

        # Query the 'membresia' table for the membership types
        cursor.execute("SELECT id_membresia, membresia FROM membresia")
        rows = cursor.fetchall()

        # Populate the QComboBox with membership types
        for row in rows:
            id_membresia, membresia = row
            self.membresia_input.addItem(membresia, id_membresia)  # Store id as userData

        # Close the database connection
    
    def get_selected_membership_id(self):
        # Get the selected membership ID
        return self.membresia_input.currentData()
    

    def mostrar_frame(self):
        ret, frame = self.cap.read()
        if ret:
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            qimg = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
            self.foto_label.setPixmap(QPixmap.fromImage(qimg).scaled(200, 200, Qt.KeepAspectRatio))


    def tomar_foto(self):
        ret, frame = self.cap.read()
        if ret:
            cv2.imwrite('foto.jpg', frame)
            self.timer.stop()
            self.cap.release()
    
    def guardar_usuario(self):
        nombre = self.nombre_input.text()
        fecha_ingreso = self.fecha_ingreso_input.date().toString('yyyy-MM-dd')
        fecha_vencimiento = self.fecha_vencimiento_input.date().toString('yyyy-MM-dd')

        cursor.execute('''
            INSERT INTO usuarios (nombre, id_membresia, fecha_ingreso, fecha_vencimiento, foto)
            VALUES (?,?,?,?,?);
        ''', (nombre, self.get_selected_membership_id(), fecha_ingreso, fecha_vencimiento, 'foto.jpg'))
        conn.commit()

        self.close()
        menu = Menu()
        menu.show()

#Clase para la pantalla de editar usuario
class EditarUsuario(CenteredWindow):
    def __init__(self, id_usuario):
        super().__init__()
        
        self.id_usuario = id_usuario

        self.setWindowTitle('Editar usuario')
        self.setGeometry(200, 200, 400, 300)
        self.center()
        
        layout = QFormLayout()
        self.setLayout(layout)

        cursor.execute('''
            SELECT nombre, fecha_ingreso, fecha_vencimiento
            FROM usuarios
            WHERE id =?;
        ''', (self.id_usuario,))
        usuario = cursor.fetchone()

        self.nombre_input = QLineEdit(usuario[0])
        self.fecha_ingreso_input = QDateEdit()
        self.fecha_ingreso_input.setDate(datetime.date.fromisoformat(usuario[1]))
        self.fecha_vencimiento_input = QDateEdit()
        self.fecha_vencimiento_input.setDate(datetime.date.fromisoformat(usuario[2]))

        layout.addRow('Nombre:', self.nombre_input)
        layout.addRow('Fecha de ingreso:', self.fecha_ingreso_input)
        layout.addRow('Fecha de vencimiento:', self.fecha_vencimiento_input)

        self.guardar_button = QPushButton('Guardar')
        self.guardar_button.clicked.connect(self.guardar_cambios)
        layout.addWidget(self.guardar_button)

    def guardar_cambios(self):
        nombre = self.nombre_input.text()
        fecha_ingreso = self.fecha_ingreso_input.date().toString('yyyy-MM-dd')
        fecha_vencimiento = self.fecha_vencimiento_input.date().toString('yyyy-MM-dd')

        cursor.execute('''
            UPDATE usuarios
            SET nombre =?, fecha_ingreso =?, fecha_vencimiento =?
            WHERE id =?;
        ''', (nombre, fecha_ingreso, fecha_vencimiento, self.id_usuario))
        conn.commit()
        print("guardar cambios")
        self.close()
        menu = Menu()
        menu.show()
        

class AccesoUsuarios(CenteredWindow): 
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Listar usuarios')
        self.setGeometry(100, 100, 600, 400)
        self.center()

        layout = QFormLayout()
        self.setLayout(layout)

        self.nombre_input = QLineEdit()

        # Header label
        self.header_label = QLabel("Ingresa tu número de usuario:")
        self.header_label.setFont(QFont("Arial", 12))  # Optional: set font size
        layout.addWidget(self.header_label)

        # User ID input
        self.user_id_input = QLineEdit()
        self.user_id_input.setMaxLength(11)  # Limit input length to 11 digits
        layout.addWidget(self.user_id_input)

        # Search button
        self.search_button = QPushButton("Acceder")
        self.search_button.clicked.connect(self.search_user)
        layout.addWidget(self.search_button)

        # Information display area (initially empty)
        self.info_label = QLabel("")
        layout.addWidget(self.info_label)
        
    def search_user(self):
        user_id = self.user_id_input.text()

        if user_id.isdigit():  # Check if input is a number
            # Prepare SQL query
            query = "SELECT nombre, membresia.membresia, fecha_ingreso, fecha_vencimiento FROM usuarios LEFT JOIN membresia on membresia.id_membresia = usuarios.id_membresia WHERE id=?"
    
            cursor.execute(query, (int(user_id),))

            # Fetch search results
            user_data = cursor.fetchone()
            # Get current date and time
            now = datetime.datetime.now()
            formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
            if user_data:  # If user found, display information
                info_text = f"Nombre: {user_data[0]}\nMembresia: {user_data[1]}\nFecha Ingreso: {user_data[2]}\nFecha Vencimiento: {user_data[3]}\nHora de Ingreso: {formatted_datetime}"
                self.info_label.setText(info_text)
                date_from_string = datetime.datetime.strptime(user_data[3], "%Y-%m-%d")

                
                vencido = 1 if now > date_from_string else 0

                log_query = '''
                    INSERT INTO logs (usuario_id, nombre, hora_acceso, fecha_vencimiento, vencido)
                    VALUES (?, ?, ?, ?, ?);
                '''

                
                cursor.execute(log_query, (user_id, user_data[0], formatted_datetime, user_data[3], vencido))
                conn.commit()

            else:
                self.info_label.setText("Usuario no encontrado.")
        else:
            self.info_label.setText("Por favor, ingrese un número de usuario válido.")

class AsistenciaUsuarios(CenteredWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Asistencia usuarios')
        self.setGeometry(100, 100, 600, 400)
        self.center()

        layout = QFormLayout()
        self.setLayout(layout)
        
        # Table widget for displaying logs data
        self.logs_table = QTableWidget()
        self.logs_table.setColumnCount(4)
        self.logs_table.setHorizontalHeaderLabels(['Nombre', 'Hora de Acceso', 'Fecha de Vencimiento', 'Vencido'])
        self.logs_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.logs_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.logs_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.logs_table)

        # Load data from the logs table
        self.load_logs_data()

    def load_logs_data(self):
        # Fetch data from the logs table
        query = '''
            SELECT nombre, hora_acceso, fecha_vencimiento, vencido
            FROM logs
        '''
        cursor.execute(query)
        logs = cursor.fetchall()

        # Populate the table with the data
        self.logs_table.setRowCount(0)  # Clear existing rows

        for i, log in enumerate(logs):
            self.logs_table.insertRow(i)
            self.logs_table.setItem(i, 0, QTableWidgetItem(log[0]))  # Nombre
            self.logs_table.setItem(i, 1, QTableWidgetItem(log[1]))  # Hora de Acceso
            self.logs_table.setItem(i, 2, QTableWidgetItem(log[2]))  # Fecha de Vencimiento
            vencido_text = "Sí" if log[3] else "No"  # Convert 1/0 to "Sí"/"No"
            self.logs_table.setItem(i, 3, QTableWidgetItem(vencido_text))

        self.logs_table.resizeColumnsToContents()



# Clase para la pantalla de listar usuarios
class ListarUsuarios(CenteredWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Listar usuarios')
        self.setGeometry(100, 100, 600, 400)
        self.center()
        

        layout = QGridLayout()
        self.setLayout(layout)

        # Add search input and button
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por ID o nombre...")
        layout.addWidget(QLabel("Buscar:"), 0, 0)
        layout.addWidget(self.search_input, 0, 1)

        self.search_button = QPushButton("Buscar")
        self.search_button.clicked.connect(self.search_users)
        layout.addWidget(self.search_button, 0, 2)


        self.usuarios_table = QTableWidget()
        self.usuarios_table.setRowCount(0)
        self.usuarios_table.setColumnCount(4)
        self.usuarios_table.setHorizontalHeaderLabels(['Nombre', 'Membresia','Fecha de ingreso', 'Fecha de vencimiento'])
        self.usuarios_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.usuarios_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.usuarios_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.usuarios_table, 1, 0, 1, 3)

        # Add edit button
        self.editar_button = QPushButton('Editar')
        self.editar_button.clicked.connect(self.editar_usuario)
        layout.addWidget(self.editar_button, 2, 0, 1, 3, alignment=Qt.AlignCenter)

        # Load all users initially
        self.load_users()

    def load_users(self, filter_query=None):
        """Load users into the table. Optionally filter results by query."""

        # Fetch data based on filter query
        if filter_query:
            cursor.execute('''
                SELECT usuarios.nombre, membresia.membresia, usuarios.fecha_ingreso, usuarios.fecha_vencimiento
                FROM usuarios
                LEFT JOIN membresia on membresia.id_membresia = usuarios.id_membresia
                WHERE usuarios.id LIKE ? OR usuarios.nombre LIKE ?;
            ''', (f"%{filter_query}%", f"%{filter_query}%"))
        else:
            cursor.execute('''
                SELECT usuarios.nombre, membresia.membresia, usuarios.fecha_ingreso, usuarios.fecha_vencimiento
                FROM usuarios
                LEFT JOIN membresia on membresia.id_membresia = usuarios.id_membresia;
            ''')

        usuarios = cursor.fetchall()
        # Populate table
        self.usuarios_table.setRowCount(0)  # Clear previous rows
        for i, usuario in enumerate(usuarios):
            self.usuarios_table.insertRow(i)
            self.usuarios_table.setItem(i, 0, QTableWidgetItem(usuario[0]))
            self.usuarios_table.setItem(i, 1, QTableWidgetItem(usuario[1]))
            self.usuarios_table.setItem(i, 2, QTableWidgetItem(usuario[2]))
            self.usuarios_table.setItem(i, 3, QTableWidgetItem(usuario[3]))


    def search_users(self):
        """Filter users based on search input."""
        query = self.search_input.text()
        self.load_users(filter_query=query)

    def editar_usuario(self):
        """Handle editing of selected user."""
        row = self.usuarios_table.currentRow()
        if row != -1:
            nombre = self.usuarios_table.item(row, 0).text()
            membresia = self.usuarios_table.item(row, 1).text()
            fecha_ingreso = self.usuarios_table.item(row, 2).text()
            fecha_vencimiento = self.usuarios_table.item(row, 3).text()

            # Retrieve user ID based on selected row data
            
            id_usuario = cursor.execute('''
                SELECT id
                FROM usuarios
                LEFT JOIN membresia on membresia.id_membresia = usuarios.id_membresia
                WHERE usuarios.nombre = ? AND membresia.membresia = ? AND fecha_ingreso = ? AND fecha_vencimiento = ?;
            ''', (nombre, membresia, fecha_ingreso, fecha_vencimiento)).fetchone()[0]
            
            self.editar = EditarUsuario(id_usuario)
            self.editar.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(open('style.css').read())
    login = Login()
    login.show()

    sys.exit(app.exec_())