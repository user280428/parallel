from GUI.const import home_path
import os


setup_path = os.getcwd()


# Чтение параметров из файла setup
def open_setup_file():
    f = open(setup_path, "r")
    lines = f.readlines()

    _ip = lines[2].strip()
    _login = lines[4].strip()
    _password = lines[6].strip()

    _satellites = lines[9].strip().split()

    _start_month = int(lines[13].strip())
    _start_year = int(lines[15].strip())
    _end_month = int(lines[17].strip())
    _end_year = int(lines[19].strip())

    _sun_angle = float(lines[21].strip())
    _f_nec_diff = float(lines[23].strip())
    _dst_diff = float(lines[25].strip())
    _ddst_diff = float(lines[27].strip())
    _kp_max = float(lines[29].strip())
    _lat_1 = float(lines[31].strip())
    _lat_2 = float(lines[33].strip())
    _lon_1 = float(lines[35].strip())
    _lon_2 = float(lines[37].strip())

    _l_max = int(lines[41].strip())
    _century = int(lines[43].strip())
    f.close()

    return _ip, _login, _password, \
        _satellites, \
        _start_month, _start_year, _end_month, _end_year, \
        _sun_angle, _f_nec_diff, _dst_diff, _ddst_diff, _kp_max, \
        _lat_1, _lat_2, _lon_1, _lon_2, \
        _l_max, _century


# Сохранение параметров в файл setup
def save_setup_file(
        _ip, _login, _password,
        _satellites,
        _start_month, _start_year, _end_month, _end_year,
        _sun_angle, _f_nec_diff, _dst_diff, _ddst_diff, _kp_max,
        _lat_1, _lat_2, _lon_1, _lon_2,
        _l_max, _century
):
    f = open(setup_path, "w")

    satellite_string = ""
    for sat in _satellites:
        satellite_string += f"{sat} "

    f.write(
        f"""DATABASE SETTINGS
IP address
{_ip}
Login
{_login}
Password
{_password}

SATELLITE SETTINGS
{satellite_string}

SELECTING SETTINGS
start month
{_start_month}
start year
{_start_year}
end month
{_end_month}
end year
{_end_year}
sun position angle
{_sun_angle}
abs diff f and nec
{_f_nec_diff}
Dst max
{_ddst_diff}
dDst max
{_ddst_diff}
Kp max
{_kp_max}
Min Lat
{_lat_1}
Max Lat
{_lat_2}
Min Lon
{_lon_1}
Max Lon
{_lon_2}

CALCULATING SETTINGS
L max
{_l_max}
Century
{_century}
"""
    )

    f.close()


# if __name__ == "__main__":
#     print(open_setup_file())
