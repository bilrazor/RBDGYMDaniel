# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.hashers import make_password

class Tcategorias(models.Model):
    categoriaid = models.AutoField(db_column='CategoriaId', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=20)  # Field name made lowercase.
    imagen = models.CharField(db_column='Imagen', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'tcategorias'


class Tclases(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=40)  # Field name made lowercase.
    horarios = models.CharField(db_column='Horarios', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tclases'


class Tpedidos(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    fecha = models.DateField(db_column='Fecha', blank=True, null=True)  # Field name made lowercase.
    cantidad = models.IntegerField(db_column='Cantidad')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tpedidos'


class Tpersona(models.Model):
    idpersona = models.AutoField(db_column='IdPersona', primary_key=True)  # Field name made lowercase.
    dni = models.CharField(max_length=50, blank=True, null=True)
    nombre = models.CharField(max_length=500, blank=True, null=True)
    correo = models.CharField(max_length=200, blank=True, null=True)
    password = models.CharField(max_length=200, blank=True, null=True)
    pago = models.IntegerField(db_column='Pago', blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(max_length=2000, blank=True, null=True)
    telefono = models.IntegerField(blank=True, null=True)
    session_token = models.CharField(max_length=2000, blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    class Meta:
        managed = False
        db_table = 'tpersona'


class Tproductos(models.Model):
    productosid = models.AutoField(db_column='ProductosId', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=400)  # Field name made lowercase.
    color = models.CharField(db_column='Color', max_length=100, blank=True, null=True)  # Field name made lowercase.
    precio = models.CharField(db_column='Precio', max_length=100, blank=True, null=True)  # Field name made lowercase.
    descripcion = models.CharField(db_column='Descripcion', max_length=250)  # Field name made lowercase.
    imagen = models.CharField(db_column='Imagen', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    categoriaid = models.ForeignKey(Tcategorias, models.DO_NOTHING, db_column='CategoriaID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tproductos'
