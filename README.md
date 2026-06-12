# Analizador y Visualizador de Límites

Proyecto para **MATE1133** de la Universidad Católica de Temuco.

## Descripción

Aplicación de escritorio desarrollada en Python para el cálculo simbólico y la
visualización gráfica de límites matemáticos.

El programa permite ingresar una función `f(x)` y un valor de tendencia `h`.
Luego muestra el resultado del límite, una explicación del procedimiento y un
gráfico de la función.

Soporta límites bilaterales, laterales por izquierda y derecha, además de
tendencias hacia infinito positivo y negativo.

## Estructura del proyecto

| Archivo | Descripción |
| --- | --- |
| `limites.py` | Contiene la lógica matemática: sustitución directa, transformaciones algebraicas y límites laterales. |
| `main.py` | Contiene la interfaz gráfica, las entradas, los resultados y el gráfico generado con Matplotlib. |

## Requisitos

- Python 3.10 o superior
- SymPy
- CustomTkinter
- Matplotlib

Para instalar las dependencias:

```bash
pip install sympy customtkinter matplotlib
```

## Ejecución

Desde la carpeta del proyecto, ejecutar:

```bash
python main.py
```

## Funcionalidades

### Sustitución directa

El programa intenta resolver primero el límite reemplazando `x` directamente
por el valor de `h`.

### Transformaciones algebraicas

Cuando encuentra una indeterminación, intenta aplicar distintas
transformaciones:

- Factorización
- Cancelación de términos comunes
- Expansión y simplificación
- Simplificación trigonométrica

### Límites laterales

El usuario puede seleccionar la dirección del límite:

- **Bilateral:** evalúa el límite desde ambos lados.
- **Izquierda (-):** aproxima `x` hacia `h` usando valores menores.
- **Derecha (+):** aproxima `x` hacia `h` usando valores mayores.

### Límites al infinito

- Escribir `oo` evalúa el límite cuando `x` tiende a infinito positivo.
- Escribir `-oo` evalúa el límite cuando `x` tiende a infinito negativo.

### Visualización gráfica

La aplicación genera un gráfico de `f(x)` alrededor de `h`. Cuando corresponde,
también muestra el punto del límite y una línea vertical en el valor evaluado.

### Explicación del procedimiento

La interfaz muestra los métodos utilizados, las indeterminaciones encontradas,
las transformaciones aplicadas y la comparación de los límites laterales.

## Sintaxis de entrada

La función debe escribirse utilizando sintaxis de Python y SymPy:

| Operación | Escritura | Ejemplo |
| --- | --- | --- |
| Potencia | `**` | `x**2` |
| Multiplicación | `*` | `2*x` |
| Seno | `sin()` | `sin(x)` |
| Coseno | `cos()` | `cos(x)` |
| Logaritmo natural | `log()` | `log(x)` |
| Raíz cuadrada | `sqrt()` | `sqrt(x)` |
| Valor absoluto | `Abs()` | `Abs(x)` |
| Fracción | `/` | `(x**2 - 1)/(x - 1)` |

El operador de multiplicación `*` es obligatorio. Por ejemplo, se debe escribir
`2*x` y no `2x`.

## Ejemplos de uso

| Función | Valor de `h` | Dirección | Resultado esperado |
| --- | ---: | --- | --- |
| `(x**2 - 1)/(x - 1)` | `1` | Bilateral | `2` |
| `Abs(x)/x` | `0` | Derecha (+) | `1` |
| `Abs(x)/x` | `0` | Izquierda (-) | `-1` |
| `Abs(x)/x` | `0` | Bilateral | No existe |
| `1/(x - 2)` | `2` | Derecha (+) | `oo` |
| `1/(x - 2)` | `2` | Izquierda (-) | `-oo` |
| `(2*x**2 + 5)/(3*x**2 + 1)` | `oo` | Bilateral | `2/3` |
| `sin(x)/x` | `0` | Bilateral | `1` |

## Notas técnicas

- El gráfico se construye sin NumPy, utilizando ciclos para generar los puntos.
- Las discontinuidades se representan como cortes en la curva.
- Para límites al infinito, el centro visual del gráfico se fija en `x = 0`.
- SymPy se utiliza como apoyo para manipular y evaluar expresiones simbólicas.
