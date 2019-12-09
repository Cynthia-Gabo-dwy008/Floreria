class elemento:
    cod=0
    nombre=""
    valor=0
    cantidad=0

    def __init__(self,codigo,nombre,valor,cantidad):
        self.cod=codigo
        self.nombre=nombre
        self.valor=valor
        self.cantidad=cantidad
    
    def toString(self):
        return {
            'codigo': str(self.cod),
            'nombre': self.nombre,
            'valor': str(self.valor),
            'cantidad': str(self.cantidad),
            'total':str(self.total())
        }
    def total(self):
        return str(int(self.valor)*int(self.cantidad))
    