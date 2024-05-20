from bd.db_controlador import sesion
from modelos.Servicio import Servicio

class ServicioControlador:

    @staticmethod
    def obtener_servicios():
        servicios = sesion.query(Servicio).all()
        lista_servicios = [(servicio.NombreServicio, servicio.Num_Convenio) for servicio in servicios]
        return lista_servicios
