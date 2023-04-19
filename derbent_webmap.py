# IMPORTS
import geopandas as gpd
import folium
from folium import plugins


# READ DATA
boundary = gpd.read_file('./webmap_derbent/contents/city_boundary.geojson', encoding='UTF-8')
bound = gpd.read_file('./webmap_derbent/contents/city_boundary_lin.geojson', encoding='UTF-8')
unesco = gpd.read_file('./webmap_derbent/contents/unesco_ply.geojson', encoding='UTF-8')
dosmesto = gpd.read_file('./webmap_derbent/contents/dosmesto_lin.geojson', encoding='UTF-8')
okn = gpd.read_file('./webmap_derbent/contents/okn_ply.geojson', encoding='UTF-8')


# OKN CLASSIFICATION
o_federal = okn.loc[okn['Тип'] == 'ОКН федерального значения']
o_region = okn.loc[okn['Тип'] == 'ОКН регионального значения']
o_municip = okn.loc[okn['Тип'] == 'ОКН муниципальный']
o_find = okn.loc[okn['Тип'] == 'ОКН выявленный']
o_cgfo = okn.loc[okn['Тип'] == 'ИЦГФО']


# POINTS FOR HEATMAP AND CLUSTERING
okn_c = okn.centroid


# CREATING MAP
m = folium.Map(location=[boundary.centroid.y.mean(), boundary.centroid.x.mean()], zoom_start=13,
               tiles="cartodb positron", control_scale=True, min_zoom=11, max_zoom=20)


# ADD UNESCO BOUNDARY
unsc = folium.GeoJson(
    unesco,
    name="Зоны охраны ЮНЕСКО",
    style_function=lambda x: {
        "fillColor": '#ef7b5e',
        "weight": 0,
        "fillOpacity": 0.1,
    },
    zoom_on_click=False,
).add_to(m)

# ADD OKN POLYGONS
o_fed = folium.GeoJson(
    o_federal,
    name='ОКН Федерального значения',
    tooltip=folium.GeoJsonTooltip(fields=['Наименование']),
    popup=folium.GeoJsonPopup(fields=['Адрес', 'Наименование', 'Тип', 'Владелец',
                                      'Дата возникновения', 'Назначение', 'Состояние']),
    style_function=lambda x: {
        "fillColor": '#63031d',
        "weight": 0.1,
        "fillOpacity": 0.7,
    },
    zoom_on_click=True
)

o_reg = folium.GeoJson(
    o_region,
    name='ОКН регионального значения',
    tooltip=folium.GeoJsonTooltip(fields=['Наименование']),
    popup=folium.GeoJsonPopup(fields=['Адрес', 'Наименование', 'Тип', 'Владелец', 'Дата возникновения',
                                      'Назначение', 'Состояние']),
    style_function=lambda x: {
        "fillColor": '#af0636',
        "weight": 0.1,
        "fillOpacity": 0.7,
    },
    zoom_on_click=True
)

o_mun = folium.GeoJson(
    o_municip,
    name='ОКН муниципальный',
    tooltip=folium.GeoJsonTooltip(fields=['Наименование']),
    popup=folium.GeoJsonPopup(fields=['Адрес', 'Наименование', 'Тип', 'Владелец', 'Дата возникновения',
                                      'Назначение', 'Состояние']),
    style_function=lambda x: {
        "fillColor": '#cc654c',
        "weight": 0.1,
        "fillOpacity": 0.7,
    },
    zoom_on_click=True
)

o_fin = folium.GeoJson(
    o_find,
    name='ОКН выявленный',
    tooltip=folium.GeoJsonTooltip(fields=['Наименование']),
    popup=folium.GeoJsonPopup(fields=['Адрес', 'Наименование', 'Тип', 'Владелец', 'Дата возникновения',
                                      'Назначение', 'Состояние']),
    style_function=lambda x: {
        "fillColor": '#b27054',
        "weight": 0.1,
        "fillOpacity": 0.7,
    },
    zoom_on_click=True
)

o_cgf = folium.GeoJson(
    o_cgfo,
    name='Исторически ценные градоформирующие объекты',
    tooltip=folium.GeoJsonTooltip(fields=['Наименование']),
    popup=folium.GeoJsonPopup(fields=['Адрес', 'Наименование', 'Тип', 'Владелец', 'Дата возникновения',
                                      'Назначение', 'Состояние']),
    style_function=lambda x: {
        "fillColor": '#ea8a6e',
        "weight": 0.1,
        "fillOpacity": 0.7,
    },
    zoom_on_click=True,
)

# GROUP OKN FEATURES
OKN_all = folium.FeatureGroup(name='Объекты культурного наследия')
o_fed.add_to(OKN_all)
o_reg.add_to(OKN_all)
o_mun.add_to(OKN_all)
o_fin.add_to(OKN_all)
o_cgf.add_to(OKN_all)
OKN_all.add_to(m)


# ADD DOSTOPRIMECHATEL'NOYE MESTO'S BOUNDARY
dsms = folium.GeoJson(
    dosmesto,
    name="Зоны достопримечательного места",
    style_function=lambda x: {
        "color": '#ef7b5e',
        "weight": 2,
    },
    zoom_on_click=False,
).add_to(m)

# ADD CITY BOUNDARY
c_bnd = folium.GeoJson(
    bound,
    name="Границы города Дербент",
    style_function=lambda x: {
        "color": '#848f95',
        "weight": 2.5,
        "dashArray": 8
    },
    zoom_on_click=False,
).add_to(m)


# OKN CLUSTERS
okn_cl = folium.GeoJson(
    okn_c,
    marker=folium.vector_layers.CircleMarker(
        radius=1,
        fill_opacity=0,
        weight=0
    )
)
marker_cluster = plugins.MarkerCluster(name='Кластеры объектов культурного наследия')
mc1= folium.plugins.FeatureGroupSubGroup(marker_cluster, 'Кластеры объектов культурного наследия')
m.add_child(marker_cluster)
m.add_child(mc1)
mc1.add_child(okn_cl)


# PLUGINS AND SAVING FILE
folium.plugins.Fullscreen(
    position='topleft',
    title='Полноэкранный режим',
    title_cancel='Выйти из полноэкранного режима'
).add_to(m)

folium.plugins.Search(
    OKN_all,
    search_label='Name',
    geom_type='Polygon',
    search='Поиск ОКН по названию',
    position='topright'
).add_to(m)

folium.plugins.MousePosition(
    empty_string='нет данных',
    prefix='Координаты:',
    separator=';'
).add_to(m)

folium.plugins.MiniMap(
    tile_layer='cartodb positron',
    position='bottomleft',
    width='200',
    height='140',
    zoom_level_offset=-7,
).add_to(m)

folium.LayerControl().add_to(m)

m.save(r'webmap_derbent/example.html')