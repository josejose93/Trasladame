# TRASLADAME

## Configuración
Primero debemos clonar o descargar el repositorio
```
git clone https://github.com/josejose93/Trasladame.git
```

Una vez clonado, dentro de la carpeta del repo (Trasladame), crearemos un ambiente virtual, ASEGUREMONOS DE TENER INSTALADO VENV (VIRTUAL ENVIRONMENT) PARA ESTO

```
python3 -m venv trasladame-env
```
Entramos al ambiente virtual
```
source trasladame-env/bin/activate
```

Luego instalamos los paquetes necesarios para que nuestro Backend funcione con pip o pip3 deacuerdo a nuestra configuración, en el ejemplo usaré pip

```
pip install -r requirements.txt
```

Asegurémonos de tener una base de datos postgres
```
createdb trasladame_db
```

Ya estamos listos para arrancar el backend, para esto navegamos a la carpeta mencionada, la configuración del backend la encontraremos en: [backend](https://github.com/josejose93/Trasladame/tree/main/backend) pero antes naveguemos a la carpeta con:
```
cd backend
```
