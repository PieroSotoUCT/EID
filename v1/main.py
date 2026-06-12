import customtkinter as ctk
from sympy import lambdify, oo, sympify
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Se importa la logica matematica desde limites.py para mantener separadas
# la interfaz y la resolucion de los limites.
from limites import calcular_limite_propio, limite_lateral, x

# ─────────────────────────────────────────────
#  INTERFAZ GRAFICA
# ─────────────────────────────────────────────

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Ventana principal que contiene el panel de controles y el grafico.
ventana = ctk.CTk()
ventana.geometry("1050x700")
ventana.title("Analizador y Visualizador de Límites — MATE1133")
ventana.resizable(True, True)


# ── Layout principal: izquierda (controles) + derecha (grafico) ──

# El panel izquierdo recibe los datos y muestra el desarrollo.
frame_izq = ctk.CTkFrame(ventana, width=340, corner_radius=12)
frame_izq.pack(side="left", fill="y", padx=14, pady=14)
frame_izq.pack_propagate(False)

# El panel derecho se reserva para la visualizacion de Matplotlib.
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
#NEW
entrada_h = ctk.CTkEntry(
    frame_izq,
    width=280,
    height=36,
    placeholder_text="Ej: 1  ó  oo",
    font=ctk.CTkFont(size=13)
)
entrada_h.pack(padx=20, pady=(4, 16))
ctk.CTkLabel(
    frame_izq,
    text="Dirección del límite:",
    font=ctk.CTkFont(size=13, weight="bold"),
    anchor="w"
).pack(padx=20, anchor="w")

selector_direccion = ctk.CTkOptionMenu(
    frame_izq,
    values=["Bilateral", "Izquierda (−)", "Derecha (+)"],
    width=280
)
selector_direccion.pack(padx=20, pady=(4, 16))
#NEW


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

# FigureCanvasTkAgg permite insertar el grafico dentro de CustomTkinter.
canvas = FigureCanvasTkAgg(figura, master=frame_der)
canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)


# ─────────────────────────────────────────────
#  FUNCION PRINCIPAL: calcular()
# ─────────────────────────────────────────────

def calcular():
    """Lee las entradas, ejecuta el algoritmo y actualiza la interfaz."""
    try:
        # strip elimina espacios accidentales al inicio y al final.
        funcion_str = entrada_funcion.get().strip()
        h_str = entrada_h.get().strip()

        if not funcion_str or not h_str:
            label_resultado.configure(text="Completa ambos campos", text_color="#ff8a65")
            return

        # Sympify convierte el texto ingresado en una expresion de SymPy.
        expresion = sympify(funcion_str)

        # Se aceptan distintas formas de escribir infinito.
        if h_str.lower() in ["oo", "inf", "infinito"]:
            h_val = oo
        elif h_str.lower() in ["-oo", "-inf"]:
            h_val = -oo
        else:
            h_val = sympify(h_str)

        # ── Ejecutar algoritmo con selecciones
        #NEW
        direccion = selector_direccion.get()
        if direccion == "Izquierda (−)":
            resultado = limite_lateral(expresion, h_val, "-")
            pasos = [f"Límite por la izquierda en x → {h_val}", f"Resultado: {resultado}"]
        elif direccion == "Derecha (+)":
            resultado = limite_lateral(expresion, h_val, "+")
            pasos = [f"Límite por la derecha en x → {h_val}", f"Resultado: {resultado}"]
        else:
            resultado, pasos = calcular_limite_propio(expresion, h_val)
        #NEW
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

        # La caja se habilita solo mientras se reemplaza su contenido.
        caja_pasos.configure(state="normal")
        caja_pasos.delete("1.0", "end")
        caja_pasos.insert("end", "\n".join(pasos))
        caja_pasos.configure(state="disabled")

        # ── Graficar ──
        graficar(expresion, h_val, resultado)

    except Exception as e:
        # Evita que la aplicacion se cierre si el usuario ingresa datos invalidos.
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
    # Se limpia el grafico anterior antes de dibujar la nueva funcion.
    ax.clear()
    ax.set_facecolor("#1e1e2e")
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_edgecolor("#555")
    ax.grid(True, color="#333", linestyle="--", linewidth=0.5)

    # Para limites finitos, el grafico se centra alrededor de h.
    # En limites al infinito se utiliza cero como centro visual.
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

    # Se construyen las listas con un ciclo while, sin utilizar NumPy.
    lista_x = []
    lista_y = []
    f = lambdify(x, expresion, modules=["sympy"])

    paso_iter = (fin - inicio) / 400
    xi = inicio
    while xi <= fin:
        lista_x.append(xi)
        try:
            yi = float(f(xi))
            # Los valores demasiado grandes se omiten para cuidar la escala.
            if abs(yi) > 1e6:
                lista_y.append(None)
            else:
                lista_y.append(yi)
        except Exception:
            lista_y.append(None)
        xi += paso_iter

    # Cuando aparece None se corta la linea para no unir discontinuidades.
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


# Mantiene abierta la ventana y espera las acciones del usuario.
ventana.mainloop()
