from sympy import cancel, expand, factor, limit, simplify, symbols, trigsimp
import sympy as sp


# Este archivo contiene solamente la parte matematica del programa.
# main.py envia la expresion y el valor h, y recibe el resultado y los pasos.

# Variable simbolica usada en todos los calculos.
x = symbols("x")


def es_indeterminado(valor):
    """Determina si un valor simbolico es una indeterminacion."""
    # None significa que algun intento anterior no pudo obtener un valor.
    if valor is None:
        return True

    # nan representa un valor indefinido y zoo una division por cero compleja.
    if valor in [sp.nan, sp.zoo]:
        return True

    # Esta segunda comprobacion cubre resultados que SymPy entrega como texto.
    if str(valor) in ["nan", "zoo"]:
        return True

    return False


def sustitucion_directa(expresion, h_val):
    """
    PASO 1: Intentar sustitucion directa x -> h.
    Retorna (resultado, exito).
    """
    try:
        # Se reemplaza x por h y se simplifica el resultado obtenido.
        resultado = expresion.subs(x, h_val)
        resultado = sp.simplify(resultado)

        # Si aparece una indeterminacion, el algoritmo debe probar otro metodo.
        if es_indeterminado(resultado):
            return None, False

        if resultado in [sp.zoo, sp.nan]:
            return None, False

        return resultado, True
    except Exception:
        return None, False


def aplicar_algebra(expresion):
    """
    PASO 2: Aplicar transformaciones algebraicas con SymPy.
    Retorna una lista de expresiones transformadas para intentar.
    """
    transformaciones = []

    # Cada transformacion se guarda junto a su nombre para mostrarla en pantalla.
    # Los try-except permiten continuar si una tecnica no sirve para la expresion.
    try:
        transformaciones.append(("Factorizacion", factor(expresion)))
    except Exception:
        pass

    try:
        transformaciones.append(("Cancelacion", cancel(expresion)))
    except Exception:
        pass

    try:
        transformaciones.append(
            ("Expansion + Simplificacion", simplify(expand(expresion)))
        )
    except Exception:
        pass

    try:
        transformaciones.append(("Simplif. Trigonometrica", trigsimp(expresion)))
    except Exception:
        pass

    return transformaciones


def limite_lateral(expresion, h_val, direccion):
    """
    PASO 3: Calcular limite lateral (izquierda o derecha).
    direccion: "+" o "-"
    """
    # Esta funcion sera reemplazada por aproximaciones hechas con ciclos.
    # Por ahora se conserva para mantener el funcionamiento del primer avance.
    try:
        resultado = limit(expresion, x, h_val, direccion)
        return resultado
    except Exception:
        return None


def calcular_limite_propio(expresion, h_val):
    """
    Construye el calculo del limite paso a paso.
    Retorna (resultado_final, pasos_realizados).
    """
    pasos = []
    resultado_final = None

    # Primero se utiliza el metodo mas simple: reemplazar x directamente por h.
    pasos.append("PASO 1: Sustitucion directa x -> h")
    resultado, exito = sustitucion_directa(expresion, h_val)

    if exito:
        pasos.append(f"  -> Resultado directo: {resultado}")
        pasos.append("  No hay indeterminacion. Limite obtenido.")
        return resultado, pasos

    pasos.append("  -> Indeterminacion detectada (ej: 0/0, infinito/infinito).")
    pasos.append("  -> Se aplican transformaciones algebraicas.")

    pasos.append("\nPASO 2: Transformaciones algebraicas con SymPy")
    transformaciones = aplicar_algebra(expresion)

    # Se prueban las transformaciones una por una hasta encontrar un resultado.
    for nombre, expresion_transformada in transformaciones:
        pasos.append(f"  -> Intentando: {nombre}")
        resultado, exito = sustitucion_directa(expresion_transformada, h_val)
        if exito:
            pasos.append(f"  Exito con {nombre}. Resultado: {resultado}")
            resultado_final = resultado
            break
        else:
            pasos.append(f"    Aun indeterminado despues de {nombre}.")

    pasos.append("\nPASO 3: Verificacion con limites laterales")
    lim_izq = limite_lateral(expresion, h_val, "-")
    lim_der = limite_lateral(expresion, h_val, "+")
    pasos.append(f"  -> Limite por la izquierda: {lim_izq}")
    pasos.append(f"  -> Limite por la derecha: {lim_der}")

    if lim_izq is not None and lim_der is not None:
        # Un limite existe solamente cuando ambos lados llegan al mismo valor.
        if sp.simplify(lim_izq - lim_der) == 0:
            pasos.append("  Limites laterales iguales. El limite existe.")
            resultado_final = lim_izq
        else:
            pasos.append("  Limites laterales distintos. El limite no existe.")
            resultado_final = None

    if resultado_final is None and lim_izq is not None:
        resultado_final = lim_izq

    return resultado_final, pasos
