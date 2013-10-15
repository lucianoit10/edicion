from trytond.pool import Pool
from .edicion import *

def register():
     Pool.register(
        Edicion,
        Publicacion,
        #EdicionPresupuestado,
        PublicacionPresupuestado,
        Info,
        module='edicion', type_='model')

Pool.register(
        ActualizarWizard,
        module='edicion', type_='wizard')
