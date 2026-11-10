from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from alumnos.models import Alumno
from catalogo.models import Producto
from empleados.models import Empleado

from .models import DetallePedido, Pedido


def _cajero(user):
    """Devuelve el Empleado si el usuario es Cajero; si no, None."""
    try:
        empleado = user.empleado
    except Empleado.DoesNotExist:
        return None
    return empleado if empleado.puesto == "Cajero" else None


def _lineas(request):
    """Arma el ticket a partir del carrito de la sesion y calcula el total."""
    carrito = request.session.get("carrito", {})
    productos = Producto.objects.filter(id__in=[int(i) for i in carrito])
    lineas = []
    total = Decimal("0")
    for p in productos:
        cantidad = carrito[str(p.id)]
        subtotal = p.precio * cantidad
        lineas.append({"producto": p, "cantidad": cantidad, "subtotal": subtotal})
        total += subtotal
    return lineas, total


@login_required
def caja(request):
    if _cajero(request.user) is None:
        return HttpResponseForbidden("Este usuario no es Cajero.")
    lineas, total = _lineas(request)
    return render(request, "pedidos/caja.html", {
        "productos": Producto.objects.order_by("nombre"),
        "lineas": lineas,
        "total": total,
    })


@login_required
@require_POST
def agregar(request, producto_id):
    if _cajero(request.user) is None:
        return HttpResponseForbidden("Este usuario no es Cajero.")
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = request.session.get("carrito", {})
    carrito[str(producto.id)] = carrito.get(str(producto.id), 0) + 1
    request.session["carrito"] = carrito
    return redirect("caja")


@login_required
@require_POST
def cancelar(request):
    request.session["carrito"] = {}
    messages.info(request, "Orden cancelada. La pantalla quedó lista para otro cliente.")
    return redirect("caja")


@login_required
@require_POST
def cobrar(request):
    empleado = _cajero(request.user)
    if empleado is None:
        return HttpResponseForbidden("Este usuario no es Cajero.")

    lineas, total = _lineas(request)
    if not lineas:
        messages.error(request, "Error: agregue al menos un producto antes de cobrar.")
        return redirect("caja")

    matricula = request.POST.get("matricula", "").strip()
    alumno = Alumno.objects.filter(matricula=matricula).first()
    if alumno is None:
        messages.error(request, "Error: matrícula no registrada en el sistema. Verifique los datos.")
        return redirect("caja")

    with transaction.atomic():
        pedido = Pedido.objects.create(alumno=alumno, empleado=empleado, total=total)
        for linea in lineas:
            DetallePedido.objects.create(
                pedido=pedido,
                producto=linea["producto"],
                cantidad=linea["cantidad"],
                precio_aplicado=linea["producto"].precio,
            )

    request.session["carrito"] = {}
    messages.success(request, f"Orden #{pedido.id} registrada y enviada a cocina.")
    return redirect("caja")