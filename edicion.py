from trytond.model import ModelSQL, ModelView, fields
from trytond.wizard import Wizard, StateView, StateTransition, Button
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


class PublicacionPresupuestado(ModelSQL,ModelView):
    'PublicacionPresupuestado'
    __name__ = 'edicion.publicacion_presupuestado'
    fecha = fields.Date('FECHA')
    cliente = fields.Many2One('party.party', 'CLIENTE', required=True)
    venta = fields.Many2One('sale.sale', 'VENTA', required=True)
    linea = fields.Many2One('sale.line', 'LINEA', required=True, ondelete='CASCADE')
    tipo = fields.Char('TIPO', required=True)
    producto = fields.Many2One('product.product', 'PRODUCTO', required=True)
    ubicacion = fields.Char('UBICACION', required=True)
    medidas = fields.Numeric('MEDIDAS', required=True)
    descrip = fields.Text('DESCRIPCION', required=True)


class Info(ModelView):
    'Info'
    __name__ = 'edicion.info'
    info = fields.Char('INFO', readonly=True)


class ActualizarWizard(Wizard):
    'ActualizarWizard'
    __name__ = 'edicion.actualizar_wizard'

    start = StateView('edicion.info',
                      'edicion.comenzar_form',
                      [Button('Cancelar', 'end', 'tryton-cancel'),
                      Button('Siguiente', 'actualizar', 'tryton-go-next', default=True)])

    finalizar = StateView('edicion.info',
                      'edicion.finalizar_form',
                      [Button('Finalizar', 'end', 'tryton-go-next', default=True)])

    actualizar = StateTransition()

    def crear_publicacion(self,cliente,producto,descripcion,medidas,ubic,fecha):
        edicion = Pool().get('edicion.edicion')
        publicacion = Pool().get('edicion.publicacion')
        edic = 0
        try:
            edic= edicion(edicion.search([('fecha', '=', fecha)])[0])
        except:
            edic=edicion.create([{
            'fecha':fecha
            }])[0]
            edic.save()
        pub = publicacion.create([{
            'fecha':fecha,
            'cliente':cliente,
            'edicion':edic,
            'tipo': producto.category.name,
            'producto' : producto,
            'descrip' : descripcion ,
            'medidas' : medidas,
            'ubicacion': ubic
            }])[0]
        pub.save()

    def transition_actualizar(self):
        pub_pres = Pool().get('edicion.publicacion_presupuestado')
        desactualizadas= pub_pres.search([('venta.state', '=', 'processing')])
        for d in desactualizadas:
            self.crear_publicacion(d.cliente,d.producto,d.descrip,d.medidas,d.ubicacion,d.fecha)
            pub_pres.delete([d])
        return 'finalizar'