from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import os
from datetime import date
import mysql.connector
import database as db 

# Configuración
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
app = Flask(__name__, template_folder=template_dir)
app.secret_key = 'your_secret_key'

# Conexión a la base de datos
database = mysql.connector.connect(
    host="localhost",
    user="perez",
    password="",
    database="mercaflask",
    port="3306"
)

# Ruta para el formulario de inicio de sesión
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        rol = request.form['rol']

        cursor = db.db.cursor(dictionary=True)  # Utilizamos db.db para obtener la conexión

        if rol == 'empleado':
            cursor.execute('SELECT * FROM usuarios WHERE Nombre = %s AND cedula = %s', (username, password))
        else:
            cursor.execute('SELECT * FROM admin WHERE nombre = %s AND cc = %s', (username, password))

        user = cursor.fetchone()

        if user:
            session['id_usuario'] = user['ID_usuario'] if rol == 'empleado' else user['cc']
            if rol == 'empleado':
                return redirect(url_for('ventas'))
            else:
                return redirect(url_for('compras'))

        flash('Invalid username or password')
        return redirect(url_for('index'))




# Ruta para la gestión de usuarios
@app.route('/usuarios')
def usuarios():
    cursor = database.cursor()
    cursor.execute("SELECT * FROM usuarios")
    myresult = cursor.fetchall()
    
    # Convertir datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    
    cursor.close()
    return render_template('usuarios.html', data=insertObject)

# Ruta para guardar usuarios en la base de datos
@app.route('/usuarios', methods=['POST'])
def guardar_usuario():
    ID_usuario = request.form['ID_usuario']
    Nombre = request.form['Nombre']
    cedula = request.form['Cedula']
    fecha_registro = request.form['fecha_registro']

    if ID_usuario and Nombre and cedula and fecha_registro:
        try:
            cursor = database.cursor()
            sql = "INSERT INTO usuarios (ID_usuario, Nombre, cedula, fecha_registro) VALUES (%s, %s, %s, %s)"
            data = (ID_usuario, Nombre, cedula, fecha_registro)
            cursor.execute(sql, data)
            database.commit()
        except mysql.connector.errors.IntegrityError:
            flash('Error: El ID de usuario ya existe.', 'error')
        except mysql.connector.errors.DataError:
            flash('Error: El valor de la cédula es demasiado largo.', 'error')

    return redirect(url_for('usuarios'))

# Ruta para eliminar usuarios
@app.route('/delete/<string:id>')
def delete(id):
    cursor = database.cursor()
    sql = "DELETE FROM usuarios WHERE ID_usuario = %s"
    data = (id,)
    cursor.execute(sql, data)
    database.commit()
    return redirect(url_for('usuarios'))

# Ruta para editar usuarios 
@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    ID_usuario = request.form['ID_usuario']
    Nombre = request.form['Nombre']
    cedula = request.form['Cedula']
    fecha_registro = request.form['fecha_registro']

    if ID_usuario and Nombre and cedula and fecha_registro:
        try:
            cursor = database.cursor()
            sql = "UPDATE usuarios SET ID_usuario = %s, Nombre = %s, cedula = %s, fecha_registro = %s WHERE ID_usuario = %s"
            data = (ID_usuario, Nombre, cedula, fecha_registro, id)
            cursor.execute(sql, data)
            database.commit()
        except mysql.connector.errors.IntegrityError:
            flash('Error: El ID de usuario ya existe.', 'error')
        except mysql.connector.errors.DataError:
            flash('Error: El valor de la cédula es demasiado largo.', 'error')

    return redirect(url_for('usuarios'))

# Ruta para mostrar la página de proveedores
@app.route('/proveedores')
def proveedores():
    cursor = database.cursor()
    cursor.execute("SELECT * FROM proveedores")
    myresult = cursor.fetchall()
    
    # Convertir datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    
    cursor.close()
    return render_template('proveedores.html', data=insertObject)

# Ruta para guardar proveedores en la base de datos
@app.route('/proveedores', methods=['POST'])
def guardar_proveedor():
    ID_proveedor = request.form['ID_proveedor']
    Nombre_empresa = request.form['Nombre_empresa']
    Nombre_representante_legal = request.form['Nombre_representante_legal']
    tipo_proveedor = request.form['tipo_proveedor']
    direccion = request.form['direccion']
    telefono = request.form['telefono']
    email = request.form['email']
    URL = request.form['URL']

    if ID_proveedor and Nombre_empresa and Nombre_representante_legal and tipo_proveedor and direccion and telefono and email and URL:
        try:
            cursor = database.cursor()
            sql = "INSERT INTO proveedores (ID_proveedor, Nombre_empresa, Nombre_representante_legal, tipo_proveedor, direccion, telefono, email, URL) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            data = (ID_proveedor, Nombre_empresa, Nombre_representante_legal, tipo_proveedor, direccion, telefono, email, URL)
            cursor.execute(sql, data)
            database.commit()
        except mysql.connector.errors.IntegrityError:
            flash('Error: El ID de proveedor ya existe.', 'error')
        except mysql.connector.errors.DataError:
            flash('Error: Uno de los valores es demasiado largo.', 'error')

    return redirect(url_for('proveedores'))

# Ruta para eliminar proveedores
@app.route('/delete_proveedor/<string:id>')
def delete_proveedor(id):
    cursor = database.cursor()
    sql = "DELETE FROM proveedores WHERE ID_proveedor = %s"
    data = (id,)
    cursor.execute(sql, data)
    database.commit()
    return redirect(url_for('proveedores'))

# Ruta para editar proveedores 
@app.route('/editar_proveedor/<string:id>', methods=['POST'])
def editar_proveedor(id):
    ID_proveedor = request.form['ID_proveedor']
    Nombre_empresa = request.form['Nombre_empresa']
    Nombre_representante_legal = request.form['Nombre_representante_legal']
    tipo_proveedor = request.form['tipo_proveedor']
    direccion = request.form['direccion']
    telefono = request.form['telefono']
    email = request.form['email']
    URL = request.form['URL']

    if ID_proveedor and Nombre_empresa and Nombre_representante_legal and tipo_proveedor and direccion and telefono and email and URL:
        try:
            cursor = database.cursor()
            sql = "UPDATE proveedores SET ID_proveedor = %s, Nombre_empresa = %s, Nombre_representante_legal = %s, tipo_proveedor = %s, direccion = %s, telefono = %s, email = %s, URL = %s WHERE ID_proveedor = %s"
            data = (ID_proveedor, Nombre_empresa, Nombre_representante_legal, tipo_proveedor, direccion, telefono, email, URL, id)
            cursor.execute(sql, data)
            database.commit()
        except mysql.connector.errors.IntegrityError:
            flash('Error: El ID de proveedor ya existe.', 'error')
        except mysql.connector.errors.DataError:
            flash('Error: Uno de los valores es demasiado largo.', 'error')

    return redirect(url_for('proveedores'))

# Ruta para mostrar la página de inventario
@app.route('/inventario')
def inventario():
    cursor = database.cursor()
    cursor.execute("SELECT * FROM producto")
    productos = cursor.fetchall()
    
    cursor.execute("SELECT * FROM proveedores")
    proveedores = cursor.fetchall()

    cursor.close()
    return render_template('inventario.html', data=productos, proveedores=proveedores)

# Ruta para filtrar productos
@app.route('/filtrar_productos', methods=['POST'])
def filtrar_productos():
    proveedor = request.form.get('proveedor')
    precio = request.form.get('precio')
    cantidad = request.form.get('cantidad')

    cursor = database.cursor()

    # Construir la consulta SQL base
    sql = "SELECT * FROM producto WHERE 1=1"

    # Aplicar filtros según los parámetros recibidos
    if proveedor:
        sql += f" AND ID_proveedor = {proveedor}"
    if precio:
        sql += f" AND valor_producto < {precio}"
    if cantidad:
        sql += f" AND cantidad_inicial > {cantidad}"

    cursor.execute(sql)
    productos_filtrados = cursor.fetchall()
    cursor.close()

    # Renderizar la página de inventario con productos filtrados
    cursor = database.cursor()
    cursor.execute("SELECT * FROM proveedores")
    proveedores = cursor.fetchall()
    cursor.close()
    
    return render_template('inventario.html', data=productos_filtrados, proveedores=proveedores)

# Ruta para agregar productos
@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    ID_producto = request.form['ID_producto']
    Nombre_producto = request.form['Nombre_producto']
    Descripcion = request.form['Descripcion']
    valor_producto = request.form['valor_producto']
    cantidad_inicial = request.form['cantidad_inicial']
    ID_proveedor = request.form['ID_proveedor']

    if ID_producto and Nombre_producto and Descripcion and valor_producto and cantidad_inicial and ID_proveedor:
        try:
            cursor = database.cursor()
            sql = "INSERT INTO producto (ID_producto, Nombre_producto, Descripcion, valor_producto, cantidad_inicial, ID_proveedor) VALUES (%s, %s, %s, %s, %s, %s)"
            data = (ID_producto, Nombre_producto, Descripcion, valor_producto, cantidad_inicial, ID_proveedor)
            cursor.execute(sql, data)
            database.commit()
        except mysql.connector.errors.IntegrityError:
            flash('Error: El ID de producto ya existe.', 'error')
        except mysql.connector.errors.DataError:
            flash('Error: Uno de los valores es demasiado largo.', 'error')

    return redirect(url_for('inventario'))

# Ruta para eliminar productos
@app.route('/delete_producto/<string:id>')
def delete_producto(id):
    cursor = database.cursor()
    sql = "DELETE FROM producto WHERE ID_producto = %s"
    data = (id,)
    cursor.execute(sql, data)
    database.commit()
    return redirect(url_for('inventario'))

# Ruta para editar productos 
@app.route('/editar_producto/<string:id>', methods=['POST'])
def editar_productos(id):
    ID_producto = request.form['ID_producto']
    Nombre_producto = request.form['Nombre_producto']
    Descripcion = request.form['Descripcion']
    valor_producto = request.form['valor_producto']
    cantidad_inicial = request.form['cantidad_inicial']
    ID_proveedor = request.form['ID_proveedor']

    if ID_producto and Nombre_producto and Descripcion and valor_producto and cantidad_inicial and ID_proveedor:
        try:
            cursor = database.cursor()
            sql = "UPDATE producto SET ID_producto = %s, Nombre_producto = %s, Descripcion = %s, valor_producto = %s, cantidad_inicial = %s, ID_proveedor = %s WHERE ID_producto = %s"
            data = (ID_producto, Nombre_producto, Descripcion, valor_producto, cantidad_inicial, ID_proveedor, id)
            cursor.execute(sql, data)
            database.commit()
        except mysql.connector.errors.IntegrityError:
            flash('Error: El ID de producto ya existe.', 'error')
        except mysql.connector.errors.DataError:
            flash('Error: Uno de los valores es demasiado largo.', 'error')

    return redirect(url_for('inventario'))


@app.route('/productos_por_categoria')
def productos_por_categoria():
    cursor = database.cursor()
    cursor.execute('''
        SELECT cp.nombre_categoria, COUNT(p.ID_producto) as cantidad 
        FROM producto p 
        JOIN categoria_producto cp ON p.ID_categoria_producto = cp.ID_categoria_producto 
        GROUP BY cp.nombre_categoria
    ''')
    data = cursor.fetchall()
    cursor.close()

    categorias = [item[0] for item in data]
    cantidades = [item[1] for item in data]

    return render_template('productos_por_categoria.html', categorias=categorias, cantidades=cantidades)


# Ruta para el dashboard
@app.route('/dashboard')
def dashboard():
    # Consulta para obtener la cantidad de productos
    cursor = database.cursor()
    cursor.execute('SELECT Nombre_producto, cantidad_inicial FROM producto ORDER BY cantidad_inicial DESC LIMIT 5')
    data_productos = cursor.fetchall()
    nombres_productos = [producto[0] for producto in data_productos]
    cantidades_iniciales = [producto[1] for producto in data_productos]

    # Consulta para obtener los productos devueltos con motivo
    cursor.execute('''
        SELECT p.Nombre_producto, dd.descripcion as Motivo_devolucion
        FROM detalle_devolucion dd
        JOIN producto p ON dd.ID_producto = p.ID_producto
    ''')
    productos_devueltos = cursor.fetchall()

    # Consulta para obtener las ventas en una fecha específica
    fecha_especifica = '2024-07-10'  # Debes ajustar esto a la fecha deseada
    cursor.execute('''
        SELECT SUM(dv.cantidad) as total_ventas
        FROM detalle_ventas dv
        JOIN ventas v ON dv.ID_venta = v.ID_venta
        WHERE v.fecha_venta = %s
    ''', (fecha_especifica,))
    total_ventas = cursor.fetchone()[0] or 0

    # Consulta para obtener los productos más vendidos
    cursor.execute('''
        SELECT p.Nombre_producto, SUM(dv.cantidad) as Cantidad_vendida
        FROM detalle_ventas dv
        JOIN producto p ON dv.ID_producto = p.ID_producto
        GROUP BY p.Nombre_producto
        ORDER BY Cantidad_vendida DESC
        LIMIT 5
    ''')
    productos_mas_vendidos = cursor.fetchall()

    cursor.close()

    return render_template('dashboard.html', 
                           nombres_productos=nombres_productos, 
                           cantidades_iniciales=cantidades_iniciales,
                           productos_devueltos=productos_devueltos,
                           fecha_especifica=fecha_especifica,
                           total_ventas=total_ventas,
                           productos_mas_vendidos=productos_mas_vendidos)



# Ruta para el dashboard de ventas
@app.route('/dashboard_ventas')
def dashboard_ventas():
    cursor = database.cursor()

    # Consulta para obtener los trabajadores con más ventas
    cursor.execute('''
        SELECT u.Nombre AS nombre, COUNT(v.ID_venta) AS ventas
        FROM ventas v
        JOIN usuarios u ON v.ID_usuario = u.ID_usuario
        GROUP BY u.Nombre
        ORDER BY ventas DESC
        LIMIT 5
    ''')
    trabajadores = cursor.fetchall()
    trabajadores = [{"nombre": t[0], "ventas": t[1]} for t in trabajadores]

    # Consulta para obtener los productos con bajo stock
    cursor.execute('''
        SELECT Nombre_producto AS nombre, cantidad_inicial AS stock
        FROM producto
        ORDER BY cantidad_inicial ASC
        LIMIT 5
    ''')
    productos = cursor.fetchall()
    productos = [{"nombre": p[0], "stock": p[1]} for p in productos]

    # Consulta para obtener los productos con precios más bajos
    cursor.execute('''
        SELECT Nombre_producto AS nombre, valor_producto AS precio
        FROM producto
        ORDER BY valor_producto ASC
        LIMIT 5
    ''')
    productos_precios = cursor.fetchall()
    productos_precios = [{"nombre": p[0], "precio": p[1]} for p in productos_precios]

    cursor.close()

    return render_template('dashboard_ventas.html', 
                           trabajadores=trabajadores, 
                           productos=productos, 
                           productos_precios=productos_precios)



#DANILOOOOO COMIENZO


@app.route('/ventas', methods=['GET', 'POST'])
def ventas():
    if 'id_usuario' not in session:
        return redirect(url_for('index'))

    cursor = db.db.cursor(dictionary=True)

    categorias = []
    productos = []
    selected_categoria_id = request.form.get('categoria_id', None)
    search_query = request.form.get('search_query', '')

    venta_id = session.get('venta_id')

    if request.method == 'POST':
        if 'id_producto' in request.form and 'cantidad' in request.form:
            id_producto = request.form['id_producto']
            cantidad = int(request.form['cantidad'])

            cursor.execute('SELECT * FROM producto WHERE ID_producto = %s', (id_producto,))
            producto = cursor.fetchone()

            if producto and producto['stock'] >= cantidad:
                try:
                    if not venta_id:
                        # Crear una nueva venta
                        cursor.execute('INSERT INTO ventas (fecha_venta, ID_usuario) VALUES (NOW(), %s)', (session['id_usuario'],))
                        db.db.commit()
                        venta_id = cursor.lastrowid
                        session['venta_id'] = venta_id

                    # Insertar detalle de venta
                    cursor.execute('INSERT INTO detalle_ventas (ID_venta, ID_producto, cantidad, valor_venta_producto) VALUES (%s, %s, %s, %s)', 
                                   (venta_id, id_producto, cantidad, producto['valor_producto']))
                    db.db.commit()

                    # Actualizar total de la venta
                    cursor.execute('SELECT SUM(cantidad * valor_venta_producto) AS total FROM detalle_ventas WHERE ID_venta = %s', (venta_id,))
                    total_venta = cursor.fetchone()['total'] or 0
                    cursor.execute('UPDATE ventas SET total = %s WHERE ID_venta = %s', (total_venta, venta_id))
                    db.db.commit()

                    # Actualizar stock del producto
                    new_stock = producto['stock'] - cantidad
                    cursor.execute('UPDATE producto SET stock = %s WHERE ID_producto = %s', (new_stock, id_producto))
                    db.db.commit()

                    flash('Producto agregado a la venta')
                except mysql.connector.Error as err:
                    flash(f"Error al agregar producto a la venta: {err}")
            else:
                flash('No hay suficiente stock')
        else:
            flash('error')

    # Obtener categorías y productos para mostrar en la página
    cursor.execute('SELECT * FROM categoria_producto')
    categorias = cursor.fetchall()

    query = 'SELECT * FROM producto'
    if selected_categoria_id:
        query += ' WHERE ID_categoria_producto = %s'
        cursor.execute(query, (selected_categoria_id,))
    elif search_query:
        query += ' WHERE nombre_producto LIKE %s'
        cursor.execute(query, ('%' + search_query + '%',))
    else:
        cursor.execute(query)

    productos = cursor.fetchall()

    # Obtener detalles de la venta actual
    detalles_venta = []
    total_venta = 0
    if venta_id:
        cursor.execute('SELECT dv.ID_detalle_venta, dv.ID_venta, p.nombre_producto, dv.cantidad, dv.valor_venta_producto '
                       'FROM detalle_ventas dv '
                       'JOIN producto p ON dv.ID_producto = p.ID_producto '
                       'WHERE dv.ID_venta = %s', (venta_id,))
        detalles_venta = cursor.fetchall()

        cursor.execute('SELECT total FROM ventas WHERE ID_venta = %s', (venta_id,))
        total_venta = cursor.fetchone()['total'] or 0

    cursor.close()

    return render_template('ventas.html', categorias=categorias, productos=productos, detalles_venta=detalles_venta, selected_categoria_id=selected_categoria_id, search_query=search_query, total_venta=total_venta)

@app.route('/ventas/editar/<int:id>', methods=['POST'])
def editar_producto(id):
    if request.method == 'POST':
        nueva_cantidad = int(request.form['cantidad'])

        cursor = db.db.cursor(dictionary=True)
        cursor.execute('SELECT * FROM detalle_ventas WHERE ID_detalle_venta = %s', (id,))
        detalle_venta = cursor.fetchone()

        if detalle_venta:
            id_producto = detalle_venta['ID_producto']
            cursor.execute('SELECT * FROM producto WHERE ID_producto = %s', (id_producto,))
            producto = cursor.fetchone()

            if producto:
                diferencia = nueva_cantidad - detalle_venta['cantidad']
                nuevo_stock = producto['stock'] - diferencia
                cursor.execute('UPDATE producto SET stock = %s WHERE ID_producto = %s', (nuevo_stock, id_producto))
                db.db.commit()

                cursor.execute('UPDATE detalle_ventas SET cantidad = %s WHERE ID_detalle_venta = %s', (nueva_cantidad, id))
                db.db.commit()

                # Actualizar total de la venta
                cursor.execute('SELECT SUM(cantidad * valor_venta_producto) AS total FROM detalle_ventas WHERE ID_venta = %s', (detalle_venta['ID_venta'],))
                total_venta = cursor.fetchone()['total'] or 0
                cursor.execute('UPDATE ventas SET total = %s WHERE ID_venta = %s', (total_venta, detalle_venta['ID_venta']))
                db.db.commit()

                flash('Producto editado correctamente')

    return redirect(url_for('ventas'))

@app.route('/ventas/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    cursor = db.db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM detalle_ventas WHERE ID_detalle_venta = %s', (id,))
    detalle_venta = cursor.fetchone()

    if detalle_venta:
        id_producto = detalle_venta['ID_producto']
        cantidad = detalle_venta['cantidad']
        cursor.execute('SELECT * FROM producto WHERE ID_producto = %s', (id_producto,))
        producto = cursor.fetchone()

        if producto:
            nuevo_stock = producto['stock'] + cantidad
            cursor.execute('UPDATE producto SET stock = %s WHERE ID_producto = %s', (nuevo_stock, id_producto))
            db.db.commit()

            cursor.execute('DELETE FROM detalle_ventas WHERE ID_detalle_venta = %s', (id,))
            db.db.commit()

            # Actualizar total de la venta
            cursor.execute('SELECT SUM(cantidad * valor_venta_producto) AS total FROM detalle_ventas WHERE ID_venta = %s', (detalle_venta['ID_venta'],))
            total_venta = cursor.fetchone()['total'] or 0
            cursor.execute('UPDATE ventas SET total = %s WHERE ID_venta = %s', (total_venta, detalle_venta['ID_venta']))
            db.db.commit()

            flash('Producto eliminado correctamente')

    return redirect(url_for('ventas'))

@app.route('/ventas/cancelar', methods=['POST'])
def cancelar_venta():
    venta_id = session.get('venta_id', None)

    if venta_id:
        cursor = db.db.cursor(dictionary=True)
        cursor.execute('SELECT * FROM detalle_ventas WHERE ID_venta = %s', (venta_id,))
        detalles_venta = cursor.fetchall()

        for detalle in detalles_venta:
            id_producto = detalle['ID_producto']
            cantidad = detalle['cantidad']
            cursor.execute('SELECT * FROM producto WHERE ID_producto = %s', (id_producto,))
            producto = cursor.fetchone()

            if producto:
                nuevo_stock = producto['stock'] + cantidad
                cursor.execute('UPDATE producto SET stock = %s WHERE ID_producto = %s', (nuevo_stock, id_producto))
                db.db.commit()

        cursor.execute('DELETE FROM detalle_ventas WHERE ID_venta = %s', (venta_id,))
        cursor.execute('DELETE FROM ventas WHERE ID_venta = %s', (venta_id,))
        db.db.commit()

        session.pop('venta_id', None)

        flash('Venta cancelada correctamente')

    return redirect(url_for('ventas'))

@app.route('/ventas/finalizar', methods=['POST'])
def finalizar_venta():
    venta_id = session.get('venta_id', None)

    if venta_id:
        cursor = db.db.cursor(dictionary=True)
        
        # Asegurarse de que el total se ha calculado y actualizado correctamente
        cursor.execute('SELECT SUM(cantidad * valor_venta_producto) AS total FROM detalle_ventas WHERE ID_venta = %s', (venta_id,))
        total_venta = cursor.fetchone()['total'] or 0
        cursor.execute('UPDATE ventas SET total = %s WHERE ID_venta = %s', (total_venta, venta_id))
        db.db.commit()

        session.pop('venta_id', None)

        flash('Venta finalizada correctamente')

    return redirect(url_for('ventas'))

#compras

# Función para obtener la lista de proveedores
def obtener_proveedores():
    try:
        connection = db.db
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM proveedores"
        cursor.execute(query)
        proveedores = cursor.fetchall()
        return proveedores
    except Exception as e:
        print(f"Error al obtener proveedores: {str(e)}")
        return []

# Función para obtener la lista de productos filtrados por proveedor
def obtener_productos_filtrados(proveedor_id):
    try:
        connection = db.db
        cursor = connection.cursor(dictionary=True)
        if proveedor_id:
            query = "SELECT * FROM producto WHERE ID_proveedor = %s ORDER BY nombre_producto ASC"
            cursor.execute(query, (proveedor_id,))
        else:
            query = "SELECT * FROM producto ORDER BY nombre_producto ASC"
            cursor.execute(query)
        productos = cursor.fetchall()
        return productos
    except Exception as e:
        print(f"Error al obtener productos filtrados: {str(e)}")
        return []

# Función para buscar productos por nombre
def buscar_productos(nombre_producto):
    try:
        connection = db.db
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM producto WHERE nombre_producto LIKE %s ORDER BY nombre_producto ASC"
        cursor.execute(query, ('%' + nombre_producto + '%',))
        productos = cursor.fetchall()
        return productos
    except Exception as e:
        print(f"Error al buscar productos: {str(e)}")
        return []

@app.route('/compras', methods=['GET', 'POST'])
def compras():
    if request.method == 'POST':
        if 'proveedor_id' in request.form:
            proveedor_id = request.form['proveedor_id']
            productos = obtener_productos_filtrados(proveedor_id)
        elif 'buscar' in request.form:
            nombre_producto = request.form['buscar']
            productos = buscar_productos(nombre_producto)
        else:
            flash('Acción no válida.', 'danger')
            return redirect(url_for('compras'))
    else:
        productos = obtener_productos_filtrados(None)  # Obtener todos los productos al cargar la página
    
    proveedores = obtener_proveedores()
    total_compra = calcular_total_compra(session.get('carrito', []))
    
    return render_template('compras.html', proveedores=proveedores, productos=productos, total_compra=total_compra, carrito=session.get('carrito', []))

# Función para agregar al carrito
@app.route('/agregar_al_carrito/<int:producto_id>', methods=['POST'])
def agregar_al_carrito(producto_id):
    cantidad = int(request.form['cantidad'])
    try:
        connection = db.db
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM producto WHERE ID_producto = %s"
        cursor.execute(query, (producto_id,))
        producto = cursor.fetchone()
        
        if producto:
            precio_total = producto['valor_producto'] * cantidad
            producto_carrito = {
                'ID_producto': producto['ID_producto'],
                'nombre_producto': producto['nombre_producto'],
                'cantidad': cantidad,
                'precio_total': precio_total
            }
            carrito = session.get('carrito', [])
            carrito.append(producto_carrito)
            session['carrito'] = carrito
            flash('Producto añadido al carrito.', 'success')
        else:
            flash('Producto no encontrado.', 'danger')
    except Exception as e:
        flash(f'Error al agregar producto al carrito: {str(e)}', 'danger')
    
    return redirect(url_for('compras'))


# Función para eliminar un producto del carrito de compras
@app.route('/eliminar_del_carrito/<int:index>', methods=['POST'])
def eliminar_del_carrito(index):
    carrito = session.get('carrito', [])
    if 0 <= index < len(carrito):
        del carrito[index]
        session['carrito'] = carrito
        flash('Producto eliminado del carrito.', 'success')
    else:
        flash('Índice de carrito no válido.', 'danger')
    
    return redirect(url_for('compras'))

# Función para calcular el total de la compra
def calcular_total_compra(carrito):
    total = 0
    for producto in carrito:
        total += float(producto['precio_total'])  # Asegúrate de que producto['precio_total'] sea numérico
    return total

# Función para cancelar la compra (vaciar carrito)
@app.route('/cancelar_compra', methods=['POST'])
def cancelar_compra():
    session.pop('carrito', None)
    flash('Compra cancelada.', 'info')
    return redirect(url_for('compras'))


@app.route('/finalizar_compra', methods=['POST'])
def finalizar_compra():
    carrito = session.get('carrito', [])
    if carrito:
        try:
            connection = db.db
            cursor = db.get_db_cursor()

            fecha_actual = date.today()
            insert_compra_query = "INSERT INTO compras (fecha_compra, valor_compra) VALUES (%s, %s)"
            cursor.execute(insert_compra_query, (fecha_actual, calcular_total_compra(carrito)))
            connection.commit()

            id_compra = cursor.lastrowid
            for item in carrito:
                producto_id = item.get('ID_producto')
                if producto_id is None:
                    flash(f'El producto en el carrito no tiene un ID válido.', 'danger')
                    continue

                cantidad = item['cantidad']
                precio_total = item['precio_total']

                obtener_proveedor_query = "SELECT ID_proveedor FROM producto WHERE ID_producto = %s"
                cursor.execute(obtener_proveedor_query, (producto_id,))
                proveedor_id_result = cursor.fetchone()

                if proveedor_id_result is None:
                    flash(f'No se encontró proveedor para el producto con ID {producto_id}.', 'warning')
                    continue
                
                proveedor_id = proveedor_id_result['ID_proveedor']
                valor_compra_producto = float(precio_total) * cantidad

                insert_detalle_query = "INSERT INTO detalle_compra (ID_compra, ID_producto, cantidad, ID_proveedor, valor_compra_producto) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(insert_detalle_query, (id_compra, producto_id, cantidad, proveedor_id, valor_compra_producto))
                connection.commit()

                # Actualizar el stock
                actualizar_stock_query = "UPDATE producto SET stock = stock + %s WHERE ID_producto = %s"
                cursor.execute(actualizar_stock_query, (cantidad, producto_id))
                connection.commit()

            session.pop('carrito', None)
            flash('Compra finalizada correctamente.', 'success')
        
        except Exception as e:
            flash(f'Error al finalizar compra: {str(e)}', 'danger')
            connection.rollback()
            return redirect(url_for('compras'))
        
        finally:
            cursor.close()

    else:
        flash('No hay productos en el carrito para finalizar la compra.', 'warning')

    return redirect(url_for('compras'))



#DANILO FINAL

if __name__ == '__main__':
    app.run(debug=True, port=5000)
