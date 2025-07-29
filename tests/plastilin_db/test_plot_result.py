import time
from http import HTTPStatus

from utils.api.constants import PLOT_RESULT_FIELDS


class TestPlotResultCreate:
    # @pytest.mark.skip(reason='TODO: fix')
    def test_plot_result_create(self, get_token, plastilin_db_api, data_helper):
        token = get_token('standalone_user')

        plot_data = data_helper.generate_plot_result_data(
            field_name=PLOT_RESULT_FIELDS['field_name'],
            year=PLOT_RESULT_FIELDS['year'],
            region=PLOT_RESULT_FIELDS['region'],
            base_plot_name=PLOT_RESULT_FIELDS['base_plot_name'],
            row_count=PLOT_RESULT_FIELDS['row_count'],
            repeats=PLOT_RESULT_FIELDS['repeats'],
            phenotypic_fields=PLOT_RESULT_FIELDS['phenotypic_fields'],
            dev_stage_fields=PLOT_RESULT_FIELDS['dev_stage_fields'],
        )
        excel_file, filename = data_helper.create_plot_result_excel(plot_data=plot_data)

        spec_name = data_helper.generate_random_string('Тестовая культура для загрузки')

        spec_id = data_helper.get_or_create_spec_id_by_name(
            token=token,
            russian_name=spec_name,
        )
        response = plastilin_db_api.create_plot_result(
            token=token,
            file_name=filename,
            file_path=excel_file,
            spec_id=spec_id,
        )
        assert response.status == HTTPStatus.CREATED

        _, _, year_id = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=spec_name,
            field_name=PLOT_RESULT_FIELDS['field_name'],
            year=PLOT_RESULT_FIELDS['year'],
            region=PLOT_RESULT_FIELDS['region'],
        )

        response_combined_plot_field_line_genealogy = (
            plastilin_db_api.get_combined_plot_field_line_genealogy(
                token=token,
                year_id=year_id,
                page=1,
                page_size=250,
            )
        )
        assert response_combined_plot_field_line_genealogy.status == HTTPStatus.OK
        response_data = response_combined_plot_field_line_genealogy.json()

        data_helper.compare_plot_response_with_api(response_data, plot_data)

    # @pytest.mark.skip(reason='TODO: fix')
    def test_plot_result_update(self, get_token, plastilin_db_api, data_helper):
        token = get_token('standalone_user')

        plot_data = data_helper.generate_plot_result_data(
            field_name=PLOT_RESULT_FIELDS['field_name'],
            year=PLOT_RESULT_FIELDS['year'],
            region=PLOT_RESULT_FIELDS['region'],
            base_plot_name=PLOT_RESULT_FIELDS['base_plot_name'],
            row_count=PLOT_RESULT_FIELDS['row_count'],
            repeats=PLOT_RESULT_FIELDS['repeats'],
            phenotypic_fields=PLOT_RESULT_FIELDS['phenotypic_fields'],
            dev_stage_fields=PLOT_RESULT_FIELDS['dev_stage_fields'],
        )
        excel_file, filename = data_helper.create_plot_result_excel(plot_data=plot_data)

        spec_name = data_helper.generate_random_string('Тестовая культура для загрузки')

        spec_id = data_helper.get_or_create_spec_id_by_name(
            token=token,
            russian_name=spec_name,
        )
        response = plastilin_db_api.create_plot_result(
            token=token,
            file_name=filename,
            file_path=excel_file,
            spec_id=spec_id,
        )
        assert response.status == HTTPStatus.CREATED

        plot_data = data_helper.generate_plot_result_data(
            field_name=PLOT_RESULT_FIELDS['field_name'],
            year=PLOT_RESULT_FIELDS['year'],
            region=PLOT_RESULT_FIELDS['region'],
            base_plot_name=PLOT_RESULT_FIELDS['base_plot_name'],
            row_count=PLOT_RESULT_FIELDS['row_count'],
            repeats=PLOT_RESULT_FIELDS['repeats'],
            phenotypic_fields=PLOT_RESULT_FIELDS['phenotypic_fields'],
            dev_stage_fields=PLOT_RESULT_FIELDS['dev_stage_fields'],
        )
        excel_file, filename = data_helper.create_plot_result_excel(plot_data=plot_data)

        response = plastilin_db_api.create_plot_result(
            token=token,
            file_name=filename,
            file_path=excel_file,
            spec_id=spec_id,
        )
        assert response.status == HTTPStatus.CREATED

        _, _, year_id = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=spec_name,
            field_name=PLOT_RESULT_FIELDS['field_name'],
            year=PLOT_RESULT_FIELDS['year'],
            region=PLOT_RESULT_FIELDS['region'],
        )
        
        time.sleep(5)
        response_combined_plot_field_line_genealogy = (
            plastilin_db_api.get_combined_plot_field_line_genealogy(
                token=token,
                year_id=year_id,
                page=1,
                page_size=250,
            )
        )
        assert response_combined_plot_field_line_genealogy.status == HTTPStatus.OK
        response_data = response_combined_plot_field_line_genealogy.json()

        data_helper.compare_plot_response_with_api(response_data, plot_data)
