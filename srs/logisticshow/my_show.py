# from typing import Union
import plotly.graph_objs as go
import numpy as np
from srs.logisticmodeling.config import *
from srs.logisticmodeling.my_math import *
from srs.logisticshow.cosmetic import *

def find_free_place(placed_goods: list, car_dims: [int, int, int], last_dims: [int, int, int], dims: [int, int, int],
                    flag_new_column: bool = False):
    if len(placed_goods) == 0:
        return [0, 0, 0]
    last_xyz = placed_goods[-1][1]
    if not flag_new_column and last_xyz[2] + last_dims[2] + dims[2] < car_dims[2]:
        return last_xyz[0:2] + [last_xyz[2] + last_dims[2]]
    if not flag_new_column and last_xyz[1] + last_dims[1] + dims[1] < car_dims[1]:
        return [last_xyz[0], last_xyz[1] + last_dims[1], 0]
    if last_xyz[0] + last_dims[0] + dims[0] < car_dims[0]:
        return [last_xyz[0] + last_dims[0], 0, 0]
    return None

def get_voxels_dims(dims: [int, int, int]):
    return [dims[i] // VOXEL_RANGE for i in range(3)]

def packaging(available_goods: dict, available_car: str, method: str = "strict") -> list:
    placed_goods = []

    if method == "strict":
        total_weight = 0.
        for goods in available_goods.keys():
            counter = 0
            for _ in range(available_goods[goods]):
                tmp = find_free_place(placed_goods=placed_goods, dims=CARGOS[goods].dims,
                                      car_dims=TRUCKS[available_car].dims,
                                      flag_new_column=True if counter == 0 else False,
                                      last_dims=CARGOS[placed_goods[-1][0]].dims if len(placed_goods) > 0
                                      else [0, 0, 0])
                total_weight += CARGOS[goods].gross_weight
                if tmp is None:
                    my_print(f"Товар {goods} не умещается!", "r")
                    # talk("Мало места!")
                    break
                elif total_weight > TRUCKS[available_car].weight:
                    total_weight -= CARGOS[goods].gross_weight
                    my_print(f"Товар {goods} слишком тяжёлый!", "r")
                    # talk("Перегруз!")
                    break
                else:
                    placed_goods += [[goods, tmp]]
                    counter += 1
            if counter > 0:
                my_print(f"Товаров {goods}: {counter} штук", "c")
        my_print(f"Общий вес: {total_weight} кг (Грузоподъёмность: {TRUCKS[available_car].weight} кг", "m")

    if method == "bruteforce":
        """Пока что нет поворота X и Y"""
        voxels = get_voxels_dims(dims=TRUCKS[available_car].dims)
        print(f"В машине {available_car} столько дециметров по каждому направлению: {voxels}")
        max_value = 0
        best_placed_goods = []

        all_goods = []
        for goods in available_goods.keys():
            all_goods += [goods] * available_goods[goods]
        all_goods_combinations = remove_equal_elements(list(all_combinations(all_goods)))
        if PRINT_ALL:
            print(f"Все комбинации: {all_goods_combinations}")

        for comb in all_goods_combinations:
            tmp_value = 0
            comb_dims = [get_voxels_dims(CARGOS[i].dims) for i in comb]
            if PRINT_ALL:
                print(f"{comb_dims}")
            # tmp = [[[[x, y, z] for _ in comb] for x in range(voxels[0]) for y in range(voxels[1])
            #        for z in range(voxels[2])] for _ in comb]

        placed_goods = best_placed_goods

    return placed_goods

def cylinder(x, y, z, r, dz, color: str, opacity: float = 0.5):
    """Create a cylindrical mesh located at x, y, z, with radius r and height dz"""
    center_z = np.linspace(0, dz, 15)
    theta = np.linspace(0, 2*np.pi, 15)
    theta_grid, z_grid = np.meshgrid(theta, center_z)
    x = r * np.cos(theta_grid) + x
    y = z_grid + y
    z = r * np.sin(theta_grid) + z
    return go.Mesh3d(x=x, y=y, z=z, alphahull=1, flatshading=True, color=color, opacity=opacity)

def get_cube_mesh(pos: [int, int, int], dims: [int, int, int], color: str, name: str, alpha: float = OPACITY):
    x, y, z = np.meshgrid(np.linspace(pos[0], pos[0]+dims[0], 2),
                          np.linspace(pos[1], pos[1]+dims[1], 2),
                          np.linspace(pos[2], pos[2]+dims[2], 2))
    x = x.flatten()
    y = y.flatten()
    z = z.flatten()
    return go.Mesh3d(x=x, y=y, z=z, alphahull=1, flatshading=True, color=color, opacity=alpha, name=name)

def show_cargo_filling(available_goods: dict, available_car: str, method: str = "strict",
                       show_params: str = "") -> None:
    """Функция упаковывает груз по кузову грузовой машины и отображает расстановку
    В алгоритмы присутствуют следующие аспекты:
    1. Нельзя поместить товаров больше чем имеется по объёбу и по массе
    2.
    :param available_goods: Перевозимые грузы {Название груза: Количество груза}
    :param available_car: Название грузовой машины
    :param method: Метод упаковки: {strict, bruteforce}
    :param show_params: Список экстра-отображения"""
    if available_car not in TRUCKS.keys():
        raise ValueError(f"Название грузовой машины «{available_car}» не обнаружено в базе данных! Смотри config.py")
    for goods in available_goods:
        if goods not in CARGOS.keys():
            raise ValueError(f"Название груза «{goods}» не обнаружено в базе данных! Смотри config.py")
    if method not in ["strict", "bruteforce"]:
        raise ValueError(f"Метод «{method}» не подходит. Смотри описание!")

    # Решение задачи упаковки
    placed_goods = packaging(available_goods=available_goods, available_car=available_car, method=method)

    # Вывод алгоритма
    my_print(f"В машину {available_car} помещено {len(placed_goods)} товаров", "c")
    if PRINT_ALL:
        for goods in placed_goods:
            my_print(f"     {goods[0]}: [x={goods[1][0]}, y={goods[1][1]}, z={goods[1][2]}]", "b")

    # Показ моделек
    if method == "strict":
        head = 0.7 if "колёса" in show_params else 0
        whl_r = 500 if "колёса" in show_params else 0
        whl_h = 300 if "колёса" in show_params else 0
        dim = TRUCKS[available_car].dims
        data = [get_cube_mesh(pos=[0]*3, dims=dim, color='blue', name=available_car, alpha=0.1),
                get_cube_mesh(pos=[0, dim[1]*(1-head)/2, 0],
                              dims=[-dim[1]*head, dim[1]*head, dim[1]*head],
                              color='grey', name=available_car, alpha=0.4)]
        for seq in [[-1, -1], [-1, 1], [1, -1], [1, 1]]:
            # data += [cylinder(dim[0], dim[1]/2 + dim[1]/2*seq[1], 0, whl_r, whl_h*seq[1], color='grey', opacity=0.8)]
            data += [get_cube_mesh(pos=[dim[0]/2 + seq[0]*dim[0]/4 - whl_r/2, dim[1]/2 + dim[1]/2*seq[1], whl_r/2],
                                   dims=[whl_r, seq[1]*whl_h, -whl_r], color='grey', name=available_car, alpha=0.4)]
        annotation = []
        for goods in placed_goods:
            r0 = goods[1]
            r1 = CARGOS[goods[0]].dims
            data += [get_cube_mesh(pos=[r0[0] - dR, r0[1] - dR, r0[2] - dR], dims=[r1[0] - dR, r1[1] - dR, r1[2] - dR],
                                   color=CARGOS[goods[0]].color, name=goods[0])]

            if "свободное место" in show_params:
                flag_top = True  # Проверка на верхний элемент
                flag_wide = True  # Проверка на боковой элемент
                flag_line = True  # Проверка на продольное заполнение
                for other_good in placed_goods:
                    flag_line = False if other_good[1][0] > goods[1][0] else flag_line
                    flag_wide = False if other_good[1][1] > goods[1][1] and other_good[1][0] == goods[1][0] else flag_wide
                    flag_top = False if other_good[1][2] > goods[1][2] and other_good[1][0] == goods[1][0] and \
                        other_good[1][1] == goods[1][1] else flag_top
                for i in range(3):
                    if [flag_line, flag_wide, flag_top][i]:
                        x = np.array([r0[0]+r1[0] - dR, TRUCKS[available_car].dims[0]] if i == 0 else
                                     [r0[0]+r1[0]/2, r0[0]+r1[0]/2])
                        y = np.array([r0[1]+r1[1] - dR, TRUCKS[available_car].dims[1]] if i == 1 else
                                     [r0[1]+r1[1]/2, r0[1]+r1[1]/2])
                        z = np.array([r0[2]+r1[2] - dR, TRUCKS[available_car].dims[2]] if i == 2 else
                                     [r0[2]+r1[2]/2, r0[2]+r1[2]/2])
                        txt = f"{(TRUCKS[available_car].dims[i] - (r0[i]+r1[i])) // 10} cм"
                        annotation += [dict(showarrow=False, x=(x[0]+x[1])/2, y=(y[0]+y[1])/2, z=(z[0]+z[1])/2,
                                            text=txt, xanchor="left", xshift=2, opacity=0.7)]
                        data += [go.Scatter3d(x=x, y=y, z=z, mode='lines+markers',
                                              marker=dict(size=2, color=["red", "green", "blue"][i]),
                                              name=f"Место{[' продольное', ' сбоку', ' сверху'][i]}: " + txt)]
        fig = go.Figure(data=data)
        fig.update_layout(showlegend=True, scene=dict(annotations=annotation,
                                                      aspectmode='manual',
                                                      aspectratio=dict(x=1,
                                                                       y=(dim[1] + whl_h*2) / (dim[0] + dim[1]*head),
                                                                       z=(dim[2] + whl_r/2) / (dim[0] + dim[1]*head))))
        fig.show()

if __name__ == '__main__':
    show_cargo_filling(available_car=["Газель Next", "Ford Transit", "ГАЗ Валдай", "MAN TGM 18.250",
                                      "DAF XF95 series"][3],
                       show_params=["", "свободное место", "колёса", "колёса, свободное место"][0],
                       method=["strict", "bruteforce"][0],  # работает только метод strict
                       available_goods={
                           # Москва - СПБ [MAN TGM 18.250]
                           "Кофемашина": 48,
                           "Мультиварка": 60,
                           "Микроволновая печь": 60,
                           # СПБ- Великий новгород - Тверь - Москва [MAN TGM 18.250]
                           # "Тормозные колодки и диски": 504,
                           # "Сальники и манжеты": 500,
                           # "Свечи зажигания": 650,
                           # Москва - Екатеринбург - Чеблябинск [MAN TGM 18.250]
                           # "Электрочайники": 198,
                           # "Малый набор инструментов": 224,
                           # "Средний набор инструментов": 108,
                           # "Большой набор инструментов": 56,
                           # "Профессиональный набор инструментов": 60,
                           # Екатеринбург - Чеблябинск - Казань - Нижний Новгород - Москва [MAN TGM 18.250]
                           # "Крепежные детали": 36,
                           # "Запчасти для насосов 1": 112,
                           # "Запчасти для насосов 2": 108,
                           # "Стоматологические фрезы": 112,
                           # "Комплектующие пылесосов 1": 112,
                           # "Комплектующие пылесосов 2": 108,
                       })
    # talk()
