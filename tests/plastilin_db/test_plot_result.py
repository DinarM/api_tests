import time
from http import HTTPStatus

import pytest

from utils.api.constants import PLOT_RESULT_FIELDS


class TestPlotResultCreate:
    def test_plot_result_create_with_all_fields(self, get_token, plastilin_db_api, data_helper):
        token = get_token()

        plot_data = data_helper.generate_plot_result_data(
            field_name=PLOT_RESULT_FIELDS['field_name'],
            year=PLOT_RESULT_FIELDS['year'],
            region=PLOT_RESULT_FIELDS['region'],
            base_plot_name=PLOT_RESULT_FIELDS['base_plot_name'],
            row_count=PLOT_RESULT_FIELDS['row_count'],
            repeats=PLOT_RESULT_FIELDS['repeats'],
            number_of_plots=PLOT_RESULT_FIELDS['number_of_plots'],
            phenotypic_fields=PLOT_RESULT_FIELDS['phenotypic_fields'],
            dev_stage_fields=PLOT_RESULT_FIELDS['dev_stage_fields'],
        )
        excel_file, filename = data_helper.create_plot_result_excel(plot_data=plot_data)

        spec_name = data_helper.generate_random_string('Тестовая культура для загрузки')

        spec_id, _, year_id = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=spec_name,
            field_name=PLOT_RESULT_FIELDS['field_name'],
            year=PLOT_RESULT_FIELDS['year'],
            region=PLOT_RESULT_FIELDS['region'],
        )

        response = plastilin_db_api.create_plot_result(
            token=token,
            file_name=filename,
            file_path=excel_file,
            spec_id=spec_id,
        )
        assert response.status == HTTPStatus.CREATED

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


    def test_plot_result_update_phenotypic_fields_and_dev_stage_fields(
        self, get_token, plastilin_db_api, data_helper
    ):
        token = get_token()

        plot_data = data_helper.generate_plot_result_data(
            field_name=PLOT_RESULT_FIELDS['field_name'],
            year=PLOT_RESULT_FIELDS['year'],
            region=PLOT_RESULT_FIELDS['region'],
            base_plot_name=PLOT_RESULT_FIELDS['base_plot_name'],
            row_count=PLOT_RESULT_FIELDS['row_count'],
            repeats=PLOT_RESULT_FIELDS['repeats'],
            number_of_plots=PLOT_RESULT_FIELDS['number_of_plots'],
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

        plot_data_new = data_helper.generate_plot_result_data(
            field_name=PLOT_RESULT_FIELDS['field_name'],
            year=PLOT_RESULT_FIELDS['year'],
            region=PLOT_RESULT_FIELDS['region'],
            base_plot_name=PLOT_RESULT_FIELDS['base_plot_name'],
            row_count=PLOT_RESULT_FIELDS['row_count'],
            repeats=PLOT_RESULT_FIELDS['repeats'],
            number_of_plots=PLOT_RESULT_FIELDS['number_of_plots'],
            phenotypic_fields=PLOT_RESULT_FIELDS['phenotypic_fields'],
            dev_stage_fields=PLOT_RESULT_FIELDS['dev_stage_fields'],
        )
        excel_file, filename = data_helper.create_plot_result_excel(plot_data=plot_data_new)

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
        
        time.sleep(4)

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

        data_helper.compare_plot_response_with_api(response_data, plot_data_new)

    # @pytest.mark.skip(reason='TODO: fix')
    @pytest.mark.parametrize('repeats, number_of_plots, phenotypic_fields, dev_stage_fields', [
        (None, None, None, None),
        (None, None, None, PLOT_RESULT_FIELDS['dev_stage_fields']),
        (None, None, PLOT_RESULT_FIELDS['phenotypic_fields'], None),
        (None, PLOT_RESULT_FIELDS['number_of_plots'], None, None),
        (PLOT_RESULT_FIELDS['repeats'], None, None, None),
    ])
    def test_plot_result_create_without_some_fields(
        self, get_token, plastilin_db_api, data_helper, repeats, 
        number_of_plots, phenotypic_fields, dev_stage_fields
    ):
        token = get_token('other.standalone_user')

        plot_data = data_helper.generate_plot_result_data(
            field_name=PLOT_RESULT_FIELDS['field_name'],
            year=PLOT_RESULT_FIELDS['year'],
            region=PLOT_RESULT_FIELDS['region'],
            base_plot_name=PLOT_RESULT_FIELDS['base_plot_name'],
            row_count=PLOT_RESULT_FIELDS['row_count'],
            repeats=repeats,
            number_of_plots=number_of_plots,
            phenotypic_fields=phenotypic_fields,
            dev_stage_fields=dev_stage_fields,
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
    @pytest.mark.parametrize('repeats, number_of_plots, phenotypic_fields, dev_stage_fields', [
        (None, None, None, None),
        (None, None, None, PLOT_RESULT_FIELDS['dev_stage_fields']),
        (None, None, PLOT_RESULT_FIELDS['phenotypic_fields'], None),
        (None, PLOT_RESULT_FIELDS['number_of_plots'], None, None),
        (PLOT_RESULT_FIELDS['repeats'], None, None, None),
    ])
    def test_plot_result_update_without_some_fields(
        self, get_token, plastilin_db_api, data_helper, repeats, 
        number_of_plots, phenotypic_fields, dev_stage_fields
    ):
        token = get_token('other.standalone_user')

        plot_data = data_helper.generate_plot_result_data(
            field_name=PLOT_RESULT_FIELDS['field_name'],
            year=PLOT_RESULT_FIELDS['year'],
            region=PLOT_RESULT_FIELDS['region'],
            base_plot_name=PLOT_RESULT_FIELDS['base_plot_name'],
            row_count=PLOT_RESULT_FIELDS['row_count'],
            repeats=PLOT_RESULT_FIELDS['repeats'],
            number_of_plots=PLOT_RESULT_FIELDS['number_of_plots'],
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

        plot_data_new = data_helper.generate_plot_result_data(
            field_name=PLOT_RESULT_FIELDS['field_name'],
            year=PLOT_RESULT_FIELDS['year'],
            region=PLOT_RESULT_FIELDS['region'],
            base_plot_name=PLOT_RESULT_FIELDS['base_plot_name'],
            row_count=PLOT_RESULT_FIELDS['row_count'],
            repeats=repeats,
            number_of_plots=number_of_plots,
            phenotypic_fields=phenotypic_fields,
            dev_stage_fields=dev_stage_fields,
        )
        excel_file_new, filename_new = data_helper.create_plot_result_excel(
            plot_data=plot_data_new
        )

        response = plastilin_db_api.create_plot_result(
            token=token,
            file_name=filename_new,
            file_path=excel_file_new,
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
        
        time.sleep(4)

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