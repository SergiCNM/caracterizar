# Corrección de Bugs y Optimización del Sistema de Secciones en Wafer Map

Revisión completa de [wafers.py](file:///c:/GITHUB/Python/caracterizar/modules/wafers.py) centrada en el funcionamiento con secciones (quadrant mode).

---

## Convención de Coordenadas (confirmada)

```
Grid visual del wafer (ejemplo 4" con dies 15000x15000):

  x_idx:  0      1      2      3      4
         (0,0)  (-1,0) (-2,0) (-3,0) (-4,0)   ← btn.x = -x_idx
y_idx 0   □      □      □      □      □
         (0,-1) (-1,-1)(-2,-1)(-3,-1)(-4,-1)
y_idx 1   □      □      ●O     □      □        ← origin en real_origin_chip="-2 -1"
         (0,-2) ...
y_idx 2   □      □      □      □      □
```

| Concepto | Convención |
|---|---|
| **Índices de grid** (`x_idx, y_idx`) | Positivos (0, 1, 2...) desde top-left |
| **Coordenadas de botón** (`btn.x, btn.y`) | Negativos: `btn.x = -x_idx`, `btn.y = -y_idx` |
| **wafer_positions** (fichero .py) | Relativas a `real_origin_chip`, derecha = X negativo, abajo = Y negativo |
| **`change_coord_to_origin(btn.x, btn.y, origin)`** | Convierte coord botón → posición relativa a origin |

> [!IMPORTANT]
> Derecha = X más negativo, Abajo = Y más negativo. El (0,0) del grid visual es top-left. Las funciones geométricas (`is_in_by_index`, `is_home_by_index`) esperan **índices positivos** (`x_idx, y_idx`).

---

## Bugs Encontrados

### Bug 1 — DOBLE CONTEO en MarkAll y UnmarkAll (CRÍTICO)

**Ubicación**: [MarkAll](file:///c:/GITHUB/Python/caracterizar/modules/wafers.py#L735-L832) y [UnmarkAll](file:///c:/GITHUB/Python/caracterizar/modules/wafers.py#L834-L926)

**Problema**: Ambas funciones cuentan en dos bucles secuenciales:
1. Iteran sobre **botones visibles** (widgets QWaferButton) → acumulan totales
2. Iteran sobre **`all_buttons_states`** (que incluye los mismos botones visibles) → vuelven a acumular

**Resultado**: Botones visibles contados **2 veces**. Contadores inflados.

**Fix**: Sincronizar visibles → `all_buttons_states` primero, luego contar UNA sola vez con `_update_totals_from_states()`.

---

### Bug 2 — `_calculate_original_button_type` usa coordenadas con signo INCORRECTO (CRÍTICO)

**Ubicación**: [_calculate_original_button_type](file:///c:/GITHUB/Python/caracterizar/modules/wafers.py#L928-L946)

**Problema**: Se llama con `coord = (btn.x, btn.y)` que son valores **negativos**, pero `is_in_by_index()` espera **índices positivos**:

```python
coord = (i.x, i.y)  # (-x_idx, -y_idx) → NEGATIVO
self._calculate_original_button_type(coord[0], coord[1])  # pasa negativo

# is_in_by_index con negativos:
pos_x = -x_idx * xsize  # NEGATIVO → pow(R - (-val), 2) siempre > R² → siempre False
```

**Resultado**: `is_in_by_index` retorna **siempre False** → `_calculate_original_button_type` retorna "out" para TODO. UnmarkAll convierte todos los IN en OUT.

**Fix**: Usar `abs()` en `_calculate_original_button_type`:
```python
def _calculate_original_button_type(self, x_coord, y_coord):
    x_idx = abs(x_coord)  # Convertir coord botón → índice positivo
    y_idx = abs(y_coord)
    # ... usar x_idx, y_idx para is_in_by_index, is_home_by_index, etc.
```

---

### Bug 3 — MarkAll convierte TODOS los botones a MEAS en `all_buttons_states` (CRÍTICO)

**Ubicación**: [MarkAll, bucle all_buttons_states](file:///c:/GITHUB/Python/caracterizar/modules/wafers.py#L794-L819)

**Problema**: Línea 796: `btnType = "meas"` se aplica **sin verificación** a todos los botones en `all_buttons_states`, incluidos los OUT.

**Fix**: Solo marcar como MEAS los botones cuyo tipo actual sea "in". OUT se mantiene como OUT.

---

### Bug 4 — `get_sorted_measured_buttons` falla en secciones > (0,0) (CRÍTICO)

**Ubicación**: [get_sorted_measured_buttons](file:///c:/GITHUB/Python/caracterizar/modules/wafers.py#L951-L1018)

**Problema**: Itera con índices locales `(0..numx, 0..numy)` pero `buttons_by_coord` usa **índices absolutos del grid**:

```python
# Iteración usa índices locales:
coord_key = (x, y)  # (0, 1, 2...)
btn = self.buttons_by_coord.get(coord_key)  # NO ENCUENTRA NADA

# Pero las claves son absolutas:
# buttons_by_coord[(x_start_idx + x, y_start_idx + y)] = btn
# En sección (1,0): claves como (50, 0), (51, 0)...
```

**Impacto en SaveWafer**: Al guardar desde sección > (0,0), `wafer_positions` sale VACÍO porque no encuentra botones.

**Fix**: La función debe poder encontrar botones independientemente de la sección activa. Para SaveWafer/total_meas, necesitamos un `get_sorted_measured_buttons` que trabaje con `all_buttons_states` para obtener TODOS los MEAS del wafer completo.

---

### Bug 5 — `total_meas()` solo cuenta botones VISIBLES (CRÍTICO con secciones)

**Ubicación**: [total_meas](file:///c:/GITHUB/Python/caracterizar/modules/wafers.py#L1020-L1104)

**Problema**: Solo itera `self.centralWidget().findChildren(QWaferButton)` → solo botones de la sección actual.

**Requisito**: Los contadores deben mostrar totales del **wafer completo** (todas las secciones).

**Fix**: Sincronizar visibles → `all_buttons_states`, luego contar desde `all_buttons_states`.

---

### Bug 6 — `all_buttons_states` no se inicializa para TODAS las secciones (IMPORTANTE)

**Ubicación**: [all_buttons_states init](file:///c:/GITHUB/Python/caracterizar/modules/wafers.py#L533)

**Problema**: Empieza vacío `{}`. Solo se puebla al visitar secciones o cambiar estados. Secciones nunca visitadas no existen → `_update_totals_from_states()` no las cuenta.

**Fix**: Pre-calcular todos los estados en `__init__` sin crear widgets.

---

### Issue 7 — Velocidad lenta al cambiar de sección (RENDIMIENTO)

**Ubicación**: [_refresh_display](file:///c:/GITHUB/Python/caracterizar/modules/wafers.py#L1596-L1632)

**Problema**: Destruye todos los widgets (`deleteLater`) y los recrea. Cada `QWaferButton` requiere: init + setStyleSheet + connect + addWidget.

**Optimización**: Pre-calcular estilos, bloquear señales, evitar processEvents innecesarios.

---

## Proposed Changes

### Fase 1: Inicialización completa de `all_buttons_states` (Bug 6)

#### [MODIFY] [wafers.py](file:///c:/GITHUB/Python/caracterizar/modules/wafers.py) — `WaferWindow.__init__`

Añadir nuevo método `_init_all_buttons_states()` y llamarlo tras `add_die_buttons`:

```python
def _init_all_buttons_states(self):
    """Pre-calcula estados de TODOS los dies del wafer completo (todas las secciones)"""
    wafer_size_um = self.wafer.wafer_size_mm * 1000
    est_x = max(1, int(wafer_size_um / self.wafer.xsize))
    est_y = max(1, int(wafer_size_um / self.wafer.ysize))
    
    for y_idx in range(est_y):
        for x_idx in range(est_x):
            coord = (-x_idx, -y_idx)  # Convención negativa de QWaferButton
            if coord in self.all_buttons_states:
                continue  # Ya existe (botón visible en sección actual)
            
            btnType = "out"
            is_home = self.wafer.is_home_by_index(x_idx, y_idx)
            is_origin = self.wafer.is_origin_by_index(x_idx, y_idx)
            if is_origin:
                btnType = "meas"
            if self.wafer.is_in_by_index(x_idx, y_idx):
                btnType = "in"
            if self.wafer.is_to_measure_by_index(x_idx, y_idx):
                btnType = "meas"
            
            self.all_buttons_states[coord] = {
                'btnType': btnType,
                'home': is_home,
                'origin': is_origin,
                'message': ''
            }
```

En `__init__`, después de línea 543:
```python
self.numx, self.numy = self.add_die_buttons(wafer, enable)
# Registrar botones visibles en all_buttons_states
for btn in self.centralWidget().findChildren(QWaferButton):
    coord = (btn.x, btn.y)
    self.all_buttons_states[coord] = {
        'btnType': btn._btnType, 'home': btn._home,
        'origin': btn._origin, 'message': ''
    }
# Pre-calcular estados de secciones no visibles
self._init_all_buttons_states()
```

---

### Fase 2: Corregir `_calculate_original_button_type` (Bug 2)

#### [MODIFY] [wafers.py](file:///c:/GITHUB/Python/caracterizar/modules/wafers.py#L928-L946)

```python
def _calculate_original_button_type(self, x_coord, y_coord):
    """Calcula el tipo original basado en geometría. Acepta coords de botón (negativas)."""
    x_idx = abs(x_coord)  # Convertir a índice positivo para funciones geométricas
    y_idx = abs(y_coord)
    
    btnType = "out"
    if self.wafer.is_origin_by_index(x_idx, y_idx):
        btnType = "meas"
    if self.wafer.is_in_by_index(x_idx, y_idx):
        btnType = "in"
    if self.wafer.is_to_measure_by_index(x_idx, y_idx):
        btnType = "meas"
    return btnType
```

---

### Fase 3: Reescribir MarkAll y UnmarkAll (Bugs 1, 3)

#### [MODIFY] [wafers.py](file:///c:/GITHUB/Python/caracterizar/modules/wafers.py#L735-L926)

**MarkAll** — Solo marca IN→MEAS en la sección visible, contadores del wafer completo:

```python
def MarkAll(self):
    self.centralWidget().setUpdatesEnabled(False)
    self._skip_total_meas = True
    try:
        # 1. Sincronizar botones visibles → all_buttons_states
        for btn in self.centralWidget().findChildren(QWaferButton):
            coord = (btn.x, btn.y)
            self.all_buttons_states[coord] = {
                'btnType': btn._btnType, 'home': btn._home,
                'origin': btn._origin, 'message': btn._message
            }
        
        # 2. Marcar solo los IN visibles como MEAS (sección actual)
        for btn in self.centralWidget().findChildren(QWaferButton):
            if btn._btnType == "in":
                coord = (btn.x, btn.y)
                btn._btnType = "meas"
                self._apply_button_style(btn, "meas")
                name = ""
                if btn._home: name = "H"
                if btn._origin: name = "O"
                btn.setText(name)
                self.all_buttons_states[coord]['btnType'] = "meas"
        
        # 3. Contadores globales desde all_buttons_states
        self._update_totals_from_states()
    finally:
        self.centralWidget().setUpdatesEnabled(True)
        self.centralWidget().update()
        self._skip_total_meas = False
```

**UnmarkAll** — Restaura sección visible + secciones no visibles:

```python
def UnmarkAll(self):
    self.centralWidget().setUpdatesEnabled(False)
    self._skip_total_meas = True
    try:
        # 1. Restaurar botones visibles a su tipo geométrico original
        for btn in self.centralWidget().findChildren(QWaferButton):
            coord = (btn.x, btn.y)
            original = self._calculate_original_button_type(coord[0], coord[1])
            btn._btnType = original
            self._apply_button_style(btn, original)
            name = ""
            if btn._home: name = "H"
            if btn._origin: name = "O"
            btn.setText(name)
            self.all_buttons_states[coord]['btnType'] = original
            self.all_buttons_states[coord]['home'] = btn._home
            self.all_buttons_states[coord]['origin'] = btn._origin
        
        # 2. Restaurar secciones NO visibles
        visible_coords = {(btn.x, btn.y) for btn in self.centralWidget().findChildren(QWaferButton)}
        for coord, state in self.all_buttons_states.items():
            if coord not in visible_coords:
                original = self._calculate_original_button_type(coord[0], coord[1])
                state['btnType'] = original
        
        # 3. Contadores globales
        self._update_totals_from_states()
    finally:
        self.centralWidget().setUpdatesEnabled(True)
        self.centralWidget().update()
        self._skip_total_meas = False
```

---

### Fase 4: Corregir `total_meas` y `get_sorted_measured_buttons` (Bugs 4, 5)

#### [MODIFY] [wafers.py](file:///c:/GITHUB/Python/caracterizar/modules/wafers.py#L951-L1104)

**`total_meas()`** — Sincronizar visibles → `all_buttons_states`, contar global:

```python
def total_meas(self):
    if self._skip_total_meas:
        return
    self._skip_total_meas = True
    self.centralWidget().setUpdatesEnabled(False)
    try:
        # Sincronizar botones visibles → all_buttons_states
        for btn in self.centralWidget().findChildren(QWaferButton):
            coord = (btn.x, btn.y)
            if coord in self.all_buttons_states:
                self.all_buttons_states[coord]['btnType'] = btn._btnType
        
        # Contar desde all_buttons_states (wafer completo)
        self._update_totals_from_states()
        
        # Aplicar highlight init_chip/end_chip solo a botones visibles
        # ... (lógica de meas_selected)
    finally:
        self.centralWidget().setUpdatesEnabled(True)
        self.centralWidget().update()
        self._skip_total_meas = False
```

**`get_sorted_measured_buttons()`** — Corregir para que funcione con secciones:
- Para **SaveWafer**: Crear versión que trabaja con `all_buttons_states` para obtener TODOS los MEAS
- Para **highlight visual**: Mantener versión que solo usa botones visibles pero con claves correctas

```python
def get_all_measured_positions_sorted(self):
    """Devuelve todas las coordenadas MEAS del wafer completo, ordenadas según navigation_options"""
    # Obtener todos los MEAS de all_buttons_states
    meas_coords = []
    for coord, state in self.all_buttons_states.items():
        if state['btnType'] in ["meas", "meas_selected", "meas_success", "meas_warning", "meas_error"]:
            meas_coords.append(coord)
    
    # Ordenar según navigation_options (starting_location, direction, row/col)
    # ... lógica de ordenación basada en coordenadas
    return meas_coords
```

---

### Fase 5: Corregir SaveWafer para modo secciones

#### [MODIFY] [wafers.py](file:///c:/GITHUB/Python/caracterizar/modules/wafers.py#L1271-L1373)

En `SaveWafer`, usar `get_all_measured_positions_sorted()` en lugar de `get_sorted_measured_buttons()` para que capture TODOS los chips MEAS del wafer, no solo la sección visible. Las coordenadas se convierten con `change_coord_to_origin(coord[0], coord[1], real_origin_chip)`.

---

### Fase 6: Optimización de velocidad (Issue 7)

#### [MODIFY] [wafers.py](file:///c:/GITHUB/Python/caracterizar/modules/wafers.py#L1596-L1668)

1. **Pre-calcular strings de estilo** como dict estático en `QWaferButton`:
```python
BUTTON_STYLES = {
    t: f"font-size: 8pt; text-align: center; border: 1px solid #DDDDDD; background-color: {c};"
    for t, c in COLORS_DIES.items()
}
```

2. **Bloquear señales** durante reconstrucción masiva de botones
3. **Evitar `processEvents()`** innecesarios durante creación

---

## Resumen de Cambios por Archivo

| Archivo | Cambios |
|---|---|
| [wafers.py](file:///c:/GITHUB/Python/caracterizar/modules/wafers.py) | `_init_all_buttons_states()` nuevo, `_calculate_original_button_type` fix abs(), `MarkAll` reescrito, `UnmarkAll` reescrito, `total_meas` reescrito, `get_all_measured_positions_sorted` nuevo, `SaveWafer` actualizado, `get_sorted_measured_buttons` fix claves, optimización estilos |

---

## Open Questions

> [!IMPORTANT]
> **UNMARK ALL con secciones**: ¿Debe desmarcar **solo la sección visible** (como MARK ALL) o **todo el wafer de golpe**? En el plan propongo que UnmarkAll restaure TODAS las secciones (visible + no visibles) al estado geométrico original, ya que el caso de uso típico es "empezar de cero".

> [!IMPORTANT]
> **SaveWafer con secciones**: ¿Debe siempre guardar TODOS los chips MEAS del wafer completo, independientemente de qué sección esté visible? (Lo propongo así porque perder posiciones al guardar es peligroso.)

---

## Verification Plan

### Manual Verification

1. **Test sin secciones** (wafer 4" con dies grandes, ej: Gabriele 15000x15000):
   - MarkAll/UnmarkAll funcionan → contadores correctos
   - SaveWafer guarda `wafer_positions` correctas → comparar con fichero original

2. **Test con secciones** (wafer grande con dies pequeños para forzar quadrant mode):
   - Contadores IN/OUT/MEAS = totales del wafer completo al cargar
   - Marcar chips en sección 1 → navegar a sección 2 → volver → chips persisten
   - MarkAll sección 1 → navegar sección 2 → OUT sigue OUT, IN sigue IN
   - UnmarkAll → todo restaurado
   - SaveWafer → fichero contiene TODAS las posiciones MEAS de todo el wafer

3. **Test de rendimiento**: Medir tiempo de cambio de sección antes/después
