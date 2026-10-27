import json
import os
from datetime import datetime, timedelta
import urllib.request

CONFIG_FILE = "config.json"
# Reemplaza con la URL RAW de tu archivo de configuración en tu repositorio de GitHub
GITHUB_RAW_URL = "https://raw.githubusercontent.com/TU_USUARIO/TU_REPO/main/config_remote.json"

def load_local_config():
    if not os.path.exists(CONFIG_FILE):
        default_data = {
            "jumps": 0, 
            "background_index": 0, 
            "last_sync_date": datetime.now().strftime("%Y-%m-%d")
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(default_data, f)
        return default_data
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_local_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

def check_github_sync():
    config = load_local_config()
    last_sync_str = config.get("last_sync_date", "2026-01-01")
    last_sync = datetime.strptime(last_sync_str, "%Y-%m-%d")
    
    # Valida si han pasado 7 días o más desde la última actualización
    if datetime.now() - last_sync >= timedelta(days=7):
        try:
            req = urllib.request.urlopen(GITHUB_RAW_URL, timeout=5)
            remote_data = json.loads(req.read().decode())
            print("Sincronización con GitHub exitosa:", remote_data)
            
            # Actualiza fecha de sincronización
            config["last_sync_date"] = datetime.now().strftime("%Y-%m-%d")
            save_local_config(config)
            return remote_data
        except Exception as e:
            print("Aviso: No se pudo conectar a GitHub para actualizar:", e)
    return None




