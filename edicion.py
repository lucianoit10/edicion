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

    @classmethod
    def __setup__(cls):
        super(Edicion, cls).__setup__()
        cls._sql_constraints = [
            ('edicion_fecha', 'UNIQUE(fecha)',
                'no se pueden crear 2 ediciones con la misma fecha'),
            ]

class Publicacion(ModelSQL,ModelView):
    'Publicacion'
    __name__ = 'edicion.publicacion'
    fecha = fields.Date('FECHA')
    cliente = fields.Many2One('party.party', 'CLIENTE', required=True)
    linea = fields.Many2One('sale.line', 'LINEA', required=True, ondelete='CASCADE')
    tipo = fields.Char('TIPO', required=True)
    producto = fields.Many2One('product.product', 'PRODUCTO', required=True)
    ubicacion = fields.Char('UBICACION', required=True)
    medidas = fields.Numeric('MEDIDAS', required=True)
    edicion = fields.Many2One('edicion.edicion', 'EDICION', on_change=['edicion'], required=True )
    descrip = fields.Text('DESCRIPCION', required=True)
    esta_publicada = fields.Boolean('Esta Publicada', select=False)

    def on_change_edicion(self):
        v = self.edicion.fecha
        return {'fecha': v}

class EdicionPresupuestado(ModelSQL):
    'EdicionPresupuestado'
    __name__ = 'edicion.edicion_presupuestado'
    _rec_name = 'fecha'
    fecha = fields.Date('FECHA', readonly=False, required=True)
    publicaciones = fields.One2Many('edicion.publicacion_presupuestado', 'edicion', 'PUBLICACIONES')

    @classmethod
    def __setup__(cls):
        super(EdicionPresupuestado, cls).__setup__()
        cls._sql_constraints = [
            ('edicion_fecha', 'UNIQUE(fecha)',
                'no se pueden crear 2 ediciones con la misma fecha'),
            ]

class PublicacionPresupuestado(ModelSQL):
    'Publicacion'
    __name__ = 'edicion.publicacion_presupuestado'
    fecha = fields.Date('FECHA')
    cliente = fields.Many2One('party.party', 'CLIENTE', required=True)
    venta = fields.Many2One('sale.sale', 'VENTA', required=True)
    linea = fields.Many2One('sale.line', 'LINEA', required=True, ondelete='CASCADE')
    tipo = fields.Char('TIPO', required=True)
    producto = fields.Many2One('product.product', 'PRODUCTO', required=True)
    ubicacion = fields.Char('UBICACION', required=True)
    medidas = fields.Numeric('MEDIDAS', required=True)
    edicion = fields.Many2One('edicion.edicion_presupuestado', 'EDICION', on_change=['edicion'], required=True )
    descrip = fields.Text('DESCRIPCION', required=True)

    def on_change_edicion(self):
        v = self.edicion.fecha
        return {'fecha': v}