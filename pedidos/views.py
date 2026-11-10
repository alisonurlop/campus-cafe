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

from .models import DetallePedido, Incidencia, Pedido


def _cajero(user):
    """Devuelve el Empleado si el usuario es Cajero; si no, None."""
    try:
        empleado = user.empleado
    except Empleado.DoesNotExist:
        return None
    return empleado if empleado.puesto == "Cajero" else None


def _cocinero(user):
    """Devuelve el Empleado si el usuario es Cocinero; si no, None."""
    try:
        empleado = user.empleado
    except Empleado.DoesNotExist:
        return None
    return empleado if empleado.puesto == "Cocinero" else None


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
def inicio(request):
    """Manda a cada empleado a su pantalla segun su puesto."""
    if _cajero(request.user):
        return redirect("caja")
    if _cocinero(request.user):
        return redirect("cocina")
    return HttpResponseForbidden("Este usuario no tiene un puesto asignado.")


# ---------- CU-01 Registrar pedido (Cajero) ----------

@login_required
def caja(request):
    if _cajero(request.user) is None:
        return HttpResponseForbidden("Este usuario no es Cajero.")
    lineas, total = _lineas(request)
    alertas = Incidencia.objects.filter(pedido__estatus="Pendiente").select_related("pedido__alumno")
    return render(request, "pedidos/caja.html", {
        "productos": Producto.objects.order_by("nombre"),
        "lineas": lineas,
        "total": total,
        "alertas": alertas,
    })


@login_required
@require_POST
def agregar(request, producto_id):
    if _cajero(request.user) is None:
        return HttpResponseForbidden("Este usuario no es Cajero.")
    producto = get_object_or_404(Producto, id=producto_id)
    # Un producto agotado (marcado por cocina) no se puede vender.
    if not producto.disponible:
        messages.error(request, f"Error: {producto.nombre} está agotado y no se puede agregar.")
        return redirect("caja")
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

    # Si cocina agoto un producto despues de agregarlo al ticket, se quita y no se cobra.
    agotados = [l["producto"] for l in lineas if not l["producto"].disponible]
    if agotados:
        carrito = request.session.get("carrito", {})
        for producto in agotados:
            carrito.pop(str(producto.id), None)
        request.session["carrito"] = carrito
        nombres = ", ".join(p.nombre for p in agotados)
        messages.error(request, f"Error: se agotó {nombres}. Se quitó del ticket; revise la orden.")
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


# ---------- CU-02 Consultar órdenes pendientes y CU-03 Actualizar estado (Cocinero) ----------

@login_required
def cocina(request):
    """CU-02: lista de pedidos pendientes y listos, con su detalle."""
    if _cocinero(request.user) is None:
        return HttpResponseForbidden("Este usuario no es Cocinero.")
    pedidos = (
        Pedido.objects.filter(estatus__in=["Pendiente", "Listo"])
        .select_related("alumno", "incidencia")
        .prefetch_related("detalles__producto")
        .order_by("fecha_hora")
    )
    return render(request, "pedidos/cocina.html", {
        "pedidos": pedidos,
        "productos": Producto.objects.order_by("nombre"),
    })

@login_required
@require_POST
def avanzar(request, pedido_id):
    """CU-03: Pendiente -> Listo -> Entregado."""
    if _cocinero(request.user) is None:
        return HttpResponseForbidden("Este usuario no es Cocinero.")
    siguiente = {"Pendiente": "Listo", "Listo": "Entregado"}
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if pedido.estatus not in siguiente:
        messages.error(request, f"El pedido #{pedido.id} ya fue entregado.")
        return redirect("cocina")
    pedido.estatus = siguiente[pedido.estatus]
    pedido.save()
    messages.success(request, f"Pedido #{pedido.id} marcado como {pedido.estatus}.")
    return redirect("cocina")

#------------CU-05 Registrar incidencia (RF-09)-------------------
@login_required
@require_POST
def incidencia(request, pedido_id):
    """CU-05: el cocinero reporta un problema (por ejemplo, falta de insumos)."""
    if _cocinero(request.user) is None:
        return HttpResponseForbidden("Este usuario no es Cocinero.")
    pedido = get_object_or_404(Pedido, id=pedido_id, estatus="Pendiente")
    descripcion = request.POST.get("descripcion", "").strip()
    if not descripcion:
        messages.error(request, "Error: describa qué insumo falta.")
        return redirect("cocina")
    Incidencia.objects.update_or_create(pedido=pedido, defaults={"descripcion": descripcion})
    messages.success(request, f"Incidencia registrada en el pedido #{pedido.id}. Se avisó al cajero.")
    return redirect("cocina")


@login_required
@require_POST
def disponibilidad(request, producto_id):
    """CU-05: el cocinero marca un producto como agotado o vuelve a ponerlo disponible."""
    if _cocinero(request.user) is None:
        return HttpResponseForbidden("Este usuario no es Cocinero.")
    producto = get_object_or_404(Producto, id=producto_id)
    producto.disponible = not producto.disponible
    producto.save()
    if producto.disponible:
        messages.success(request, f"{producto.nombre} volvió a estar disponible en caja.")
    else:
        messages.success(request, f"{producto.nombre} marcado como agotado. Caja ya no puede venderlo.")
    return redirect("cocina")

# ---------- CU-04 Consultar estado del pedido (Estudiante) ----------

def estado(request):
    """CU-04: el alumno consulta el estado de sus pedidos con su matricula."""
    matricula = request.GET.get("matricula", "").strip()
    alumno = None
    pedidos = []
    error = ""
    if matricula:
        alumno = Alumno.objects.filter(matricula=matricula).first()
        if alumno is None:
            error = "Matrícula no registrada. Verifique los datos."
        else:
            pedidos = Pedido.objects.filter(alumno=alumno).order_by("-fecha_hora")[:5]
    return render(request, "pedidos/estado.html", {
        "matricula": matricula, "alumno": alumno, "pedidos": pedidos, "error": error,
    })