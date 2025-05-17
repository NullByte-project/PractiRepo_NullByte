# PractiRepo
#### Por NullByte Team

PractiRepo es una aplicación web para subir y visualizar informes y documentos de prácticas de la carrera de Desarrollo Familiar de la Universidad de Caldas.





## A instalar
Serán instalados:
- Git: Para clonar el repositorio.
- Python (3.8 o superior): Lenguaje base del proyecto.
- pip: Gestor de paquetes de Python.
- FastAPI: Framework para APIs de Python.
- Otros requerimientos de `requirements.txt`.

También: Será clonado el repositorio del proyecto.

## Cómo instalar Git
🔹En Windows:
- Ve a: https://git-scm.com/download/win
- El instalador se descargará automáticamente.
- Ejecuta el archivo .exe descargado.
- Acepta las opciones por defecto (puedes dejar todo como está).
- Al finalizar, abre CMD o PowerShell y escribe:
```http
git --version
```
✅ Si ves la versión, Git está instalado correctamente.

🔹En Ubuntu/Debian/Linux:
```http
sudo apt update
sudo apt install git
git --version
```

🔹En macOS:
- Opción 1 – usando Homebrew:
```http
brew install git
```
- Opción 2 – usando Xcode:
Simplemente escribe `git` en la terminal y el sistema te ofrecerá instalar las herramientas de línea de comandos de Xcode (incluye Git).
## Cómo instalar Python
🔹En Windows:
- Ve a: https://www.python.org/downloads/
- Descarga e instala la última versión de Python.
- Asegúrate de marcar "Add Python to PATH" durante la instalación.
- Verifica desde la terminal (CMD o PowerShell):
```http
python --version
```

🔹En Ubuntu/Debian/Linux:
```http
sudo apt update
sudo apt install python3 python3-pip
python3 --version
```

🔹En macOS:
```http
brew install python
python3 --version
```

## Cómo instalar Pip
🔹En Windows:
Si instalaste Python desde python.org, pip ya viene incluido.

Verifica con:
```http
pip --version
```
Si no aparece, prueba:
```http
python -m ensurepip --upgrade
```

🔹En Ubuntu/Debian/Linux:
```http
sudo apt update
sudo apt install python3-pip
pip3 --version
```
Nota: Usa pip3 si tu sistema diferencia entre Python 2 y 3.

🔹En macOS:
Si tienes instalado Python con Homebrew:
```http
brew install python
pip3 --version
```


## Cómo clonar el repositorio
Para clonar el repositorio ejecute los siguientes comandos, para clonar y para crear la carpeta de la aplicación:
```http
git clone https://github.com/NullByte-project/PractiRepo_NullByte.git
cd PractiRepo
```
## Cómo instalar los requerimientos
Para instalar todas las dependencias ejecute el comando:
```http
pip install -r requirements.txt
```
## Cómo ejecutar la aplicación
Para ejecutar la aplicación debemos en visual studio abrir por separado la carpeta del frontend y el backend. Seguido, hacemos lo siguiente:
- Backend:
```http
uvicorn main:app --reload
```
- Frontend:
```http
ng serve -o
```
