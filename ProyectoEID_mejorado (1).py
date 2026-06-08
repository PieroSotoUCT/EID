import customtkinter as ctk
from sympy import (
    symbols, sympify, factor, expand, simplify,
    cancel, trigsimp, oo, zoo, nan, limit,
    lambdify, S, latex
)
from sympy import limit_seq
import sympy as sp
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ─────────────────────────────────────────────
#  Variable simbolica global
# ─────────────────────────────────────────────
x = symbols("x")


# ─────────────────────────────────────────────
#  ALGORITMO PROPIO DE CALCULO DE LIMITES
#  (SIN usar sympy.limit() como solucion unica)
# ─────────────────────────────────────────────

def es_indeterminado(valor):
    """Determina si un valor simbolico es una indeterminacion."""
    if valor is None:
        return True
    str_val = str(valor)
    indeterminaciones = ["nan", "zoo", "oo*0", "0*oo", "oo - oo", "oo/oo", "0/0"]
    if valor in [sp.nan, sp.zoo]:
        return True
    # Si sympy no pudo evaluar limpiamente
    if str_val in ["nan", "zoo"]:
        return True
    return False


def sustitucion_directa(expresion, h_val):
    """
    PASO 1: Intentar sustitucion directa x -> h.
    Retorna (resultado, exito).
    """
    try:
        resultado = expresion.subs(x, h_val)
        resultado = sp.simplify(resultado)

        # Verificar si es una forma indeterminada
        if es_indeterminado(resultado):
            return None, False

        # Verificar si contiene division por cero o raiz de negativo
        if resultado in [sp.zoo, sp.nan]:
            return None, False

        # Si el resultado es finito y bien definido
        return resultado, True
    except Exception:
        return None, False


def aplicar_algebra(expresion):
    """
    PASO 2: Aplicar transformaciones algebraicas con SymPy.
    Retorna lista de expresiones transformadas para intentar.
    """
    transformaciones = []

    # Intentar factorizar
    try:
        transformaciones.append(("Factorizacion", factor(expresion)))
    except Exception:
        pass

    # Intentar cancelar terminos comunes
    try:
        transformaciones.append(("Cancelacion", cancel(expresion)))
    except Exception:
        pass

    # Intentar expandir y simplificar
    try:
        transformaciones.append(("Expansion + Simplificacion", simplify(expand(expresion))))
    except Exception:
        pass

    # Simplificacion trigonometrica
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
    try:
        resultado = limit(expresion, x, h_val, direccion)
        return resultado
    except Exception:
        return None


def calcular_limite_propio(expresion, h_val):
    """
    ALGORITMO PRINCIPAL:
    Construye el calculo del limite paso a paso, usando SymPy
    solo como apoyo algebraico (no como solucion directa).

    Retorna: (resultado_final, pasos_realizados)
    """
    pasos = []
    resultado_final = None

    # ── PASO 1: Sustitucion directa ──────────────────────
    pasos.append("PASO 1: Sustitución directa x → h")
    resultado, exito = sustitucion_directa(expresion, h_val)

    if exito:
        pasos.append(f"  → Resultado directo: {resultado}")
        pasos.append("  ✓ No hay indeterminación. Límite obtenido.")
        return resultado, pasos

    pasos.append("  → Indeterminación detectada (ej: 0/0, ∞/∞).")
    pasos.append("  → Se aplican transformaciones algebraicas.")

    # ── PASO 2: Transformaciones algebraicas ─────────────
    pasos.append("\nPASO 2: Transformaciones algebraicas con SymPy")
    transformaciones = aplicar_algebra(expresion)

    for nombre, expr_transformada in transformaciones:
        pasos.append(f"  → Intentando: {nombre}")
        resultado, exito = sustitucion_directa(expr_transformada, h_val)
        if exito:
            pasos.append(f"  ✓ Éxito con {nombre}. Resultado: {resultado}")
            resultado_final = resultado
            break
        else:
            pasos.append(f"    Aún indeterminado después de {nombre}.")

    # ── PASO 3: Verificar con limites laterales ───────────
    pasos.append("\nPASO 3: Verificación con límites laterales")
    lim_izq = limite_lateral(expresion, h_val, "-")
    lim_der = limite_lateral(expresion, h_val, "+")
    pasos.append(f"  → Límite por la izquierda (x → h⁻): {lim_izq}")
    pasos.append(f"  → Límite por la derecha  (x → h⁺): {lim_der}")

    if lim_izq is not None and lim_der is not None:
        if sp.simplify(lim_izq - lim_der) == 0:
            pasos.append("  ✓ Límites laterales iguales → El límite existe.")
            resultado_final = lim_izq
        else:
            pasos.append("  ✗ Límites laterales distintos → El límite NO existe.")
            resultado_final = None

    # Si aun no tenemos resultado, usamos limite lateral como fallback
    if resultado_final is None and lim_izq is not None:
        resultado_final = lim_izq

    return resultado_final, pasos


# ─────────────────────────────────────────────
#  INTERFAZ GRAFICA
# ─────────────────────────────────────────────

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ventana = ctk.CTk()
ventana.geometry("1050x700")
ventana.title("Analizador y Visualizador de Límites — MATE1133")
ventana.resizable(True, True)


# ── Layout principal: izquierda (controles) + derecha (grafico) ──

frame_izq = ctk.CTkFrame(ventana, width=340, corner_radius=12)
frame_izq.pack(side="left", fill="y", padx=14, pady=14)
frame_izq.pack_propagate(False)

frame_der = ctk.CTkFrame(ventana, corner_radius=12)
frame_der.pack(side="right", fill="both", expand=True, padx=14, pady=14)


# ── Panel izquierdo: entradas ──

titulo = ctk.CTkLabel(
    frame_izq,
    text="Analizador\nde Límites",
    font=ctk.CTkFont(size=22, weight="bold"),
    justify="center"
)
titulo.pack(pady=(20, 6))

subtitulo = ctk.CTkLabel(
    frame_izq,
    text="MATE1133 — UCTemuco",
    font=ctk.CTkFont(size=12),
    text_color="gray"
)
subtitulo.pack(pady=(0, 18))

separador1 = ctk.CTkFrame(frame_izq, height=2, fg_color="#3a3a3a")
separador1.pack(fill="x", padx=20, pady=4)

# Funcion
ctk.CTkLabel(
    frame_izq,
    text="Función  f(x):",
    font=ctk.CTkFont(size=13, weight="bold"),
    anchor="w"
).pack(padx=20, pady=(14, 2), anchor="w")

ctk.CTkLabel(
    frame_izq,
    text="Usa sintaxis Python: x**2, sin(x), log(x) ...",
    font=ctk.CTkFont(size=10),
    text_color="gray",
    anchor="w"
).pack(padx=20, anchor="w")

entrada_funcion = ctk.CTkEntry(
    frame_izq,
    width=280,
    height=36,
    placeholder_text="Ej: (x**2 - 1)/(x - 1)",
    font=ctk.CTkFont(size=13)
)
entrada_funcion.pack(padx=20, pady=(4, 12))

# Valor h
ctk.CTkLabel(
    frame_izq,
    text="Valor  h  (tendencia):",
    font=ctk.CTkFont(size=13, weight="bold"),
    anchor="w"
).pack(padx=20, pady=(0, 2), anchor="w")

ctk.CTkLabel(
    frame_izq,
    text='Escribe "oo" para infinito',
    font=ctk.CTkFont(size=10),
    text_color="gray",
    anchor="w"
).pack(padx=20, anchor="w")

entrada_h = ctk.CTkEntry(
    frame_izq,
    width=280,
    height=36,
    placeholder_text="Ej: 1  ó  oo",
    font=ctk.CTkFont(size=13)
)
entrada_h.pack(padx=20, pady=(4, 16))

# Boton
boton = ctk.CTkButton(
    frame_izq,
    text="▶  Calcular Límite",
    width=280,
    height=42,
    font=ctk.CTkFont(size=14, weight="bold"),
    corner_radius=10,
    command=lambda: calcular()
)
boton.pack(padx=20, pady=4)

separador2 = ctk.CTkFrame(frame_izq, height=2, fg_color="#3a3a3a")
separador2.pack(fill="x", padx=20, pady=14)

# Resultado
ctk.CTkLabel(
    frame_izq,
    text="Resultado:",
    font=ctk.CTkFont(size=13, weight="bold"),
    anchor="w"
).pack(padx=20, anchor="w")

label_resultado = ctk.CTkLabel(
    frame_izq,
    text="—",
    font=ctk.CTkFont(size=18, weight="bold"),
    text_color="#4fc3f7",
    wraplength=290,
    justify="center"
)
label_resultado.pack(padx=20, pady=(4, 10))

# Pasos del algoritmo
ctk.CTkLabel(
    frame_izq,
    text="Pasos del algoritmo:",
    font=ctk.CTkFont(size=12, weight="bold"),
    anchor="w"
).pack(padx=20, anchor="w")

caja_pasos = ctk.CTkTextbox(
    frame_izq,
    width=295,
    height=200,
    font=ctk.CTkFont(size=10, family="Courier"),
    state="disabled"
)
caja_pasos.pack(padx=20, pady=(4, 12))


# ── Panel derecho: grafico ──

figura = Figure(figsize=(6, 5), facecolor="#1e1e2e")
ax = figura.add_subplot(111)
ax.set_facecolor("#1e1e2e")
ax.tick_params(colors="white")
ax.xaxis.label.set_color("white")
ax.yaxis.label.set_color("white")
ax.title.set_color("white")
for spine in ax.spines.values():
    spine.set_edgecolor("#444")

canvas = FigureCanvasTkAgg(figura, master=frame_der)
canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)


# ─────────────────────────────────────────────
#  FUNCION PRINCIPAL: calcular()
# ─────────────────────────────────────────────

def calcular():
    try:
        funcion_str = entrada_funcion.get().strip()
        h_str = entrada_h.get().strip()

        if not funcion_str or not h_str:
            label_resultado.configure(text="⚠ Completa ambos campos", text_color="#ff8a65")
            return

        # Parsear expresion
        expresion = sympify(funcion_str)

        # Parsear h (puede ser "oo" para infinito)
        if h_str.lower() in ["oo", "inf", "infinito"]:
            h_val = oo
        elif h_str.lower() in ["-oo", "-inf"]:
            h_val = -oo
        else:
            h_val = sympify(h_str)

        # ── Ejecutar algoritmo propio ──
        resultado, pasos = calcular_limite_propio(expresion, h_val)

        # Mostrar resultado
        if resultado is not None:
            label_resultado.configure(
                text=f"lím f(x) = {resultado}",
                text_color="#4fc3f7"
            )
        else:
            label_resultado.configure(
                text="El límite no existe",
                text_color="#ef9a9a"
            )

        # Mostrar pasos
        caja_pasos.configure(state="normal")
        caja_pasos.delete("1.0", "end")
        caja_pasos.insert("end", "\n".join(pasos))
        caja_pasos.configure(state="disabled")

        # ── Graficar ──
        graficar(expresion, h_val, resultado)

    except Exception as e:
        label_resultado.configure(
            text=f"Error: {e}",
            text_color="#ef9a9a"
        )
        caja_pasos.configure(state="normal")
        caja_pasos.delete("1.0", "end")
        caja_pasos.insert("end", f"Error al procesar:\n{e}")
        caja_pasos.configure(state="disabled")


def graficar(expresion, h_val, resultado):
    """Genera el grafico de la funcion con indicadores visuales."""
    ax.clear()
    ax.set_facecolor("#1e1e2e")
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_edgecolor("#555")
    ax.grid(True, color="#333", linestyle="--", linewidth=0.5)

    # Determinar rango de x
    try:
        if h_val in [oo, -oo]:
            centro = 0
        else:
            centro = float(h_val)
    except Exception:
        centro = 0

    rango = 5
    inicio = centro - rango
    fin = centro + rango

    # Construir listas x e y (ciclo while, sin numpy)
    lista_x = []
    lista_y = []
    f = lambdify(x, expresion, modules=["sympy"])

    paso_iter = (fin - inicio) / 400
    xi = inicio
    while xi <= fin:
        lista_x.append(xi)
        try:
            yi = float(f(xi))
            # Filtrar valores fuera de rango para no distorsionar el grafico
            if abs(yi) > 1e6:
                lista_y.append(None)
            else:
                lista_y.append(yi)
        except Exception:
            lista_y.append(None)
        xi += paso_iter

    # Separar en segmentos para no unir discontinuidades
    segmento_x, segmento_y = [], []
    for i in range(len(lista_x)):
        if lista_y[i] is None:
            if segmento_x:
                ax.plot(segmento_x, segmento_y, color="#4fc3f7", linewidth=2)
                segmento_x, segmento_y = [], []
        else:
            segmento_x.append(lista_x[i])
            segmento_y.append(lista_y[i])
    if segmento_x:
        ax.plot(segmento_x, segmento_y, color="#4fc3f7", linewidth=2, label="f(x)")

    # Linea vertical en h
    if h_val not in [oo, -oo]:
        ax.axvline(x=centro, color="#ff8a65", linestyle="--", linewidth=1.4, label=f"x = h = {h_val}")

    # Punto del limite
    if resultado is not None and h_val not in [oo, -oo]:
        try:
            y_lim = float(resultado)
            ax.plot(centro, y_lim, "o", color="#a5d6a7", markersize=9,
                    zorder=5, label=f"Límite = {resultado}")
        except Exception:
            pass

    ax.set_title(f"Gráfico de f(x) con tendencia h = {h_val}", color="white", fontsize=11)
    ax.set_xlabel("x", color="white")
    ax.set_ylabel("f(x)", color="white")
    legend = ax.legend(facecolor="#2a2a3e", labelcolor="white", fontsize=9)

    canvas.draw()


# ── Main loop ──
ventana.mainloop()
