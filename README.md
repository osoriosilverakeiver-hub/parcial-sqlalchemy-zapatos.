# Sistema de inventario de zapatos — SQLAlchemy ORM

## Información del proyecto

- **Estudiante:** Keiver Juseph Osorio Silvera
- **Asignatura:** [Escribe el nombre de la asignatura]
- **Docente:** [Escribe el nombre del docente]
- **Lenguaje:** Python
- **ORM:** SQLAlchemy 2.x
- **Base de datos:** SQLite

## Descripción

Aplicación de consola para administrar el inventario de una tienda de zapatos.
Permite registrar zapatos, listar el inventario, buscar por ID, actualizar
precios y eliminar registros. La persistencia se implementa con SQLAlchemy ORM
y SQLite.

## Estructura

```text
tienda_zapatos/
├── main.py
├── datos.py
├── requirements.txt
├── README.md
└── evidencias/
```

- `main.py`: menú e interacción con el usuario. Se conserva el flujo del programa suministrado.
- `datos.py`: conexión, modelo ORM, creación de tabla y operaciones CRUD.
- `requirements.txt`: dependencia SQLAlchemy.
- `zapateria.db`: archivo SQLite que se genera al ejecutar el programa por primera vez.
- `evidencias/`: capturas reales de las pruebas.

## Instalación y ejecución

Requisitos: Python 3 instalado.

```bash
python -m pip install -r requirements.txt
python main.py
```

En Windows también puede utilizarse `py -m pip install -r requirements.txt`
y `py main.py`.

Al iniciar, `main.py` llama a `datos.inicializar_bd()`. SQLAlchemy crea
`zapateria.db` y la tabla `zapatos` si todavía no existen.

## Implementación ORM

La clase `Zapato` hereda de `Base`, que hereda de `DeclarativeBase`.
`__tablename__ = "zapatos"` define el nombre de la tabla. Los atributos
`id`, `modelo`, `talla` y `precio` se mapean a columnas con `mapped_column`.
El ID es clave primaria y autoincremental.

La conexión se crea con:

```python
engine = create_engine("sqlite:///zapateria.db", echo=False)
```

La creación de tablas se realiza con:

```python
Base.metadata.create_all(engine)
```

## Preguntas técnicas

### 1. ¿Qué clase de Python representa la tabla?

La clase `Zapato` representa la tabla `zapatos`. Hereda de `Base`, una clase
declarativa de SQLAlchemy. El atributo `__tablename__` indica el nombre de la
tabla y cada atributo declarado con `Mapped` y `mapped_column` representa
una columna. En este proyecto, `id` es entero y clave primaria; `modelo` es
texto; `talla` es entero y `precio` es real (`Float`).

### 2. ¿Qué ocurre al ejecutar el programa por primera vez?

`main.py` llama a `datos.inicializar_bd()` antes de mostrar el menú.
Esta función ejecuta `Base.metadata.create_all(engine)`. El motor utiliza
la dirección SQLite `sqlite:///zapateria.db`; si el archivo no existe,
SQLite lo crea. Luego SQLAlchemy crea la tabla `zapatos` según el modelo.
En ejecuciones posteriores, `create_all` no duplica una tabla que ya existe.

### 3. ¿Qué recorrido siguen los datos al registrar?

El menú solicita modelo, talla y precio en `main.py`. Luego llama a
`datos.crear_zapato(modelo, talla, precio)`. La función crea un objeto
`Zapato`, abre una sesión con `Session(engine)`, agrega el objeto mediante
`sesion.add(zapato)` y confirma la transacción con `sesion.commit()`.
Después devuelve `True` para que el menú muestre el mensaje de éxito.

### 4. ¿Para qué se utiliza una sesión? ¿Qué pasa sin commit?

La sesión administra la comunicación y la unidad de trabajo entre los
objetos Python y la base de datos. Se utiliza para agregar, consultar,
modificar y eliminar objetos. `commit()` confirma los cambios pendientes.
Si se cierra la sesión sin confirmar, la transacción pendiente se revierte;
por tanto, el cambio no queda guardado permanentemente.

### 5. ¿Cómo funciona la búsqueda por ID?

`buscar_zapato(id_zapato)` abre una sesión y ejecuta
`sesion.get(Zapato, id_zapato)`. Si encuentra la clave primaria, devuelve
el objeto `Zapato`; si no existe, devuelve `None`. El menú comprueba
ese resultado y muestra los datos o el mensaje "Zapato no encontrado".

### 6. ¿Cómo se actualiza el precio?

`actualizar_precio(id_zapato, nuevo_precio)` obtiene el objeto con
`sesion.get`. Si no existe, devuelve `False`. Si existe, asigna
`zapato.precio = nuevo_precio` y ejecuta `sesion.commit()` para guardar
el cambio. La función devuelve `True` cuando la actualización se confirma.

### 7. ¿Qué ocurre al eliminar?

`eliminar_zapato(id_zapato)` busca primero el objeto. Si no existe,
devuelve `False`. Si existe, llama a `sesion.delete(zapato)` y después
a `sesion.commit()`. Para verificar la eliminación, se puede listar el
inventario o volver a buscar el mismo ID: ya no debe aparecer y la búsqueda
debe devolver `None`.

### 8. ¿Qué sucede al cerrar y volver a ejecutar?

Los registros permanecen porque se guardan en el archivo persistente
`zapateria.db`, no solamente en la memoria del programa. Al ejecutar de
nuevo, el motor se conecta al mismo archivo y las consultas recuperan los
registros confirmados anteriormente. Los registros eliminados no reaparecen.

## Pruebas y evidencias

Ejecuta las pruebas siguientes y guarda capturas reales en `evidencias/`.
No se incluyen capturas simuladas: las imágenes deben corresponder a la
ejecución realizada por el estudiante.

1. **Registro:** registra, por ejemplo, Adidas Run, talla 42, precio 180000;
   y Nike Air, talla 40, precio 220000. Guarda `evidencias/01_registro.png`.
2. **Listado:** selecciona la opción 2 y guarda `evidencias/02_listado.png`.
3. **Búsqueda:** busca por ID uno de los zapatos y guarda
   `evidencias/03_busqueda.png`.
4. **Actualización:** cambia el precio de Adidas Run a 200000 y guarda
   `evidencias/04_actualizacion.png`.
5. **Eliminación:** elimina Nike Air y guarda `evidencias/05_eliminacion.png`.
6. **Persistencia:** sal del programa, vuelve a ejecutar `python main.py`,
   lista los registros y guarda `evidencias/06_persistencia.png`.

Los ID asignados pueden variar. Utiliza los que muestre tu programa.

### Pruebas con un ID inexistente

Prueba buscar, actualizar y eliminar el ID `99999` (siempre que no exista).
La búsqueda devuelve `None` y el menú informa que no encontró el zapato.
La actualización y la eliminación devuelven `False`, muestran que el zapato
no fue encontrado y no cambian los demás registros.

## Conclusiones

1. La implementación permite realizar las operaciones CRUD con SQLAlchemy ORM
   y conservar los datos en SQLite.
2. El ORM permite trabajar con objetos Python y métodos de sesión en lugar
   de escribir manualmente sentencias SQL para cada operación.
3. Fue necesario comprender el ciclo de vida de una sesión y confirmar las
   transacciones con `commit()` para que los cambios quedaran persistidos.

## Repositorio de partida

https://github.com/epimient/orm_sql

**Antes de entregar:** completa los datos de asignatura y docente, ejecuta
todas las pruebas, agrega las capturas reales y verifica que el README las
muestre correctamente en GitHub.
