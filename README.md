# Enriquecimiento de Cuentas en Salesforce — IAC

Sistema de entity resolution para enriquecer cuentas de Salesforce con datos oficiales colombianos (Supersociedades, RUES).

## Problema

IAC tiene cuentas en Salesforce con campos de NIT, CIIU, sector e industria vacíos o incorrectos. Este proyecto cruza las cuentas contra fuentes oficiales colombianas gratuitas para completar esos campos automáticamente.

## Cómo funciona

El sistema usa dos rutas de matching:

1. **NIT exacto** — si la cuenta tiene NIT, busca directamente en el corpus. Score = 1.0.
2. **Similitud de texto (TF-IDF)** — si no tiene NIT, normaliza el nombre y lo compara contra el corpus usando n-gramas de caracteres con similitud coseno.

### Umbrales de decisión

| Score | Acción |
|---|---|
| ≥ 0.85 | Actualización automática |
| 0.70 – 0.84 | Cola de revisión manual |
| < 0.70 | Sin match, requiere fuente adicional (RUES) |

## Estructura

```
iac-enrichment/
├── data/
│   ├── raw/           → Archivos fuente (Supersociedades xlsx, exports SF)
│   ├── processed/     → Corpus unificado normalizado (parquet + csv)
│   └── output/        → CSVs y Excel enriquecidos
├── scripts/
│   ├── build_corpus.py         → Une y normaliza las 3 bases de datos
│   ├── enrich_accounts.py      → Motor de matching NIT + TF-IDF
│   ├── run_sf_nit_pilot.py      → Prueba con cuentas SF + NIT
│   ├── run_full_pilot.py        → Prueba con corpus de 3 fuentes
│   ├── run_totales.py           → Prueba con cuentas totales IAC
│   └── utils.py                 → Funciones compartidas
├── mcp_local/
│   └── diagnostics_server.py
├── requirements.txt
└── README.md
```

## Fuentes de datos (corpus de referencia)

| Fuente | Registros | Contenido |
|---|---|---|
| Supersociedades — Plenas individuales | ~3,100 | Sociedades grandes, NIIF Plenas |
| Supersociedades — Pymes individuales | ~22,700 | Sociedades medianas/pequeñas |
| 10,000 empresas más grandes | ~14,000 | Ranking por ingresos, incluye macrosector |
| **Total corpus único** | **~30,400** | Deduplicado por NIT |

## Resultados del piloto

| Prueba | Cuentas | Matches | % |
|---|---|---|---|
| P1: sin NIT, solo Supersociedades | 1,683 | 383 | 22.8% |
| P2: con NIT, solo Supersociedades | 1,683 | 502 | 29.8% |
| P3: con NIT, 3 fuentes | 1,683 | 740 | 44.0% |

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

```bash
# 1. Construir corpus
python scripts/build_corpus.py

# 2. Enriquecer cuentas
python scripts/enrich_accounts.py --input data/raw/cuentas_sf.csv
```

## Tecnologías

Python · pandas · scikit-learn (TF-IDF) · simple-salesforce · openpyxl · Power BI

## Autor

Juan Pablo Hernández Ortiz — IAC, Ingeniería Asistida por Computador
Especialización en Analítica y Ciencia de Datos, Universidad de Antioquia
