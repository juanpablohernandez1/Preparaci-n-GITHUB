# Seguridad y privacidad

Este repositorio está pensado para **documentación y reproducibilidad académica**.

## Qué NO debe subirse a GitHub
- Credenciales de Salesforce (OAuth client secret, refresh token, passwords).
- Archivos `.env` o cualquier token.
- Exportaciones reales de cuentas (CSV/XLSX) con datos personales o comerciales sensibles.
- Parquets/CSVs masivos de clientes.

## Qué SÍ se versiona aquí
- Notebooks con el flujo metodológico (sin datos reales embebidos).
- Código fuente para construir corpus y ejecutar matching **sobre datos locales**.
- Documentación, referencias y resultados agregados (porcentajes) obtenidos del avance.

Si accidentalmente se subió un secreto: **revocar/rotar credenciales** y borrar el historial (BFG/git filter-repo).
