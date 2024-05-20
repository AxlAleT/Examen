from bd.db_controlador import sesion
from modelos.Servicio import Servicio

class ServicioControlador:
    """
    Controlador para la gestión de los servicios.

    Methods:
        obtener_servicios(): Obtiene una lista de tuplas con el nombre del servicio y su número de convenio.
    """

    @staticmethod
    def obtener_servicios():
        """
        Obtiene una lista de tuplas con el nombre del servicio y su número de convenio.

        Returns:
            list: Lista de tuplas (nombre del servicio, número de convenio).
        """
        servicios = sesion.query(Servicio).all()
        lista_servicios = [(servicio.NombreServicio, servicio.Num_Convenio) for servicio in servicios]
        return lista_servicios
