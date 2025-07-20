from http import HTTPStatus


class TestPlotResultCreate:
    def test_plot_result_create(self, get_token, plastilin_db_api, data_helper):
        token = get_token('standalone_user')

        plot_data = data_helper.generate_plot_result_data(
            field_name='Конкурсный питомник',
            year=2023,
            region='Краснодарский край',
            base_plot_name='Делянка',
            row_count=5,
            repeats=3,
            phenotypic_fields=[
                {'name': 'Высота растения', 'type': 'float', 'unit': 'см'},
                {'name': 'Устойчивость к болезням', 'type': 'string'},
            ],
            dev_stage_fields=[
                {'name': 'Развертывание первых листьев', 'type': 'date'},
                {'name': 'Фаза дозревания', 'type': 'date'},
            ]
        )
        excel_file, filename = data_helper.create_plot_result_excel(plot_data=plot_data)

        spec_id = data_helper.get_or_create_spec_id_by_name(
            token=token,
            russian_name=data_helper.generate_random_string('Тестовая культура для загрузки НЬЮ2'),
        )
        response = plastilin_db_api.create_plot_result(
            token=token,
            file_name=filename,
            file_path=excel_file,
            spec_id=spec_id,
        )
        assert response.status == HTTPStatus.CREATED
        