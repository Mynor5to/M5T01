#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import random
import string
import colorama
from colorama import Fore, Style
import requests  # Importado por requerimiento (sin uso de red asignado)
import aiohttp   # Importado por requerimiento (sin uso de red asignado)
import names

# Inicializar colorama para soporte de colores en la terminal
colorama.init(autoreset=True)

# Directorio base especificado para Termux
BASE_DIR = '/storage/emulated/0/Termux/'

def clear_screen():
    """Limpia la terminal según el sistema operativo."""
    os.system('clear' if os.name == 'posix' else 'cls')

def show_banner():
    """Muestra el banner inicial con arte ASCII y estética hacker."""
    banner_text = f"""{Fore.MAGENTA}
 ███╗   ███╗███████╗████████╗ ██████╗ 
 ████╗ ████║██╔════╝╚══██╔══╝██╔═══██╗
 ██╔████╔██║███████╗   ██║   ██║   ██║
 ██║╚██╔╝██║╚════██║   ██║   ██║   ██║
 ██║ ╚═╝ ██║███████║   ██║   ╚██████╔╝
 ╚═╝     ╚═╝╚══════╝   ╚═╝    ╚═════╝ 
{Fore.CYAN}[*] Generador de Combinaciones Avanzado
{Fore.GREEN}[*] Autor: M5to
{Style.RESET_ALL}"""
    print(banner_text)

def get_target_files():
    """Obtiene la lista de archivos .txt disponibles en el directorio base."""
    if not os.path.exists(BASE_DIR):
        try:
            # Crear el directorio si no existe
            os.makedirs(BASE_DIR)
        except Exception as e:
            print(f"{Fore.RED}[!] ERROR al crear directorio base: {e}{Style.RESET_ALL}")
            return []
    
    try:
        # Listar exclusivamente archivos con extensión .txt
        archivos = [f for f in os.listdir(BASE_DIR) if f.endswith('.txt')]
        return archivos
    except Exception as e:
        print(f"{Fore.RED}[!] ERROR al leer el directorio: {e}{Style.RESET_ALL}")
        return []

def animate_loading(text, duration=2):
    """Muestra una animación de carga sencilla usando puntos."""
    print(f"\n{Fore.CYAN}[*] {text}", end="")
    for _ in range(duration * 2):
        time.sleep(0.4)
        sys.stdout.write(f"{Fore.MAGENTA}.")
        sys.stdout.flush()
    print(f"{Style.RESET_ALL}")

def progress_bar(current, total, prefix="Generando"):
    """Implementa una barra de progreso animada sin librerías externas."""
    percent = float(current) * 100 / total
    filled = int(30 * current // total)
    bar = '█' * filled + '-' * (30 - filled)
    
    # Imprimir barra usando retorno de carro (\r) para sobrescribir la línea
    sys.stdout.write(f"\r{Fore.CYAN}{prefix} |{Fore.GREEN}{bar}{Fore.CYAN}| {percent:.1f}% ({current}/{total}){Style.RESET_ALL}")
    sys.stdout.flush()
    if current == total:
        print()

def main():
    clear_screen()
    show_banner()
    
    # 1. Selección del archivo de nombres
    print(f"{Fore.CYAN}[>] Escaneando archivos en {BASE_DIR}...{Style.RESET_ALL}")
    archivos_txt = get_target_files()
    
    if not archivos_txt:
        print(f"\n{Fore.RED}[!] ERROR: No se encontraron archivos .txt en {BASE_DIR}{Style.RESET_ALL}")
        archivo_seleccionado = None
    else:
        print(f"\n{Fore.GREEN}[+] Archivos detectados:{Style.RESET_ALL}")
        for idx, f in enumerate(archivos_txt, 1):
            print(f"{Fore.CYAN}    [{idx}] {f}{Style.RESET_ALL}")
        
        while True:
            try:
                opcion = int(input(f"\n{Fore.MAGENTA}>>> Selecciona el número del archivo objetivo: {Style.RESET_ALL}"))
                if 1 <= opcion <= len(archivos_txt):
                    archivo_seleccionado = archivos_txt[opcion - 1]
                    break
                else:
                    print(f"{Fore.RED}[!] Entrada inválida. Selecciona un número de la lista.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}[!] Formato incorrecto. Ingresa un número entero.{Style.RESET_ALL}")
    
    # 2. Nombre de salida
    nombre_salida = input(f"\n{Fore.MAGENTA}>>> Ingresa el nombre del archivo de resultados (ej. salida.txt): {Style.RESET_ALL}")
    if not nombre_salida.endswith('.txt'):
        nombre_salida += '.txt'
    ruta_salida = os.path.join(BASE_DIR, nombre_salida)

    # 3. Tipo de contraseña
    print(f"\n{Fore.CYAN}[+] Configuración del componente:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}    [1] Numérico (exclusivamente dígitos 0-9){Style.RESET_ALL}")
    print(f"{Fore.CYAN}    [2] Alfanumérico (letras y números mezclados){Style.RESET_ALL}")
    print(f"{Fore.CYAN}    [3] Alfanumérico con símbolos (letras, números y !@#$%) {Style.RESET_ALL}")
    
    while True:
        tipo_pass = input(f"\n{Fore.MAGENTA}>>> Selecciona el tipo de componente (1/2/3): {Style.RESET_ALL}")
        if tipo_pass in ['1', '2', '3']:
            break
        print(f"{Fore.RED}[!] Opción no reconocida.{Style.RESET_ALL}")
        
    # 4. Longitud del componente
    while True:
        try:
            longitud = int(input(f"\n{Fore.MAGENTA}>>> Longitud de caracteres para el componente: {Style.RESET_ALL}"))
            if longitud > 0:
                break
            print(f"{Fore.RED}[!] La longitud debe ser mayor a 0.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}[!] Ingresa un número entero.{Style.RESET_ALL}")

    # Configuración del set de caracteres
    if tipo_pass == '1':
        caracteres = string.digits
    elif tipo_pass == '2':
        caracteres = string.ascii_letters + string.digits
    else:
        caracteres = string.ascii_letters + string.digits + "!@#$%"

    # 5. Parámetros de cobertura para combinaciones
    while True:
        try:
            minimo_nombres = int(input(f"\n{Fore.MAGENTA}>>> Mínimo de nombres requeridos (se rellenará si el archivo contiene menos): {Style.RESET_ALL}"))
            variaciones = int(input(f"{Fore.MAGENTA}>>> Cantidad de variaciones a generar por cada nombre: {Style.RESET_ALL}"))
            if minimo_nombres >= 0 and variaciones > 0:
                break
        except ValueError:
            print(f"{Fore.RED}[!] Ingresa números enteros válidos.{Style.RESET_ALL}")

    # Lectura del archivo objetivo
    lista_nombres = []
    if archivo_seleccionado:
        ruta_entrada = os.path.join(BASE_DIR, archivo_seleccionado)
        try:
            with open(ruta_entrada, 'r', encoding='utf-8') as f:
                lista_nombres = [linea.strip() for linea in f if linea.strip()]
            print(f"\n{Fore.GREEN}[+] Extracción exitosa. Nombres leídos: {len(lista_nombres)}{Style.RESET_ALL}")
        except Exception as e:
            print(f"\n{Fore.RED}[!] ERROR accediendo a {archivo_seleccionado}: {e}{Style.RESET_ALL}")
    
    # Lógica de relleno con librería 'names' si no se cumple el mínimo
    if len(lista_nombres) < minimo_nombres:
        faltantes = minimo_nombres - len(lista_nombres)
        print(f"{Fore.CYAN}[*] Inyectando {faltantes} nombres adicionales generados aleatoriamente...{Style.RESET_ALL}")
        for _ in range(faltantes):
            lista_nombres.append(names.get_first_name())
    
    if not lista_nombres:
        print(f"{Fore.RED}[!] ERROR FATAL: No hay nombres en memoria para procesar.{Style.RESET_ALL}")
        sys.exit(1)

    total_combinaciones = len(lista_nombres) * variaciones
    
    animate_loading("Inicializando motor criptográfico")

    # Generación y escritura en archivo
    print(f"\n{Fore.CYAN}[*] Ejecutando generación en lote...{Style.RESET_ALL}")
    
    try:
        with open(ruta_salida, 'w', encoding='utf-8') as f_out:
            contador = 0
            for nombre in lista_nombres:
                for _ in range(variaciones):
                    # Generación aleatoria del componente basado en los parámetros definidos
                    componente = "".join(random.choices(caracteres, k=longitud))
                    
                    # Formato especificado: NombreComponente:ComponenteNombre
                    linea_resultado = f"{nombre}{componente}:{componente}{nombre}\n"
                    f_out.write(linea_resultado)
                    
                    contador += 1
                    progress_bar(contador, total_combinaciones)
                    
                    # Efecto visual en la barra de progreso para lotes pequeños
                    if total_combinaciones <= 1500:
                        time.sleep(0.002)
                        
        print(f"\n{Fore.GREEN}[+] Secuencia finalizada con éxito.{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Entradas totales generadas: {Fore.MAGENTA}{total_combinaciones}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Archivo volcado en: {Fore.GREEN}{ruta_salida}{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"\n{Fore.RED}[!] ERROR CRÍTICO de E/S durante la escritura: {e}{Style.RESET_ALL}")

if __name__ == '__main__':
    # Intercepta la interrupción manual (Ctrl+C) de forma limpia
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Proceso abortado por el usuario.{Style.RESET_ALL}")
        sys.exit(0)