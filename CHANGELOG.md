# Changelog

Todos los cambios importantes en este proyecto se documentan en este archivo.

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
