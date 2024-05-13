# from typing import Union
import plotly.graph_objs as go
import numpy as np
from srs.logisticmodeling.config import *
from srs.logisticshow.cosmetic import *

def find_free_place(placed_goods: list, car_dims: [int, int, int], last_dims: [int, int, int], dims: [int, int, int]):
    if len(placed_goods) == 0:
        return [0, 0, 0]
    last_xyz = placed_goods[-1][1]
    if last_xyz[2] + last_dims[2] + dims[2] < car_dims[2]:
        return last_xyz[0:2] + [last_xyz[2] + last_dims[2]]
    if last_xyz[1] + last_dims[1] + dims[1] < car_dims[1]:
        return [last_xyz[0], last_xyz[1] + last_dims[1], 0]
    if last_xyz[0] + last_dims[0] + dims[0] < car_dims[0]:
        return [last_xyz[0] + last_dims[0], 0, 0]
    return None

def show_cargo_filling(available_goods: dict, available_car: str) -> None:
    """Функция упаковывает груз по кузову грузовой машины и отображает расстановку
    В алгоритмы присутствуют следующие аспекты:
    1. Нельзя поместить товаров больше чем имеется
    2.
    :param available_goods: Перевозимые грузы {Название груза: Количество груза}
    :param available_car: Название грузовой машины"""
    if available_car not in TRUCKS.keys():
        raise ValueError(f"Название грузовой машины «{available_car}» не обнаружено в базе данных! Смотри config.py")
    for goods in available_goods:
        if goods not in CARGOS.keys():
            raise ValueError(f"Название груза «{available_car}» не обнаружено в базе данных! Смотри config.py")
    placed_goods = []

    for goods in available_goods.keys():
        while True:
            tmp = find_free_place(placed_goods=placed_goods, dims=CARGOS[goods].dims,
                                  car_dims=TRUCKS[available_car].dims,
                                  last_dims=CARGOS[placed_goods[-1][0]].dims if len(placed_goods) > 0 else [0, 0, 0])
            if tmp is None or available_goods[goods] <= 0:
                break
            placed_goods += [[goods, tmp]]
            available_goods[goods] -= 1

    # Вывод алгоритма
    my_print(f"В машину {available_car} помещено {len(placed_goods)} товаров:", "c")
    for goods in placed_goods:
        my_print(f"     {goods[0]}: [x={goods[1][0]}, y={goods[1][1]}, z={goods[1][2]}]", "b")

    def get_cube_mesh(pos: [int, int, int], dims: [int, int, int], color: str, name: str, alpha: float = OPACITY):
        # create points
        x, y, z = np.meshgrid(
            np.linspace(pos[0], pos[0]+dims[0], 2),
            np.linspace(pos[1], pos[1]+dims[1], 2),
            np.linspace(pos[2], pos[2]+dims[2], 2),
        )
        x = x.flatten()
        y = y.flatten()
        z = z.flatten()
        return go.Mesh3d(x=x, y=y, z=z, alphahull=1, flatshading=True, color=color, opacity=alpha, name=name)

    # Показ моделек
    data = [get_cube_mesh(pos=[0] * 3, dims=TRUCKS[available_car].dims, color='blue', name=available_car, alpha=0.1)]
    for goods in placed_goods:
        r0 = goods[1]
        r1 = CARGOS[goods[0]].dims
        data += [get_cube_mesh(pos=[r0[0] - dR, r0[1] - dR, r0[2] - dR], dims=[r1[0] - dR, r1[1] - dR, r1[2] - dR],
                               color=CARGOS[goods[0]].color, name=goods[0])]
    fig = go.Figure(data=data)
    fig.update_layout(showlegend=True)
    fig.show()

if __name__ == '__main__':
    show_cargo_filling(available_goods={"Кофемашина": 20000,
                                        "Мультиварка": 20,
                                        "Микроволновая печь": 100,
                                        },
                       available_car="DAF XF95 series")
