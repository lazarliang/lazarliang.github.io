# Состав команды: 
Лян Лазарь, Скопин Артемий, Шурупова Анна, Сурогина Галина
# Ссылка на карту:
https://lazarliang.github.io/ 
# Краткая информация о городе: 
Город Дербент располагается на юге России в Республике Дагестан, численность населения города 123 700 человек. Он является самым древним российским городом, первое поселение  Куро-Аракской культуры, возникло здесь в эпоху ранней бронзы пять тысяч лет назад. Дербент — историческое поселение федерального значения и один из наиболее сохранившихся исторических городов России.
В городе присутствует многообразие объектов культурного значения различных типов: федеральные (40 объектов), региональные (68 объектов), муниципальные (3 объекта), выявленные (5 объектов) . Также существует перечень и исторически ценных градоформирующих объектов (ИЦГФО) — это те здания и сооружения, которые формируют историческую застройку и объединены в том числе масштабом, объемом, структурой, стилем, конструктивными материалами, цветовым решением и декоративными элементами (168 объектов). Международный охранный статус имеют цитадель «Нарын-Кала» и историческая часть города, включенные в список памятников Всемирного Наследия ЮНЕСКО в 2003 г.
# Описание используемых данных с указанием источников:
Данные по объектам культурного наследия были взяты с сайта управления архитектуры и градостроительства г. Дербент:  https://makederbent.ru/heritage1. Путем геокодирования был получен точечный слой со следующими атрибутами: адресом, категорией памятника, годом строительства. Далее точки были присоединены к полигональному слою зданий и вручную скорректированы по спутниковым снимкам. Слой был дополнен информацией из кадастровой карты (https://pkk.rosreestr.ru/)  о виде собственности объекта, данными с Яндекс панорам (http://yandex.ru/maps) о  состоянием объекта и данными с Яндекс и 2ГИС (https://2gis.ru/derbent) о назначении объекта.
# Описание проделанной работы и основные методы:
**Этап 1:** Были подготовлены обязательные тематические слои: административные границы, ОКН - объекты капитального строительства (полигоны зданий/памятников), дополнительно добавлены слои обозначающие границу зон достопримечательного места, относящихся к исторической части города, и границу зоны охраны ЮНЕСКО.  Перед написанием кода слои были приведены в “user-friendly” вид: таблица атрибутов проверена на предмет ошибок и согласованности категорий, исправлена геометрия. После файлы были переведены в geojson, а все их значения были переведены для русский в целях наиболее удобного восприятия информации. 

**Этап 2:** Далее в программе PyCharm был написан код с использованием библиотеки folium, результатом которого стала веб-карта. Для нее были настроены следующие характеристики:

✅ категоризация полигонов зданий ОКН по цветам в зависимости от категории объекта (федеральные, региональные, местные, выявленные, ИЦГФО)

✅ при наведении курсора на полигоны ОКН отображается наименование объекта и время постройки, при нажатии на объект откроется pop-up, содержащий более подробное описание характеристик объекта, представленное в виде таблицы со столбцами: адрес, наименование объекта, тип (категория объекта), владелец объекта, дата возникновения объекта, назначение и состояние объекта. 

✅ в левом нижнем углу веб-карты добавлена легенда для представленных на карте слоев

✅ настроено агрегирование полигонов ОКН

✅ настроены элементы управления интерактивной картой: Layer Control, Mouse Position, Fullscreen, Mini Map, Search (по названию ОКН)

✅ настроена регулярная сетка, отражающая концентрацию количества объектов ОКН на территории 

# Что было самым сложным в работе
Сложности возникли с созданием собственной подложки и настройкой переключения слоев подложки в зависимости от зума: 
- у *folium* отсутствует функционал управления слоями в зависимости от уровня зума, а времени на изучение javascript и html в контексте текущих дедлайнов попросту не было :(
- плохо работает подключение векторных тайлов: необходимая для экономии ресурсов береговая линия с MapTiler отказывалась прогружаться (был использован *folium.plugins.VectorGridProtobuf*)

Также не удалось построить heatmap для отображения концентрации взамен/вместе с регулярной четырехугольной сеткой, поскольку были проблемы со считыванием координат:
- *"Error: setting an array element with a sequence. The requested array has an inhomogeneous shape after 1 dimensions. The detected shape was (284,) + inhomogeneous part"*
- либо же *plugins.folium.Heatmap()* воспринимал данные ему широту и долготу как текст, а не число

# Что получилось в работе и вы можете этим гордиться
Получилось:

**- добавить легенду для обозначений ОКН**

```python
folium.plugins.FloatImage(
    image='https://i.ibb.co/njtKPzn/city-boundary.png',
    bottom=12,
    left=0.75,
    width='225px',
    height='30px'
).add_to(m) 

```

**- настроить категоризацию зданий по цветам в зависимости от их типа**

```python
o_federal = okn.loc[okn['Тип'] == 'ОКН федерального значения']
o_region = okn.loc[okn['Тип'] == 'ОКН регионального значения']
o_municip = okn.loc[okn['Тип'] == 'ОКН муниципальный']
o_find = okn.loc[okn['Тип'] == 'ОКН выявленный']
o_cgfo = okn.loc[okn['Тип'] == 'ИЦГФО']

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

# GROUP OKN FEATURES
OKN_all = folium.FeatureGroup(name='Объекты культурного наследия')
o_fed.add_to(OKN_all)
o_reg.add_to(OKN_all)
o_mun.add_to(OKN_all)
o_fin.add_to(OKN_all)
o_cgf.add_to(OKN_all)
OKN_all.add_to(m)

```

**- создать информативный веб-сайт, отражающий многочисленные характеристики объектов ОКН**

# Что не получилось и почему
Из-за ограничений folium много времени ушло на попытки создания собственной векторной подложки, которая по итогу не присутствует на веб-сайте
Ввиду этого мы не успели подготовить некоторые дополнительные тематические картограммы, посвященные степени изношенности объектов ОКН и эпохе их возникновения
