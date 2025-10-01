import FreeSimpleGUI as sg
import re
import pandas as pd

from datetime import datetime
from sqlalchemy import create_engine
import numpy as np

from GUI import SunPreparing
from GUI.layouts import *
from GUI.setup import *


codeIndex = ["DST", "KP"]

kp_types_final = [0, 0.33, 0.67, 1, 1.33, 1.67, 2, 2.33, 2.67,
                  3, 3.33, 3.67, 4, 4.33, 4.67, 5, 5.33, 5.67,
                  6, 6.33, 6.67, 7, 7.33, 7.67, 8, 8.33, 8.67, 9]

kp_types_raw = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
                13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                26, 27]


# TODO: Сделать выбор спутников для модели


# Вспомогательная функция для чтения из БД
def code_condition(code: list):
    match len(code):
        case 1:
            return f"CODE = '{code[0]}'"
        case 2:
            return f"CODE = '{code[0]}' OR CODE = '{code[1]}'"
        case 3:
            return f"CODE = '{code[0]}' OR CODE = '{code[1]}' OR CODE = '{code[2]}'"


# 4 Функции для чтения из БД
def prepare_query(
        date1: float | int,
        date2: float | int,
        lat1: float | int,
        lat2: float | int,
        lon1: float | int,
        lon2: float | int,
        code: list[str]
) -> str:
    selectquery = f"""
SELECT 
    CODE,
    DATE,
    latitude,
    longitude,
    radius,
    n,
    e,
    c,
    f
FROM `geomag`.`sat_sec_plain`
WHERE 
{code_condition(code)}
AND
DATE >= {str(date1)} AND DATE < {str(date2)}
AND
latitude >= {str(lat1)} AND latitude < {str(lat2)}
AND
longitude >= {str(lon1)} AND longitude < {str(lon2)}
                """

    return selectquery


def prepare_query_index(date1, date2, code):
    selectquery = r"SELECT CODE, DATE, value " + \
                  "FROM `geomag`.`index` WHERE "

    temp = 'CODE = "' + code[0] + '"'

    for i in range(1, len(code)):
        temp = temp + ' OR CODE = "' + code[i] + '"'

    # selectquery = selectquery + temp
    selectquery = selectquery + '(' + temp + ')'

    selectquery = selectquery + ' AND DATE >= ' + str(date1)
    selectquery = selectquery + ' AND DATE < ' + str(date2)

    return selectquery


def download_data_from_sql(date1, date2, dbConnect, code, lat1=-90, lat2=+90, long1=-180, long2=+180):
    d1 = datetime.strptime(date1, "%Y-%m-%d").timestamp()
    d2 = datetime.strptime(date2, "%Y-%m-%d").timestamp()

    selectquery = prepare_query(d1, d2, lat1, lat2, long1, long2, code)

    frame = pd.read_sql(selectquery, dbConnect)

    #     frame.to_pickle('data/SWARM_sec_{}_{}.pkl'.format(date1, date2))
    return frame


def download_data_from_sql_index(date1, date2, dbConnect, code):
    d1 = datetime.strptime(date1, "%Y-%m-%d").timestamp()
    d2 = datetime.strptime(date2, "%Y-%m-%d").timestamp()

    selectquery = prepare_query_index(d1, d2, code)

    frame = pd.read_sql(selectquery, dbConnect)

    #     frame.to_pickle('data/SWARM_sec_{}_{}.pkl'.format(date1, date2))
    return frame


# Валидаторы
def month_validator(answer, text):
    if len(answer.split()) == 0:
        sg.popup("Неверное значение", f"Не введено значение для '{text}'")
        return False

    if not re.match("^[0-9]+$", answer.split()[0]):
        sg.popup("Неверное значение", f"Введите целое число для '{text}'")
        return False

    if int(answer.split()[0]) < 1 or int(answer.split()[0]) > 12:
        sg.popup("Неверное значение", f"Номер месяца должен быть от 1 до 12 для '{text}'")
        return False

    return True


def year_validator(answer, text):
    if len(answer.split()) == 0:
        sg.popup("Неверное значение", f"Не введено значение для '{text}'")
        return False

    if not re.match("^[0-9]+$", answer.split()[0]):
        sg.popup("Неверное значение", f"Введите целое число для '{text}'")
        return False

    return True


def zeta_validator(answer, text):
    if len(answer.split()) == 0:
        sg.popup("Неверное значение", f"Не введено значение для '{text}'")
        return False

    if not re.match("[+-]?([0-9]*[.])?[0-9]+", answer.split()[0]):
        sg.popup("Неверное значение", f"Введите действительное число для '{text}'")
        return False

    if float(answer.split()[0]) < -90 or float(answer.split()[0]) > 90:
        sg.popup("Неверное значение", f"Угол должен быть от -90 до 90 для '{text}'")
        return False

    return True


def double_positive_validator(answer, text):
    if len(answer.split()) == 0:
        sg.popup("Неверное значение", f"Не введено значение для '{text}'")
        return False

    if not re.match("[+-]?([0-9]*[.])?[0-9]+", answer.split()[0]):
        sg.popup("Неверное значение", f"Введите действительное число для '{text}'")
        return False

    if float(answer.split()[0]) <= 0:
        sg.popup("Неверное значение", f"Значение должно быть больше 0 для '{text}'")
        return False

    return True


def coord_validator(answer, text):
    if len(answer.split()) == 0:
        sg.popup("Неверное значение", f"Не введено значение для '{text}'")
        return False

    if not re.match(r'^(-?(?:180(?:\.0+)?|1[0-7][0-9](?:\.[0-9]+)?|[0-9]?[0-9](?:\.[0-9]+)?))$', answer.split()[0]):
        sg.popup("Неверное значение", f"Введите действительное число для '{text}'")
        return False

    return True


ip, login, password, \
    satellites, \
    start_month, start_year, end_month, end_year, \
    sun_angle, f_nec_diff, dst_diff, ddst_diff, kp_max, \
    lat_1, lat_2, lon_1, lon_2, \
    l_max, century = open_setup_file()

# Основное окно, открывающееся при запуске программы
window = sg.Window("Data selection", layout, icon="GCRAS_logo_rus_curves.ico")

# История окон, необходимая для переключения между ними
layouts_history = ["-MAIN_LAYOUT-"]

while True:

    event, values = window.read()
    print(event, values)

    # Остановка программы при закрытии окна
    if event == sg.WIN_CLOSED:
        break

    # Обработка кнопки с настройками БД
    if event == "-DB_SETTINGS_MENU_BUTTON-":
        # Добавляем в историю окон, что мы тут были
        layouts_history.append("-DB_SETTINGS_LAYOUT-")
        # Прячем предыдущее окно
        window[layouts_history[-2]].update(visible=False)
        # Показываем текущее окно
        window[layouts_history[-1]].update(visible=True)
        # Применяем изменения
        window.refresh()

        # Далее анолоничные действия имеют аналогичный эффект

    # Обработка кнопки с изменением настроек БД
    if event == "-CHANGE_DB_SETTINGS_BUTTON-":
        layouts_history.append("-DB_SETTINGS_CHANGE_LAYOUT-")
        window[layouts_history[-2]].update(visible=False)
        window[layouts_history[-1]].update(visible=True)
        window.refresh()

    # Обработка кнопки с сохранением параметров БД
    if event == "-SAVE_DB_SETTINGS_BUTTON-":
        # Аналогично с изменением параметров отбора

        ip = values["-DB_SETTINGS_IP_INPUT-"]
        login = values["-DB_SETTINGS_LOGIN_INPUT-"]
        password = values["-DB_SETTINGS_PASSWORD_INPUT-"]

        window["-DB_SETTINGS_IP-"].update(values["-DB_SETTINGS_IP_INPUT-"])
        window["-DB_SETTINGS_LOGIN-"].update(values["-DB_SETTINGS_LOGIN_INPUT-"])
        window["-DB_SETTINGS_PASSWORD-"].update(values["-DB_SETTINGS_PASSWORD_INPUT-"])

        save_setup_file(ip, login, password,
                        satellites,
                        start_month, start_year, end_month, end_year,
                        sun_angle, f_nec_diff, dst_diff, ddst_diff, kp_max,
                        lat_1, lat_2, lon_1, lon_2,
                        l_max, century)

        page = layouts_history.pop()
        window[page].update(visible=False)
        window[layouts_history[-1]].update(visible=True)
        window.refresh()

    # Обработка кнопки с проверкой подключения
    if event == "-CHECK_CONNECTION_BUTTON-":
        # Пытаемся создать подключение и подключиться
        try:
            sqlEngine = create_engine(f"mysql+pymysql://{login}:{password}@{ip}", pool_recycle=3600)
            dbConnection = sqlEngine.connect()
            dbConnection.close()
            sg.popup("Проверка доступа к базе данных", "Проверка доступа к базе данных пройдена успешна")

        # Если не получилось, выбрасываем ошибку
        except Exception as e:
            sg.popup("Произошла ошибка", f"Подключение не установлено\n{e}")

    # Обработка кнопки со спутниками
    if event == "-SATELLITE_SETTINGS_MENU_BUTTON-":
        layouts_history.append("-SATELLITE_SETTINGS_LAYOUT-")
        window[layouts_history[-2]].update(visible=False)
        window[layouts_history[-1]].update(visible=True)
        window.refresh()

    # Обработка кнопки с изменением спутников
    if event == "-CHANGE_SATELLITE_SETTINGS_BUTTON-":
        layouts_history.append("-SATELLITE_SETTINGS_CHANGE_LAYOUT-")
        window[layouts_history[-2]].update(visible=False)
        window[layouts_history[-1]].update(visible=True)
        window.refresh()

    # Обработка кнопки с сохранением параметров спутников
    if event == "-SAVE_SATELLITE_SETTINGS_BUTTON-":
        satellites = []
        if values["-SWA-"]:
            satellites.append("SWA")

        if values["-SWB-"]:
            satellites.append("SWB")

        if values["-SWC-"]:
            satellites.append("SWC")

        if values["-MSS-1-"]:
            satellites.append("MSS-1")

        if values["-MSS-2-"]:
            satellites.append("MSS-2")

        save_setup_file(ip, login, password,
                        satellites,
                        start_month, start_year, end_month, end_year,
                        sun_angle, f_nec_diff, dst_diff, ddst_diff, kp_max,
                        lat_1, lat_2, lon_1, lon_2,
                        l_max, century)

        window["-SATELLITE_SETTINGS-"].update("\n".join(satellites))

        page = layouts_history.pop()
        window[page].update(visible=False)
        window[layouts_history[-1]].update(visible=True)
        window.refresh()

    # Обработка кнопки с настройками отбора
    if event == "-DATA_SETTINGS_MENU_BUTTON-":
        layouts_history.append("-DATA_SETTINGS_LAYOUT-")
        window[layouts_history[-2]].update(visible=False)
        window[layouts_history[-1]].update(visible=True)
        window.refresh()

    # Обработка кнопки с изменением настроек отбора
    if event == "-CHANGE_DATA_SETTINGS_BUTTON-":
        layouts_history.append("-DATA_SETTINGS_CHANGE_LAYOUT-")
        window[layouts_history[-2]].update(visible=False)
        window[layouts_history[-1]].update(visible=True)
        window.refresh()

    # Обработка кнопки с сохранением настроек отбора
    if event == "-SAVE_DATA_SETTINGS_BUTTON-":
        no_errors = True

        # Проверка правильности начального месяца из строки ввода
        if month_validator(values["-START_MONTH_INPUT-"], "Номер месяца начала исследуемого периода"):
            # Обновляем месяц в переменной
            start_month = int(values["-START_MONTH_INPUT-"].split()[0])
            # Меняем месяц в приложении
            window["-START_MONTH-"].update(start_month)
        else:
            # Если возникла ошибка
            no_errors = False
            # Возвращаем в строку ввода старое значение
            window["-START_MONTH_INPUT-"].update(start_month)

        # Аналогично для месяца и года конца интервала

        # Проверка правильности начального года из строки ввода
        if year_validator(values["-START_YEAR_INPUT-"], "Номер года начала исследуемого периода"):
            start_year = int(values["-START_YEAR_INPUT-"].split()[0])
            window["-START_YEAR-"].update(start_year)
        else:
            no_errors = False
            window["-START_YEAR_INPUT-"].update(start_year)

        # Проверка правильности конечного месяца из строки ввода
        if month_validator(values["-END_MONTH_INPUT-"], "Номер месяца конца исследуемого периода"):
            end_month = int(values["-END_MONTH_INPUT-"].split()[0])
            window["-END_MONTH-"].update(end_month)
        else:
            no_errors = False
            window["-END_MONTH_INPUT-"].update(end_month)

        # Проверка правильности конечного года из строки ввода
        if year_validator(values["-END_YEAR_INPUT-"], "Номер года конца исследуемого периода"):
            end_year = int(values["-END_YEAR_INPUT-"].split()[0])
            window["-END_YEAR-"].update(end_year)
        else:
            no_errors = False
            window["-END_YEAR_INPUT-"].update(end_year)

        # Проверка правильности угла солнца из строки ввода
        if zeta_validator(values["-ZETA_0_INPUT-"], "Угол положения солнца над уровнем горизонта"):
            sun_angle = float(values["-ZETA_0_INPUT-"])
            window["-ZETA_0-"].update(sun_angle)
        else:
            no_errors = False
            window["-ZETA_0_INPUT-"].update(sun_angle)

        # Проверка правильности разницы разницы векторных и скалярных измерения
        if double_positive_validator(values["-F_NEC_DIFF_INPUT-"],
                                     "Максимальное отклонение векторный измерений от скалярных (модуль разности) [нТл]"):
            f_nec_diff = float(values["-F_NEC_DIFF_INPUT-"])
            window["-F_NEC_DIFF-"].update(f_nec_diff)
        else:
            no_errors = False
            window["-F_NEC_DIFF_INPUT-"].update(f_nec_diff)

        # Проверка правильности максимального DST индекса
        if double_positive_validator(values["-DST_DIFF_INPUT-"], "Максимальное значение Dst индекса"):
            Dst_diff = float(values["-DST_DIFF_INPUT-"])
            window["-DST_DIFF-"].update(Dst_diff)
        else:
            no_errors = False
            window["-DST_DIFF_INPUT-"].update(dst_diff)

        # Проверка правильности максимальной производной DST индекса (dDST)
        if double_positive_validator(values["-DDST_DIFF_INPUT-"],
                                     "Максимальное значение dDst индекса (производная Dst по времени)"):
            ddst_diff = float(values["-DDST_DIFF_INPUT-"])
            window["-DDST_DIFF-"].update(ddst_diff)
        else:
            no_errors = False
            window["-DDST_DIFF_INPUT-"].update(ddst_diff)

        # Проверка правильности максимального Kp индекса
        if double_positive_validator(values["-KP_MAX_INPUT-"], "Максимальное значение Kp индекса"):
            kp_max = float(values["-KP_MAX_INPUT-"])
            window["-KP_MAX-"].update(kp_max)
        else:
            no_errors = False
            window["-KP_MAX_INPUT-"].update(kp_max)

        if coord_validator(values["-MIN_LAT_INPUT-"], "Минимальная широта"):
            lat_1 = float(values["-MIN_LAT_INPUT-"])
            window["-MIN_LAT-"].update(lat_1)
        else:
            no_errors = False
            window["-MIN_LAT_INPUT-"].update(lat_1)

        if coord_validator(values["-MAX_LAT_INPUT-"], "Максимальная широта"):
            lat_2 = float(values["-MAX_LAT_INPUT-"])
            window["-MAX_LAT-"].update(lat_2)
        else:
            no_errors = False
            window["-MAX_LAT_INPUT-"].update(kp_max)

        if coord_validator(values["-MIN_LON_INPUT-"], "Минимальная долгота"):
            lon_1 = float(values["-MIN_LON_INPUT-"])
            window["-MIN_LON-"].update(lon_1)
        else:
            no_errors = False
            window["-MIN_LON_INPUT-"].update(lon_1)

        if coord_validator(values["-MAX_LON_INPUT-"], "Максимальная долгота"):
            lon_2 = float(values["-MAX_LON_INPUT-"])
            window["-MAX_LON-"].update(lon_2)
        else:
            no_errors = False
            window["-MAX_LON_INPUT-"].update(lon_2)

        # Сохраняем обновленные параметры в файл setup/setup
        save_setup_file(ip, login, password,
                        satellites,
                        start_month, start_year, end_month, end_year,
                        sun_angle, f_nec_diff, dst_diff, ddst_diff, kp_max,
                        lat_1, lat_2, lon_1, lon_2,
                        l_max, century)

        # Если нет ошибок
        if no_errors:
            # Удаляем из истории окно изменения настроек
            page = layouts_history.pop()
            # Закрываем окно
            window[page].update(visible=False)
            # Открываем предыдущее окно
            window[layouts_history[-1]].update(visible=True)
            window.refresh()

    # Обработка кнопки с настройками модели
    if event == "-MODEL_SETTINGS_MENU_BUTTON-":
        layouts_history.append("-MODEL_SETTINGS_LAYOUT-")
        window[layouts_history[-2]].update(visible=False)
        window[layouts_history[-1]].update(visible=True)
        window.refresh()

    # Обработка кнопки с изменением настроек модели
    if event == "-CHANGE_MODEL_SETTINGS_BUTTON-":
        layouts_history.append("-MODEL_SETTINGS_CHANGE_LAYOUT-")
        window[layouts_history[-2]].update(visible=False)
        window[layouts_history[-1]].update(visible=True)
        window.refresh()

    # Обработка кнопки с сохранением настроек модели
    if event == "-SAVE_MODEL_SETTINGS_BUTTON-":
        no_errors = True

        if int(values["-L_MAX_INPUT-"]) > 0:
            l_max = int(values["-L_MAX_INPUT-"].split()[0])
            window["-L_MAX-"].update(l_max)
        else:
            no_errors = False
            window["-L_MAX_INPUT-"].update(l_max)

        if int(values["-CENT_MAX_INPUT-"]) > 0:
            century = int(values["-CENT_MAX_INPUT-"].split()[0])
            window["-CENT_MAX-"].update(century)
        else:
            no_errors = False
            window["-CENT_MAX_INPUT-"].update(century)

        save_setup_file(ip, login, password,
                        satellites,
                        start_month, start_year, end_month, end_year,
                        sun_angle, f_nec_diff, dst_diff, ddst_diff, kp_max,
                        lat_1, lat_2, lon_1, lon_2,
                        l_max, century)

        if no_errors:
            page = layouts_history.pop()
            window[page].update(visible=False)
            window[layouts_history[-1]].update(visible=True)
            window.refresh()

    # Обработка кнопки с меню обработки данных
    if event == "-DATA_CALCULATION_MENU_BUTTON-":
        layouts_history.append("-DATA_PROCESSING_LAYOUT-")
        window[layouts_history[-2]].update(visible=False)
        window[layouts_history[-1]].update(visible=True)
        window.refresh()

    # Обработка кнопки с обработкой данных
    if event == "-START_DATA_PROCESSING_BUTTON-":
        # Подготавливаем даты
        date1 = f"{start_year}-{str(start_month).zfill(2)}-01"
        date2 = f"{end_year}-{str(end_month).zfill(2)}-01"

        # Создание списка ['2023-01-01', '2023-02-01', ....
        month_list = pd.date_range(date1, date2,
                                   freq="MS").strftime("%Y-%m-%d").tolist()

        # Создаем подключение к БД
        sqlEngine = create_engine(f"mysql+pymysql://{login}:{password}@{ip}", pool_recycle=3600)

        # Подключаемся к БД
        dbConnection = sqlEngine.connect()

        # Делаем нажатую кнопку неактивной
        window["-START_DATA_PROCESSING_BUTTON-"].update(disabled=True)
        window["-PROCESSING_PROGRESS_TEXT-"].update("Происходит загрузка данных")
        # Отображаем прогресбар
        window["-PROCESSING_PROGRESS_TEXT-"].update(visible=True)
        window.refresh()

        # Загружаем данные в DataFrame
        result = download_data_from_sql(month_list[0], month_list[1], dbConnection, satellites)
        # Переформатируем дату из UNIX
        result["DATETIME"] = result.DATE.map(lambda a: datetime.fromtimestamp(a))
        # Берем первые 60 строк DataFrame
        result = result.iloc[0::60, :]
        # Обновляем прогресбар
        window["-PROCESSING_PROGRESS_BAR-"].UpdateBar((1) * 1000 / (len(month_list) - 1))
        # Запрашиваем из БД данные за месяц
        for i in range(1, len(month_list) - 1):
            frame = download_data_from_sql(month_list[i], month_list[i + 1], dbConnection, satellites)
            frame["DATETIME"] = frame.DATE.map(lambda a: datetime.fromtimestamp(a))
            # Сохраняем результат в DataFrame
            result = pd.concat([result, frame.iloc[0::60, :]])
            del frame
            window["-PROCESSING_PROGRESS_BAR-"].UpdateBar((i + 1) * 1000 / (len(month_list) - 1))
        print(result.head())

        # Обновляем текст
        window["-PROCESSING_PROGRESS_TEXT-"].update("Происходит загрузка индексов")
        window.refresh()
        # Подключаемся к БД
        dbConnection = sqlEngine.connect()
        codeIndex = ["DST", "KP"]
        # Запрашиваем индексы из БД
        index = download_data_from_sql_index(month_list[0], month_list[-1], dbConnection, codeIndex)
        dbConnection.close()
        # Выбираем часть DataFrame, в которой данные об DST
        DST = index[index.CODE == "DST"]
        # Преобразуем дату из UNIX
        DST["DATETIME"] = DST.DATE.map(lambda a: datetime.fromtimestamp(a))
        DST["Dst"] = DST["value"]

        # Аналогично с KP  индексом
        KP = index[index.CODE == "KP"]
        KP["Kp final"] = 0
        # Заменяем KP*3 на KP
        # например, 8 -> 2.67
        for i in range(len(kp_types_raw)):
            KP.loc[KP["value"] == kp_types_raw[i], "Kp final"] = kp_types_final[i]
        KP["DATETIME"] = KP.DATE.map(lambda a: datetime.fromtimestamp(a))

        # Создаем DataFrame, где KP будет для каждой минуты
        Kp_M = KP[["Kp final", "DATETIME"]]
        Kp_M = Kp_M.set_index("DATETIME")
        Kp_M = Kp_M.resample("60s").asfreq()
        Kp_M = pd.DataFrame(Kp_M).interpolate(method="time")

        # Аналогично с DST
        Dst_M = DST[["Dst", "DATETIME"]]
        Dst_M = Dst_M.set_index("DATETIME")
        Dst_M = Dst_M.resample("60s").asfreq()
        Dst_M = pd.DataFrame(Dst_M).interpolate(method="time")
        # Считаем dDST
        Dst_M["dDst"] = Dst_M.Dst.diff()
        Dst_M.at[Dst_M.index[0], "dDst"] = Dst_M.at[Dst_M.index[1], "dDst"]

        # Меняем надпись
        window["-PROCESSING_PROGRESS_TEXT-"].update("Происходит отбор данных")
        window.refresh()

        # Джоиним таблицы с данными, с DST и с KP
        result = result.set_index("DATETIME")
        result = pd.merge(result, Kp_M[["Kp final"]], how="left", left_index=True, right_index=True)
        result = pd.merge(result, Dst_M[["Dst", "dDst"]], how="left", left_index=True, right_index=True)

        print(result.head())

        # Считаем угол солнца относительно горизонта
        result["sun decl"] = result.index.map(lambda a: SunPreparing.datenum2000(a)).map(
            lambda a: SunPreparing.sun_md2000(a)[1])

        # Считаем кошироту
        result["colat"] = 90 - result["latitude"]

        rad = np.pi / 180
        # ???
        result["cos zeta"] = np.cos(result["colat"] * rad) * np.sin(result["sun decl"]) + np.sin(
            result["colat"] * rad) * np.cos(result["sun decl"]) * np.cos(
            ((result.index.map(lambda a: SunPreparing.datenum2000(a)) + 0.5) % 1) * 2 * np.pi + result[
                "longitude"] * rad)

        # ???
        cos_zeta_0 = np.cos((90 - sun_angle) / 180 * np.pi)

        print(result.head())

        df = result[result["f"] > 0]
        print("f => 0")
        print(df.head())
        df = df[df["cos zeta"] < cos_zeta_0]
        print("zeta")
        print(df.head())
        df = df[abs(df["f"] - np.sqrt(df["n"] ** 2 + df["e"] ** 2 + df["c"] ** 2)) <= f_nec_diff]
        print("f diff")
        print(df.head())
        df = df[abs(df["Dst"]) < dst_diff]
        print("dst")
        print(df.head())
        df = df[abs(df["dDst"]) < ddst_diff]
        print("ddst")
        print(df.head())
        df = df[df["Kp final"] < kp_max]
        print("kp")
        print(df.head())
        df["radius"] = df["radius"] / 1000
        df["B_r"] = -df["c"]
        df["B_theta"] = -df["n"]
        df["B_lambda"] = df["e"]

        print(df.head())

        df = df[["CODE", "DATE", "latitude", "longitude", "radius", "n", "e", "c", "f", "colat", "B_r", "B_theta",
                 "B_lambda"]]

        print(df.head())

        sqlEngine = create_engine(
            f"mysql+pymysql://{login}:{password}@{ip}/geomag", pool_recycle=3600)

        try:
            df.to_sql("selected_data", con=sqlEngine, index=False, if_exists="replace")
            df.to_csv("out.csv")
        except Exception as e:
            sg.popup("Произошла ошибка", f"{e}")

        window["-PROCESSING_PROGRESS_TEXT-"].update("Отбор данных завершен")
        window["-START_DATA_PROCESSING_BUTTON-"].update(disabled=False)

    # Обработка кнопки Назад
    if event[:13] == "-BACK_BUTTON-":
        page = layouts_history.pop()
        window[page].update(visible=False)
        window[layouts_history[-1]].update(visible=True)
        window.refresh()

window.close()
