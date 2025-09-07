import tkinter as tk

class Participante:
    def __init__(self,nombre,institucion):
        self.nombre = nombre
        self.institucion = institucion

    def mostrar_info(self):
        print(f"Nombre: {self.nombre}, Institucion: {self.institucion}" )

class BandaEscolar(Participante):
    Categorias_validas = ['Primaria', 'Basico', 'Diversificado']
    Criterios_validos = ['ritmo', 'uniformidad', 'coreografía', 'alineación', 'puntualidad']

    def __init__(self,nombre,institucion,categoria,promedio = 0):
        super().__init__(nombre,institucion)
        self.set_categoria(categoria)
        self._puntajes = {}
        self.total = 0
        self.promedio = float(promedio)

    def set_categoria(self, categoria):
        categoria = categoria.strip().capitalize()
        if categoria not in self.Categorias_validas:
            raise ValueError(f"Categoría inválida: {categoria}")
        self._categoria = categoria

    def registrar_puntajes(self, puntajes):
        for criterio in BandaEscolar.Criterios_validos:
            if criterio not in puntajes:
                raise ValueError(f"Falta puntaje para el criterio: {criterio}")
            valor = puntajes[criterio]
            if not (0 <= valor <= 10):
                raise ValueError(f"Puntaje inválido para {criterio}: {valor}")
        self._puntajes = puntajes
        self.suma_puntajes()
        self.calcular_promedio()

    def suma_puntajes(self):
        self.total = sum(self._puntajes.values())

    def calcular_promedio(self):
        if self._puntajes:
            self.promedio = self.total / len(self._puntajes)
        else:
            self.promedio = 0

    def mostrar_info(self):
        if self._puntajes:
            return f"Nombre:{self.nombre}, Categoria:({self._categoria}), Instituto: {self.institucion} | Total: {self.total}"
        else:
            return f"Nombre:{self.nombre}, Categoria:({self._categoria}), Instituto: {self.institucion} | Sin evaluar"

class Concurso:
    def __init__(self,nombre,fecha):
        self.nombre = nombre
        self.fecha = fecha
        self.bandas = {}
        self.cargar_bandas()

    def cargar_bandas(self):
        try:
            with open("bandas.txt", "r", encoding="utf-8") as f:
                for linea in f:
                    linea = linea.strip()
                    if linea:
                        nombre, institucion, categoria, promedio = linea.split(":")
                        if promedio.strip() == "":
                            promedio_val = 0
                        else:
                            promedio_val = float(promedio)
                        banda = BandaEscolar(nombre, institucion, categoria,promedio_val)
                        self.bandas[nombre] = banda
            print("Bandas cargadas desde archivo.")
        except FileNotFoundError:
            print("Archivo no encontrado")
        except Exception as e:
            print("Error: cargando bandas desde archivo", e)

        self.cargar_puntajes()

    def cargar_puntajes(self):
        try:
            with open("puntajes.txt", "r", encoding="utf-8") as f:
                for linea in f:
                    datos = linea.strip().split(":")
                    nombre = datos[0]
                    if nombre in self.bandas:
                        puntajes = {
                            'ritmo': float(datos[1]),
                            'uniformidad': float(datos[2]),
                            'coreografía': float(datos[3]),
                            'alineación': float(datos[4]),
                            'puntualidad': float(datos[5])
                        }
                        self.bandas[nombre]._puntajes = puntajes
                        self.bandas[nombre].suma_puntajes()
                        self.bandas[nombre].calcular_promedio()
            print("Puntajes cargados desde archivo.")
        except FileNotFoundError:
            print("Archivo no encontrado")
        except Exception as e:
            print("Error: cargando puntuajes desde archivo", e)

    def guardar_bandas(self):
        with open("bandas.txt", "w", encoding="utf-8") as f:
            for banda in self.bandas.values():
                f.write(f"{banda.nombre}:{banda.institucion}:{banda._categoria}:{banda.promedio}\n")

    def guardar_puntajes(self):
        with open("puntajes.txt", "w", encoding="utf-8") as f:
            for banda in self.bandas.values():
                ritmo = banda._puntajes.get('ritmo', 0)
                uniformidad = banda._puntajes.get('uniformidad', 0)
                coreografia = banda._puntajes.get('coreografía', 0)
                alineacion = banda._puntajes.get('alineación', 0)
                puntualidad = banda._puntajes.get('puntualidad', 0)
                f.write(f"{banda.nombre}:{ritmo}:{uniformidad}:{coreografia}:{alineacion}:{puntualidad}\n")

    def inscribir_banda(self,banda):
        if banda.nombre in self.bandas:
            raise ValueError(f"La banda '{banda.nombre}' ya está inscrita.")
        self.bandas[banda.nombre] = banda
        self.guardar_bandas()

    def registrar_evaluacion(self, nombre_banda, puntajes):
        if nombre_banda not in self.bandas:
            raise ValueError(f"La banda '{nombre_banda}' no está inscrita.")
        self.bandas[nombre_banda].registrar_puntajes(puntajes)
        self.guardar_bandas()
        self.guardar_puntajes()

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
        mayores = [b for b in bandas[1:] if b.promedio > pivote.promedio]
        iguales = [b for b in bandas[1:] if b.promedio == pivote.promedio]
        menores = [b for b in bandas[1:] if b.promedio < pivote.promedio]

        return self.quick_sort_bandas(menores) + [pivote] + iguales + self.quick_sort_bandas(mayores)

class ConcursoBandasApp:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Concurso de Bandas - Quetzaltenango")
        self.ventana.geometry("500x300")
        self.ventana.config(bg="#2e2a2a")

        self.concurso = Concurso("Concurso 14 de Septiembre", "2025-09-14")
        self.menu()

        tk.Label(
            self.ventana,
            text="Sistema de Inscripción y Evaluación de Bandas Escolares\nConcurso 14 de Septiembre - Quetzaltenango",
            font=("Arial", 12, "bold"),
            justify="center",
            bg = "#2e2a2a",
            fg= "white"
        ).pack(pady=20)

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
        ventana_inscribir.geometry("450x250")
        ventana_inscribir.config(bg="#2e2a2a")

        tk.Label(ventana_inscribir, text="Nombre de la banda:",bg="#2e2a2a",fg= "white").place(x=30, y=30)
        entrada_nombre = tk.Entry(ventana_inscribir, bg="#b8b6b6")
        entrada_nombre.place(x=180, y=30)

        tk.Label(ventana_inscribir, text="Institución:",bg="#2e2a2a",fg= "white").place(x=30, y=70)
        entrada_inst = tk.Entry(ventana_inscribir, bg="#b8b6b6")
        entrada_inst.place(x=180, y=70)

        tk.Label(ventana_inscribir, text="Categoría (Primaria, Básico, Diversificado)",bg="#2e2a2a",fg= "white").place(x=130, y=110)
        entrada_cat = tk.Entry(ventana_inscribir, bg="#b8b6b6")
        entrada_cat.place(x=180, y=140)

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

        tk.Button(ventana_inscribir, text="Guardar", command=guardar,bg="#4a90e2",relief="raised",bd=4,activebackground="#357ABD",activeforeground="white").place(x=215, y=180)

    def registrar_evaluacion(self):
        ventana_eval = tk.Toplevel(self.ventana)
        ventana_eval.title("Registrar Evaluación")
        ventana_eval.geometry("460x350")
        ventana_eval.config(bg="#2e2a2a")

        tk.Label(ventana_eval, text="Nombre de la banda:",bg="#2e2a2a",fg= "white").pack()
        entrada_nombre = tk.Entry(ventana_eval, bg="#b8b6b6")
        entrada_nombre.pack()

        entradas = {}
        for criterio in BandaEscolar.Criterios_validos:
            tk.Label(ventana_eval, text=f"{criterio}:",bg="#2e2a2a",fg= "white").pack(pady=2)
            e = tk.Entry(ventana_eval, bg="#b8b6b6")
            e.pack(pady=2)
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

        tk.Button(ventana_eval, text="Guardar", command=guardar,bg="#4a90e2",relief="raised",bd=4,activebackground="#357ABD",activeforeground="white").pack(pady=10)

    def listar_bandas(self):
        ventana_listar = tk.Toplevel(self.ventana)
        ventana_listar.title("Listado de Bandas")
        ventana_listar.geometry("450x400")
        ventana_listar.config(bg="#2e2a2a")

        tk.Label(ventana_listar, text="--- Bandas Inscritas ---", font=("Arial", 12, "bold"),bg="#2e2a2a",fg= "white").pack(pady=5)

        for banda in self.concurso.bandas.values():
            tk.Label(ventana_listar, text=banda.mostrar_info(),bg="#2e2a2a",fg= "white").pack()

    def ver_ranking(self):
        ventana_ranking = tk.Toplevel(self.ventana)
        ventana_ranking.title("Ranking Final")
        ventana_ranking.geometry("450x400")
        ventana_ranking.config(bg="#2e2a2a")

        tk.Label(ventana_ranking, text="--- Ranking Final ---", font=("Arial", 12, "bold"),bg="#2e2a2a",fg= "white").pack(pady=5)

        ordenador = Ordenamiento()
        bandas_ordenadas = ordenador.quick_sort_bandas(list(self.concurso.bandas.values()))
        bandas_ordenadas.reverse()
        for banda in bandas_ordenadas:
            tk.Label(ventana_ranking, text=banda.mostrar_info(),bg="#2e2a2a",fg= "white").pack()


if __name__ == "__main__":
    ConcursoBandasApp()