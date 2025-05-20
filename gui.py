import socket
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.ttk import Progressbar
import speedtest  # <== NUEVO

# CONFIGURACIÓN
PUERTO = 5001
BUFFER_SIZE = 4096
CARPETA_DESTINO = "archivos_recibidos"

# Diccionario de nombres por IP
PEERS = {
    "Dylan (100.105.15.30)": "100.105.15.30",
    "Alan (100.84.55.40)": "100.84.55.40",
    "Juan (100.73.140.77)": "100.73.140.77",
    "Luis (100.75.115.35)": "100.75.115.35"
}

# Crear carpeta si no existe
if not os.path.exists(CARPETA_DESTINO):
    os.makedirs(CARPETA_DESTINO)

def enviar_archivo():
    destino_nombre = ip_seleccionada.get()
    if not destino_nombre:
        messagebox.showwarning("IP no seleccionada", "Selecciona una IP destino.")
        return

    destino_ip = PEERS[destino_nombre]
    filepath = filedialog.askopenfilename()
    if not filepath:
        return

    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)

    try:
        client_socket = socket.socket()
        client_socket.connect((destino_ip, PUERTO))
        client_socket.send(f"{filename}|{filesize}".encode())

        with open(filepath, 'rb') as f:
            bytes_enviados = 0
            while True:
                bytes_leidos = f.read(BUFFER_SIZE)
                if not bytes_leidos:
                    break
                client_socket.sendall(bytes_leidos)
                bytes_enviados += len(bytes_leidos)
                progreso_envio["value"] = (bytes_enviados / filesize) * 100
                ventana.update_idletasks()

        client_socket.close()
        progreso_envio["value"] = 0
        messagebox.showinfo("Enviado", f"Archivo enviado a {destino_nombre}")
    except Exception as e:
        progreso_envio["value"] = 0
        messagebox.showerror("Error", f"No se pudo enviar el archivo:\n{str(e)}")

def recibir_archivo():
    try:
        server_socket = socket.socket()
        server_socket.bind(('', PUERTO))
        server_socket.listen(1)
        messagebox.showinfo("Esperando", f"Esperando archivo en puerto {PUERTO}...")

        conn, addr = server_socket.accept()
        info = conn.recv(BUFFER_SIZE).decode()
        filename, filesize = info.split("|")
        filesize = int(filesize)

        filepath = os.path.join(CARPETA_DESTINO, filename)
        with open(filepath, 'wb') as f:
            bytes_recibidos = 0
            while True:
                bytes_leidos = conn.recv(BUFFER_SIZE)
                if not bytes_leidos:
                    break
                f.write(bytes_leidos)
                bytes_recibidos += len(bytes_leidos)
                progreso_recepcion["value"] = (bytes_recibidos / filesize) * 100
                ventana.update_idletasks()

        conn.close()
        server_socket.close()
        progreso_recepcion["value"] = 0
        messagebox.showinfo("Recibido", f"Archivo guardado como:\n{filepath}")
    except Exception as e:
        progreso_recepcion["value"] = 0
        messagebox.showerror("Error", f"Error al recibir archivo:\n{str(e)}")

# === NUEVA FUNCIÓN ===
def medir_ancho_banda():
    try:
        s = speedtest.Speedtest()
        s.get_best_server()
        bajada = round(s.download() / 1_000_000, 2)  # Mbps
        subida = round(s.upload() / 1_000_000, 2)    # Mbps
        messagebox.showinfo("Ancho de Banda",
                            f"Bajada: {bajada} Mbps\nSubida: {subida} Mbps")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo medir el ancho de banda:\n{str(e)}")

# INTERFAZ
ventana = tk.Tk()
ventana.title("Transferencia Tailscale")
ventana.geometry("380x400")

tk.Label(ventana, text="Transferencia de archivos (Tailscale)", font=('Arial', 12, 'bold')).pack(pady=10)

# Menú desplegable de IPs
tk.Label(ventana, text="Selecciona IP del receptor:").pack()
ip_seleccionada = tk.StringVar()
combo = ttk.Combobox(ventana, textvariable=ip_seleccionada, values=list(PEERS.keys()), state="readonly", width=30)
combo.pack(pady=5)

# Barra de progreso para envío
tk.Label(ventana, text="Progreso de envío:").pack()
progreso_envio = Progressbar(ventana, length=300, mode='determinate')
progreso_envio.pack(pady=5)

# Barra de progreso para recepción
tk.Label(ventana, text="Progreso de recepción:").pack()
progreso_recepcion = Progressbar(ventana, length=300, mode='determinate')
progreso_recepcion.pack(pady=5)

# Botones
tk.Button(ventana, text="📤 Enviar archivo", command=enviar_archivo, width=25).pack(pady=10)
tk.Button(ventana, text="📥 Recibir archivo", command=recibir_archivo, width=25).pack(pady=5)
tk.Button(ventana, text="📶 Medir ancho de banda", command=medir_ancho_banda, width=25).pack(pady=10)  # <== NUEVO

ventana.mainloop()
