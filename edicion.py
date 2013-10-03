from trytond.model import ModelSQL, ModelView, fields
from trytond.pyson import Equal
from trytond.pool import Pool

class Edicion(ModelSQL,ModelView):
    'Edicion'
    __name__ = 'edicion.edicion'
    _rec_name = 'fecha'
    fecha = fields.Date('FECHA', readonly=False, required=True)
    cant_hojas = fields.Integer('CANTIDAD DE HOJAS')
    publicaciones = fields.One2Many('edicion.publicacion', 'edicion', 'PUBLICACIONES')

class Publicacion(ModelSQL,ModelView):
    'Publicacion'
    __name__ = 'edicion.publicacion'
    fecha = fields.Date('FECHA')
    cliente = fields.Many2One('party.party', 'CLIENTE', required=True)
    tipo = fields.Char('TIPO', required=True)
    producto = fields.Many2One('product.product', 'PRODUCTO', required=True)
    ubicacion = fields.Char('UBICACION', required=True)
    medidas = fields.Numeric('MEDIDAS', required=True)
    edicion = fields.Many2One('edicion.edicion', 'EDICION', on_change=['edicion'], required=True )
    decrip = fields.Text('DESCRIPCION', required=True)
    esta_publicada = fields.Boolean('Esta Publicada', select=False)

    def on_change_edicion(self):
        v = self.edicion.fecha
        return {'fecha': v}