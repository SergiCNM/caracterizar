# Changelog

Todos los cambios importantes en este proyecto se documentan en este archivo.

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
