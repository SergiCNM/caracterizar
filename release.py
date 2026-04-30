import os
import re
import subprocess
import sys
from datetime import datetime

CONFIG_PATH = os.path.join("config", "config.toml")
CHANGELOG_PATH = "CHANGELOG.md"

def run_command(command, capture_output=True):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, 
                                stdout=subprocess.PIPE if capture_output else None,
                                stderr=subprocess.PIPE if capture_output else None)
        return result.stdout.strip() if capture_output else ""
    except subprocess.CalledProcessError as e:
        print(f"\nError ejecutando comando: {command}")
        if capture_output:
            print(f"Salida: {e.stderr}")
        return None

def get_current_version():
    if not os.path.exists(CONFIG_PATH):
        print(f"Error: No se encuentra {CONFIG_PATH}")
        return None
    
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        content = f.read()
        match = re.search(r'version\s*=\s*"([^"]+)"', content)
        if match:
            return match.group(1)
    return None

def get_latest_tag():
    # Obtener el último tag ordenado por versión
    tags = run_command("git tag -l --sort=-v:refname")
    if tags:
        return tags.split("\n")[0].replace("v", "")
    return None

def update_config_version(new_version):
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    
    new_content = re.sub(r'(version\s*=\s*)"[^"]+"', f'\\1"{new_version}"', content)
    
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

def get_changelog_entry(version):
    if not os.path.exists(CHANGELOG_PATH):
        return "No se encontró CHANGELOG.md"
    
    with open(CHANGELOG_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Buscar el encabezado de la versión (ej: ## [2.2.2])
    version_header = f"## [{version}]"
    start_index = content.find(version_header)
    
    if start_index == -1:
        return None
    
    # Buscar el siguiente encabezado de versión (que empiece por ## [)
    next_header_match = re.search(r'\n## \[', content[start_index + len(version_header):])
    
    if next_header_match:
        end_index = start_index + len(version_header) + next_header_match.start()
        return content[start_index:end_index].strip()
    else:
        # Es la última entrada (o la única)
        return content[start_index:].strip()

def main():
    print("=== Automatización de Release - Caracterizar ===\n")

    # 1. Sincronización Inicial y Detección
    print("Sincronizando con el repositorio remoto...")
    run_command("git fetch origin")
    status_output = run_command("git status -uno")
    
    if "is behind" in status_output:
        print("El repositorio local está por detrás del remoto. Realizando pull...")
        run_command("git pull --rebase origin main")

    current_version = get_current_version()
    latest_tag = get_latest_tag()

    if not current_version:
        print("No se pudo detectar la versión en config.toml. Abortando.")
        return

    print(f"Versión actual en config.toml: {current_version}")
    print(f"Última versión en GitHub (tag): {latest_tag if latest_tag else 'Ninguna'}")

    if latest_tag and current_version != latest_tag:
        print(f"ADVERTENCIA: Las versiones no coinciden! (Tag: {latest_tag}, Local: {current_version})")
    
    # 2. Seleccionar tipo de update
    try:
        v_parts = [int(p) for p in current_version.split(".")]
    except ValueError:
        print(f"Error al parsear la versión '{current_version}'. Asegúrate de que tenga formato X.Y.Z")
        return
    
    print("\nSelecciona el tipo de actualización:")
    print(f"1. Patch: {v_parts[0]}.{v_parts[1]}.{v_parts[2]+1}")
    print(f"2. Minor: {v_parts[0]}.{v_parts[1]+1}.0")
    print(f"3. Major: {v_parts[0]+1}.0.0")
    
    choice = input("\nOpción (1/2/3): ")
    if choice == "1":
        new_version = f"{v_parts[0]}.{v_parts[1]}.{v_parts[2]+1}"
    elif choice == "2":
        new_version = f"{v_parts[0]}.{v_parts[1]+1}.0"
    elif choice == "3":
        new_version = f"{v_parts[0]+1}.0.0"
    else:
        print("Opción no válida. Abortando.")
        return

    print(f"\nNueva versión calculada: {new_version}")

    # 3. Modificar config.toml automáticamente
    update_config_version(new_version)
    print(f"Archivo {CONFIG_PATH} actualizado a la versión {new_version}.")

    # 4. Pausa para intervención manual
    print("\n--- Estado de archivos (git status) ---")
    print(run_command("git status --short"))
    
    print(f"\nPOR FAVOR, ACTUALIZA {CHANGELOG_PATH} MANUALMENTE AHORA.")
    print(f"Debes añadir una sección para la versión [{new_version}].")
    input("Pulsa Enter cuando hayas guardado los cambios en el CHANGELOG...")

    # 5. Resumen final
    print("\n" + "="*40)
    print("RESUMEN FINAL DE LA ACTUALIZACIÓN")
    print("="*40)
    print(f"Versión: {current_version} -> {new_version}")
    
    print("\nArchivos que se subirán (git add .):")
    print(run_command("git status --short"))
    
    print("\nContenido detectado en CHANGELOG.md para esta versión:")
    changelog_entry = get_changelog_entry(new_version)
    if changelog_entry:
        print("-" * 20)
        print(changelog_entry)
        print("-" * 20)
    else:
        print(f"¡AVISO! No se ha detectado la entrada '## [{new_version}]' en el CHANGELOG.md")
        
    # 6. Confirmación final y Ejecución
    confirm = input("\n¿Deseas subir los cambios a GitHub? (S/N): ").lower()
    
    if confirm == 's':
        print("\nEjecutando comandos Git...")
        # 1. Add y Commit
        run_command("git add .")
        run_command(f'git commit -m "Version v{new_version}"')
        
        # 2. Tag
        run_command(f'git tag -a v{new_version} -m "Version v{new_version}"')
        
        # 3. Push Rama
        print("Subiendo rama main...")
        push_branch = run_command("git push origin main", capture_output=True)
        
        # 4. Push Tag
        if push_branch is not None:
            print(f"Subiendo tag v{new_version}...")
            run_command(f"git push origin v{new_version}")
            print("\n¡Actualización completada con éxito!")
        else:
            print("\nERROR: Falló el push de la rama main. El tag no se ha subido al remoto.")
            print("Intenta sincronizar manualmente.")
    else:
        print("\nCancelando y revirtiendo cambios locales...")
        run_command(f"git checkout -- {CONFIG_PATH} {CHANGELOG_PATH}")
        print("Archivos revertidos a su estado original.")

if __name__ == "__main__":
    main()
