# 🧠 Red Social con Grafos en Python (BFS)

Este proyecto es una simulación de una red social utilizando estructuras de **grafos**. Está implementado en **Python** con una interfaz gráfica hecha en **Tkinter**.

Permite agregar usuarios, conectar amistades y visualizar recomendaciones de nuevos amigos usando el algoritmo **Breadth-First Search (BFS)**.

---

## 📌 Funcionalidades

- ✅ Agregar usuarios a la red social (nodos del grafo).
- ✅ Conectar usuarios como amigos (aristas del grafo).
- ✅ Visualizar la red social gráficamente en tiempo real.
- ✅ Ver los amigos directos de un usuario.
- ✅ Obtener sugerencias de amistad a 2 niveles de distancia (amigos de amigos).
- ✅ Interacción 100% mediante interfaz gráfica.

---

## 🧱 Estructura del proyecto

- `Grafo`: Clase que representa la red social con listas de adyacencia.
- `AplicacionRedSocial`: Clase que construye la interfaz gráfica con Tkinter.
- Se usa **BFS (Breadth-First Search)** para buscar sugerencias de amigos a partir de un nodo.

---

## 🎯 Requisitos técnicos

- Python 3.7 o superior
- Bibliotecas estándar: `tkinter`, `collections`, `random`, `math`

---
## 🧱 Clases y Metodos principales

### Clase GrafoRedSocial
```python
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
```

