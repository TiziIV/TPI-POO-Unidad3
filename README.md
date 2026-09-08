# Trabajo Práctico Integrador — Unidad 3: Programación Orientada a Objetos (De Java a Python)

**Carrera:** Tecnicatura Universitaria en Programación — UTN FRM  
**Materia:** Programación IV / POO  
**Integrantes:** Tiziano Valentini y Juan Martín García

---

## 1. Descripción del Proyecto

Este proyecto aborda la migración y refactorización de un modelo orientado a objetos del dominio `Figura` / `Poligono` / `Lado` originado en Java hacia un diseño idiomático en Python. Se aplican los principios de:
* Encapsulamiento por convención frente al control estático.
* Descriptores `@property` frente a getters/setters artificiales.
* Relaciones estructurales definidas por el ciclo de vida (Composición, Agregación, Asociación) y copia defensiva.
* Contratos explícitos mediante Clases Abstractas (`abc.ABC`) frente a contratos estructurales desacoplados vía Duck Typing (`typing.Protocol`).

---

## 2. Estructura del Repositorio

| Archivo / Carpeta | Descripción técnica |
|---|---|
| `figuras.py` | Dominio completo refactorizado (Partes 1 a 4). Contiene la jerarquía `Figura`/`Poligono`, `Lado`, `Etiqueta` (`@dataclass(frozen=True)`), `Taller`, `FactoriaPoligonoRegular` y el protocolo estructural `Exportable`. |
| `parte1_diagnostico.py` | Código inicial refactorizado y saneado de los 8 Java-ismos de diseño y del ruido sintáctico. |
| `parte1_diagnostico_Original.py` | Copia de respaldo del código de partida con la ceremonia de Java intacta para análisis comparativo. |
| `demo_sintomas.py` | Script que demuestra empíricamente la manifestación de fallas antes de corregir (default mutable compartido y aliasing de colecciones), además del acceso transparente con `@property`. |
| `libreria_externa.py` | Módulo de un tercero (`PlanoCAD`). Se mantiene sin modificar para validar el contrato estructural mediante `Protocol`. |
| `main.py` | Script de demostración integrador. Prueba el taller, el ciclo de vida de composición/agregación, la exportación conjunta y la falla temprana en instanciación. |
| `informe.md` | Documentación técnica: tabla de 8 Java-ismos, tabla de equivalencias Java-Python y justificación de decisiones de arquitectura. |
| `mypy.ini` | Configuración del linter estático de tipos. |
| `uml/modelo_final.md` | Diagrama de clases final en formato Mermaid, reflejando las relaciones de agregación, composición, asociación y contratos estructurales. |
| `tests/test_tpi.py` | Suite de 6 pruebas unitarias automatizadas con `pytest` que verifican las invariantes del modelo. |

---

## 3. Decisiones Clave de Arquitectura

1. **Rediseño de `PoligonoRegular` (Parte 3):** Se eliminó la relación de herencia artificial `PoligonoRegular extends Poligono`, la cual existía únicamente por restricciones de tipado del compilador de Java. En su lugar, se adoptó una fábrica estática (`FactoriaPoligonoRegular`) que construye las subclases de dominio concretas (`Triangulo`, `Cuadrado`, etc.) garantizando lados de igual longitud.
2. **`ABC` vs. `Protocol` (Parte 4):** Se utilizó `abc.ABC` para la relación ontológica de jerarquía (`Triangulo` *es-un* `Poligono`) forzando la implementación de `lados_esperados()`. Por el contrario, se definió `Exportable` como `typing.Protocol` para permitir que `PlanoCAD` (código cerrado de un tercero) cumpla el contrato de exportación en runtime sin acoplamiento por herencia.
3. **Ciclo de Vida y Copia Defensiva (Parte 2):**
  * **Composición (`Poligono` → `Lado`):** `Poligono` construye copias defensivas independientes de los lados recibidos.
  * **Agregación (`Taller` → `Poligono`):** `Taller` recibe objetos polígonos externos; su destrucción no afecta la existencia de las figuras.
  * **Asociación (`Lado` → `Etiqueta`):** Referencia opcional (0..1) desacoplable.

---

## 4. Instrucciones de Ejecución y Verificación

Asegúrese de contar con las dependencias instaladas en el entorno:
```bash
pip install pytest mypy