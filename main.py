import socket
import sys
import threading
from datetime import datetime

# Imprimir encabezado de inicio
print("-" * 60)
print("              ESCÁNER DE PUERTOS TCP BÁSICO             ")
print("-" * 60)

# 1. Entrada de datos por parte del usuario
target_input = input("Ingresa la IP o Dominio a escanear (ej. 127.0.0.1 o scanme.nmap.org): ")

try:
    # Convierte un nombre de dominio (ej. google.com) a una IP válida
    target_ip = socket.gethostbyname(target_input)
except socket.gaierror:
    print("\n[!] Error: No se pudo resolver el nombre del host/dominio.")
    sys.exit()

# Definir rango de puertos a escanear
try:
    start_port = int(input("Puerto inicial (ej. 1): "))
    end_port = int(input("Puerto final (ej. 1024): "))
except ValueError:
    print("\n[!] Error: Ingresa un número válido para los puertos.")
    sys.exit()

print("-" * 60)
print(f"Escaneando objetivo: {target_ip}")
print(f"Rango de puertos:   {start_port} - {end_port}")
print(f"Hora de inicio:     {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("-" * 60)

open_ports = []
lock = threading.Lock() # Evita colisiones al imprimir o modificar la lista

def scan_port(port):
    """
    Intenta establecer una conexión TCP a un puerto específico.
    """
    try:
        # AF_INET = IPv4 | SOCK_STREAM = TCP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Establece un tiempo de espera en segundos para evitar bloqueos
        s.settimeout(1.0)
        
        # connect_ex devuelve 0 si la conexión fue exitosa (Puerto Abierto)
        result = s.connect_ex((target_ip, port))
        
        if result == 0:
            with lock:
                print(f"[+] Puerto {port}: ABIERTO")
                open_ports.append(port)
                
        s.close()
        
    except Exception:
        pass

# 2. Creación y ejecución de hilos (Multi-threading)
threads = []

for port in range(start_port, end_port + 1):
    thread = threading.Thread(target=scan_port, args=(port,))
    threads.append(thread)
    thread.start()

# Esperar a que todos los hilos terminen su ejecución
for thread in threads:
    thread.join()

# 3. Resumen final de resultados
print("-" * 60)
print("Escaneo completado.")
if open_ports:
    print(f"Puertos abiertos encontrados: {sorted(open_ports)}")
else:
    print("No se encontraron puertos abiertos en el rango especificado.")
print("-" * 60)
