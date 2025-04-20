from facilibras.dependencias.dal import T_ExercicioDAO


class ExercicioControle:
    def __init__(self, dao: T_ExercicioDAO) -> None:
        self.dao = dao

    def listar_exercicios(self):
        return self.dao.listar()
    
    def listar_exercicios_por_categoria(self):
        ...

    def listar_categorias(self):
        ...
