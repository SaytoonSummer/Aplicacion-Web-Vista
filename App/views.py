from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from datetime import datetime
from .firebase_config import auth, database, get_user_info_from_firebase
from reportlab.pdfgen import canvas
from .models import Producto, Proveedor
from reportlab.lib.pagesizes import letter
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from requests.exceptions import HTTPError
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


def ventas(request):
    productos = Producto.objects.all()

    if request.method == 'POST':
        producto_id = int(request.POST.get('producto_id'))
        nueva_cantidad = int(request.POST.get('cantidad'))

        producto = get_object_or_404(Producto, pk=producto_id)
        cantidad_vendida = producto.cantidad - \
            nueva_cantidad

        producto.cantidad = nueva_cantidad

        producto.ventas += cantidad_vendida
        producto.save()

        firebase_id = str(producto.id)
        data_firebase = {
            'nombre_producto': producto.nombre_producto,
            'descripcion': producto.descripcion,
            'precio': str(producto.precio),
            'cantidad': str(producto.cantidad),
            'ventas': str(producto.ventas),
        }
        database.child('Producto').child(firebase_id).update(data_firebase)

    context = {'productos': productos}
    return render(request, 'App/ventas.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = auth.sign_in_with_email_and_password(username, password)

            request.session['firebase_user_id'] = user['localId']
            request.session['firebase_user_token'] = user['idToken']

            return redirect('inventory')

        except Exception as e:
            print(f"Error de autenticación: {e}")
            messages.error(
                request, 'Error de autenticación. Por favor, verifica tus credenciales.')

    return render(request, 'App/login.html')


def user(request):
    firebase_user_id = request.session.get('firebase_user_id')
    firebase_user_token = request.session.get('firebase_user_token')

    if firebase_user_id and firebase_user_token:
        try:
            user_info = get_user_info_from_firebase(firebase_user_token)

            email = user_info['users'][0]['email'] if user_info and 'users' in user_info else None
            context = {
                'username': email,
            }

            return render(request, 'App/user.html', context)

        except HTTPError as e:
            print(f"Error al obtener información del usuario de Firebase: {e}")

    messages.error(
        request, 'Error al obtener información del usuario de Firebase.')
    return redirect('login')


def index(request):
    return render(request, 'App/index.html')


def contact(request):
    return render(request, 'App/contact.html')


def support(request):
    return render(request, 'App/support.html')


def obtener_datos_para_reporte():
    productos = Producto.objects.all()
    return productos


def report(request):
    productos = Producto.objects.all()

    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    nombre_archivo = f"reporte_inventario_{fecha_actual}.pdf"

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'

    pdf = SimpleDocTemplate(response, pagesize=letter)
    data = [['Nombre del Producto', 'Descripción', 'Precio', 'Cantidad', 'Ventas']]

    for producto in productos:
        data.append([producto.nombre_producto, producto.descripcion, str(
            producto.precio), str(producto.cantidad), str(producto.ventas)])

    tabla = Table(data)
    estilo_tabla = TableStyle([('BACKGROUND', (0, 0), (-1, 0), '#EB5E28'),
                              ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
                              ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                              ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                              ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                              ('BACKGROUND', (0, 1), (-1, -1), '#FFFCF2')])

    tabla.setStyle(estilo_tabla)

    elementos = [tabla]
    pdf.build(elementos)

    return response


def inventory(request):
    data_firebase = database.child('Producto').get().val()

    numero_objetos = len(data_firebase) if data_firebase else 0

    productos = Producto.objects.all()

    ventas_totales = sum(producto.ventas for producto in productos)

    context = {
        'productos': productos,
        'numero_objetos': numero_objetos,
        'ventas_totales': ventas_totales,
    }

    return render(request, 'App/inventory.html', context)


def input(request):
    if request.method == 'POST':
        nombre_producto = request.POST.get('nombre_producto', '')
        descripcion = request.POST.get('descripcion', '')
        precio = request.POST.get('precio', '')
        cantidad = request.POST.get('cantidad', '')

        nuevo_producto = Producto(
            nombre_producto=nombre_producto,
            descripcion=descripcion,
            precio=precio,
            cantidad=cantidad,
        )
        nuevo_producto.save()

        nuevo_producto_id = nuevo_producto.id

        data_firebase = {
            'nombre_producto': nombre_producto,
            'descripcion': descripcion,
            'precio': precio,
            'cantidad': cantidad,
        }
        database.child('Producto').child(nuevo_producto_id).set(data_firebase)

        return redirect('inventory')

    return render(request, 'App/input.html')


def update(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)

    if request.method == 'POST':
        producto.nombre_producto = request.POST.get('nombre_producto', '')
        producto.descripcion = request.POST.get('descripcion', '')
        producto.precio = request.POST.get('precio', '')
        producto.cantidad = request.POST.get('cantidad', '')
        producto.save()

        data_firebase = {
            'nombre_producto': producto.nombre_producto,
            'descripcion': producto.descripcion,
            'precio': producto.precio,
            'cantidad': producto.cantidad,
        }
        database.child('Producto').child(producto.id).update(data_firebase)

        return redirect('inventory')

    return render(request, 'App/update.html', {'producto': producto})


def delete(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)

    if request.method == 'POST':
        try:
            firebase_id = str(producto.id)

            database.child('Producto').child(firebase_id).remove()
        except Exception as e:
            print(f"Error al eliminar producto de Firebase: {e}")

        producto.delete()

        return redirect('inventory')

    return render(request, 'App/delete.html', {'producto': producto})


def stakeholders(request):
    proveedores = Proveedor.objects.all()

    context = {
        'proveedores': proveedores,
    }

    return render(request, 'App/stakeholders.html', context)


def inputsh(request):
    if request.method == 'POST':
        nombre_proveedor = request.POST.get('nombre_proveedor', '')
        direccion = request.POST.get('direccion', '')
        telefono = request.POST.get('telefono', '')
        email = request.POST.get('email', '')

        nuevo_proveedor = Proveedor(
            nombre_proveedor=nombre_proveedor,
            direccion=direccion,
            telefono=telefono,
            email=email,
        )
        nuevo_proveedor.save()

        nuevo_proveedor_id = nuevo_proveedor.id

        data_firebase = {
            'nombre_proveedor': nombre_proveedor,
            'direccion': direccion,
            'telefono': telefono,
            'email': email,
        }
        database.child('Proveedor').child(
            nuevo_proveedor_id).set(data_firebase)

        return redirect('stakeholders')

    return render(request, 'App/inputsh.html')


def updatesh(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, pk=proveedor_id)

    if request.method == 'POST':
        proveedor.nombre_proveedor = request.POST.get('nombre_proveedor', '')
        proveedor.direccion = request.POST.get('direccion', '')
        proveedor.telefono = request.POST.get('telefono', '')
        proveedor.email = request.POST.get('email', '')
        proveedor.save()

        data_firebase = {
            'nombre_proveedor': proveedor.nombre_proveedor,
            'direccion': proveedor.direccion,
            'telefono': proveedor.telefono,
            'email': proveedor.email,
        }
        database.child('Proveedor').child(proveedor.id).update(data_firebase)

        return redirect('stakeholders')

    return render(request, 'App/updatesh.html', {'proveedor': proveedor})


def deletesh(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, pk=proveedor_id)

    if request.method == 'POST':
        try:
            firebase_id = str(proveedor.id)
            database.child('Proveedor').child(firebase_id).remove()
        except Exception as e:
            print(f"Error al eliminar proveedor de Firebase: {e}")

        proveedor.delete()

        return redirect('stakeholders')

    return render(request, 'App/deletesh.html', {'proveedor': proveedor})
