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

    # Algunas expresiones contienen nan o zoo dentro de un resultado mayor.
    try:
        if valor.has(sp.nan) or valor.has(sp.zoo):
            return True
    except Exception:
        pass

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

        if es_indeterminado(resultado):
            return None

        return resultado
    except Exception:
        return None


def limites_laterales_iguales(lim_izq, lim_der):
    """Comprueba si ambos limites laterales representan el mismo resultado."""
    if lim_izq is None or lim_der is None:
        return False

    # Esta comparacion directa permite reconocer casos como oo == oo.
    if lim_izq == lim_der:
        return True

    try:
        return sp.simplify(lim_izq - lim_der) == 0
    except Exception:
        return False


def calcular_limite_propio(expresion, h_val):
    """
    Construye una explicacion del procedimiento utilizado para calcular el limite.
    Retorna (resultado_final, explicacion).
    """
    explicacion = []
    resultado_final = None

    # Primero se utiliza el metodo mas simple: reemplazar x directamente por h.
    explicacion.append("Sustitución directa")
    explicacion.append("")
    explicacion.append(f"Se reemplaza x por {h_val} en la funcion.")
    resultado, exito = sustitucion_directa(expresion, h_val)

    if exito:
        explicacion.append(f"El resultado obtenido es {resultado}.")
        explicacion.append("")
        explicacion.append("Como no aparece una indeterminación,")
        explicacion.append("ese valor corresponde al límite.")
        return resultado, explicacion

    explicacion.append("La sustitución produce una indeterminación.")
    explicacion.append("")
    explicacion.append("Transformaciones algebraicas")
    explicacion.append("")
    explicacion.append("Se intenta simplificar la función para")
    explicacion.append("eliminar la indeterminación encontrada.")
    transformaciones = aplicar_algebra(expresion)

    # Se prueban las transformaciones una por una hasta encontrar un resultado.
    for nombre, expresion_transformada in transformaciones:
        resultado, exito = sustitucion_directa(expresion_transformada, h_val)
        if exito:
            explicacion.append(f"Método utilizado: {nombre}.")
            explicacion.append(f"Expresión obtenida: {expresion_transformada}")
            explicacion.append(f"Resultado al reemplazar: {resultado}")
            resultado_final = resultado
            break

    explicacion.append("")
    explicacion.append("Verificación con límites laterales")
    explicacion.append("")
    lim_izq = limite_lateral(expresion, h_val, "-")
    lim_der = limite_lateral(expresion, h_val, "+")
    explicacion.append(f"Por la izquierda: {lim_izq}")
    explicacion.append(f"Por la derecha: {lim_der}")

    if lim_izq is not None and lim_der is not None:
        # Un limite existe solamente cuando ambos lados llegan al mismo valor.
        if limites_laterales_iguales(lim_izq, lim_der):
            explicacion.append("")
            explicacion.append("Ambos lados entregan el mismo valor,")
            explicacion.append("por lo tanto el límite existe.")
            resultado_final = lim_izq
        else:
            explicacion.append("")
            explicacion.append("Los resultados laterales son diferentes,")
            explicacion.append("por lo tanto el límite no existe.")
            return None, explicacion

    return resultado_final, explicacion
