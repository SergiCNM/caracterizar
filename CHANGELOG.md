# Changelog

Todos los cambios importantes en este proyecto se documentan en este archivo.

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
