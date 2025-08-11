from http import HTTPStatus

from utils.api.constants import FIELDS, TEST_CULTURES


class TestCombinedPlotFieldLineGenealogyGet:
    def test_combined_plot_field_line_genealogy_get_success(
        self, get_token, plastilin_db_api, data_helper, schema_validator
    ):
        token = get_token('company_1.head_of_company')
        _, _, year_id = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=TEST_CULTURES['barley']['russian_name'],
            field_name=FIELDS['field_2']['field_name'],
            year=FIELDS['field_2']['year'],
            region=FIELDS['field_2']['region'],
        )
        response = plastilin_db_api.get_combined_plot_field_line_genealogy(
            token=token,
            year_id=year_id,
            page=1,
            page_size=250,
        )
        assert response.status == HTTPStatus.OK
        response_data = response.json()
        schema_validator.assert_valid_response(
            response_data, 'plastilin_db/combined_plot_field_line_genealogy/get_response.json'
        )


    def test_combined_plot_field_line_genealogy_get_success_for_all_users(
        self, get_token, plastilin_db_api, data_helper, schema_validator
    ):

        spec_name = 'Тестовая культура для ролевых тестов'

        tokens = {
            'company_1.head_of_company': get_token('company_1.head_of_company'),
            'company_1.division_1.employee_1': get_token('company_1.division_1.employee_1'),
            'company_1.division_1.head_of_division': get_token('company_1.division_1.head_of_division'),
            'company_1.division_2.employee_1': get_token('company_1.division_2.employee_1'),
            'company_1.division_2.head_of_division': get_token('company_1.division_2.head_of_division'),
        }

        users_data = data_helper.create_plot_data_for_all_users(
            spec_name=spec_name,
            **tokens,
        )

        print(users_data)
        
        assert users_data == 1