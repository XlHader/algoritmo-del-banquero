""" Algoritmo del Banquero - Sistema de Gestión de Recursos 
    Desarrollado por Hader G. Rincón Ortiz
    Universidad Technológica de Pereira
    Fecha: 20 de marzo de 2025
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit,
    QMessageBox, QGridLayout, QGroupBox,
    QListWidget
)
from PyQt5.QtCore import Qt, QTimer

STYLE_SHEET = """
    QMainWindow {
        background-color: #f0f0f0;
    }
    QGroupBox {
        border: 2px solid #c0c0c0;
        border-radius: 5px;
        margin-top: 1ex;
        font-weight: bold;
        background-color: white;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 3px 0 3px;
        color: #2c3e50;
    }
    QPushButton {
        background-color: #3498db;
        color: white;
        border: none;
        padding: 8px;
        border-radius: 4px;
        font-weight: bold;
    }
    QPushButton:disabled {
        background-color: #bdc3c7;
    }
    QPushButton:hover {
        background-color: #2980b9;
    }
    QLineEdit {
        padding: 6px;
        border: 2px solid #bdc3c7;
        border-radius: 4px;
        background-color: white;
    }
    QLineEdit:disabled {
        background-color: #ecf0f1;
        border-color: #95a5a6;
    }
    QListWidget {
        border: 1px solid #bdc3c7;
        border-radius: 4px;
        background-color: white;
    }
    QLabel {
        color: #2c3e50;
        font-weight: bold;
    }
"""


class BankersAlgorithm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(
            "Algoritmo del Banquero - Sistema de Gestión de Recursos")
        self.setGeometry(100, 100, 1400, 900)
        self.setStyleSheet(STYLE_SHEET)

        # Variables del algoritmo
        self.n_recursos = 0
        self.n_procesos = 0
        self.vector_E = []
        self.vector_P = []
        self.vector_A = []
        self.matriz_asignados = []
        self.matriz_necesitados = []
        self.secuencia_resultado = []
        self.paso_actual = 0

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.setup_ui()

    def setup_ui(self):
        # Panel superior
        top_panel = QHBoxLayout()

        # Panel de entrada
        input_group = QGroupBox("Entrada de Datos")
        input_layout = QVBoxLayout()

        # Configuración inicial
        config_layout = QHBoxLayout()
        self.process_input = QLineEdit()
        self.resource_input = QLineEdit()
        config_layout.addWidget(QLabel("Procesos:"))
        config_layout.addWidget(self.process_input)
        config_layout.addWidget(QLabel("Recursos:"))
        config_layout.addWidget(self.resource_input)
        self.init_button = QPushButton("Inicializar")
        config_layout.addWidget(self.init_button)
        input_layout.addLayout(config_layout)

        # Entrada de vectores
        vector_layout = QHBoxLayout()
        self.vector_input = QLineEdit()
        self.vector_input.setPlaceholderText("Inicialice el sistema primero")
        self.vector_input.setEnabled(False)
        vector_layout.addWidget(self.vector_input)
        input_layout.addLayout(vector_layout)

        # Estado actual
        estado_group = QGroupBox("Estado Actual del Sistema")
        estado_layout = QGridLayout()
        self.label_E = QLabel("Vector E: No establecido")
        self.label_P = QLabel("Vector P: No establecido")
        self.label_A = QLabel("Vector A: No establecido")
        estado_layout.addWidget(self.label_E, 0, 0)
        estado_layout.addWidget(self.label_P, 1, 0)
        estado_layout.addWidget(self.label_A, 2, 0)
        estado_group.setLayout(estado_layout)

        # Botones de acción
        button_layout = QHBoxLayout()

        # Agregar todos los botones al layout principal
        self.add_existentes_button = QPushButton("Establecer Existentes")
        self.edit_existentes_button = QPushButton("Editar Existentes")
        self.add_asignados_button = QPushButton("Agregar Asignados")
        self.add_necesitados_button = QPushButton("Agregar Necesitados")

        # Deshabilitar botones inicialmente
        self.add_asignados_button.setEnabled(False)
        self.add_necesitados_button.setEnabled(False)
        self.add_existentes_button.setEnabled(False)
        self.edit_existentes_button.setEnabled(False)

        # Agregar los botones al layout en orden
        button_layout.addWidget(self.add_existentes_button)
        button_layout.addWidget(self.edit_existentes_button)
        button_layout.addWidget(self.add_asignados_button)
        button_layout.addWidget(self.add_necesitados_button)

        input_layout.addLayout(button_layout)

        self.edit_existentes_button.clicked.connect(self.editar_existentes)

        input_group.setLayout(input_layout)
        self.main_layout.addWidget(input_group)
        self.main_layout.addWidget(estado_group)

        # Panel de visualización
        display_layout = QHBoxLayout()

        # Lista de asignados
        asignados_group = QGroupBox("Recursos Asignados")
        asignados_layout = QVBoxLayout()
        self.lista_asignados = QListWidget()
        asignados_layout.addWidget(self.lista_asignados)
        asignados_group.setLayout(asignados_layout)
        display_layout.addWidget(asignados_group)

        self.lista_asignados.setContextMenuPolicy(Qt.CustomContextMenu)
        self.lista_asignados.customContextMenuRequested.connect(
            lambda pos: self.mostrar_menu_contextual(
                self.lista_asignados, "asignados", pos)
        )

        # Lista de necesitados
        necesitados_group = QGroupBox("Recursos Necesitados")
        necesitados_layout = QVBoxLayout()
        self.lista_necesitados = QListWidget()
        necesitados_layout.addWidget(self.lista_necesitados)
        necesitados_group.setLayout(necesitados_layout)
        display_layout.addWidget(necesitados_group)

        self.main_layout.addLayout(display_layout)

        # Después de crear self.lista_necesitados
        self.lista_necesitados.setContextMenuPolicy(Qt.CustomContextMenu)
        self.lista_necesitados.customContextMenuRequested.connect(
            lambda pos: self.mostrar_menu_contextual(
                self.lista_necesitados, "necesitados", pos)
        )

        # Panel de resultados
        results_group = QGroupBox("Resultados")
        results_layout = QVBoxLayout()
        self.lista_resultados = QListWidget()
        results_layout.addWidget(self.lista_resultados)
        results_group.setLayout(results_layout)
        self.main_layout.addWidget(results_group)

        # Botón de ejecución
        self.run_button = QPushButton("Ejecutar Algoritmo")
        self.run_button.setEnabled(False)
        self.main_layout.addWidget(self.run_button)

        # Timer para mostrar resultados paso a paso
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.mostrar_siguiente_paso)

        # Conexiones
        self.init_button.clicked.connect(self.inicializar_sistema)
        self.add_asignados_button.clicked.connect(self.agregar_asignados)
        self.add_necesitados_button.clicked.connect(self.agregar_necesitados)
        self.add_existentes_button.clicked.connect(self.establecer_existentes)
        self.run_button.clicked.connect(self.ejecutar_algoritmo)

    def inicializar_sistema(self):
        try:
            self.n_procesos = int(self.process_input.text())
            self.n_recursos = int(self.resource_input.text())
            if self.n_procesos <= 0 or self.n_recursos <= 0:
                raise ValueError("Los valores deben ser positivos")

            # Deshabilitar el botón de ejecución al inicializar
            self.run_button.setEnabled(False)

            # Inicializar estructuras
            self.matriz_asignados = []
            self.matriz_necesitados = []
            self.vector_E = [0] * self.n_recursos
            self.vector_P = [0] * self.n_recursos
            self.vector_A = [0] * self.n_recursos

            # Limpiar listas
            self.lista_asignados.clear()
            self.lista_necesitados.clear()
            self.lista_resultados.clear()

            # Habilitar componentes
            self.vector_input.setEnabled(True)
            self.vector_input.setPlaceholderText(
                f"Ingrese {self.n_recursos} valores separados por espacio")
            self.add_asignados_button.setEnabled(True)
            self.add_necesitados_button.setEnabled(True)
            self.add_existentes_button.setEnabled(True)

            # Actualizar etiquetas de estado
            self.label_E.setText("Vector E: No establecido")
            self.label_P.setText(
                "Vector P: [" + ", ".join(["0"] * self.n_recursos) + "]")
            self.label_A.setText("Vector A: No establecido")

            # Mensaje de confirmación
            QMessageBox.information(self, "Sistema Inicializado",
                                    f"Sistema inicializado con {self.n_procesos} procesos y {self.n_recursos} recursos")

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def editar_existentes(self):
        self.vector_input.setText(" ".join(map(str, self.vector_E)))
        self.add_existentes_button.setEnabled(True)
        self.edit_existentes_button.setEnabled(False)

    def actualizar_etiquetas_estado(self):
        if self.vector_E:
            self.label_E.setText(f"Vector E: {self.vector_E}")
        if self.vector_P:
            self.label_P.setText(f"Vector P: {self.vector_P}")
        if self.vector_A:
            self.label_A.setText(f"Vector A: {self.vector_A}")

    def parse_vector(self, text):
        try:
            valores = [int(x) for x in text.strip().split()]
            if len(valores) != self.n_recursos:
                raise ValueError(f"Se esperaban {self.n_recursos} valores")
            return valores
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
            return None

    def agregar_asignados(self):
        valores = self.parse_vector(self.vector_input.text())
        if valores:
            self.matriz_asignados.append(valores)
            self.lista_asignados.addItem(" ".join(map(str, valores)))
            self.vector_input.clear()

            if len(self.matriz_asignados) == self.n_procesos:
                self.add_asignados_button.setEnabled(False)
                self.actualizar_vector_P()
                self.actualizar_etiquetas_estado()
        self.verificar_inicio()

    def agregar_necesitados(self):
        valores = self.parse_vector(self.vector_input.text())
        if valores:
            self.matriz_necesitados.append(valores)
            self.lista_necesitados.addItem(" ".join(map(str, valores)))
            self.vector_input.clear()

            if len(self.matriz_necesitados) == self.n_procesos:
                self.add_necesitados_button.setEnabled(False)
        self.verificar_inicio()

    def establecer_existentes(self):
        valores = self.parse_vector(self.vector_input.text())
        if valores:
            self.vector_E = valores
            self.add_existentes_button.setEnabled(False)
            self.edit_existentes_button.setEnabled(True)
            self.vector_input.clear()
            self.actualizar_vector_A()
            self.actualizar_etiquetas_estado()
            self.verificar_inicio()

    def actualizar_vector_P(self):
        self.vector_P = [sum(fila[i] for fila in self.matriz_asignados)
                         for i in range(self.n_recursos)]

    def actualizar_vector_A(self):
        self.vector_A = [self.vector_E[i] - self.vector_P[i]
                         for i in range(self.n_recursos)]
        self.actualizar_etiquetas_estado()

    def verificar_inicio(self):
        condiciones_cumplidas = (
            len(self.matriz_asignados) == self.n_procesos and
            len(self.matriz_necesitados) == self.n_procesos and
            # Verificar que vector E esté establecido
            len(self.vector_E) == self.n_recursos and
            all(x >= 0 for x in self.vector_A)
        )

        if condiciones_cumplidas:
            self.run_button.setEnabled(True)
            print("Sistema listo para ejecutar")  # Para debug
        else:
            self.run_button.setEnabled(False)

    def ejecutar_algoritmo(self):
        self.lista_resultados.clear()
        self.lista_resultados.addItem("Estado Inicial:")
        self.lista_resultados.addItem(f"Vector E: {self.vector_E}")
        self.lista_resultados.addItem(f"Vector P: {self.vector_P}")
        self.lista_resultados.addItem(f"Vector A: {self.vector_A}")

        # Iniciar algoritmo
        self.secuencia_resultado = []
        self.paso_actual = 0
        procesos_completados = [False] * self.n_procesos
        vector_A_temp = self.vector_A.copy()

        while len(self.secuencia_resultado) < self.n_procesos:
            encontrado = False
            for i in range(self.n_procesos):
                if not procesos_completados[i]:
                    if all(self.matriz_necesitados[i][j] <= vector_A_temp[j]
                           for j in range(self.n_recursos)):
                        self.secuencia_resultado.append(i)
                        procesos_completados[i] = True
                        vector_A_temp = [vector_A_temp[j] + self.matriz_asignados[i][j]
                                         for j in range(self.n_recursos)]
                        encontrado = True
                        break

            if not encontrado:
                self.lista_resultados.addItem("Estado inseguro detectado!")
                return

        self.lista_resultados.addItem("\nSecuencia segura encontrada!")
        self.timer.start()

    def mostrar_siguiente_paso(self):
        if self.paso_actual < len(self.secuencia_resultado):
            proceso = self.secuencia_resultado[self.paso_actual]
            self.lista_resultados.addItem(f"\nPaso {self.paso_actual + 1}:")
            self.lista_resultados.addItem(f"Proceso P{proceso + 1} completado")

            # Actualizar vectores P y A
            vector_P_temp = [self.vector_P[j] - self.matriz_asignados[proceso][j]
                             for j in range(self.n_recursos)]
            vector_A_temp = [self.vector_E[j] - vector_P_temp[j]
                             for j in range(self.n_recursos)]

            self.lista_resultados.addItem(f"Vector P: {vector_P_temp}")
            self.lista_resultados.addItem(f"Vector A: {vector_A_temp}")

            self.paso_actual += 1
        else:
            self.timer.stop()
            secuencia = " → ".join(f"P{p+1}" for p in self.secuencia_resultado)
            self.lista_resultados.addItem(f"\nSecuencia final: {secuencia}")

    def crear_menu_contextual(self, lista, tipo):
        from PyQt5.QtWidgets import QMenu
        menu = QMenu()
        editar_action = menu.addAction("Editar")
        eliminar_action = menu.addAction("Eliminar")

        def on_editar():
            item = lista.currentItem()
            if item:
                valores = item.text().split()
                self.vector_input.setText(item.text())
                if tipo == "asignados":
                    self.matriz_asignados.pop(lista.currentRow())
                    self.add_asignados_button.setEnabled(True)
                else:
                    self.matriz_necesitados.pop(lista.currentRow())
                    self.add_necesitados_button.setEnabled(True)
                lista.takeItem(lista.currentRow())
                self.actualizar_vector_P()
                self.actualizar_vector_A()
                self.actualizar_etiquetas_estado()
                self.verificar_inicio()

        def on_eliminar():
            if lista.currentItem():
                if tipo == "asignados":
                    self.matriz_asignados.pop(lista.currentRow())
                    self.add_asignados_button.setEnabled(True)
                else:
                    self.matriz_necesitados.pop(lista.currentRow())
                    self.add_necesitados_button.setEnabled(True)
                lista.takeItem(lista.currentRow())
                self.actualizar_vector_P()
                self.actualizar_vector_A()
                self.actualizar_etiquetas_estado()
                self.verificar_inicio()

        editar_action.triggered.connect(on_editar)
        eliminar_action.triggered.connect(on_eliminar)
        return menu

    def mostrar_menu_contextual(self, lista, tipo, position):
        menu = self.crear_menu_contextual(lista, tipo)
        menu.exec_(lista.viewport().mapToGlobal(position))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BankersAlgorithm()
    window.show()
    sys.exit(app.exec_())
