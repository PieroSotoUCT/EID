================================================================================
  ANALIZADOR Y VISUALIZADOR DE LÍMITES
  MATE1133 — Universidad Católica de Temuco
================================================================================

DESCRIPCIÓN
--------------------------------------------------------------------------------
Aplicación de escritorio desarrollada en Python para el cálculo simbólico y
visualización gráfica de límites matemáticos. El programa permite al usuario
ingresar una función f(x) y un valor de tendencia h, y retorna el resultado del
límite junto con el desarrollo paso a paso del algoritmo utilizado.

Soporta límites bilaterales, laterales por izquierda y por derecha, incluyendo
tendencias hacia el infinito positivo y negativo.


ESTRUCTURA DEL PROYECTO
--------------------------------------------------------------------------------
  limites.py    Módulo matemático. Contiene toda la lógica de cálculo de
                límites utilizando SymPy: sustitución directa, transformaciones
                algebraicas y cálculo de límites laterales.

  main.py       Módulo de interfaz gráfica. Gestiona la ventana principal,
                los campos de entrada, el selector de dirección, la visualización
                de resultados y el gráfico generado con Matplotlib.


REQUISITOS
--------------------------------------------------------------------------------
  Python         3.10 o superior
  sympy          Cálculo simbólico
  customtkinter  Interfaz gráfica moderna
  matplotlib     Visualización de funciones

  Instalación de dependencias:
      pip install sympy customtkinter matplotlib


EJECUCIÓN
--------------------------------------------------------------------------------
  python main.py


FUNCIONALIDADES
--------------------------------------------------------------------------------
  1. Cálculo de límites por sustitución directa
     Intenta resolver el límite reemplazando x por h directamente.

  2. Transformaciones algebraicas automáticas
     En caso de indeterminación (0/0, ∞/∞), aplica factorización, cancelación,
     expansión y simplificación trigonométrica hasta resolver el límite.

  3. Límites laterales
     El usuario puede seleccionar la dirección del límite mediante un menú
     desplegable con tres opciones:
       - Bilateral     : evalúa el límite desde ambos lados (comportamiento
                         predeterminado).
       - Izquierda (−) : evalúa el límite cuando x se aproxima a h por valores
                         menores.
       - Derecha (+)   : evalúa el límite cuando x se aproxima a h por valores
                         mayores.

  4. Límites al infinito
     Escribir "oo" en el campo de tendencia evalúa el límite cuando x → +∞.
     Escribir "-oo" evalúa el límite cuando x → −∞.

  5. Visualización gráfica
     Se genera un gráfico de f(x) en el entorno de h, con marcadores para la
     asíntota vertical y el valor del límite cuando corresponde.

  6. Desarrollo del algoritmo
     Se muestra en pantalla cada paso ejecutado: qué método se intentó, si hubo
     indeterminación, qué transformación resolvió el límite y la verificación
     con límites laterales.


SINTAXIS DE ENTRADA
--------------------------------------------------------------------------------
  La función debe ingresarse con sintaxis Python/SymPy:

    Potencias          x**2         (equivale a x²)
    Multiplicación     2*x          (el operador * es obligatorio)
    Seno               sin(x)
    Coseno             cos(x)
    Logaritmo natural  log(x)
    Valor absoluto     Abs(x)
    Fracción           (x**2 - 1)/(x - 1)

  Ejemplos válidos:
    (x**2 - 1)/(x - 1)         con h = 1
    Abs(x)/x                   con h = 0
    (2*x**2 + 5)/(3*x**2 + 1)  con h = oo
    1/(x - 2)                  con h = 2


CASOS DE PRUEBA RECOMENDADOS
--------------------------------------------------------------------------------
  Función                        h       Dirección      Resultado esperado
  ---------------------------    -----   -----------    --------------------
  (x**2 - 1)/(x - 1)            1       Bilateral      2
  Abs(x)/x                       0       Derecha (+)    1
  Abs(x)/x                       0       Izquierda (−)  -1
  Abs(x)/x                       0       Bilateral      No existe
  1/(x - 2)                      2       Derecha (+)    oo
  1/(x - 2)                      2       Izquierda (−)  -oo
  (2*x**2 + 5)/(3*x**2 + 1)     oo      Bilateral      2/3
  sin(x)/x                       0       Bilateral      1


NOTAS TÉCNICAS
--------------------------------------------------------------------------------
  - El gráfico se construye sin NumPy, utilizando un ciclo de iteración manual
    sobre el intervalo [h−5, h+5] con 400 puntos de muestreo.
  - Las discontinuidades se detectan comparando el valor absoluto de f(x) contra
    un umbral de 1×10⁶ y se representan como cortes en la curva.
  - Para límites al infinito, el centro visual del gráfico se fija en x = 0.
  - SymPy maneja internamente los casos en que el límite lateral diverge hacia
    oo o -oo, los cuales se muestran correctamente en el resultado.


================================================================================
