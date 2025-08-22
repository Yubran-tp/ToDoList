import tkinter as tk
from tkinter import messagebox
import mysql.connector


def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="todolistbd"  
    )

def guardar_usuario():
    nombre = entry_nombre.get()
    contraseña = entry_contraseña.get()
    correo = entry_correo.get()
    
    if not nombre or not contraseña or not correo:
        messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos")
        return
   
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "INSERT INTO usuarios (nombre, contraseña, correo) VALUES (%s, %s, %s)"
        valores = (nombre, contraseña, correo)
        cursor.execute(sql, valores)
        conn.commit()
        conn.close()
       
        messagebox.showinfo("Éxito", "Usuario guardado correctamente")

        entry_nombre.delete(0, tk.END)
        entry_contraseña.delete(0, tk.END)
        entry_correo.delete(0, tk.END)
    
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar en la base de datos\n{e}")


def eliminar_usuario():
    nombre = entry_nombre.get()

    if not nombre:
        messagebox.showwarning("Campo vacío", "Por favor escribe un nombre para eliminar")
        return

    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "DELETE FROM usuarios WHERE nombre = %s"
        cursor.execute(sql, (nombre,))
        conn.commit()
        filas_afectadas = cursor.rowcount
        conn.close()

        if filas_afectadas > 0:
            messagebox.showinfo("Éxito", f"Se eliminó el usuario con nombre: {nombre}")
        else:
            messagebox.showwarning("No encontrado", f"No existe un usuario con el nombre: {nombre}")

        entry_nombre.delete(0, tk.END)
        entry_contraseña.delete(0, tk.END)
        entry_correo.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar de la base de datos\n{e}")


def buscar_usuario():
    nombre = entry_nombre.get()

    if not nombre:
        messagebox.showwarning("Campo vacío", "Por favor escribe un nombre para buscar")
        return

    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "SELECT nombre, contraseña, correo FROM usuarios WHERE nombre = %s"
        cursor.execute(sql, (nombre,))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            messagebox.showinfo("Resultado",
                                f"Nombre: {resultado[0]}\ncontraseña: {resultado[1]}\nCorreo: {resultado[2]}")
        else:
            messagebox.showwarning("No encontrado", f"No existe un usuario con el nombre: {nombre}")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo buscar en la base de datos\n{e}")



def agregar_tarea():
    tarea = entry_tarea.get()
    if not tarea:
        messagebox.showwarning("Campo vacío", "Escribe una tarea para agregar")
        return

    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "INSERT INTO tareas (descripcion, estado) VALUES (%s, %s)"
        cursor.execute(sql, (tarea, "Pendiente"))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Tarea agregada correctamente")
        entry_tarea.delete(0, tk.END)
        mostrar_tareas()

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo agregar la tarea\n{e}")


def eliminar_tarea():
    seleccion = listbox_tareas.curselection()
    if not seleccion:
        messagebox.showwarning("Nada seleccionado", "Por favor selecciona una tarea para eliminar")
        return

    indice = seleccion[0]
    tarea_id = listbox_tareas.get(indice).split(" | ")[0].replace("ID: ", "")

    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "DELETE FROM tareas WHERE id = %s"
        cursor.execute(sql, (tarea_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", f"Tarea con ID {tarea_id} eliminada")
        mostrar_tareas()

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar la tarea\n{e}")


def mostrar_tareas():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, descripcion, estado FROM tareas")
        resultados = cursor.fetchall()
        conn.close()

        listbox_tareas.delete(0, tk.END)
        for fila in resultados:
            listbox_tareas.insert(tk.END, f"ID: {fila[0]} | {fila[1]} | Estado: {fila[2]}")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar las tareas\n{e}")

ventana = tk.Tk()
ventana.title("Usuarios y To-Do List")
ventana.geometry("400x650")

tk.Label(ventana, text="Registro de Usuarios").pack(pady=5)
tk.Label(ventana, text="Ingrese sus datos").pack(pady=5)

tk.Label(ventana, text="Nombre:").pack()
entry_nombre = tk.Entry(ventana, width=30)
entry_nombre.pack()

tk.Label(ventana, text="Password:").pack()
entry_contraseña = tk.Entry(ventana, width=30)
entry_contraseña.pack()

tk.Label(ventana, text="Correo:").pack()
entry_correo = tk.Entry(ventana, width=30)
entry_correo.pack()

btn_guardar = tk.Button(ventana, text="Guardar Usuario", command=guardar_usuario, bg="blue", fg="white")
btn_guardar.pack(pady=5)

btn_eliminar = tk.Button(ventana, text="Eliminar Usuario", command=eliminar_usuario, bg="blue", fg="white")
btn_eliminar.pack(pady=5)

btn_buscar = tk.Button(ventana, text="Buscar Usuario", command=buscar_usuario, bg="blue", fg="white")
btn_buscar.pack(pady=5)

tk.Label(ventana, text="Agregar tareas").pack(pady=10)

entry_tarea = tk.Entry(ventana, width=30)
entry_tarea.pack(pady=5)

btn_agregar_tarea = tk.Button(ventana, text="Agregar Tarea", command=agregar_tarea, bg="blue", fg="white")
btn_agregar_tarea.pack(pady=5)

listbox_tareas = tk.Listbox(ventana, width=50, height=10)
listbox_tareas.pack(pady=10)

btn_eliminar_tarea = tk.Button(ventana, text="Eliminar Tarea Seleccionada", command=eliminar_tarea, bg="blue", fg="white")
btn_eliminar_tarea.pack(pady=5)

mostrar_tareas()

ventana.mainloop()