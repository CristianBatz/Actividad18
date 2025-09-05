import tkinter as tk

class ConcursoBandasApp:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Concurso de Bandas - Quetzaltenango")
        self.ventana.geometry("500x300")

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

        tk.Label(ventana_inscribir, text="Nombre de la banda:").pack(pady=5)
        entrada_nombre = tk.Entry(ventana_inscribir)
        entrada_nombre.pack(pady=5)

        def guardar():
            nombre = entrada_nombre.get()
            print(f"Banda inscrita: {nombre}")
            ventana_inscribir.destroy()

        tk.Button(ventana_inscribir, text="Guardar", command=guardar).pack(pady=10)

    def registrar_evaluacion(self):
        print("Se abrió la ventana: Registrar Evaluación")
        tk.Toplevel(self.ventana).title("Registrar Evaluación")

    def listar_bandas(self):
        print("Se abrió la ventana: Listado de Bandas")
        tk.Toplevel(self.ventana).title("Listado de Bandas")

    def ver_ranking(self):
        print("Se abrió la ventana: Ranking Final")
        tk.Toplevel(self.ventana).title("Ranking Final")

class Participante:
    def __init__(self,nombre,institucion):
        self.nombre = nombre
        self.institucion = institucion

    def mostrar_info(self):
        print(f"Nombre: {self.nombre}, Institucion: {self.institucion}" )

class BandaEscolar(Participante):
    Categorias_validas = ['Primaria', 'Básico', 'Diversificado']
    Criterios_validos = ['ritmo', 'uniformidad', 'coreografía', 'alineación', 'puntualidad']

    def __init__(self,nombre,institucion,categoria,puntuaje,promedio):
        super().__init__(nombre,institucion)
        self.set_categoria(categoria)
        self._puntuaje = puntuaje
        self.total = 0
        self.promedio = promedio
        self.registrar_puntaje = {}

    def set_categoria(self, categoria):
        if categoria not in self.Categorias_validas:
            raise ValueError(f"Categoría inválida: {categoria}")
        self._categoria = categoria

    def registrar_puntajes(self, puntajes):
        for criterio in self.Criterios_validos:
            if criterio not in puntajes:
                raise ValueError(f"Falta el criterio de evaluación: {criterio}")

        for criterio in puntajes:
            if criterio not in self.Criterios_validos:
                raise ValueError(f"Criterio inválido: {criterio}")

        for criterio, valor in puntajes.items():
            if not isinstance(valor, (int, float)) or not (0 <= valor <= 10):
                raise ValueError(f"Puntaje inválido en '{criterio}': {valor}")

        self._puntajes = puntajes

    def suma_puntajes(self):
        self.total += self._puntajes

    def promedio(self):
        self.promedio = self.total / len(self._puntajes)

    def mostrar_info(self):
        print(f"Nombre: {self.nombre}, Institucion: {self.institucion}, Categoria: {self._categoria}, Total: {self.total}")

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

if __name__ == "__main__":
    ConcursoBandasApp()