import tkinter as tk

class ConcursoBandasApp:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Concurso de Bandas - Quetzaltenango")
        self.ventana.geometry("500x300")

        self.concurso = Concurso("Concurso 14 de Septiembre", "2025-09-14")
        self.menu()

        tk.Label(
            self.ventana,
            text="Sistema de Inscripción y Evaluación de Bandas Escolares\nConcurso 14 de Septiembre - Quetzaltenango",
            font=("Arial", 12, "bold"),
            justify="center"
        ).pack(pady=50)

        self.ventana.mainloop()

    def menu(self):
        barra = tk.Menu(self.ventana)
        opciones = tk.Menu(barra, tearoff=0)
        opciones.add_command(label="Inscribir Banda", command=self.inscribir_banda)
        opciones.add_command(label="Registrar Evaluación", command=self.registrar_evaluacion)
        opciones.add_command(label="Listar Bandas", command=self.listar_bandas)
        opciones.add_command(label="Ver Ranking", command=self.ver_ranking)
        opciones.add_separator()
        opciones.add_command(label="Salir", command=self.ventana.quit)
        barra.add_cascade(label="Opciones", menu=opciones)
        self.ventana.config(menu=barra)

    def inscribir_banda(self):
        ventana_inscribir = tk.Toplevel(self.ventana)
        ventana_inscribir.title("Inscribir Banda")
        ventana_inscribir.geometry("500x300")

        tk.Label(ventana_inscribir, text="Nombre de la banda:").pack(pady=5)
        entrada_nombre = tk.Entry(ventana_inscribir)
        entrada_nombre.pack(pady=5)

        tk.Label(ventana_inscribir, text="Institución:").pack(pady=5)
        entrada_inst = tk.Entry(ventana_inscribir)
        entrada_inst.pack(pady=5)

        tk.Label(ventana_inscribir, text="Categoría (Primaria, Básico, Diversificado):").pack(pady=5)
        entrada_cat = tk.Entry(ventana_inscribir)
        entrada_cat.pack(pady=5)

        def guardar():
            nombre = entrada_nombre.get()
            institucion = entrada_inst.get()
            categoria = entrada_cat.get()
            promedio = 0
            try:
                banda = BandaEscolar(nombre, institucion, categoria, promedio)
                self.concurso.inscribir_banda(banda)
                print(f"Banda inscrita: {nombre}")
            except ValueError as e:
                print("Error:", e)
            ventana_inscribir.destroy()

        tk.Button(ventana_inscribir, text="Guardar", command=guardar).pack(pady=10)

    def registrar_evaluacion(self):
        ventana_eval = tk.Toplevel(self.ventana)
        ventana_eval.title("Registrar Evaluación")
        ventana_eval.geometry("500x300")

        tk.Label(ventana_eval, text="Nombre de la banda:").pack()
        entrada_nombre = tk.Entry(ventana_eval)
        entrada_nombre.pack()

        entradas = {}
        for criterio in BandaEscolar.Criterios_validos:
            tk.Label(ventana_eval, text=f"{criterio}:").pack()
            e = tk.Entry(ventana_eval)
            e.pack()
            entradas[criterio] = e

        def guardar():
            nombre = entrada_nombre.get()
            puntajes = {}
            for criterio, entry in entradas.items():
                try:
                    puntajes[criterio] = float(entry.get())
                except ValueError:
                    puntajes[criterio] = 0
            try:
                self.concurso.registrar_evaluacion(nombre, puntajes)
                print(f"Evaluación registrada para {nombre}: {puntajes}")
            except ValueError as e:
                print("Error:", e)
            ventana_eval.destroy()

        tk.Button(ventana_eval, text="Guardar", command=guardar).pack(pady=10)

    def listar_bandas(self):
        ventana_listar = tk.Toplevel(self.ventana)
        ventana_listar.title("Listado de Bandas")
        ventana_listar.geometry("400x400")

        tk.Label(ventana_listar, text="--- Bandas Inscritas ---", font=("Arial", 12, "bold")).pack(pady=5)

        for banda in self.concurso.bandas.values():
            tk.Label(ventana_listar, text=banda.mostrar_info()).pack()

    def ver_ranking(self):
        ventana_ranking = tk.Toplevel(self.ventana)
        ventana_ranking.title("Ranking Final")
        ventana_ranking.geometry("400x400")

        tk.Label(ventana_ranking, text="--- Ranking Final ---", font=("Arial", 12, "bold")).pack(pady=5)

        ordenador = Ordenamiento()
        bandas_ordenadas = ordenador.quick_sort_bandas(list(self.concurso.bandas.values()))
        bandas_ordenadas.reverse()
        for banda in bandas_ordenadas:
            tk.Label(ventana_ranking, text=banda.mostrar_info()).pack()


class Participante:
    def __init__(self,nombre,institucion):
        self.nombre = nombre
        self.institucion = institucion

    def mostrar_info(self):
        print(f"Nombre: {self.nombre}, Institucion: {self.institucion}" )

class BandaEscolar(Participante):
    Categorias_validas = ['Primaria', 'Básico', 'Diversificado']
    Criterios_validos = ['ritmo', 'uniformidad', 'coreografía', 'alineación', 'puntualidad']

    def __init__(self,nombre,institucion,categoria,promedio = 0):
        super().__init__(nombre,institucion)
        self.set_categoria(categoria)
        self._puntuajes = {}
        self.total = 0
        self.promedio = promedio

    def set_categoria(self, categoria):
        categoria = categoria.strip().capitalize()
        if categoria not in self.Categorias_validas:
            self.Categorias_validas.append(categoria)
        self._categoria = categoria

    def registrar_puntajes(self, puntajes):
        puntajes_normalizados = {}
        for criterio, valor in puntajes.items():
            criterio = criterio.strip().lower()
            puntajes_normalizados[criterio] = valor
            if criterio not in self.Criterios_validos:
                self.Criterios_validos.append(criterio)
        self._puntuajes = puntajes_normalizados
        self.suma_puntajes()
        self.calcular_promedio()

    def suma_puntajes(self):
        self.total = sum(self._puntuajes.values())

    def calcular_promedio(self):
        if self._puntuajes:
            self.promedio = self.total / len(self._puntuajes)
        else:
            self.promedio = 0

    def mostrar_info(self):
        if self._puntuajes:
            return f"Nombre:{self.nombre}, Categoria:({self._categoria}), Instituto: {self.institucion} | Total: {self.total}"
        else:
            return f"Nombre:{self.nombre}, Categoria:({self._categoria}), Instituto: {self.institucion} | Sin evaluar"

class Concurso:
    def __init__(self,nombre,fecha):
        self.nombre = nombre
        self.fecha = fecha
        self.bandas = {}

    def inscribir_banda(self,banda):
        if banda.nombre in self.bandas:
            raise ValueError(f"La banda '{banda.nombre}' ya está inscrita.")
        self.bandas[banda.nombre] = banda

    def registrar_evaluacion(self, nombre_banda, puntajes):
        if nombre_banda not in self.bandas:
            raise ValueError(f"La banda '{nombre_banda}' no está inscrita.")
        self.bandas[nombre_banda].registrar_puntajes(puntajes)

    def listar_bandas(self):
        print("\n--- Bandas Inscritas ---")
        for banda in self.bandas.values():
            print(banda.mostrar_info())

    def ranking(self):
        print("\n--- Ranking Final ---")
        for banda in self.bandas.values():
            print(banda.mostrar_info())

class Ordenamiento:
    def quick_sort_bandas(self,bandas):
        if len(bandas) <= 1:
            return bandas

        pivote = bandas[0]
        menores = [b for b in bandas[1:] if b.promedio < pivote.promedio]
        iguales = [b for b in bandas[1:] if b.promedio == pivote.promedio]
        mayores = [b for b in bandas[1:] if b.promedio > pivote.promedio]

        return self.quick_sort_bandas(menores) + [pivote] + iguales + self.quick_sort_bandas(mayores)
if __name__ == "__main__":
    ConcursoBandasApp()