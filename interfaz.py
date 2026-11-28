# interfaz.py
# esta es la ventana del analizador de cadenas, hecha con tkinter.
# la parte de autómatas esta en afd.py, aqui solo se arma la ventana
# y se llaman esas funciones.
#
# para correrlo:  python3 interfaz.py

import tkinter as tk
from tkinter import ttk, messagebox

import afd as automatas


class Analizador:
    def __init__(self, ventana):
        self.ventana = ventana
        ventana.title("Analizador de cadenas con AFD")
        ventana.geometry("780x860")

        # aqui guardo las condiciones como las escribio el usuario.
        # los afd se vuelven a construir cada vez que se prueba una cadena,
        # asi si cambian el alfabeto no hay problema.
        self.condiciones = []

        #alfabeto
        marco_alfabeto = ttk.LabelFrame(ventana, text="1. Alfabeto")
        marco_alfabeto.pack(fill="x", padx=10, pady=5)
        ttk.Label(marco_alfabeto, text="Símbolos separados por comas:").pack(side="left", padx=5, pady=5)
        self.entrada_alfabeto = ttk.Entry(marco_alfabeto, width=20)
        self.entrada_alfabeto.insert(0, "0,1")
        self.entrada_alfabeto.pack(side="left", padx=5)

        #condiciones
        marco_cond = ttk.LabelFrame(ventana, text="2. Condiciones")
        marco_cond.pack(fill="x", padx=10, pady=5)

        fila = ttk.Frame(marco_cond)
        fila.pack(fill="x", padx=5, pady=5)
        ttk.Label(fila, text="Tipo:").pack(side="left")
        self.combo_tipo = ttk.Combobox(fila, values=automatas.TIPOS, state="readonly", width=32)
        self.combo_tipo.current(0)
        self.combo_tipo.pack(side="left", padx=5)
        self.combo_tipo.bind("<<ComboboxSelected>>", self.cambio_tipo)

        ttk.Label(fila, text="x o símbolo:").pack(side="left")
        self.entrada_texto = ttk.Entry(fila, width=10)
        self.entrada_texto.pack(side="left", padx=5)

        ttk.Label(fila, text="n:").pack(side="left")
        self.entrada_numero = ttk.Entry(fila, width=5)
        self.entrada_numero.pack(side="left", padx=5)

        self.var_negar = tk.BooleanVar()
        ttk.Checkbutton(fila, text="Negar", variable=self.var_negar).pack(side="left", padx=5)

        self.etiqueta_ayuda = ttk.Label(marco_cond, foreground="gray")
        self.etiqueta_ayuda.pack(anchor="w", padx=5)

        botones = ttk.Frame(marco_cond)
        botones.pack(fill="x", padx=5, pady=5)
        ttk.Button(botones, text="Agregar", command=self.agregar).pack(side="left")
        ttk.Button(botones, text="Quitar seleccionada", command=self.quitar).pack(side="left", padx=5)
        ttk.Button(botones, text="Ver tabla", command=self.ver_tabla).pack(side="left")
        ttk.Button(botones, text="Cargar ejemplo", command=self.cargar_ejemplo).pack(side="right")

        self.lista = tk.Listbox(marco_cond, height=5)
        self.lista.pack(fill="x", padx=5, pady=5)

        #operacion entre dos condiciones
        marco_op = ttk.LabelFrame(ventana, text="3. Operación entre dos condiciones")
        marco_op.pack(fill="x", padx=10, pady=5)

        fila_op = ttk.Frame(marco_op)
        fila_op.pack(fill="x", padx=5, pady=5)
        ttk.Label(fila_op, text="A:").pack(side="left")
        self.combo_a = ttk.Combobox(fila_op, state="readonly", width=24)
        self.combo_a.pack(side="left", padx=5)
        self.combo_op = ttk.Combobox(fila_op, values=automatas.OPERACIONES, state="readonly", width=12)
        self.combo_op.current(0)
        self.combo_op.pack(side="left", padx=5)
        ttk.Label(fila_op, text="B:").pack(side="left")
        self.combo_b = ttk.Combobox(fila_op, state="readonly", width=24)
        self.combo_b.pack(side="left", padx=5)

        fila_op2 = ttk.Frame(marco_op)
        fila_op2.pack(fill="x", padx=5, pady=5)
        ttk.Button(fila_op2, text="Ver tabla del resultado", command=self.ver_tabla_operacion).pack(side="left")
        ttk.Label(fila_op2, text="Unión: A o B.   Intersección: A y B.   Diferencia: A pero no B.",
                  foreground="gray").pack(side="left", padx=10)

        #probar cadena
        marco_prueba = ttk.LabelFrame(ventana, text="4. Probar cadena")
        marco_prueba.pack(fill="both", expand=True, padx=10, pady=5)

        fila2 = ttk.Frame(marco_prueba)
        fila2.pack(fill="x", padx=5, pady=5)
        ttk.Label(fila2, text="Cadena:").pack(side="left")
        self.entrada_cadena = ttk.Entry(fila2, width=25)
        self.entrada_cadena.pack(side="left", padx=5)
        self.entrada_cadena.bind("<Return>", lambda evento: self.probar())
        ttk.Button(fila2, text="Probar todas", command=self.probar).pack(side="left")
        ttk.Button(fila2, text="Probar operación", command=self.probar_operacion).pack(side="left", padx=5)

        self.etiqueta_resultado = tk.Label(marco_prueba, text="", font=("Arial", 20, "bold"))
        self.etiqueta_resultado.pack(pady=5)

        self.texto_detalle = tk.Text(marco_prueba, height=10, font=("Courier", 12))
        self.texto_detalle.pack(fill="both", expand=True, padx=5, pady=5)

        self.cambio_tipo()

    #funciones de apoyo

    def leer_alfabeto(self):
        # convierte "0,1" en ["0", "1"] y revisa que este bien
        partes = [p.strip() for p in self.entrada_alfabeto.get().split(",")]
        sigma = []
        for p in partes:
            if p == "":
                continue
            if len(p) != 1:
                raise ValueError("Cada símbolo del alfabeto debe ser un solo carácter (encontré «" + p + "»).")
            if p not in sigma:
                sigma.append(p)
        if not sigma:
            raise ValueError("Escribe al menos un símbolo en el alfabeto.")
        return sigma

    def construir_todos(self):
        # arma un afd por cada condicion con el alfabeto actual
        sigma = self.leer_alfabeto()
        afds = [automatas.construir(sigma, *cond) for cond in self.condiciones]
        return sigma, afds

    def actualizar_combos(self):
        # pone las condiciones de la lista en los combos de a y b.
        # les pongo numero por si hay dos condiciones con el mismo nombre.
        nombres = [str(i + 1) + ". " + self.lista.get(i) for i in range(self.lista.size())]
        for combo in (self.combo_a, self.combo_b):
            elegido = combo.current()
            combo.config(values=nombres)
            if 0 <= elegido < len(nombres):
                combo.current(elegido)
            else:
                combo.set("")

    def armar_operacion(self):
        # construye el afd de la operacion entre a y b
        ia = self.combo_a.current()
        ib = self.combo_b.current()
        if ia < 0 or ib < 0:
            raise ValueError("Elige las condiciones A y B en la sección 3.")
        sigma, afds = self.construir_todos()
        resultado = automatas.producto(afds[ia], afds[ib], sigma, self.combo_op.get())
        return sigma, afds[ia], afds[ib], resultado

    def mostrar_tabla(self, texto):
        # abre una ventanita con la tabla de transiciones
        ventana_tabla = tk.Toplevel(self.ventana)
        ventana_tabla.title("Tabla de transiciones")
        caja = tk.Text(ventana_tabla, width=70, height=24, font=("Courier", 12))
        caja.pack(fill="both", expand=True, padx=10, pady=10)
        caja.insert("end", texto)
        caja.config(state="disabled")

    def simbolo_invalido(self, cadena, sigma):
        # regresa el primer simbolo que no este en el alfabeto, o None si todos estan bien
        for c in cadena:
            if c not in sigma:
                return c
        return None

    def poner_resultado(self, acepta):
        if acepta:
            self.etiqueta_resultado.config(text="ACEPTADA", fg="green")
        else:
            self.etiqueta_resultado.config(text="RECHAZADA", fg="red")

    def escribir_afd(self, etiqueta, maquina, recorrido, cumple):
        # escribe en el detalle por donde paso un afd y si cumplio
        marca = "sí cumple" if cumple else "no cumple"
        camino = " -> ".join(automatas.nombre_estado(maquina, q) for q in recorrido)
        self.texto_detalle.insert("end", etiqueta + maquina["nombre"] + "   " + marca + "\n")
        self.texto_detalle.insert("end", "   " + camino + "\n\n")

    # funciones de los botones

    def cambio_tipo(self, evento=None):
        # muestra una ayuda segun el tipo elegido y activa o desactiva el campo n
        tipo = self.combo_tipo.get()
        if tipo in ("Empieza con", "Contiene", "Termina en"):
            ayuda = "Escribe la cadena x en «x o símbolo». Ejemplo: 101"
            usa_n = False
        elif tipo in ("Cantidad par del símbolo", "Cantidad impar del símbolo"):
            ayuda = "Escribe un solo símbolo. Ejemplo: 1"
            usa_n = False
        else:
            ayuda = "Escribe un solo símbolo y el número n. Ejemplo: símbolo 1, n = 2"
            usa_n = True
        self.etiqueta_ayuda.config(text=ayuda)
        self.entrada_numero.config(state="normal" if usa_n else "disabled")

    def agregar(self):
        # guardo la condicion y antes la pruebo construyendo su afd para ver que no tenga errores
        tipo = self.combo_tipo.get()
        texto = self.entrada_texto.get().strip()
        numero = self.entrada_numero.get().strip() if str(self.entrada_numero.cget("state")) == "normal" else ""
        negada = self.var_negar.get()
        try:
            sigma = self.leer_alfabeto()
            maquina = automatas.construir(sigma, tipo, texto, numero, negada)
        except ValueError as error:
            messagebox.showerror("Dato incorrecto", str(error))
            return
        self.condiciones.append((tipo, texto, numero, negada))
        self.lista.insert("end", maquina["nombre"])
        self.entrada_texto.delete(0, "end")
        self.entrada_numero.delete(0, "end")
        self.var_negar.set(False)
        self.actualizar_combos()

    def quitar(self):
        seleccion = self.lista.curselection()
        if not seleccion:
            messagebox.showinfo("Quitar", "Selecciona una condición de la lista.")
            return
        i = seleccion[0]
        self.lista.delete(i)
        self.condiciones.pop(i)
        # al quitar una condicion los numeros cambian, entonces limpio a y b
        self.combo_a.set("")
        self.combo_b.set("")
        self.actualizar_combos()

    def ver_tabla(self):
        # tabla de transiciones de la condicion seleccionada en la lista
        seleccion = self.lista.curselection()
        if not seleccion:
            messagebox.showinfo("Ver tabla", "Selecciona una condición de la lista.")
            return
        try:
            sigma, afds = self.construir_todos()
        except ValueError as error:
            messagebox.showerror("Dato incorrecto", str(error))
            return
        self.mostrar_tabla(automatas.tabla_texto(afds[seleccion[0]], sigma))

    def ver_tabla_operacion(self):
        # tabla de transiciones del afd que sale de la operacion
        try:
            sigma, a, b, resultado = self.armar_operacion()
        except ValueError as error:
            messagebox.showerror("Dato incorrecto", str(error))
            return
        self.mostrar_tabla(automatas.tabla_texto(resultado, sigma))

    def probar(self):
        # prueba la cadena con todas las condiciones a la vez (interseccion de todas)
        cadena = self.entrada_cadena.get().strip()
        if not self.condiciones:
            messagebox.showinfo("Probar", "Primero agrega al menos una condición.")
            return
        try:
            sigma, afds = self.construir_todos()
        except ValueError as error:
            messagebox.showerror("Dato incorrecto", str(error))
            return

        self.texto_detalle.delete("1.0", "end")
        malo = self.simbolo_invalido(cadena, sigma)
        if malo is not None:
            self.poner_resultado(False)
            self.texto_detalle.insert("end", "El símbolo «" + malo + "» no está en el alfabeto.\n")
            return

        acepta, recorridos, cumple = automatas.correr(afds, cadena)
        self.poner_resultado(acepta)

        mostrar = cadena if cadena else "ε (cadena vacía)"
        self.texto_detalle.insert("end", "Cadena: " + mostrar + "   (todas las condiciones)\n\n")
        for j, maquina in enumerate(afds):
            self.escribir_afd("", maquina, recorridos[j], cumple[j])

    def probar_operacion(self):
        # prueba la cadena con el afd que sale de la operacion entre a y b
        cadena = self.entrada_cadena.get().strip()
        try:
            sigma, a, b, resultado = self.armar_operacion()
        except ValueError as error:
            messagebox.showerror("Dato incorrecto", str(error))
            return

        self.texto_detalle.delete("1.0", "end")
        malo = self.simbolo_invalido(cadena, sigma)
        if malo is not None:
            self.poner_resultado(False)
            self.texto_detalle.insert("end", "El símbolo «" + malo + "» no está en el alfabeto.\n")
            return

        # corro a, b y el resultado juntos para mostrar los tres caminos
        acepta, recorridos, cumple = automatas.correr([a, b, resultado], cadena)
        self.poner_resultado(cumple[2])

        mostrar = cadena if cadena else "ε (cadena vacía)"
        self.texto_detalle.insert("end", "Cadena: " + mostrar + "   (" + self.combo_op.get().lower() + ")\n\n")
        self.escribir_afd("A: ", a, recorridos[0], cumple[0])
        self.escribir_afd("B: ", b, recorridos[1], cumple[1])
        self.escribir_afd("Resultado: ", resultado, recorridos[2], cumple[2])
        self.texto_detalle.insert(
            "end",
            "El AFD resultante tiene " + str(len(resultado["estados"])) + " estados alcanzables "
            "(A tiene " + str(len(a["estados"])) + " y B tiene " + str(len(b["estados"])) + ").\n")

    def cargar_ejemplo(self):
        # el ejemplo del reporte: empieza con 1, contiene 101 y termina en 0
        self.entrada_alfabeto.delete(0, "end")
        self.entrada_alfabeto.insert(0, "0,1")
        self.condiciones = [
            ("Empieza con", "1", "", False),
            ("Contiene", "101", "", False),
            ("Termina en", "0", "", False),
        ]
        self.lista.delete(0, "end")
        sigma, afds = self.construir_todos()
        for maquina in afds:
            self.lista.insert("end", maquina["nombre"])
        self.actualizar_combos()
        self.combo_a.current(0)
        self.combo_b.current(1)
        self.entrada_cadena.delete(0, "end")
        self.entrada_cadena.insert(0, "11010")
        self.probar()


if __name__ == "__main__":
    ventana = tk.Tk()
    Analizador(ventana)
    ventana.mainloop()