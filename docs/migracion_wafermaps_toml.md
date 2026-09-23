# Plan de Implementación: Migrar Wafermaps de `.py` a `.toml`

## 1. Contexto

### Situación actual
- **69 archivos** de wafermap en `config/default/wafermaps/`:
  - 68 archivos con patrón `*_wafermap.py`
  - 1 archivo sin sufijo: `deep_bidirectional.py`
- Los wafermaps son **100% datos estáticos**: variables simples + diccionario `wafer_parameters`.
- Se cargan mediante `exec()` en dos puntos:
  - `main.py:2686` → `run()`
  - `wafermap_file.py:115` → `WafermapFile.__init__()`
- Se generan mediante `wafers.py:357-417` → `save_wafermap()`
- El sistema ya usa `toml` para la configuración principal (`modules/config.py`)

### Formato de un wafermap actual (ejemplo)
```python
global wafer_parameters

wafer_name = "NANUSENS"
wafer_size = 8
xsize = 25056.0
ysize = 31388.0
nchips = 26
nmodules = 4
real_origin_chip = "-2 -1"
origin_chip = "0 0"
home_chip = "0 0"
flat_orientation = 0
navigation_options = ['UPPER-LEFT', 'UNI-DIRECTIONAL', 'ROW']
wafer_positions = ['0 0', '-1 0', ...]
wafer_modules = ['0.0 0.0', '0.0 450.0', ...]
wafer_modules_name = ['1', '2', '3', '4']

wafer_parameters = {
    "wafer_name": wafer_name,
    "wafer_size": wafer_size,
    ...
}
```

### Formato objetivo (TOML)
```toml
wafer_name = "NANUSENS"
wafer_size = 8
xsize = 25056.0
ysize = 31388.0
nchips = 26
nmodules = 4
origin_chip = "0 0"
home_chip = "0 0"
real_origin_chip = "-2 -1"
flat_orientation = 0
navigation_options = ["UPPER-LEFT", "UNI-DIRECTIONAL", "ROW"]
wafer_positions = ["0 0", "-1 0", ...]
wafer_modules = ["0.0 0.0", "0.0 450.0", ...]
wafer_modules_name = ["1", "2", "3", "4"]
```

---

## 2. Archivos a modificar

| # | Archivo | Líneas clave | Cambio |
|---|---------|-------------|--------|
| 1 | `modules/wafermap_file.py` | 23, 111-126, 226, 293-305, 309 | Añadir soporte `.toml` |
| 2 | `main.py` | 2680-2697 | `run()`: añadir rama TOML |
| 3 | `main.py` | 3476-3488 | `load_wafermaps()`: incluir `.toml` |
| 4 | `main.py` | 3601-3606 | `get_filename_wafermap()`: generalizar extensión |
| 5 | `main.py` | 3680-3691 | `set_wafermap_description()`: generalizar extensión |
| 6 | `modules/wafers.py` | 357-417 | `save_wafermap()`: opción `.toml` |
| 7 | `config/default/wafermaps/` | — | Migrar 69 archivos |

---

## 3. Pasos de implementación

### Paso 1 -- Script de conversión `.py` → `.toml`

Crear un script one-shot que convierta los 69 archivos existentes:

- Leer cada fichero `.py` con `exec()` en un namespace limpio
- Extraer el diccionario `wafer_parameters` resultante
- Escribir un fichero `.toml` con `toml.dump()`
- Nomenclatura: `nombre_wafermap.py` → `nombre_wafermap.toml`
- Caso especial: `deep_bidirectional.py` → `deep_bidirectional_wafermap.toml` (normalizar nombre)

**Ubicación sugerida:** `tools/convert_wafermaps.py` (script temporal)

**Verificación:** ejecutar `toml.load()` en cada fichero generado y comparar claves con el `.py` original.

---

### Paso 2 -- `modules/wafermap_file.py`

#### 2a. Añadir `"toml"` a `mode_types`

```python
# Linea 23:
self.mode_types = ["py", "ppg", "toml"]
```

#### 2b. Añadir import

```python
# Cabecera del archivo:
import toml
```

#### 2c. Ramas de carga (líneas 111-126)

Añadir bloque para `.toml` antes del `else`:

```python
elif self.mode_type == "toml":
    with open(self.path_to_file, "r", encoding="utf-8") as fp:
        self.wafer_parameters = toml.load(fp)
    self.wafer_size_inch = float(self.wafer_parameters["wafer_size"])
    self.set_wafer_size()
    if not "xmax" in self.wafer_parameters or not "ymax" in self.wafer_parameters:
        self.wafer_parameters["xmax"], self.wafer_parameters["ymax"] = self.get_xmax_ymax()
```

#### 2d. Método `check_file()` (líneas 224-312)

- Línea 226: `"toml"` ya estará en `mode_types` tras 2a → no falla
- Añadir verificación para `"toml"` (líneas 293-310):

```python
if self.mode_type == "toml":
    required_keys = [
        "wafer_name", "wafer_size", "xsize", "ysize",
        "nchips", "real_origin_chip", "origin_chip", "home_chip",
        "flat_orientation", "navigation_options",
        "wafer_positions", "wafer_modules"
    ]
    missing = [k for k in required_keys if k not in self.wafer_parameters]
    if missing:
        return [False, f"Missing keys in TOML: {missing}"]
```

---

### Paso 3 -- `main.py` : `run()` (líneas 2680-2697)

Añadir rama TOML antes del `else`:

```python
def run(self, runfile, folder):
    runfile_path = self.get_base_path(folder) + runfile
    if os.path.exists(runfile_path):
        try:
            if runfile.endswith(".toml"):
                import toml
                with open(runfile_path, "r", encoding="utf-8") as fp:
                    global wafer_parameters
                    wafer_parameters = toml.load(fp)
            else:
                with open(runfile_path, "r") as rnf:
                    exec(rnf.read())
        except Exception as ex:
            # ... mismo manejo de errores actual
    else:
        # ... mismo manejo de errores actual
```

---

### Paso 4 -- `main.py` : `load_wafermaps()` (líneas 3476-3488)

Modificar para incluir ambos formatos:

```python
def load_wafermaps(self):
    global widgets
    dir_wafermaps = self.getDirs("wafermaps") + "/"
    contenido = os.listdir(dir_wafermaps)
    widgets.cmbWafermaps.clear()
    widgets.cmbWafermaps.addItem("Select wafermap")

    # Incluir .py y .toml
    sorted_files = sorted([
        f for f in contenido
        if os.path.isfile(os.path.join(dir_wafermaps, f))
        and (f.endswith('_wafermap.py') or f.endswith('_wafermap.toml'))
    ])

    for fichero in sorted_files:
        # Quitar extension
        name = fichero.replace("_wafermap.py", "").replace("_wafermap.toml", "")
        widgets.cmbWafermaps.addItem(name)

    self.setup_searchable_combo(widgets.cmbWafermaps)
```

**Nota importante:** Un mismo wafermap no debe existir como `.py` y `.toml` simultáneamente en la carpeta activa, para evitar duplicados en el combo. El script de migración debe limpiar los `.py` originales una vez generados los `.toml`.

---

### Paso 5 -- `main.py` : `get_filename_wafermap()` (líneas 3601-3606)

Estrategia: buscar primero `.toml`, luego `.py` (backward compatibilidad):

```python
def get_filename_wafermap(self):
    global widgets
    wafermap_selected = self.get_wafermap_selected()
    if wafermap_selected != "":
        base = wafermap_selected + "_wafermap"
        dir_wafermaps = self.getDirs("wafermaps") + "/"
        # Preferir .toml, fallback a .py
        toml_path = os.path.join(dir_wafermaps, base + ".toml")
        if os.path.exists(toml_path):
            return base + ".toml"
        py_path = os.path.join(dir_wafermaps, base + ".py")
        if os.path.exists(py_path):
            return base + ".py"
        return base + ".toml"  # default
    return ""
```

---

### Paso 6 -- `main.py` : `set_wafermap_description()` (líneas 3680-3691)

Aplicar misma lógica de detección de extensión:

```python
def set_wafermap_description(self):
    global widgets
    wafermap_selected = self.get_wafermap_selected()
    widgets.pteWafermap.setPlainText("")
    if wafermap_selected != "":
        dir_wafermaps = self.getDirs("wafermaps") + "/"
        base = wafermap_selected + "_wafermap"
        # Preferir .toml, fallback a .py
        namefile = os.path.join(dir_wafermaps, base + ".toml")
        if not os.path.exists(namefile):
            namefile = os.path.join(dir_wafermaps, base + ".py")
        f = open(namefile, "r")
        widgets.pteWafermap.setPlainText(f.read())
        f.close()
```

---

### Paso 7 -- `modules/wafers.py` : `save_wafermap()` (líneas 357-417)

Añadir opción para guardar como `.toml`:

- Cambiar filtro del diálogo a `"Wafermaps (*.toml *.py)"`
- Detectar extensión del fichero seleccionado
- Si `.toml`: construir diccionario y usar `toml.dump()`
- Si `.py`: mantener comportamiento actual (string template)

```python
def save_wafermap(self):
    dir_wafermaps = os.getcwd() + base_dir + wafermaps_dir + "/"
    default_filename = f"{self.wafer_name}_wafermap.toml" if self.wafer_name else ""
    nameFile, _ = QFileDialog.getSaveFileName(
        self, 'Save wafermap', dir_wafermaps + default_filename,
        "Wafermaps TOML (*.toml);;Wafermaps Python (*.py)"
    )

    if nameFile == "":
        return

    wafer_data = {
        "wafer_name": self.wafer_name,
        "wafer_size": self.wafer_size_inch,
        "xsize": self.xsize,
        "ysize": self.ysize,
        "nchips": self.nchips,
        "nmodules": self.nmodules,
        "origin_chip": str(self.origin_chip),
        "home_chip": str(self.home_chip),
        "init_chip": self.init_chip,
        "end_chip": self.end_chip,
        "flat_orientation": self.flat_orientation,
        "navigation_options": self.navigation_options,
        "wafer_positions": self.wafer_positions,
        "wafer_modules": self.wafer_modules,
        "wafer_modules_name": self.wafer_modules_name,
        "real_origin_chip": str(self.real_origin_chip),
    }

    if nameFile.endswith(".toml"):
        import toml
        with open(nameFile, 'w', encoding="utf-8") as f:
            toml.dump(wafer_data, f)
    else:
        # ... mantener template .py actual
```

---

### Paso 8 -- Limpieza y migración

1. Ejecutar script de conversión (Paso 1)
2. Verificar: abrir cada `.toml` con `toml.load()` y comparar con `wafer_parameters` del `.py` original
3. **Opción A (recomendada):** Reemplazar `.py` por `.toml` en `config/default/wafermaps/`
4. **Opción B:** Mantener ambos formatos, el código da preferencia a `.toml`
5. Borrar script de conversión

---

## 4. Backward compatibility

El código modificado mantiene compatibilidad con `.py`:
- `load_wafermaps()` lee ambos formatos
- `get_filename_wafermap()` prefiere `.toml` pero cae a `.py`
- `run()` ejecuta `toml.load()` o `exec()` según extensión
- `wafermap_file.py` soporta ambos en `mode_types`

Esto permite migrar progresivamente wafermap a wafermap.

---

## 5. Riesgos y mitigaciones

| Riesgo | Impacto | Mitigación |
|--------|---------|------------|
| Campos adicionales en `.py` (ej. `init_chip`, `end_chip`) no en todos los wafermaps | Alto | El script de conversión debe extraer todas las variables globales del `.py`, no solo las del diccionario |
| `wafer_parameters` con claves faltantes | Alto | `check_file()` valida claves obligatorias |
| Archivos `.py` y `.toml` duplicados en combo | Medio | Tras migración, borrar `.py` originales |
| `deep_bidirectional.py` sin sufijo `_wafermap` | Bajo | Normalizar nombre en script de conversión |
| Reports que hacen `global wafer_parameters` | Bajo | La variable global se setea igual (desde `run()`) |

---

## 6. Checklist de verificación

- [ ] Script de conversión genera 69 ficheros `.toml` válidos
- [ ] Cada `.toml` parsea correctamente con `toml.load()`
- [ ] Claves de cada `.toml` coinciden con `wafer_parameters` del `.py` original
- [ ] `WafermapFile()` carga `.toml` sin errores
- [ ] `load_wafermaps()` muestra nombres en combo sin duplicados
- [ ] `view_wafermap()` visualiza correctamente desde `.toml`
- [ ] `start_process()` ejecuta medición con wafermap `.toml`
- [ ] `save_wafermap()` genera `.toml` válido desde la UI
- [ ] Wafermap `.py` antiguo sigue funcionando (backward compat)
