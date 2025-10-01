import FreeSimpleGUI as sg
from GUI.setup import open_setup_file


ip, login, password, \
    satellites, \
    start_month, start_year, end_month, end_year, \
    sun_angle, f_nec_diff, dst_diff, ddst_diff, kp_max, \
    lat_1, lat_2, lon_1, lon_2, \
    l_max, century = open_setup_file()


# Задаем шрифт глобально
sg.set_options(font=("Helvetica", 14))


# Основное меню программы
main_layout = [

    [
        sg.Button("Параметры Базы Данных",
                  key="-DB_SETTINGS_MENU_BUTTON-",
                  )
    ],

    [
        sg.Button("Выбор спутников",
                  key="-SATELLITE_SETTINGS_MENU_BUTTON-",
                  )
    ],

    [
        sg.Button("Параметры отбора данных",
                  key="-DATA_SETTINGS_MENU_BUTTON-",
                  )
    ],
    [
        sg.Button("Параметры рассчета модели",
                  key="-MODEL_SETTINGS_MENU_BUTTON-",
                  )
    ],
    [
        sg.Button("Запустить программу отбора данных",
                  key="-DATA_CALCULATION_MENU_BUTTON-",
                  )
    ]

]


# Меню параметров БД
db_settings_main_layout = [

    [
        sg.Text("Параметры Базы Данных",
                font=("Helvetica", 22)
                )
    ],
    [
        sg.Text("Адрес доступа к базе данных",
                )
    ],
    [
        sg.Text(ip,
                key="-DB_SETTINGS_IP-"
                )
    ],
    [
        sg.Text("Логин доступа к базе данных"
                )
    ],
    [
        sg.Text(login,
                key="-DB_SETTINGS_LOGIN-"
                )
    ],
    [
        sg.Text("Пароль доступа к базе данных"
                )
    ],
    [
        sg.Text(password,
                key="-DB_SETTINGS_PASSWORD-"
                )
    ],
    [
        sg.Button("Изменить параметры",
                  key="-CHANGE_DB_SETTINGS_BUTTON-"
                  )
    ],
    [
        sg.Button("Проверить доступ",
                  key="-CHECK_CONNECTION_BUTTON-"
                  )
    ],
    [
        sg.Button("Назад",
                  key="-BACK_BUTTON-"
                  )
    ]
]


# Меню изменения параметров БД
db_settings_change_layout = [

    [
        sg.Text("Адрес доступа к базе данных"
                )
    ],
    [
        sg.InputText(ip,
                     key="-DB_SETTINGS_IP_INPUT-",
                     do_not_clear=True
                     )
    ],
    [
        sg.Text("Логин доступа к базе данных"
                )
    ],
    [
        sg.InputText(login,
                     key="-DB_SETTINGS_LOGIN_INPUT-",
                     do_not_clear=True
                     )
    ],
    [
        sg.Text("Пароль доступа к базе данных"
                )
    ],
    [
        sg.InputText(password,
                     key="-DB_SETTINGS_PASSWORD_INPUT-",
                     do_not_clear=True
                     )
    ],
    [
        sg.Button("Сохранить параметры",
                  key="-SAVE_DB_SETTINGS_BUTTON-"
                  )
    ],
    [
        sg.Button("Назад",
                  key="-BACK_BUTTON-"
                  )
    ],
]


# Меню параметров спутников
satellite_settings_main_layout = [
    [
        sg.Text("Используемые спутники"
                )
    ],
    [
        sg.Text("\n".join(satellites),
                key="-SATELLITE_SETTINGS-",
                )
    ],
    [
        sg.Button("Изменить параметры",
                  key="-CHANGE_SATELLITE_SETTINGS_BUTTON-"
                  )
    ],
    [
        sg.Button("Назад",
                  key="-BACK_BUTTON-"
                  )
    ],
]


# Меню изменения параметров спутников
satellite_settings_change_layout = [
    [
        sg.Text("Используемые спутники"
                )
    ],
    [
        sg.Checkbox("SWA",
                    key="-SWA-",
                    default="SWA" in satellites
                    )
    ],
    [
        sg.Checkbox("SWB",
                    key="-SWB-",
                    default="SWB" in satellites
                    )
    ],
    [
        sg.Checkbox("SWC",
                    key="-SWC-",
                    default="SWC" in satellites
                    )
    ],
    [
        sg.Checkbox("MSS-1",
                    key="-MSS-1-",
                    default="MSS-1" in satellites
                    )
    ],
    [
        sg.Checkbox("MSS-2",
                    key="-MSS-2-",
                    default="MSS-2" in satellites
                    )
    ],
    [
        sg.Button("Сохранить параметры",
                  key="-SAVE_SATELLITE_SETTINGS_BUTTON-"
                  )
    ],
    [
        sg.Button("Назад",
                  key="-BACK_BUTTON-"
                  )
    ],
]


# Меню параметров отбора данных
data_settings_main_layout = [

    [
        sg.Text("Параметры отбора данных",
                font=("Helvetica", 22)
                )
    ],

    [
        sg.Column(
            [
                [
                    sg.Text("Номер месяца начала исследуемого периода"
                            )
                ],
                [
                    sg.Text(start_month,
                            key="-START_MONTH-"
                            )
                ],
                [
                    sg.Text("Номер года начала исследуемого периода"
                            )
                ],
                [
                    sg.Text(start_year,
                            key="-START_YEAR-"
                            )
                ],
                [
                    sg.Text("Номер месяца конца исследуемого периода"
                            )
                ],
                [
                    sg.Text(end_month,
                            key="-END_MONTH-"
                            )
                ],
                [
                    sg.Text("Номер года конца исследуемого периода"
                            )
                ],
                [
                    sg.Text(end_year,
                            key="-END_YEAR-"
                            )
                ],
                [
                    sg.Text("Угол положения солнца над уровнем горизонта"
                            )
                ],
                [
                    sg.Text(sun_angle,
                            key="-ZETA_0-"
                            )
                ],
                [
                    sg.Text("Максимальное отклонение векторный измерений \nот скалярных (модуль разности) [нТл]"
                            )
                ],
                [
                    sg.Text(f_nec_diff,
                            key="-F_NEC_DIFF-"
                            )
                ],
                [
                    sg.Text("Максимальное значение Dst индекса"
                            )
                ],
                [
                    sg.Text(dst_diff,
                            key="-DST_DIFF-"
                            )
                ],
                [
                    sg.Text("Максимальное значение dDst индекса \n(производная Dst по времени)"
                            )
                ],
                [
                    sg.Text(ddst_diff,
                            key="-DDST_DIFF-"
                            )
                ],
                [
                    sg.Text("Максимальное значение Kp индекса"
                            )
                ],
                [
                    sg.Text(kp_max,
                            key="-KP_MAX-"
                            )
                ],
                [
                    sg.Text("Минимальная широта"
                            )
                ],
                [
                    sg.Text(lat_1,
                            key="-MIN_LAT-"
                            )
                ],
                [
                    sg.Text("Максимальная широта"
                            )
                ],
                [
                    sg.Text(lat_2,
                            key="-MAX_LAT-"
                            )
                ],
                [
                    sg.Text("Минимальная долгота"
                            )
                ],
                [
                    sg.Text(lon_1,
                            key="-MIN_LON-"
                            )
                ],
                [
                    sg.Text("Максимальная долгота"
                            )
                ],
                [
                    sg.Text(lon_2,
                            key="-MAX_LON-"
                            )
                ],

            ],
            scrollable=True, vertical_scroll_only=True
        )],

    [
        sg.Button("Изменить параметры",
                  key="-CHANGE_DATA_SETTINGS_BUTTON-"
                  )
    ],
    [
        sg.Button("Назад",
                  key="-BACK_BUTTON-"
                  )
    ],
]


# Меню изменения параметров отбора данных
data_settings_change_layout = [

    [sg.Text("Параметры отбора данных"
             )
     ],
    [
        sg.Column([

            [
                sg.Text("Номер месяца начала исследуемого периода"
                        )
            ],
            [
                sg.InputText(start_month,
                             key="-START_MONTH_INPUT-"
                             )
            ],
            [
                sg.Text("Номер года начала исследуемого периода",
                        )
            ],
            [
                sg.InputText(start_year,
                             key="-START_YEAR_INPUT-"
                             )
            ],
            [
                sg.Text("Номер месяца конца исследуемого периода",
                        )
            ],

            [
                sg.InputText(end_month,
                             key="-END_MONTH_INPUT-"
                             )
            ],

            [
                sg.Text("Номер года конца исследуемого периода",
                        )
            ],
            [
                sg.InputText(end_year,
                             key="-END_YEAR_INPUT-"
                             )
            ],
            [
                sg.Text("Угол положения солнца над уровнем горизонта",
                        )
            ],
            [
                sg.InputText(sun_angle,
                             key="-ZETA_0_INPUT-"
                             )
            ],
            [
                sg.Text("Максимальное отклонение векторный измерений \nот скалярных (модуль разности) [нТл]",
                        )
            ],

            [
                sg.InputText(f_nec_diff,
                             key="-F_NEC_DIFF_INPUT-"
                             )
            ],
            [
                sg.Text("Максимальное значение Dst индекса",
                        )
            ],
            [
                sg.InputText(dst_diff,
                             key="-DST_DIFF_INPUT-"
                             )
            ],

            [
                sg.Text("Максимальное значение dDst индекса \n(производная Dst по времени)",
                        )
            ],

            [
                sg.InputText(ddst_diff,
                             key="-DDST_DIFF_INPUT-"
                             )
            ],
            [
                sg.Text("Максимальное значение Kp индекса",
                        )
            ],
            [
                sg.InputText(kp_max,
                             key="-KP_MAX_INPUT-"
                             )
            ],
            [
                sg.Text("Минимальная широта",
                        )
            ],
            [
                sg.InputText(lat_1,
                             key="-MIN_LAT_INPUT-"
                             )
            ],
            [
                sg.Text("Максимальная широта",
                        )
            ],
            [
                sg.InputText(lat_2,
                             key="-MAX_LAT_INPUT-"
                             )
            ],
            [
                sg.Text("Минимальная долгота",
                        )
            ],
            [
                sg.InputText(lon_1,
                             key="-MIN_LON_INPUT-"
                             )
            ],
            [
                sg.Text("Максимальная долгота",
                        )
            ],
            [
                sg.InputText(lon_2,
                             key="-MAX_LON_INPUT-"
                             )
            ]
        ],
            scrollable=True, vertical_scroll_only=True
        )],

    [
        sg.Button("Сохранить параметры",
                  key="-SAVE_DATA_SETTINGS_BUTTON-"
                  )
    ],
    [
        sg.Button("Назад",
                  key="-BACK_BUTTON-"
                  )
    ],
]


# Меню параметров модели
model_settings_main_layout = [

    [
        sg.Text("Параметры Модели",
                font=("Helvetica", 22)
                )
    ],
    [
        sg.Text("Максимальная степень сферических гармоник",
                )
    ],
    [
        sg.Text(l_max,
                key="-L_MAX-"
                )
    ],
    [
        sg.Text("Максимальная степень векового хода"
                )
    ],
    [
        sg.Text(century,
                key="-CENT_MAX-"
                )
    ],
    [
        sg.Button("Изменить параметры",
                  key="-CHANGE_MODEL_SETTINGS_BUTTON-"
                  )
    ],
    [
        sg.Button("Назад",
                  key="-BACK_BUTTON-"
                  )
    ]
]


# Меню изменения параметров модели
model_settings_change_layout = [

    [
        sg.Text("Параметры Модели",
                font=("Helvetica", 22)
                )
    ],
    [
        sg.Text("Максимальная степень сферических гармоник",
                )
    ],
    [
        sg.InputText(l_max,
                     key="-L_MAX_INPUT-"
                     )
    ],
    [
        sg.Text("Максимальная степень векового хода"
                )
    ],
    [
        sg.InputText(century,
                     key="-CENT_MAX_INPUT-"
                     )
    ],
    [
        sg.Button("Сохранить параметры",
                  key="-SAVE_MODEL_SETTINGS_BUTTON-"
                  )
    ],
    [
        sg.Button("Назад",
                  key="-BACK_BUTTON-"
                  )
    ]
]


# Меню процессинга данных
data_processing_layout = [

    [
        sg.Text("Прогресс отбора данных"
                )
    ],
    [
        sg.ProgressBar(1000,
                       size=(30, 20),
                       key="-PROCESSING_PROGRESS_BAR-"
                       )
    ],
    [
        sg.Text("Происходит отбор данных",
                key="-PROCESSING_PROGRESS_TEXT-",
                visible=False
                )
    ],
    [
        sg.Button("Начать ",
                  key="-START_DATA_PROCESSING_BUTTON-"
                  )
    ],
    [
        sg.Button("Назад",
                  key="-BACK_BUTTON-"
                  )
    ]
]


# Все меню, которые то открываются, то закрываются
layout = [
    [
        sg.Column(main_layout,
                  visible=True,
                  key="-MAIN_LAYOUT-"
                  ),

        sg.Column(db_settings_main_layout,
                  visible=False,
                  key="-DB_SETTINGS_LAYOUT-"
                  ),

        sg.Column(db_settings_change_layout,
                  visible=False,
                  key="-DB_SETTINGS_CHANGE_LAYOUT-"
                  ),

        sg.Column(satellite_settings_main_layout,
                  visible=False,
                  key="-SATELLITE_SETTINGS_LAYOUT-"
                  ),

        sg.Column(satellite_settings_change_layout,
                  visible=False,
                  key="-SATELLITE_SETTINGS_CHANGE_LAYOUT-"
                  ),

        sg.Column(data_settings_main_layout,
                  visible=False,
                  key="-DATA_SETTINGS_LAYOUT-"
                  ),

        sg.Column(data_settings_change_layout,
                  visible=False,
                  key="-DATA_SETTINGS_CHANGE_LAYOUT-"
                  ),

        sg.Column(model_settings_main_layout,
                  visible=False,
                  key="-MODEL_SETTINGS_LAYOUT-"
                  ),

        sg.Column(model_settings_change_layout,
                  visible=False,
                  key="-MODEL_SETTINGS_CHANGE_LAYOUT-"
                  ),

        sg.Column(data_processing_layout,
                  visible=False,
                  key="-DATA_PROCESSING_LAYOUT-"
                  ),
    ]
]
