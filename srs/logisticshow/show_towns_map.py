import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

from shapely.ops import snap
from shapely.geometry.polygon import Polygon
from shapely.geometry.multipolygon import MultiPolygon

from srs.logisticshow.map_figure import mapFigure


def prepare_regions(gdf, area_thr=100e6, simplify_tol=500):
    """Подготовка регионов к построению

    - Упрощение геометрии с допуском simplify_tol
    - Удаление полигонов с площадью менее area_thr
    """
    gdf_ = gdf.copy()

    # Вспомогательный столбец для упорядочивания регионов по площади
    gdf_['area'] = gdf_.geometry.apply(lambda x: x.area)

    # Удаляем маленькие полигоны
    tqdm.pandas(desc='Удаление мелких полигонов')
    gdf_.geometry = gdf_.geometry.progress_apply(lambda geometry:
                                                 MultiPolygon([p for p in geometry.geoms if p.area > area_thr])
                                                 if type(geometry) == MultiPolygon else geometry
                                                 )

    # Упрощение геометрии
    gdf_.geometry = gdf_.geometry.simplify(simplify_tol)

    geoms = gdf_.geometry.values
    pbar = tqdm(enumerate(geoms), total=len(geoms))
    pbar.set_description_str('Объединение границ после упрощения')
    # проходим по всем граничащим полигонам и объединяем границы
    for i, g in pbar:
        g1 = g
        for g2 in geoms:
            if g1.distance(g2) < 100:
                g1 = snap(g1, g2, 800)
        geoms[i] = g1
    gdf_.geometry = geoms

    # сортировка по площади
    gdf_ = gdf_.sort_values(by='area', ascending=False).reset_index(drop=True)

    return gdf_.drop(columns=['area'])

def geom2shape(g):
    """Преобразование полигонов и мультиполигонов в plotly-readable шэйпы

    Получает на вход Polygon или MultiPolygon из geopandas,
    возвращает pd.Series с координатами x и y
    """
    # Если мультиполигон, то преобразуем каждый полигон отдельно, разделяя их None'ами
    if type(g) == MultiPolygon:
        x, y = np.array([[], []])
        for poly in g.geoms:
            x_, y_ = poly.exterior.coords.xy
            x, y = (np.append(x, x_), np.append(y, y_))
            x, y = (np.append(x, None), np.append(y, None))
        x, y = x[:-1], y[:-1]
    # Если полигон, то просто извлекаем координаты
    elif type(g) == Polygon:
        x, y = np.array(g.exterior.coords.xy)
    # Если что-то другое, то возвращаем пустые массивы
    else:
        x, y = np.array([[], []])
    return pd.Series([x, y])


'''gdf = gpd.read_file("data/russia_regions.geojson")

# Упрощение геометрии
regions = prepare_regions(gdf)
# Преобразование полигонов в шейпы
regions[['x', 'y']] = regions.geometry.progress_apply(geom2shape)
# Запись на диск
regions.to_parquet('data/russia_regions.parquet')'''

# gdf.plot()

russia_map = mapFigure()
russia_map.show()

# i = 61  # Калининградская область
# tol = 50
# p = gpd.GeoSeries(gdf.geometry[i])
# p.plot("Blues")

plt.title('Default. Cylindric CRS')
plt.show()
