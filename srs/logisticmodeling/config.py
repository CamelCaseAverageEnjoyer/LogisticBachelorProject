# >>>>>>>>>>>> Параметры отображения <<<<<<<<<<<<
PRINT_ALL = True
VOXEL_RANGE = 100  # миллиметров
OPACITY = 0.3
dR = 20

# >>>>>>>>>>>> Параметры перевозимого груза <<<<<<<<<<<<
class Truck:
    def __init__(self, name: str, weight: int, dims: [int, int, int]):
        """Мини-класс для грузовых машин
        :param name: Название грузовой машины
        :param weight: Грузоподъёмность грузовой машины (в кг)
        :param dims: Габариты кузова: [длина, ширина, высота] (в миллиметрах)"""
        self.name = name
        self.weight = weight
        self.dims = dims.copy()

class Cargo:
    def __init__(self, name: str, net_weight: float, gross_weight: float, dims: [int, int, int], color: str,
                 value: int):
        """Мини-класс для перевозимого груза
        :param name: Название груза
        :param net_weight: Масса нетто (в кг)
        :param gross_weight: Масса брутто (в кг)
        :param dims: Габариты кузова: [длина, ширина, высота] (в миллиметрах)
        :param color: Цвет для отображения
        :param value: Стоимость груза (тыс. руб)"""
        self.name = name
        self.net_weight = net_weight
        self.gross_weight = gross_weight
        self.dims = dims.copy()
        self.color = color
        self.value = value

TRUCKS = {"Газель Next": Truck("Газель Next", 1500, [3360, 1809, 1881]),
          "Ford Transit": Truck("Ford Transit", 1200, [3494, 1748, 1886]),
          "ГАЗ Валдай": Truck("ГАЗ Валдай", 3500, [6100, 2176, 2200]),
          "МАЗ–4370 «Зубрёнок»": Truck("МАЗ–4370 «Зубрёнок»", 5000, [6220, 2480, 2310]),
          "MAN TGM 18.250": Truck("MAN TGM 18.250", 10000, [7490, 2490, 2923]),
          "DAF XF95 series": Truck("DAF XF95 series", 20000, [13600, 2450, 2600])}

CARGOS = {"Кофемашина": Cargo("Кофемашина", 8.0, 9.0, [600, 500, 600], color="brown", value=40),
          "Мультиварка": Cargo("Мультиварка", 14.0, 4.8, [550, 550, 550], color="green", value=50),
          "Микроволновая печь": Cargo("Микроволновая печь", 18.0, 19.5, [800, 700, 600], color="gray", value=60)}
