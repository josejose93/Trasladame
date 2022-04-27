# TRASLADAME Backend

## Configuración
Lo primero que haremos será configurar nuestras variables de ambiente, navegamos a core.
```
cd core
```

Una vez en core, creamos un archivo .env
```
touch .env
```

Dentro del archivo .env pondremos lo siguiente reemplazando DATABASE USERNAME y PASSWORD con el nombre de la database, el usuario postgres y la contraseña respectivamente (TODO SIN ESPACIOS):

```
DATABASE_NAME=DATABASE
DATABASE_USER=USERNAME
DATABASE_PASS=PASSWORD
```

Por ejemplo, si creamos anteriormente la base de datos trasladame_db, la primera línea del archivo .env sería:
```
DATABASE_NAME=trasladame_db
```

Una vez hecho esto, regresamos a la carpeta raíz del backend
```
cd ..
```

Ahora como último paso haremos las migraciones de la base de datos

```
python manage makemigrations
python manage migrate
```

Ya estamos listos para correr nuestro servido backend !!!
```
python manage runserver
```

Abrimos otra terminal en la que configuraremos el servidor frontend, continuaremos los siguientes pasos aquí: [frontend](https://github.com/josejose93/Trasladame/tree/main/frontend)
