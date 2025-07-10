from http import HTTPStatus
from utils.api.constants import TEST_CULTURES, FIELDS
import pytest


class TestPerformTTestMultipleGet:
    def test_perform_t_test_multiple_get(self, get_token, plastilin_db_api, data_helper, schema_validator):
        token = get_token('head_of_company_company_1')
        _, _, year_id = data_helper.get_or_create_spec_field_year_id(token=token, spec_name=TEST_CULTURES['barley']['russian_name'], field_name=FIELDS['field_2']['field_name'], year=FIELDS['field_2']['year'], region=FIELDS['field_2']['region'])
        year_ids = year_id
        feature = 'созревание бобов'
        control_plot = 'д 100'
        control_plot_year_id = year_id
        response = plastilin_db_api.get_perform_t_test_multiple(token, year_ids, feature, control_plot, control_plot_year_id)
        assert response.status == HTTPStatus.OK
        schema_validator.assert_valid_response(
            response.json(), 
            'plastilin_db/perform_t_test_multiple/get_response.json'
        )
    # @pytest.skip(reason='Не работает сортировка по plot_name')
    @pytest.mark.parametrize('sort_by, reverse', [('line_name', False), ('-line_name', True), ('plot_name', False), ('-plot_name', True)])
    def test_perform_t_test_multiple_get_sort_by(self, get_token, plastilin_db_api, data_helper, sort_by, reverse):
        token = get_token('head_of_company_company_1')
        _, _, year_id = data_helper.get_or_create_spec_field_year_id(token=token, spec_name=TEST_CULTURES['barley']['russian_name'], field_name=FIELDS['field_2']['field_name'], year=FIELDS['field_2']['year'], region=FIELDS['field_2']['region'])
        year_ids = year_id
        feature = 'созревание бобов'
        control_plot = 'д 100'
        control_plot_year_id = year_id
        response = plastilin_db_api.get_perform_t_test_multiple(token, year_ids, feature, control_plot, control_plot_year_id, sort_by=sort_by)
        # print(response.json())
        assert response.status == HTTPStatus.OK
        response_data = response.json()
        assert response_data, 'Ответ пустой!'

        # determine actual sort key without leading '-'
        import re

        def norm(s: str) -> str:
            return s.replace('ё', 'е').replace('Ё', 'Е')

        def nat_key(s: str):
            s_norm = norm(s)
            m = re.match(r'(\D+?)(\d+)$', s_norm.strip())
            if m:
                prefix, num = m.groups()
                return (prefix, int(num))
            return (s_norm, 0)

        key = sort_by.lstrip('-')
        # extract values in returned order
        sorted_data = [item[key] for item in response_data]
        # verify order matches expected
        assert sorted_data == sorted(
            sorted_data,
            key=nat_key,
            reverse=reverse
        ), 'Данные не отсортированы!'

    #TODO: сортировка по plot_name
    @pytest.mark.parametrize('sort_by__key, sort_by__value, reverse', [('avg', 'размер бобов', False), ('avg', '-размер бобов', True)])
    def test_perform_t_test_multiple_get_sort_by__key(self, get_token, plastilin_db_api, data_helper, sort_by__key, sort_by__value, reverse):
        token = get_token('head_of_company_company_1')
        _, _, year_id = data_helper.get_or_create_spec_field_year_id(token=token, spec_name=TEST_CULTURES['barley']['russian_name'], field_name=FIELDS['field_2']['field_name'], year=FIELDS['field_2']['year'], region=FIELDS['field_2']['region'])
        year_ids = year_id
        feature = 'созревание бобов'
        control_plot = 'д 100'
        control_plot_year_id = year_id
        response = plastilin_db_api.get_perform_t_test_multiple(token, year_ids, feature, control_plot, control_plot_year_id, sort_by__key=sort_by__key, sort_by__value=sort_by__value)
        # print(response.json())
        assert response.status == HTTPStatus.OK
        response_data = response.json()
        assert response_data, 'Ответ пустой!'

        # determine actual sort key without leading '-'
        import re

        def norm(s: str) -> str:
            return s.replace('ё', 'е').replace('Ё', 'Е')

        def nat_key(s: str):
            s_norm = norm(s)
            m = re.match(r'(\D+?)(\d+)$', s_norm.strip())
            if m:
                prefix, num = m.groups()
                return (prefix, int(num))
            return (s_norm, 0)

        key = f'{sort_by__key}_value'.lstrip('-') if sort_by__key == 'avg' else sort_by__key
        # extract values in returned order
        sorted_data = [item['features'][0][key] for item in response_data]
        # verify order matches expected
        assert sorted_data == sorted(
            sorted_data,
            # key=nat_key,
            reverse=reverse
        ), 'Данные не отсортированы!'
