from sqlalchemy import create_engine, select, String, Integer, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


# Conexión a la base de datos SQLite.
# El archivo zapateria.db se crea al conectarse si todavía no existe.
engine = create_engine("sqlite:///zapateria.db", echo=False)


# Clase base declarativa de SQLAlchemy.
class Base(DeclarativeBase):
    pass


# Modelo ORM que representa la tabla "zapatos".
class Zapato(Base):
    __tablename__ = "zapatos"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    modelo: Mapped[str] = mapped_column(String(100), nullable=False)
    talla: Mapped[int] = mapped_column(Integer, nullable=False)
    precio: Mapped[float] = mapped_column(Float, nullable=False)


def inicializar_bd():
    """Crea las tablas definidas en los modelos si todavía no existen."""
    Base.metadata.create_all(engine)


def crear_zapato(modelo, talla, precio):
    """Registra un zapato. Devuelve True si se confirma el registro."""
    try:
        with Session(engine) as sesion:
            zapato = Zapato(modelo=modelo, talla=talla, precio=precio)
            sesion.add(zapato)
            sesion.commit()
            return True
    except Exception as error:
        print(f"Error al registrar el zapato: {error}")
        return False


def listar_zapatos():
    """Devuelve una lista con todos los zapatos."""
    with Session(engine) as sesion:
        consulta = select(Zapato).order_by(Zapato.id)
        return list(sesion.scalars(consulta).all())


def buscar_zapato(id_zapato):
    """Devuelve el zapato encontrado o None si el ID no existe."""
    with Session(engine) as sesion:
        return sesion.get(Zapato, id_zapato)


def actualizar_precio(id_zapato, nuevo_precio):
    """Actualiza el precio. Devuelve False si el ID no existe."""
    with Session(engine) as sesion:
        zapato = sesion.get(Zapato, id_zapato)
        if zapato is None:
            return False

        zapato.precio = nuevo_precio
        sesion.commit()
        return True


def eliminar_zapato(id_zapato):
    """Elimina un zapato. Devuelve False si el ID no existe."""
    with Session(engine) as sesion:
        zapato = sesion.get(Zapato, id_zapato)
        if zapato is None:
            return False

        sesion.delete(zapato)
        sesion.commit()
        return True
