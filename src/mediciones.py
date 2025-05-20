import speedtest
from tkinter import messagebox

# --- Medir ancho de banda ---
def medir_ancho_banda():
    try:
        s = speedtest.Speedtest()
        s.get_best_server()
        bajada = round(s.download() / 1_000_000, 2)  # Mbps
        subida = round(s.upload() / 1_000_000, 2)    # Mbps
        messagebox.showinfo("Ancho de Banda", f"Bajada: {bajada} Mbps\nSubida: {subida} Mbps")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo medir el ancho de banda:\n{e}")

# En la GUI, botón que llama a la función medir_ancho_banda
btn_medir = tk.Button(ventana, text="📶 Medir ancho de banda", command=medir_ancho_banda, width=30)
btn_medir.pack(pady=10)
