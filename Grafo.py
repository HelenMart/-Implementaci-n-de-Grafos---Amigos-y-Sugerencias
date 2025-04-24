import tkinter as tk
from tkinter import messagebox
from collections import deque
import random
import math

class GrafoRedSocial:
    def __init__(self):
        self.lista_adyacencia = {}

    def agregar_usuario(self, nombre):
        if nombre not in self.lista_adyacencia:
            self.lista_adyacencia[nombre] = []

    def agregar_amistad(self, usuario1, usuario2):
        if usuario1 in self.lista_adyacencia and usuario2 in self.lista_adyacencia:
            if usuario2 not in self.lista_adyacencia[usuario1]:
                self.lista_adyacencia[usuario1].append(usuario2)
            if usuario1 not in self.lista_adyacencia[usuario2]:
                self.lista_adyacencia[usuario2].append(usuario1)

    def obtener_amigos_directos(self, usuario):
        return self.lista_adyacencia.get(usuario, [])

    def obtener_sugerencias(self, usuario):
        if usuario not in self.lista_adyacencia:
            return []

        visitados = set()
        nivel = {usuario: 0}
        sugerencias = set()
        cola = deque([usuario])
        visitados.add(usuario)

        while cola:
            actual = cola.popleft()
            for vecino in self.lista_adyacencia[actual]:
                if vecino not in visitados:
                    nivel[vecino] = nivel[actual] + 1
                    visitados.add(vecino)
                    cola.append(vecino)
                    if nivel[vecino] == 2 and vecino not in self.lista_adyacencia[usuario]:
                        sugerencias.add(vecino)

        return list(sugerencias)

class AplicacionRedSocial:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Red Social con Grafos (BFS)")
        self.grafo = GrafoRedSocial()
        self.posiciones = {}
        self.radio_nodo = 20
        self.usuario_seleccionado = None

        # Canvas
        self.lienzo = tk.Canvas(raiz, width=500, height=500, bg="white")
        self.lienzo.pack(side=tk.LEFT, padx=10, pady=10)
        self.lienzo.bind("<Button-1>", self.click_en_lienzo)

        # Panel lateral
        self.panel = tk.Frame(raiz)
        self.panel.pack(side=tk.RIGHT, padx=10)

        tk.Label(self.panel, text="Nombre del usuario:").pack()
        self.entrada_usuario = tk.Entry(self.panel)
        self.entrada_usuario.pack()

        tk.Button(self.panel, text="Agregar usuario", command=self.boton_agregar_usuario).pack(pady=5)

        tk.Label(self.panel, text="Amistad --> Ejemplo: Karla, Juan").pack()
        self.entrada_amistad = tk.Entry(self.panel)
        self.entrada_amistad.pack()

        tk.Button(self.panel, text="Crear amistad", command=self.boton_agregar_amistad).pack(pady=5)

        tk.Label(self.panel, text="Usuario seleccionado:").pack(pady=10)
        self.etiqueta_usuario = tk.Label(self.panel, text="(ninguno)", font=("Arial", 10, "bold"))
        self.etiqueta_usuario.pack()

        self.texto_resultado = tk.Text(self.panel, width=30, height=10)
        self.texto_resultado.pack(pady=10)

    def boton_agregar_usuario(self):
        nombre = self.entrada_usuario.get().strip()
        if not nombre:
            return
        if nombre in self.grafo.lista_adyacencia:
            messagebox.showinfo("Información", "El usuario ya existe.")
            return

        self.grafo.agregar_usuario(nombre)
        x = random.randint(50, 450)
        y = random.randint(50, 450)
        self.posiciones[nombre] = (x, y)

        self.dibujar_grafo()
        self.entrada_usuario.delete(0, tk.END)

    def boton_agregar_amistad(self):
        datos = self.entrada_amistad.get().split(",")
        if len(datos) != 2:
            messagebox.showerror("Error", "Formato incorrecto. Usa: Persona1,persona2")
            return
        usuario1, usuario2 = datos[0].strip(), datos[1].strip()
        if usuario1 not in self.grafo.lista_adyacencia or usuario2 not in self.grafo.lista_adyacencia:
            messagebox.showerror("Error", "Uno o ambos usuarios no existen.")
            return

        self.grafo.agregar_amistad(usuario1, usuario2)
        self.dibujar_grafo()
        self.entrada_amistad.delete(0, tk.END)

    def dibujar_grafo(self):
        self.lienzo.delete("all")

        for usuario, amigos in self.grafo.lista_adyacencia.items():#Linea
            x1, y1 = self.posiciones[usuario]
            for amigo in amigos:
                if usuario < amigo:
                    x2, y2 = self.posiciones[amigo]
                    self.lienzo.create_line(x1, y1, x2, y2)

        for usuario, (x, y) in self.posiciones.items():#click nombre y ndo
            color = "lightblue" if usuario != self.usuario_seleccionado else "lightgreen"
            self.lienzo.create_oval(x - self.radio_nodo, y - self.radio_nodo,
                                    x + self.radio_nodo, y + self.radio_nodo, fill=color)
            self.lienzo.create_text(x, y, text=usuario)

    def click_en_lienzo(self, evento):
        for usuario, (x, y) in self.posiciones.items():
            distancia = math.hypot(evento.x - x, evento.y - y)
            if distancia <= self.radio_nodo:
                self.usuario_seleccionado = usuario
                self.etiqueta_usuario.config(text=usuario)
                self.mostrar_informacion_usuario(usuario)
                self.dibujar_grafo()
                break

    def mostrar_informacion_usuario(self, usuario):
        amigos = self.grafo.obtener_amigos_directos(usuario)
        sugerencias = self.grafo.obtener_sugerencias(usuario)

        self.texto_resultado.delete("1.0", tk.END)
        self.texto_resultado.insert(tk.END, f"👫 Amigos directos de {usuario}:\n")
        for amigo in amigos:
            self.texto_resultado.insert(tk.END, f"- {amigo}\n")

        self.texto_resultado.insert(tk.END, f"\n🤝 Sugerencias de amistad:\n")
        for sugerencia in sugerencias:
            self.texto_resultado.insert(tk.END, f"- {sugerencia}\n")

# ventana
if __name__ == "__main__":
    raiz = tk.Tk()
    app = AplicacionRedSocial(raiz)
    raiz.mainloop()
