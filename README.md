# Algoritmo del Banquero - Simulación de Gestión de Recursos

Este proyecto implementa el **Algoritmo del Banquero** utilizando Python y PyQt5. Permite simular la asignación de recursos y verificar la seguridad del sistema, mostrando de manera interactiva la secuencia de procesos que evita bloqueos (deadlocks).

## Características

- Interfaz gráfica basada en PyQt5.
- Configuración interactiva de recursos y procesos.
- Simulación del Algoritmo del Banquero para determinar secuencias seguras.
- Visualización paso a paso del proceso de liberación de recursos.

## Requisitos

- **Python 3.x**
- **PyQt5**

Para instalar las dependencias, ejecuta:

```bash
pip install -r requirements.txt
```

o

```bash
pip install PyQt5
```

Si deseas compilar la aplicación en ejecutable, instala también **PyInstaller**:

```bash
pip install pyinstaller
```

## Ejecución con Python

Para ejecutar la aplicación directamente desde el código fuente:

```bash
python bank.py
```

## Generar Ejecutables

### En Windows

1. Abre una terminal (CMD o PowerShell) y navega hasta el directorio del proyecto.
2. Ejecuta el siguiente comando para crear un único archivo ejecutable:
   ```bash
   pyinstaller --onefile --noconsole --name=BanqueroApp bank.py
   ```
   - `--onefile`: Genera un único archivo.
   - `--noconsole`: Evita mostrar la consola (opcional para aplicaciones GUI).
   - `--name`: Especifica el nombre del ejecutable.

3. El ejecutable se generará en la carpeta `dist/` como `BanqueroApp.exe`.
4. Ejecuta el archivo generado para usar la aplicación en Windows.

### En Linux (Ubuntu)

1. Abre una terminal y dirígete al directorio del proyecto.
2. Ejecuta el siguiente comando:
   ```bash
   pyinstaller --onefile --name=banquero_app bank.py
   ```
3. Se generará un binario en la carpeta `dist/` llamado `banquero_app`.
4. Si es necesario, dale permisos de ejecución:
   ```bash
   chmod +x dist/banquero_app
   ```
5. Ejecuta el binario:
   ```bash
   ./dist/banquero_app
   ```