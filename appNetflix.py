import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import time
import mysql.connector

#Conección con la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="fidel",
    database="netflix"
)

#Funcion que muestra las series
def mostrarSeries():

    # Crear la ventana principal
    ventana1 = tk.Tk()
    ventana1.title("Series de Netflix")
    ventana1.geometry("580x200")
    bit = ventana1.config(bg="black")
     
    # Crear la tabla
    treeview = ttk.Treeview(ventana1, columns=("ID", "Título", "Género", "Temporadas"))
    treeview.heading("#0", text="")
    treeview.heading("ID", text="IDserie")
    treeview.heading("Título", text="Título" )
    treeview.heading("Género", text="Género")
    treeview.heading("Temporadas", text="Temporadas")
    treeview.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    # Configurar el estilo de la tabla
    style = ttk.Style()
    style.theme_use("default")
    style.configure("treeview", background="black", foreground="white")
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

    # Configurar el comportamiento de la tabla
    treeview.column("#0", width=0, stretch=tk.NO)
    treeview.column("ID", width=50, anchor=tk.CENTER)
    treeview.column("Título", width=200)
    treeview.column("Género", width=200)
    treeview.column("Temporadas", width=100, anchor=tk.CENTER)

    # Configurar el desplazamiento vertical
    scrollbar = ttk.Scrollbar(ventana1, orient="vertical", command=treeview.yview)
    scrollbar.grid(row=5, column=2, sticky="ns")
    treeview.configure(yscrollcommand=scrollbar.set)

    cursor = conexion.cursor()
    consulta = "SELECT idSeries, nombre, genero, temporadas FROM series"
    cursor.execute(consulta)
    resultados = cursor.fetchall()

    for i in treeview.get_children():
        treeview.delete(i)

    for serie in resultados:
        treeview.insert("", tk.END, values=(serie[0], serie[1], serie[2], serie[3]))

    cursor.close()

   
    """cursor = conexion.cursor()
    consulta = "SELECT * FROM series"
    
    cursor.execute(consulta)
    resultados = cursor.fetchall()
   
    ventana1 = tk.Toplevel(ventana)
    ventana1.title("Mostrar series")
    ventana1.geometry("400x300")
    bit = ventana1.config(bg="black")
    #ventana1.iconbitmap("img.ico")

    # Crear el widget ScrolledText
    texto_series = scrolledtext.ScrolledText(ventana1, bg="black", fg="red",font=("Americana BT", 15, "bold") )
    texto_series.pack(fill=tk.BOTH, expand=True)

    # Mostrar las series en el campo de texto
    texto_series.delete(1.0, tk.END)
    for series in resultados:
        texto_series.insert(tk.END, f"Idserie: {series[0]}\n")
        texto_series.insert(tk.END, f"Nombre: {series[1]}\n")
        texto_series.insert(tk.END, f"Género: {series[2]}\n")
        texto_series.insert(tk.END, f"Temporadas: {series[3]}\n")
        texto_series.insert(tk.END, "------------------------\n")
        
    cursor.close()
    #conexion.close()"""  

#funcion que gestiona la manipulacion con la base de datos a partir del boton_agregar
def agregar_serie(entry_nombre, entry_genero, entry_temporadas):
    nombre = entry_nombre.get()
    genero = entry_genero.get()
    temporadas = entry_temporadas.get()
    cursor = conexion.cursor()

    # Verificar si la serie ya existe en la base de datos
    consulta_verificacion = "SELECT * FROM series WHERE nombre = %s"
    datos_verificacion = (nombre,)
    cursor.execute(consulta_verificacion, datos_verificacion)
    resultado = cursor.fetchone()
    if resultado:
        # La serie ya existe en la base de datos
        messagebox.showerror("Netflix", "La serie ya existe en la base de datos")
        cursor.close()

        entry_nombre.delete(0, tk.END)
        entry_genero.delete(0, tk.END)
        entry_temporadas.delete(0, tk.END)
        
        entry_nombre.focus()

    # Insertar la serie en la base de datos
    consulta = "INSERT INTO series (nombre, genero, temporadas) VALUES (%s, %s, %s)"
    datos = (nombre, genero, temporadas)
    cursor.execute(consulta, datos)
    conexion.commit()

    # Cerrar la conexión
    cursor.close()

    #mensaje que confirma el ingreso correcto de la serie
    messagebox.showinfo("Netflix", "Se agregó correctamente la serie.")
    

    # Limpiar los campos de entrada
    entry_nombre.delete(0, tk.END)
    entry_genero.delete(0, tk.END)
    entry_temporadas.delete(0, tk.END)

    entry_nombre.focus()

    
#funcion donde se llama la ventana con sus instrumentos para poder agregar series
def vent_agregarSerie():
    ventana2 = tk.Toplevel(ventana)
    ventana2.title("Agregar series")
    ventana2.geometry("400x300")
    bit = ventana2.config(bg="black")
    #ventana2.iconbitmap("img.ico")

    # Etiquetas y campos de entrada
    label_nombre = tk.Label(ventana2, text="Título:", fg="white",bg="black")
    label_nombre.pack(pady=5)
    entry_nombre = tk.Entry(ventana2)
    entry_nombre.pack(pady=5)

    label_genero = tk.Label(ventana2, text="Género:", fg="white",bg="black")
    label_genero.pack(pady=5)
    entry_genero = tk.Entry(ventana2)
    entry_genero.pack(pady=5)

    label_temporadas = tk.Label(ventana2, text="Temporadas:", fg="white",bg="black")
    label_temporadas.pack(pady=5)
    entry_temporadas = tk.Entry(ventana2)
    entry_temporadas.pack(pady=5)

    boton_agregar = tk.Button(ventana2, text="Agregar serie",fg="red", bg="black", padx=10, font=15, command= lambda: agregar_serie(entry_nombre, entry_genero, entry_temporadas) )
    boton_agregar.pack(pady=5)

def existencia_serie(entry_Idserie):
    
    cursor = conexion.cursor()
    idseries = entry_Idserie.get()

    consulta = "SELECT * FROM series WHERE idseries = %s;"
    dato = (idseries,)
    cursor.execute(consulta,dato)
    
    return len(cursor.fetchall()) != 0
    
    cursor.close()


#funcion que realiza la modificacion de la serie a partir del boton_modificar  
def modificarSerie(entry_idserie,entry_nombre, entry_genero, entry_temporadas):
    idseries = entry_idserie.get()
    nombre = entry_nombre.get()
    genero = entry_genero.get()
    temporadas = entry_temporadas.get()

    if existencia_serie(entry_idserie):
        cursor = conexion.cursor()

        # Actualizar la serie en la base de datos
        consulta = "UPDATE series SET nombre = %s, genero = %s, temporadas = %s WHERE idseries = %s"
        datos = (nombre,genero,temporadas, idseries)
        cursor.execute(consulta, datos)
        conexion.commit()
        cursor.close()

        messagebox.showinfo("Netflix", "Se modifico/actualizo correctamente la Serie")

        entry_idserie.delete(0, tk.END)
        entry_nombre.delete(0, tk.END)
        entry_genero.delete(0, tk.END)
        entry_temporadas.delete(0, tk.END)
    else: 
        messagebox.showinfo("Netflix", "No existe ese identificador de serie")

    entry_idserie.focus()
    




    
#funcion que abre la ventana, para modificar serie
def vent_modificarSerie():
    ventana3 = tk.Toplevel(ventana)
    ventana3.title("Modificar serie")
    ventana3.geometry("400x300")
    bit = ventana3.config(bg="black")
    #ventana3.iconbitmap("img.ico")

    # Etiquetas y campos de entrada
    label_idserie = tk.Label(ventana3, text="IDserie:", fg="white",bg="black")
    label_idserie.pack(pady=5)
    entry_idserie = tk.Entry(ventana3)
    entry_idserie.pack(pady=5)

    label_nombre = tk.Label(ventana3, text="Título:", fg="white",bg="black")
    label_nombre.pack(pady=5)
    entry_nombre = tk.Entry(ventana3)
    entry_nombre.pack(pady=5)

    label_genero = tk.Label(ventana3, text="Género:", fg="white",bg="black")
    label_genero.pack(pady=5)
    entry_genero = tk.Entry(ventana3)
    entry_genero.pack(pady=5)

    label_temporadas = tk.Label(ventana3, text="Temporadas:", fg="white",bg="black")
    label_temporadas.pack(pady=5)
    entry_temporadas = tk.Entry(ventana3)
    entry_temporadas.pack(pady=5)

    boton_modificar = tk.Button(ventana3, text="Modificar serie",fg="red", bg="black", padx=10, font=15, command= lambda: modificarSerie(entry_idserie,entry_nombre, entry_genero, entry_temporadas))
    boton_modificar.pack(pady=5)
    

#funcion, para poder borrar serie a partir del accionar del boto_eliminar
def eliminar_series(entry_Idserie):

    if existencia_serie(entry_Idserie):

        idseries = entry_Idserie.get()
        
        cursor = conexion.cursor()

        respuesta=messagebox.askquestion("Netflix","¿Estas seguro que deseas eliminar esta serie?")
        if respuesta== "yes": 
            # Eliminar la serie de la base de datos
            consulta = "DELETE FROM series WHERE idseries = %s"
            datos = (idseries,)
            cursor.execute(consulta, datos)
            conexion.commit()
            # Cerrar la conexión
            cursor.close()
            #mensaje que confirma la aliminacion correcta
            messagebox.showinfo("Netflix", "Se elimino correctamente la Serie")
    else:
        messagebox.showinfo("Netflix", "No existe ese identificador de serie")

    # Limpiar los campos de entrada
    entry_Idserie.delete(0, tk.END)
       #conexion.close()
        #else:     

    entry_Idserie.focus()

#Con esta funcion, se abre la nueva ventana para la eliminacion de una serie
def vent_eliminarSerie():
    ventana4 = tk.Toplevel(ventana)
    ventana4.title("Eliminar series")
    ventana4.geometry("400x300")
    bit = ventana4.config(bg="black")
    #ventana4.iconbitmap("img.ico")
    label_Idserie = tk.Label(ventana4, text="Ingrese el Idserie, para eliminar", bg="black", fg="white", font=30)
    label_Idserie.pack(pady=5)
    entry_Idserie = tk.Entry(ventana4)
    entry_Idserie.pack(pady=5)
    boton_eliminar = tk.Button(ventana4, text="Eliminar Serie",fg="red", bg="black", padx=10, font=15, command=lambda: eliminar_series(entry_Idserie))
    boton_eliminar.pack(pady=5)


def creditos():
    ventana5= tk.Toplevel(ventana)
    ventana5.title("Créditos")
    ventana5.geometry("400x400")
    bit = ventana5.config(bg="black")
    
    # Fondo de la ventana de créditos
    fondo_creditos = tk.Canvas(ventana5, width=400, height=400, bg="black")
    fondo_creditos.pack()
    
    # Título de los créditos
    etiqueta_titulo = tk.Label(ventana5, text="Créditos", font=("Arial", 20, "bold"), bg="black", fg="red")
    etiqueta_titulo.place(x=150, y=20)
    
    # Información de los integrantes
    integrantes = [
        ("Integrante:", "Avila, Marcelo"),
        ("Integrante :", "Gomez, Fiamma"),
        ("Integrante :", "Gonzales, Andres"),
        ("Integrante :", "Sancassani, José Hernán")
    ]
    
    y = 80  # Posición vertical inicial de los integrantes
    
    for titulo, nombre in integrantes:
        etiqueta_integrante_titulo = tk.Label(ventana5, text=titulo, font=("Arial", 14), bg="black", fg="red")
        etiqueta_integrante_titulo.place(x=50, y=y)
        
        etiqueta_integrante_nombre = tk.Label(ventana5, text=nombre, font=("Arial", 12), bg="black", fg="red")
        etiqueta_integrante_nombre.place(x=50, y=y+30)
        
        y += 80  # Incrementar la posición vertical para el siguiente integrante
    



 

ventana = tk.Tk()
ventana.title("App para NEXFLIX")
ventana.geometry("800x600+0+0")
bit = ventana.config(bg="black")
#ventana.iconbitmap("img.ico")

# bloque del menu
barraMenu = tk.Menu(ventana)
barraMenu.config(bg="#333333", fg="white", activebackground="#555555", activeforeground="white")
archivoMenu = tk.Menu(barraMenu, tearoff=False)
archivoMenu.config(bg="#333333", fg="white", activebackground="#555555", activeforeground="white")
archivoMenu.add_command(label="Agregar", command=vent_agregarSerie)
archivoMenu.add_command(label="Modificar", command=vent_modificarSerie)
archivoMenu.add_command(label="Dar de baja", command=vent_eliminarSerie)
archivoMenu.add_command(label="Créditos", command=creditos)
archivoMenu.add_separator()
archivoMenu.add_command(label="Salir", command=ventana.quit)
barraMenu.add_cascade(label="Menú", menu=archivoMenu)
ventana.config(menu=barraMenu)

frame_titulo = tk.Frame(ventana)
frame_titulo.config(bg="black")
frame_titulo.pack(pady=50)


label_titulo = tk.Label(frame_titulo, text="NETFLIX", fg="red", bg="black", font=("Arial", 70, "bold"))
label_titulo.pack()

frame_descripcion = tk.Frame(ventana)
frame_descripcion.pack(pady=50)

label_descripcion = tk.Label(frame_descripcion, text="Sistema de gestión de series de Netflix.", fg="white", bg="black", font=30)
label_descripcion.pack()

frame_botones = tk.Frame(ventana, bg="black")
frame_botones.pack(pady=50)

boton1 = tk.Button(frame_botones, text="Mostrar\nseries", fg="white", bg="black", padx=10, font=15, command=mostrarSeries)
boton1.grid(row=0,column=0, padx=10)
boton2 = tk.Button(frame_botones, text="Agregar\nseries",fg="white", bg="black", padx=10, font=15, command=vent_agregarSerie)
boton2.grid(row=0,column=1, padx=10)
boton3 = tk.Button(frame_botones, text="Modificar\nseries", fg="white", bg="black", padx=10, font=15, command=vent_modificarSerie)
boton3.grid(row=0,column=2, padx=10)
boton4 = tk.Button(frame_botones, text="Eliminar\nseries", fg="white", bg="black", padx=10, font=15, command=vent_eliminarSerie)
boton4.grid(row=0,column=3, padx=10)

boton5 = tk.Button(frame_botones, text="Salir", fg="white", bg="black", padx=15, pady=10, font=15, command=ventana.quit)
boton5.grid(row=0,column=4, padx=10)

etiqueta = tk.Label(ventana, text="label",bg="black", fg="white")
etiqueta.pack(pady=30)
def actualizarHora():
    etiqueta.config(text=time.strftime("%H : %M : %S"))
    ventana.after(1000, actualizarHora)
actualizarHora()


ventana.mainloop()