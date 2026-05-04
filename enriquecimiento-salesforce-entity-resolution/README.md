# Enriquecimiento de cuentas en Salesforce mediante *entity resolution* (fuentes oficiales)

Repositorio académico para el reto de monografía: integración de **ciencia de datos**
(limpieza, corpus, similitud de texto, evaluación por umbrales) con un problema real de
**calidad de datos en CRM**.

## Problema (rúbrica: descripción del problema)
En organizaciones B2B, el CRM (Salesforce) concentra la cartera, pero frecuentemente faltan campos
estructurados críticos (**NIT**, **CIIU**, **industria/sector**) o están inconsistentes. Esto limita
segmentación comercial, reporting y analítica.

## Enfoque (rúbrica: desarrollo temático + relación con analítica/CD)
Se implementa un pipeline reproducible (CRISP-DM) que:
1. Construye un **corpus de referencia** unificado a partir de fuentes oficiales.
2. Aplica **lookup exacto por NIT** cuando existe.
3. Aplica **matching por nombre** con **TF‑IDF (char n‑grams) + similitud coseno** cuando no hay NIT.
4. Separa resultados por **umbrales de confianza** (auto vs revisión manual).

## Resultados (resumen cuantitativo del avance; agregados, sin datos crudos)
> Fuente: avance de monografía (PDF) + piloto sobre *Cuentas totales IAC*.

- **Cuentas únicas evaluadas**: 10,246
- **Actualización automática (alta confianza)**: 2,164 (**21.1%**)
  - **NIT exacto**: 870 (**8.5%**)
  - **TF‑IDF automático (≥ 0.85)**: 1,294 (**12.6%**)
- **Revisión manual (0.70–0.84)**: 1,399 (**13.7%**)
- **Sin match (<0.70)**: 6,683 (**65.2%**)
- **Corpus unificado**: 30,375 empresas únicas (deduplicadas por NIT)
- **Contribución por fuente (solo cuentas actualizadas automáticamente)**:
  - **10k grandes (Datos.gov.co)**: 1,591 (**73.5%**)
  - **Pymes (Supersociedades)**: 530 (**24.5%**)
  - **Plenas (Supersociedades)**: 43 (**2.0%**)
- **Scores TF‑IDF automático (n=1,294)**: min=0.8500, max=1.0000, mean=0.9762

## Estructura del repositorio
```
notebooks/   # EDA + corpus + matching + evaluación (entregable principal)
src/         # Funciones reutilizables (sin rutas personales hardcodeadas)
docs/        # Documentación y referencias (APA sugerida)
config/      # Plantillas de configuración (sin secretos)
data/        # Solo README (los datos van local)
```

## Cómo ejecutar (local)
1. Crear un entorno virtual e instalar dependencias:
   - `pip install -r requirements.txt`
2. Colocar **localmente** (no en git) los XLSX oficiales y el export de cuentas.
3. Abrir `notebooks/01_diagnostico_y_plan.ipynb` y seguir el flujo.

## Referencias (APA sugerida; ver `docs/referencias.md`)
- Superintendencia de Sociedades — descarga SIIS.
- Datos.gov.co — dataset “10.000 empresas más grandes de Colombia”.
- Salton & McGill (1983) — fundamentos de recuperación de información / TF‑IDF.

## Alineación con la rúbrica (imagen)
Este README y los notebooks están organizados para cubrir explícitamente:
- claridad y coherencia interna,
- tratamiento de fuentes,
- desarrollo temático,
- integración CD/analítica,
- citación (en `docs/referencias.md`).
