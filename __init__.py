from trytond.pool import Pool
from .edicion import *

def register():
     Pool.register(
        Edicion,
        Publicacion,
        EdicionPresupuestado,
        PublicacionPresupuestado,
        module='edicion', type_='model')
