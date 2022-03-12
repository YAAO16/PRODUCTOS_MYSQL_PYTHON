from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app= Flask(__name__)
#MySQL CONNECTION
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='productos_'
db=MySQL(app)


app.secret_key="mysecretkey"

@app.route("/")
def inicio():
  cursor=db.connection.cursor()
  cursor.execute("SELECT * FROM productos")
  datos=cursor.fetchall()
  return render_template("index.html", productos=datos)

@app.route("/agregar_producto", methods=['POST'])
def agregarProducto():
  if request.method=='POST':
    nombre=request.form['nombre']
    precio=request.form['precio']
    cursor=db.connection.cursor()
    cursor.execute("INSERT INTO productos (nombre, precio) VALUES (%s, %s)", (nombre, precio))
    db.connection.commit()
    return redirect(url_for("inicio"))

@app.route("/editar_producto/<id>")
def get_Producto(id):
  cursor=db.connection.cursor()
  cursor.execute("SELECT * FROM productos WHERE id=%s", (id))
  datos=cursor.fetchall()
  print(datos[0])
  return render_template("editarProducto.html", producto=datos[0])

@app.route("/actualizar_producto/<string:id>", methods=['POST'])
def actualizarProducto(id):
  if request.method=='POST':
    nombre=request.form['nombre']
    precio=request.form['precio']
    cursor=db.connection.cursor()
    cursor.execute("""
    UPDATE productos
    SET nombre=%s,
    precio=%s
    WHERE id=%s
    """, (nombre, precio, id))
    flash("Producto actualizado satisfactoriamente")
    db.connection.commit()
    return redirect(url_for("inicio"))

@app.route("/eliminar_producto/<string:id>")
def eliminarProducto(id):
  cursor=db.connection.cursor()
  cursor.execute("DELETE FROM productos WHERE id = {0}".format(id))
  db.connection.commit()
  flash("Contacto removido satisfactoriamente")
  return redirect(url_for("inicio"))

if __name__ == '__main__':
 app.run(port = 3000, debug = True)