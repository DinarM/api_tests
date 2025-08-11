"""
Константы для тестов
"""

from pathlib import Path

API_ENDPOINTS = {
    'auth': {'login': '/api/v1/login/'},
    'users': {
        'companies': '/api/v1/users/companies/',
        'users_by_company_id': '/api/v1/users/users_by_company_id/',
        'users_groups': '/api/v1/users/users_groups/',
        'company_structure': '/api/v1/users/company_structure/',
        'profile': '/api/v1/users/profile/',
    },
    'plastilin_db': {
        'field_year': '/api/v1/plastilin_db/field_year/',
        'species_table': '/api/v1/plastilin_db/species_table/',
        'field_year_permissions': '/api/v1/plastilin_db/field_year_permissions/',
        'user_groups_with_fields': '/api/v1/plastilin_db/user_groups_with_fields/',
        'field_year_add': '/api/v1/plastilin_db/field_year_add/',
        'field_table': '/api/v1/plastilin_db/field_table/',
        'perform_t_test_multiple': '/api/v1/plastilin_db/perform_t_test_multiple/',
        'cross_avg_values_multiple': '/api/v1/plastilin_db/cross_avg_values_multiple/',
        'field_maps': '/api/v1/plastilin_db/field_maps/',
        'field_map_coloring_data': '/api/v1/plastilin_db/field_map_coloring_data/',
        'plot_table': '/api/v1/plastilin_db/plot_table/',
        'calculate_nsr_multiple': '/api/v1/plastilin_db/calculate_nsr_multiple/',
        'plot_result': '/api/v1/plastilin_db/upload_custom_file/plot_result/',
        'combined_plot_field_line_genealogy':
            '/api/v1/plastilin_db/combined_plot_field_line_genealogy/',
        'sowing_list': '/api/v1/plastilin_db/sowing_list/',
        'download_plot_data': '/api/v1/plastilin_db/download_plot_data/',
        'download_selection_list': '/api/v1/plastilin_db/download_selection_list/',
        'export_to_excel': '/api/v1/plastilin_db/field_maps/export_to_excel/',
        'download_field_file': '/api/v1/plastilin_db/excel_file/download_field_file/',
    },
    'notice_app': {
        'notifications': '/api/v1/notice_app/notifications/',
    },
}

YEARS = {
    '2019': 2019,
    '2020': 2020,
    '2021': 2021,
    '2022': 2022,
    '2023': 2023,
    '2025': 2025,
    '2026': 2026,
}


# Тестовые данные
TEST_CULTURES = {
    'wheat': {'english_name': 'Wheat', 'russian_name': 'Пшеница'},
    'barley': {
        'english_name': 'Barley',
        'russian_name': 'Ячмень',  # для массива данных
    },
}

REGIONS = {
    'Амурская область': 'Амурская область',
    'Краснодарский край': 'Краснодарский край',
    'Алтайский край': 'Алтайский край',
    'Красноярский край': 'Красноярский край',
    'Республика Башкортостан': 'Республика Башкортостан',
    'Республика Татарстан': 'Республика Татарстан',
    'Республика Мордовия': 'Республика Мордовия',
    'Республика Марий Эл': 'Республика Марий Эл',
    'Республика Чувашия': 'Республика Чувашия',
    'Республика Удмуртия': 'Республика Удмуртия',
}

FIELDS = {
    'field_1': {
        'field_name': 'Тестовый питомник',
        'region': REGIONS['Амурская область'],
        'year': YEARS['2025'],
    },
    'field_2': {  # для массива данных
        'field_name': 'Конкурсный питомник',
        'region': REGIONS['Краснодарский край'],
        'year': YEARS['2023'],
    },
    'field_3': {
        'field_name': 'Контрольный питомник',
        'region': REGIONS['Краснодарский край'],
        'year': YEARS['2022'],
    },
}

FEATURES = {
    'созревание бобов': 'созревание бобов',
    'размер бобов': 'размер бобов',
    'белок в семенах': 'белок в семенах',
}

CONTROL_PLOT = {
    'д 100': 'д 100',
    'д 147': 'д 147',
}   

STATISTICAL_FEATURES = {
    'T-test': {
        'feature': FEATURES['созревание бобов'],
        'control_plot': CONTROL_PLOT['д 100'],
    },
    'NSR': {
        'feature': FEATURES['размер бобов'],
        'control_plot': CONTROL_PLOT['д 147'],
    },
    'CROSS_AVG': {
        'feature': FEATURES['белок в семенах'],
        'control_plot': CONTROL_PLOT['д 100'],
    },

}

PLOT_RESULT_FIELDS = {
    'field_name': 'Конкурсный питомник',
    'year': YEARS['2023'],
    'region': REGIONS['Краснодарский край'],
    'base_plot_name': 'Делянка',
    'row_count': 5,
    'repeats': 3,
    'number_of_plots': 'д',
    'phenotypic_fields': [
        {'name': 'Высота растения', 'type': 'float', 'unit': 'см'},
        {'name': 'Устойчивость к болезням', 'type': 'string'},
    ],
    'dev_stage_fields': [
        {'name': 'Всходы', 'type': 'date'},
        {'name': 'Развертывание первых листьев', 'type': 'date'},

    ],
}



PLOT_FIELDS_BY_ROLE = {
    'company_1.head_of_company': {
        'field_name': 'Питомник директора компании',
        'year': YEARS['2025'],
        'region': REGIONS['Алтайский край'],
        'base_plot_name': 'Делянка директора компании',
        'row_count': 5,
        'repeats': 2,
        'phenotypic_fields': [
            {'name': 'Высота растения', 'type': 'float', 'unit': 'см'},
        ],
        'dev_stage_fields': [
            {'name': 'Всходы', 'type': 'date'},
            {'name': 'Развертывание первых листьев', 'type': 'date'},
        ],
    },
    'company_1.division_1.head_of_division': {
        'field_name': 'Питомник руководителя дивизии 1',
        'year': YEARS['2020'],
        'region': REGIONS['Республика Башкортостан'],
        'base_plot_name': 'Делянка руководителя дивизии 1',
        'row_count': 5,
        'repeats': 2,
        'phenotypic_fields': [
            {'name': 'Высота растения', 'type': 'float', 'unit': 'см'},
        ],
        'dev_stage_fields': [
            {'name': 'Всходы', 'type': 'date'},
            {'name': 'Развертывание первых листьев', 'type': 'date'},
        ],
    },
    'company_1.division_2.head_of_division': {
        'field_name': 'Питомник руководителя дивизии 2',
        'year': YEARS['2021'],
        'region': REGIONS['Республика Мордовия'],
        'base_plot_name': 'Делянка руководителя дивизии 2',
        'row_count': 5,
        'repeats': 2,
        'phenotypic_fields': [
            {'name': 'Высота растения', 'type': 'float', 'unit': 'см'},
        ],
        'dev_stage_fields': [
            {'name': 'Всходы', 'type': 'date'},
            {'name': 'Развертывание первых листьев', 'type': 'date'},
        ],
    },
    'company_1.division_1.employee_1': {
        'field_name': 'Питомник сотрудника 1 дивизии 1',
        'year': YEARS['2020'],
        'region': REGIONS['Республика Марий Эл'],
        'base_plot_name': 'Делянка сотрудника 1 дивизии 1',
        'row_count': 5,
        'repeats': 2,
        'phenotypic_fields': [
            {'name': 'Высота растения', 'type': 'float', 'unit': 'см'},
        ],
        'dev_stage_fields': [
            {'name': 'Всходы', 'type': 'date'},
            {'name': 'Развертывание первых листьев', 'type': 'date'},
        ],
    },
    'company_1.division_2.employee_1': {
        'field_name': 'Питомник сотрудника 1 дивизии 2',
        'year': YEARS['2021'],
        'region': REGIONS['Республика Чувашия'],
        'base_plot_name': 'Делянка сотрудника 1 дивизии 2',
        'row_count': 5,
        'repeats': 2,
        'phenotypic_fields': [
            {'name': 'Высота растения', 'type': 'float', 'unit': 'см'},
        ],
        'dev_stage_fields': [
            {'name': 'Всходы', 'type': 'date'},
            {'name': 'Развертывание первых листьев', 'type': 'date'},
        ],
    },
}


PLOT_RESULT_MODIFICATIONS = {
    'modifications':                 [
                    {
                        'plot_name': 'Делянка 1/1',
                        'line_name': 'Сорт 1',
                        'plot_results': [
                            {
                                'plot_final_feature': 'высота растения',
                                'plot_final_value': '150.5',
                                'plot_final_unit': 'см'
                            }
                        ],
                        'plot_stages': [
                            {
                                'stage_of_vegetation': 'всходы',
                                'date_of_stage': '2024-05-15'
                            }
                        ]
                    }
                ]
}


REPETITIONS = {
    '10': 10,
}

TEST_DATA_PATH = Path(__file__).parent.parent.parent / 'utils' / 'data'

BAD_REQUEST_MESSAGE = {
    'invalid_credentials': 'Invalid credentials',
    'auth_locked': 'You have exceeded the allowed number of login attempts',
    'block_time': 60,
}
