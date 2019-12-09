from django.db import models

class Estado(models.Model):
    name=models.CharField(max_length=100,primary_key=True)

    def __str__(self):
        return self.name


class Flores(models.Model):
    name=models.CharField(max_length=100, primary_key=True)
    valor=models.IntegerField()
    descripcion=models.TextField()
    estado=models.ForeignKey(Estado,on_delete=models.CASCADE)
    stock=models.IntegerField()
    fotografia=models.ImageField(upload_to="flores",null=True)

    def __str__(self):
        return self.name


class Comprobante(models.Model):
    usuario=models.CharField(max_length=100)
    nombre=models.CharField(max_length=100)
    valor=models.IntegerField()
    cantidad=models.IntegerField()
    total=models.IntegerField()
    fecha=models.DateField()

    def __str__(self):
        return str(self.usuario)+' '+str(self.nombre)

