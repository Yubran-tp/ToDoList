import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gestion_tareas"
    )

def cargar_tareas():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT descripcion FROM tareas")
        tareas = cursor.fetchall()
        conn.close()

        listbox_tareas.delete(0, tk.END)
        for tarea in tareas:
            listbox_tareas.insert(tk.END, tarea[0])

    except Exception as e:
        messagebox.showerror("Error", "No se pudieron cargar las tareas.")

def agregar_tarea():
    tarea = entry_tarea.get().strip()

    if not tarea:
        messagebox.showwarning("Campo vacío", "Por favor ingrese una tarea.")
        return
    
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "INSERT INTO tareas (descripcion) VALUES (%s)"
        cursor.execute(sql, (tarea,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Tarea agregada correctamente")
        listbox_tareas.insert(tk.END, tarea)
        entry_tarea.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Error", "No se pudo guardar en la base de datos.")

def eliminar_tarea():
    seleccion = listbox_tareas.curselection()
    if not seleccion:
        messagebox.showwarning("Selección vacía", "Por favor seleccione una tarea.")
        return

    tarea_texto = listbox_tareas.get(seleccion)

    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "DELETE FROM tareas WHERE descripcion = %s"
        cursor.execute(sql, (tarea_texto,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Tarea eliminada correctamente")
        listbox_tareas.delete(seleccion)

    except Exception as e:
        messagebox.showerror("Error", "No se pudo eliminar de la base de datos.")

def completar_tarea():
    seleccion = listbox_tareas.curselection()
    if not seleccion:
        messagebox.showwarning("Selección vacía", "Por favor seleccione una tarea.")
        return

    tarea_actual = listbox_tareas.get(seleccion)
    if tarea_actual.startswith("✔️"):
        messagebox.showinfo("Información", "La tarea ya está completada.")
        return

    tarea_completada = "✔️ " + tarea_actual

    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "UPDATE tareas SET descripcion = %s WHERE descripcion = %s"
        cursor.execute(sql, (tarea_completada, tarea_actual))
        conn.commit()
        conn.close()

        listbox_tareas.delete(seleccion)
        listbox_tareas.insert(seleccion, tarea_completada)
        messagebox.showinfo("Éxito", "Tarea marcada como completada.")

    except Exception as e:
        messagebox.showerror("Error", "No se pudo marcar como completada.")

def editar_tarea():
    seleccion = listbox_tareas.curselection()
    if not seleccion:
        messagebox.showwarning("Selección vacía", "Por favor seleccione una tarea.")
        return

    tarea_original = listbox_tareas.get(seleccion)
    nueva_tarea = simpledialog.askstring("Editar tarea", "Ingrese la nueva descripción:", initialvalue=tarea_original)

    if not nueva_tarea:
        return

    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "UPDATE tareas SET descripcion = %s WHERE descripcion = %s"
        cursor.execute(sql, (nueva_tarea, tarea_original))
        conn.commit()
        conn.close()

        listbox_tareas.delete(seleccion)
        listbox_tareas.insert(seleccion, nueva_tarea)
        messagebox.showinfo("Éxito", "Tarea editada correctamente.")

    except Exception as e:
        messagebox.showerror("Error", "No se pudo editar la tarea.")

ventana = tk.Tk()
ventana.title("Lista de Tareas")
ventana.geometry("400x400")

entry_tarea = tk.Entry(ventana, width=30)
entry_tarea.pack(pady=10)

btn_agregar = tk.Button(ventana, text="Agregar tarea", width=15, command=agregar_tarea, bg="Green", fg="White")
btn_agregar.pack(pady=5)

listbox_tareas = tk.Listbox(ventana, width=50, height=10)
listbox_tareas.pack(pady=10)

btn_completar = tk.Button(ventana, text="Marcar como completada", command=completar_tarea, bg="blue", fg="white")
btn_completar.pack(pady=2)

btn_editar = tk.Button(ventana, text="Editar tarea", command=editar_tarea, bg="orange", fg="white")
btn_editar.pack(pady=2)

btn_eliminar = tk.Button(ventana, text="Eliminar tarea", width=20, command=eliminar_tarea, bg="Red", fg="White")
btn_eliminar.pack(pady=5)

cargar_tareas()

ventana.mainloop()

