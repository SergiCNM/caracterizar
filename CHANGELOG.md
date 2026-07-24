# Changelog

Todos los cambios importantes en este proyecto se documentan en este archivo.

## [3.0.0] - 2026-07-24
### Added
- **Pantalla de login con autenticación de usuario**: Nuevo sistema de login con dos modos: usuario por defecto (sin autenticación) y usuario autenticado contra la API de SIAM (`https://www.cnm.es/users/siam/api/auth/login`). Cada usuario guarda resultados en su propia carpeta `results/<username>/`.
- **Módulo `modules/auth.py`**: Función `authenticate()` que realiza POST a la API de SIAM usando `urllib` (stdlib). Maneja respuestas HTTP 200, 401, 403 y 404 con mensajes descriptivos para cada caso.
- **Radio buttons en login**: Alternancia entre modo "Default" (entrada directa) y modo "User" (con campos usuario/contraseña). La ventana cambia de tamaño dinámicamente (600x460 vs 600x700).
- **SplashScreen con verificaciones reales**: Durante la barra de progreso se ejecutan las comprobaciones reales (autenticación API, creación de carpetas de resultados, preparación del workspace).
- **Fallback a `config/default/`**: Si el usuario no tiene configuración propia (instruments, probers, tests, etc.), se usa la carpeta `config/default/` como fallback.

### Changed
- **Versión leída desde `config.toml`**: Eliminada la versión hardcodeada en `defs.py` y en la pantalla de splash. Ahora se lee desde `config/config.toml`.
- **Ventana de login mejorada**: Imágenes de usuario y contraseña, ventana sin borde con fondo translúcido, botón de toggle para mostrar/ocultar contraseña.
- **`modules/estepa.py`**: `close_connection()` envuelto en try/except para evitar bloqueos al cerrar la aplicación.
- **Nombre de usuario en título**: La ventana principal muestra `username - vX.X.X`.

### Fixed
- **SplashScreen no se cerraba**: Eliminado `time.sleep(0.5)` que bloqueaba el event loop de Qt impidiendo que la ventana se cerrara correctamente.
- **Imports eliminados**: Removidos `bcrypt` y `mysql.connector` que causaban errores si no estaban instalados.

### Removed
- Eliminado `update_tomls.py` (script obsoleto).

## [2.6.0] - 2026-07-13
### Added
- **`get_plot_parameters()` en `common.py`**: Nueva función que construye el diccionario `plot_parameters` a partir de datos de medición y configuración TOML. Soporta gráficas con series múltiples (step variable).
- **Sección `[plot]` en TOML de tests**: Todos los ficheros de configuración de tests ahora incluyen parámetros de visualización (`X_VARIABLE`, `Y1_VARIABLE`, `Y2_VARIABLE`, etiquetas, unidades, `SHOW_GRID`, `LEGEND`, etc.).
- **Tests automatizados en `release.py`**: El script de release ejecuta `pytest` automáticamente antes de proceder con el commit y push.

### Changed
- **Claves de output en mayúsculas**: Los TOML de tests ahora usan `SEPARATOR`, `PREFIX`, `VARIABLES` (con fallback a minúsculas para compatibilidad).
- **Refactorización de grid en gráficas**: Lógica más clara para activar/desactivar grid en ejes X, Y e Y2 en `main.py`.
- **Validación mejorada en `parameters_config()`**: Verifica selección de instrumento y test antes de abrir parámetros; mensajes de error más descriptivos.
- **Parámetros de sesión actualizados** en `config.toml` (proceso 19998, wafer 7, máscara CNM004).

### Fixed
- **Símbolos en `plots.py`**: Corregido acceso a `symbols_default` usando índices individuales en lugar del array completo.
- **Acceso a variables en `wafers.py`**: Añadida validación robusta antes de acceder a `variables["params"]` y `plot_parameters`.
- **Movimiento de prober**: Añadido `move_chuck_xy` después de `calculate_init_prober_movement()` para asegurar el movimiento real al chuck.

### Removed
- Eliminados ficheros obsoletos: `Keithley_2470/IV_temp.toml`, `Keithley_2470/IV_temp_test.py`, `Keithley_4200/CVKeithley_test.py`, y tests de `Keysight_B1500` (`IV_2_SMUS`, `IV_4_SMUS`, `SOLARMEMS`, `SOLARMEMS_graph`).

## [2.5.1] - 2026-05-25
### Added
- **Mejoras en gráfica**: Añadimos un segundo eje para las gráficas que fallaba en CV (Keysight E4990A). Problemas eje y2 solucionado.

## [2.5.0] - 2026-05-22
### Added
- **Rendimiento en navegación por secciones**: Implementado sistema de contenedores (`_section_container_cache`) que cachea cada sección en un `QWidget`. Al navegar, se intercambia el contenedor completo (`addWidget`/`removeWidget`) en lugar de reconstruir los 5625 botones individualmente. La primera navegación a una sección tarda ~1.4s, las siguientes ~0.06s.
- **Lectura de `max_visible_buttons` desde configuración en `DrawWafer`**: El método `DrawWafer` ahora lee `max_visible_buttons` del archivo `config.toml` (como ya hacía `view_wafermap`), garantizando que la división en secciones sea idéntica al crear y al recargar un mapa de oblea.

### Fixed
- **Highlight de init/end chip entre secciones**: `total_meas()` ahora sincroniza los estados `meas`/`meas_selected` en `all_buttons_states` para **todas** las coordenadas (no solo las visibles). Al navegar a otra sección, los botones restaurados desde caché mantienen el color correcto del rango init/end chip.
- **MarkAll ahora marca todas las secciones**: `MarkAll` actualiza `all_buttons_states` completo cambiando `in` → `meas` en todas las coordenadas, refleja los cambios visualmente en la sección actual, y establece init_chip=1 y end_chip=total_meas.
- **UnmarkAll ahora desmarca todas las secciones**: `UnmarkAll` actualiza `all_buttons_states` completo poniendo todo lo no-`out` como `in`, refleja cambios visualmente, y establece init_chip=1 y end_chip=0.

### Removed
- Eliminados prints de perfilado `[PERF]` de `add_die_buttons` y `_refresh_display`.

## [2.4.0] - 2026-05-20
### Added
- **common.py**: Se ha añadido la función save_results_to_file() para guardar los resultados de los tests. Se ha añadido la función build_results_folder() para construir la carpeta de resultados.
- **Añadir nuevos tests**: Añadidos tests unitarios para validar la gestión de resultados y funcionamiento de common.py.
- **Generación de documentación**: Se ha añadido documentación en formato Markdown dentro de la carpeta docs para uso futuro. Fichero SaveResultsDoc.md para explicar la gestión de resultados (sustituimos rutina de main.py save_lists_to_txt() que se mantiene de momento). Fichero Testing.md para explicar la suite de tests unitarios.

## [2.3.0] - 2026-05-19
### Added
- **Testing Framework**: Suite completa de tests unitarios en `tests/` para validar el módulo de estadísticas y gestión de archivos.
- **Test B1500**: Implementado test para el instrumento B1500. Modificación función dataready driver LAN. Test_test.py preparado para leer datos del B1500, guardar ficheros.

## [2.2.2] - 2026-02-13
### Changed
- **MES_FILE_test.py**: Se ha actualizado el test. Problemas con multitest y variable MEASUREMENT_STATUS.
- **HP_4155_instrument.py**: Se ha actualizado el driver del instrumento. Añadido sleep 1s despues de guardar datos.

## [2.2.1] - 2026-02-13
### Added
- **Configuration Reloading**: Recarga automática e inmediata de la configuración de instrumentos y probers al guardar cambios en la interfaz.

## [2.2.0] - 2026-02-13
### Added
- **Global Temperature Control**: Soporte para ejecutar tests (simples y cartográficos) a múltiples temperaturas definidas en la configuración del prober.
- Helper `wait_for_temperature` en `main.py` para asegurar la estabilidad térmica antes de medir.
- Parámetro `temperature_timeout` configurable en `probers.toml` (por defecto 300s).
- Simulación de temperatura en el driver `CNM_TEST_prober` para facilitar el desarrollo y pruebas.

### Changed
- Las unidades de temperatura ahora se muestran explícitamente como **°C**.
- El valor por defecto de `min_temperature` para probers se ha actualizado a **-40 °C**.
- Automatización del bucle cartográfico: se suprimen las confirmaciones de usuario (Home, Start) después de la primera temperatura.
- Al iniciar un test con control de temperatura, se solicita confirmación explícita al usuario para evitar ejecuciones accidentales.

## [2.1.1] - 2026-02-12
### Added
- Nuevo test de anillo para Keysight E4990A: `CV_IV_ring_external_test.py`.
- Soporte dinámico para instrumentos fuente (**Keithley 2470** o **2410**) en todos los tests externos de CV-IV (**HP 4192A** y **Keysight E4990A**).
- Método `config_IV` en el driver de `Keithley_2410` para compatibilidad de API.
- Parámetro `SOURCE_INSTRUMENT` en ficheros de configuración TOML.

### Changed
- Refactorización de tests externos unificando la lógica para diferentes modelos de Keithley y eliminando archivos redundantes.

## [2.1.0] - 2026-02-05
### Added
- Implementación inicial de mediciones CV e IV con diferentes instrumentos (HP4192A, HP4155 y K2470).
- Funciones para lectura y control de ficheros de wafers y subconjuntos.
- Soporte para pruebas externas de IV y CV-IV.
- Configuración inicial mediante `config/config.toml`.
- Interfaz de comandos para ejecutar tests de instrumentación.

### Changed
- Estructura de carpetas organizada para proyectos de caracterización eléctrica.
- Código base refactorizado para soportar nuevas funcionalidades de medición y logging.

### Fixed
- Correcciones menores en la lectura de ficheros de medición y drivers de instrumentos.
