"""
File name: shell.py
Description: Simulation of a CMD console with custom commands containing N number of commands

Authors:
    - Jose Navarro
    - Kevin Lopez
    - Nicolas Cruz
    - Julian Castellanos
Creation date: 2024-10
"""


import tkinter as tk
import ctypes
from ctypes import wintypes
import os
import datetime
import psutil
import shutil
import time

class SYSTEMTIME(ctypes.Structure):
    _fields_ = [
        ("wYear", wintypes.WORD),
        ("wMonth", wintypes.WORD),
        ("wDayOfWeek", wintypes.WORD),
        ("wDay", wintypes.WORD),
        ("wHour", wintypes.WORD),
        ("wMinute", wintypes.WORD),
        ("wSecond", wintypes.WORD),
        ("wMilliseconds", wintypes.WORD),
    ]

def obtener_hora_bios():
    system_time = SYSTEMTIME()
    ctypes.windll.kernel32.GetSystemTime(ctypes.byref(system_time))
    return f"{system_time.wHour:02}:{system_time.wMinute:02}:{system_time.wSecond:02}"

def obtener_fecha_desde_bios():
    system_time = SYSTEMTIME()
    ctypes.windll.kernel32.GetSystemTime(ctypes.byref(system_time))
    fecha = datetime.datetime(
        system_time.wYear,
        system_time.wMonth,
        system_time.wDay,
        system_time.wHour,
        system_time.wMinute,
        system_time.wSecond
    )
    return fecha.strftime('%Y-%m-%d %H:%M:%S')

def crear_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, 'w') as archivo:
            archivo.write('')  # Crear un archivo vacío
        return f"Archivo '{nombre_archivo}' creado exitosamente."
    except Exception as e:
        return f"Error al crear el archivo: {e}"

def abrir_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as archivo:
            contenido = archivo.read()
        return f"Contenido de '{nombre_archivo}':\n{contenido}"
    except Exception as e:
        return f"Error al abrir el archivo: {e}"

def listar_directorio():
    try:
        archivos = os.listdir('.')
        return "\n".join(archivos)
    except Exception as e:
        return f"Error al listar el directorio: {e}"

def eliminar_archivo(nombre_archivo):
    try:
        os.remove(nombre_archivo)
        return f"Archivo '{nombre_archivo}' eliminado exitosamente."
    except Exception as e:
        return f"Error al eliminar el archivo: {e}"

def renombrar_archivo(nombre_actual, nombre_nuevo):
    try:
        os.rename(nombre_actual, nombre_nuevo)
        return f"Archivo '{nombre_actual}' renombrado a '{nombre_nuevo}' exitosamente."
    except Exception as e:
        return f"Error al renombrar el archivo: {e}"

def copiar_archivo(nombre_origen, nombre_destino):
    try:
        shutil.copy(nombre_origen, nombre_destino)
        return f"Archivo '{nombre_origen}' copiado a '{nombre_destino}' exitosamente."
    except Exception as e:
        return f"Error al copiar el archivo: {e}"


def mostrar_historial():
    return "\n".join(historial_comandos)

def obtener_usuario():
    return os.getlogin()

def obtener_uptime():
    tiempo_actual = time.time()
    uptime = tiempo_actual - tiempo_inicio
    return f"Uptime: {int(uptime)} segundos"

def manejar_procesos():
    try:
        procesos = []
        for proceso in psutil.process_iter(['pid', 'name']):
            procesos.append(f"PID: {proceso.info['pid']}, Nombre: {proceso.info['name']}")
        return "\n".join(procesos)
    except Exception as e:
        return f"Error al listar los procesos: {e}"

def matar_proceso(pid):
    try:
        proceso = psutil.Process(pid)
        proceso.terminate()
        return f"Proceso con PID {pid} terminado exitosamente."
    except Exception as e:
        return f"Error al terminar el proceso con PID {pid}: {e}"

def mostrar_banner():
    text_widget.insert(tk.END, banner_content + "\n")
    text_widget.insert(tk.END, "Microsoft Windows [Versión 10.0.19042.985]\n(c) 2021 Microsoft Corporation. Todos los derechos reservados.\n\nC:\\Users\\Usuario>")

def procesar_comando(event):
    entrada = text_widget.get("insert linestart", "insert lineend").strip()
    if entrada.startswith("C:\\Users\\Usuario>"):
        comando = entrada[len("C:\\Users\\Usuario>"):].strip()
        historial_comandos.append(comando)
        if comando == "hora":
            respuesta = obtener_hora_bios()
            text_widget.insert(tk.END, f"\n{respuesta}\nC:\\Users\\Usuario>")
        elif comando == "fecha":
            respuesta = obtener_fecha_desde_bios()
            text_widget.insert(tk.END, f"\n{respuesta}\nC:\\Users\\Usuario>")
        elif comando == "cls":
            limpiar_pantalla()
        elif comando == "dir":
            respuesta = listar_directorio()
            text_widget.insert(tk.END, f"\n{respuesta}\nC:\\Users\\Usuario>")
        elif comando.startswith("echo "):
            mensaje = comando[len("echo "):].strip()
            text_widget.insert(tk.END, f"\n{mensaje}\nC:\\Users\\Usuario>")
        elif comando == "salir":
            root.destroy()
        elif comando == "ayuda":
            respuesta = (
                "Comandos disponibles:\n"
                "  hora      - Muestra la hora actual desde la BIOS\n"
                "  fecha     - Muestra la fecha actual desde la BIOS\n"
                "  cls       - Limpia la pantalla\n"
                "  dir       - Lista los archivos y directorios en el directorio actual\n"
                "  echo      - Muestra un mensaje en la consola\n"
                "  crear     - Crea un archivo vacío\n"
                "  abrir     - Abre un archivo y muestra su contenido\n"
                "  del       - Elimina un archivo\n"
                "  ren       - Renombra un archivo\n"
                "  copy      - Copia un archivo\n"
                "  his       - Muestra el historial de comandos ejecutados\n"
                "  user      - Muestra el nombre del usuario actual\n"
                "  time      - Muestra el tiempo que la shell ha estado en ejecución\n"
                "  pro      - Muestra los procesos activos\n"
                "  kill      - Termina un proceso dado su PID\n"
                "  salir     - Cierra la consola\n"
                "  ayuda     - Muestra esta lista de comandos\n"
            )
            text_widget.insert(tk.END, f"\n{respuesta}\nC:\\Users\\Usuario>")
        elif comando.startswith("crear "):
            nombre_archivo = comando[len("crear "):].strip()
            respuesta = crear_archivo(nombre_archivo)
            text_widget.insert(tk.END, f"\n{respuesta}\nC:\\Users\\Usuario>")
        elif comando.startswith("abrir "):
            nombre_archivo = comando[len("abrir "):].strip()
            respuesta = abrir_archivo(nombre_archivo)
            text_widget.insert(tk.END, f"\n{respuesta}\nC:\\Users\\Usuario>")
        elif comando.startswith("del "):
            nombre_archivo = comando[len("del "):].strip()
            respuesta = eliminar_archivo(nombre_archivo)
            text_widget.insert(tk.END, f"\n{respuesta}\nC:\\Users\\Usuario>")
        elif comando.startswith("ren "):
            partes = comando[len("ren "):].strip().split()
            if len(partes) == 2:
                nombre_actual, nombre_nuevo = partes
                respuesta = renombrar_archivo(nombre_actual, nombre_nuevo)
            else:
                respuesta = "Uso: ren <nombre_actual> <nombre_nuevo>"
            text_widget.insert(tk.END, f"\n{respuesta}\nC:\\Users\\Usuario>")
        elif comando.startswith("copy "):
            partes = comando[len("copy "):].strip().split()
            if len(partes) == 2:
                nombre_origen, nombre_destino = partes
                respuesta = copiar_archivo(nombre_origen, nombre_destino)
            else:
                respuesta = "Uso: copy <nombre_origen> <nombre_destino>"
            text_widget.insert(tk.END, f"\n{respuesta}\nC:\\Users\\Usuario>")
        elif comando == "his":
            respuesta = mostrar_historial()
            text_widget.insert(tk.END, f"\n{respuesta}\nC:\\Users\\Usuario>")
        elif comando == "user":
            respuesta = obtener_usuario()
            text_widget.insert(tk.END, f"\n{respuesta}\nC:\\Users\\Usuario>")
        elif comando == "time":
            respuesta = obtener_uptime()
            text_widget.insert(tk.END, f"\n{respuesta}\nC:\\Users\\Usuario>")
        elif comando == "pro":
            respuesta = manejar_procesos()
            text_widget.insert(tk.END, f"\n{respuesta}\nC:\\Users\\Usuario>")
        elif comando.startswith("kill "):
            try:
                pid = int(comando[len("kill "):].strip())
                respuesta = matar_proceso(pid)
            except ValueError:
                respuesta = "Uso: kill <PID>"
            text_widget.insert(tk.END, f"\n{respuesta}\nC:\\Users\\Usuario>")
        elif comando == "banner":
            mostrar_banner()
        else:
            text_widget.insert(tk.END, f"\nComando no reconocido: {comando}\nC:\\Users\\Usuario>")
    
    text_widget.see(tk.END)
    text_widget.mark_set("insert", "end-1c")
    return "break"

def limpiar_pantalla():
    text_widget.delete(1.0, tk.END)
    mostrar_banner()

def crear_ventana_cmd():
    global text_widget, root, historial_comandos, tiempo_inicio, banner_content


    historial_comandos = []
    tiempo_inicio = time.time()

    try:
        with open('banner.txt', 'r') as banner_file:
            banner_content = banner_file.read()
    except Exception as e:
        banner_content = f"Error al leer banner.txt: {e}"

  
    root = tk.Tk()
    root.title("Simulación CMD")
    root.geometry("1000x400")
    root.configure(bg="black")

    text_widget = tk.Text(root, bg="black", fg="white", insertbackground="white", font=("Consolas", 12))
    text_widget.pack(expand=True, fill='both')

    mostrar_banner()
    text_widget.bind("<Return>", procesar_comando)

    root.mainloop()

crear_ventana_cmd()
