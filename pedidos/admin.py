from django.contrib import admin

from .models import DetallePedido, Incidencia, Pedido

admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(Incidencia)