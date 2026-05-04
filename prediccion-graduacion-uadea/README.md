# Predicción de Graduación — Universidad de Antioquia

Modelos de red neuronal para predecir la probabilidad de que un estudiante admitido se gradúe del mismo programa en el que se inscribió.

## Archivos necesarios

- `graduados.csv` — registros de egresados
- `matriculados.csv` — registros de inscripciones

## Notebook

`prediccion_graduacion.ipynb` — contiene el pipeline completo: limpieza, encoding, entrenamiento y evaluación de dos modelos:

- **Exp A — MLP:** red densa sobre el vector de features OHE + numéricas
- **Exp B — Multimodal:** mismo vector + embedding aprendido para el código de programa (AUC = 0.77)

## Dependencias

```
tensorflow
scikit-learn
imbalanced-learn
pandas
numpy
matplotlib
```

## Integrantes

- Camilo Valencia
- Angel Rey
