try:
    import customtkinter as ctk
    from sympy import lambdify, oo, sympify
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
except ImportError as error:
    print("No se pudo iniciar la aplicacion porque falta una libreria.")
    print("Ejecuta: pip install sympy customtkinter matplotlib")
    print(f"Detalle: {error}")
    raise SystemExit

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
ventana.geometry("1120x760")
ventana.minsize(1050, 700)
ventana.title("Analizador y Visualizador de Límites — MATE1133")
ventana.resizable(True, True)


# ── Layout principal: izquierda (controles) + derecha (grafico) ──

# El panel izquierdo recibe los datos y muestra el desarrollo.
frame_izq = ctk.CTkFrame(ventana, width=390, corner_radius=12)
frame_izq.pack(side="left", fill="y", padx=14, pady=14)
frame_izq.pack_propagate(False)

# El panel derecho se reserva para la visualizacion de Matplotlib.
frame_der = ctk.CTkFrame(ventana, corner_radius=12)
frame_der.pack(side="right", fill="both", expand=True, padx=14, pady=14)


# ── Panel izquierdo: entradas ──

titulo = ctk.CTkLabel(
    frame_izq,
    text="Analizador de Límites",
    font=ctk.CTkFont(size=18, weight="bold"),
    justify="center"
)
titulo.pack(pady=(12, 2))

subtitulo = ctk.CTkLabel(
    frame_izq,
    text="MATE1133 — UCTemuco",
    font=ctk.CTkFont(size=10),
    text_color="gray"
)
subtitulo.pack(pady=(0, 8))

separador1 = ctk.CTkFrame(frame_izq, height=2, fg_color="#3a3a3a")
separador1.pack(fill="x", padx=20, pady=4)

# Funcion
ctk.CTkLabel(
    frame_izq,
    text="Función  f(x):",
    font=ctk.CTkFont(size=13, weight="bold"),
    anchor="w"
).pack(padx=20, pady=(8, 2), anchor="w")

ctk.CTkLabel(
    frame_izq,
    text="Usa sintaxis Python: x**2, sin(x), log(x) ...",
    font=ctk.CTkFont(size=10),
    text_color="gray",
    anchor="w"
).pack(padx=20, anchor="w")

entrada_funcion = ctk.CTkEntry(
    frame_izq,
    width=330,
    height=34,
    placeholder_text="Ej: (x**2 - 1)/(x - 1)",
    font=ctk.CTkFont(size=13)
)
entrada_funcion.pack(padx=20, pady=(4, 8))

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
    width=330,
    height=34,
    placeholder_text="Ej: 1  ó  oo",
    font=ctk.CTkFont(size=13)
)
entrada_h.pack(padx=20, pady=(4, 10))
ctk.CTkLabel(
    frame_izq,
    text="Dirección del límite:",
    font=ctk.CTkFont(size=13, weight="bold"),
    anchor="w"
).pack(padx=20, anchor="w")

selector_direccion = ctk.CTkOptionMenu(
    frame_izq,
    values=["Bilateral", "Izquierda (−)", "Derecha (+)"],
    width=330,
    font=ctk.CTkFont(size=13)
)
selector_direccion.pack(padx=20, pady=(4, 10))
# Boton
boton = ctk.CTkButton(
    frame_izq,
    text="▶  Calcular Límite",
    width=330,
    height=38,
    font=ctk.CTkFont(size=14, weight="bold"),
    corner_radius=10,
    command=lambda: calcular()
)
boton.pack(padx=20, pady=4)

separador2 = ctk.CTkFrame(frame_izq, height=2, fg_color="#3a3a3a")
separador2.pack(fill="x", padx=20, pady=9)

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
label_resultado.pack(padx=20, pady=(2, 6))

# Explicacion matematica del procedimiento
ctk.CTkLabel(
    frame_izq,
    text="Explicación del procedimiento:",
    font=ctk.CTkFont(size=14, weight="bold"),
    anchor="w"
).pack(padx=20, anchor="w")

caja_pasos = ctk.CTkTextbox(
    frame_izq,
    width=345,
    height=285,
    font=ctk.CTkFont(size=14, family="Arial"),
    wrap="word",
    state="disabled"
)
caja_pasos.pack(padx=20, pady=(4, 10))


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

def mostrar_explicacion(texto):
    """Reemplaza el contenido de la caja de explicacion."""
    caja_pasos.configure(state="normal")
    caja_pasos.delete("1.0", "end")
    caja_pasos.insert("end", texto)
    caja_pasos.configure(state="disabled")


def mostrar_error(titulo, explicacion):
    """Muestra un error comprensible sin cerrar la aplicacion."""
    label_resultado.configure(text=titulo, text_color="#ef9a9a")
    mostrar_explicacion(explicacion)


def calcular():
    """Lee las entradas, ejecuta el algoritmo y actualiza la interfaz."""
    funcion_str = entrada_funcion.get().strip()
    h_str = entrada_h.get().strip()

    if not funcion_str or not h_str:
        mostrar_error(
            "Completa ambos campos",
            "Debes ingresar una función y el valor de tendencia h."
        )
        return

    # La función y h se validan por separado para mostrar mensajes específicos.
    try:
        expresion = sympify(funcion_str)
        if not expresion.free_symbols.issubset({x}):
            raise ValueError
    except Exception:
        mostrar_error(
            "No se pudo interpretar la función",
            "Revisa la sintaxis ingresada.\n\n"
            "Recuerda escribir las multiplicaciones usando *.\n"
            "Ejemplo correcto: sin(5*x)/(x - sin(2*x))"
        )
        return

    try:
        if h_str.lower() in ["oo", "inf", "infinito"]:
            h_val = oo
        elif h_str.lower() in ["-oo", "-inf"]:
            h_val = -oo
        else:
            h_val = sympify(h_str)
            if h_val.free_symbols or h_val.is_number is not True:
                raise ValueError
    except Exception:
        mostrar_error(
            "El valor de h no es válido",
            'Ingresa un número o utiliza "oo" y "-oo" para infinito.\n\n'
            "Ejemplos válidos: 0, 2, pi, oo, -oo"
        )
        return

    try:
        direccion = selector_direccion.get()
        if direccion == "Izquierda (−)":
            resultado = limite_lateral(expresion, h_val, "-")
            pasos = [
                "Límite lateral por la izquierda",
                "",
                f"Se estudian valores de x menores que {h_val},",
                "cada vez más cercanos al punto.",
                "",
                f"El resultado obtenido es {resultado}."
            ]
        elif direccion == "Derecha (+)":
            resultado = limite_lateral(expresion, h_val, "+")
            pasos = [
                "Límite lateral por la derecha",
                "",
                f"Se estudian valores de x mayores que {h_val},",
                "cada vez más cercanos al punto.",
                "",
                f"El resultado obtenido es {resultado}."
            ]
        else:
            resultado, pasos = calcular_limite_propio(expresion, h_val)

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

        # Si Matplotlib falla, el resultado matemático se mantiene visible.
        try:
            graficar(expresion, h_val, resultado)
        except Exception:
            pasos.append("")
            pasos.append("No se pudo generar el gráfico,")
            pasos.append("pero el cálculo del límite fue completado.")

        mostrar_explicacion("\n".join(pasos))

    except Exception:
        mostrar_error(
            "No se pudo completar el cálculo",
            "Ocurrió un error inesperado durante el procedimiento.\n\n"
            "Revisa los datos ingresados e intenta nuevamente."
        )


def determinar_rango_grafico(h_val):
    """Retorna el centro y rango visible segun el valor de tendencia."""
    # Los limites al infinito necesitan un rango alejado de cero para mostrar
    # el comportamiento de la funcion en la direccion correspondiente.
    if h_val == oo:
        return None, 1, 100

    if h_val == -oo:
        return None, -100, -1

    try:
        centro = float(h_val)
    except Exception:
        centro = 0

    rango = 5
    return centro, centro - rango, centro + rango


def graficar(expresion, h_val, resultado):
    """Genera el grafico de la funcion con indicadores visuales."""
    # Se limpia el grafico anterior antes de dibujar la nueva funcion.
    ax.clear()
    ax.set_facecolor("#1e1e2e")
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_edgecolor("#555")
    ax.grid(True, color="#333", linestyle="--", linewidth=0.5)

    centro, inicio, fin = determinar_rango_grafico(h_val)

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

    if h_val == oo:
        titulo_grafico = "Comportamiento de f(x) cuando x tiende a +infinito"
    elif h_val == -oo:
        titulo_grafico = "Comportamiento de f(x) cuando x tiende a -infinito"
    else:
        titulo_grafico = f"Gráfico de f(x) con tendencia h = {h_val}"

    ax.set_title(titulo_grafico, color="white", fontsize=11)
    ax.set_xlabel("x", color="white")
    ax.set_ylabel("f(x)", color="white")
    legend = ax.legend(facecolor="#2a2a3e", labelcolor="white", fontsize=9)

    canvas.draw()


# Mantiene abierta la ventana y espera las acciones del usuario.
ventana.mainloop()
