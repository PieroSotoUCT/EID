# Analizador y Visualizador de Límites

Proyecto para **MATE1133** de la Universidad Católica de Temuco.

## Descripción

Aplicación de escritorio desarrollada en Python para calcular y visualizar
límites matemáticos. Permite ingresar una función `f(x)`, un valor de tendencia
`h` y la dirección del límite.

La aplicación muestra el resultado, explica el procedimiento utilizado y genera
un gráfico de la función.

## Funciones principales

- Calcula límites bilaterales y laterales por izquierda o derecha.
- Evalúa límites cuando `x` tiende a un punto finito, `oo` o `-oo`.
- Reconoce resultados finitos, límites infinitos y límites que no existen.
- Intenta resolver indeterminaciones mediante transformaciones algebraicas.
- Explica el procedimiento y las aproximaciones utilizadas.
- Grafica funciones, discontinuidades removibles, saltos y asíntotas verticales.
- Mantiene la aplicación abierta y muestra mensajes comprensibles ante errores.

## Estructura del proyecto

| Archivo | Descripción |
| --- | --- |
| `limites.py` | Contiene la lógica matemática, las transformaciones algebraicas y las aproximaciones laterales. |
| `main.py` | Contiene la interfaz gráfica, las validaciones y el gráfico generado con Matplotlib. |

## Requisitos

- Python 3.10 o superior
- SymPy
- CustomTkinter
- Matplotlib

```bash
pip install sympy customtkinter matplotlib
```

## Ejecución

```bash
python main.py
```

## Funcionamiento del algoritmo

### Sustitución directa

Primero se reemplaza `x` por `h`. Aunque la función esté definida en el punto,
el límite bilateral se verifica siempre mediante aproximaciones laterales.

### Transformaciones algebraicas

Cuando aparece una indeterminación, SymPy se utiliza como apoyo para intentar
factorización, cancelación, expansión y simplificación trigonométrica.

### Aproximaciones mediante ciclos

Los límites laterales se calculan sin utilizar `sympy.limit()`.

Para un punto finito, el programa genera valores cada vez más cercanos a `h`:

```text
Izquierda: h - 0.1, h - 0.01, h - 0.001...
Derecha:   h + 0.1, h + 0.01, h + 0.001...
```

Para límites al infinito, evalúa valores cuyo tamaño aumenta progresivamente.
Luego analiza si los resultados convergen, crecen hacia infinito o no se
estabilizan. La tolerancia utilizada para comparar aproximaciones es `0.0001`.

El algoritmo también analiza secuencias que se acercan lentamente a cero,
crecimientos sostenidos hacia infinito y funciones definidas solamente por uno
de los lados.

### Direcciones disponibles

- **Bilateral:** compara las aproximaciones por izquierda y derecha.
- **Izquierda (-):** estudia solamente valores menores que `h`.
- **Derecha (+):** estudia solamente valores mayores que `h`.

Para infinito positivo se escribe `oo` y para infinito negativo se escribe
`-oo`.

## Visualización gráfica

La gráfica adapta su rango según el valor de tendencia ingresado. Para límites
al infinito muestra valores alejados de cero, permitiendo observar el
comportamiento final de la función.

- Una línea vertical indica el valor `h`.
- Un punto verde lleno representa un límite que coincide con `f(h)`.
- Un punto verde vacío representa una discontinuidad removible.
- Los saltos y valores indefinidos separan la curva para evitar líneas falsas.
- Las asíntotas verticales conservan visualmente su crecimiento.

## Sintaxis de entrada

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

El operador de multiplicación `*` es obligatorio:

```text
sin(5*x)  correcto
sin(5x)   incorrecto
```

## Manejo de errores

La aplicación utiliza validaciones y bloques `try-except` para evitar cierres
inesperados. Muestra mensajes específicos cuando falta completar un campo, la
función tiene sintaxis incorrecta, `h` no es válido, falla el gráfico o falta
instalar una librería requerida.

Cuando existe un error de entrada, también se limpia el gráfico anterior para
evitar que el usuario lo confunda con el resultado actual.

## Casos de prueba

| Función | `h` | Dirección | Resultado esperado |
| --- | ---: | --- | --- |
| `(x**2 - 1)/(x - 1)` | `1` | Bilateral | `2` |
| `sin(5*x)/(x-sin(2*x))` | `0` | Bilateral | `-5` |
| `Abs(x)/x` | `0` | Bilateral | No existe |
| `1/(x - 2)` | `2` | Derecha (+) | `oo` |
| `1/(x - 2)` | `2` | Izquierda (-) | `-oo` |
| `sin(1/x)` | `0` | Bilateral | No existe |
| `(3*x**3-x)/(2*x**3+5)` | `oo` | Bilateral | `3/2` |
| `sqrt(x)` | `0` | Derecha (+) | `0` |
| `log(x)` | `0` | Derecha (+) | `-oo` |
| `exp(x)` | `oo` | Bilateral | `oo` |
| `(1 + 1/x)**x` | `oo` | Bilateral | Aproximadamente `2.718282` |

## Notas técnicas

- No se utiliza NumPy.
- Los puntos del gráfico se generan mediante ciclos.
- SymPy se usa para variables simbólicas, sustitución y manipulación algebraica.
- El cálculo lateral se realiza mediante aproximaciones programadas por el equipo.
- No se utiliza la función directa `sympy.limit()`.
- Las constantes irracionales pueden mostrarse como aproximaciones decimales.
- Algunas funciones de convergencia extremadamente lenta podrían no ser
  reconocidas por el método numérico.
