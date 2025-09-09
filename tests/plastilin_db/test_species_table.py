from http import HTTPStatus


class TestSpeciesTableCreate:
    """
    Тесты создания записей в таблице видов (species_table)
    """

    def test_create_species_table_max_length(
        self, get_token, plastilin_db_api, schema_validator, data_helper
    ):
        """
        Тест создания записи с максимальной длиной полей (255 символов)
        """
        token = get_token()

        max_length_string = data_helper.generate_random_string(length=255)

        response = plastilin_db_api.create_species_table(
            token=token, english_name=max_length_string, russian_name=max_length_string
        )

        assert response.status == HTTPStatus.CREATED

        response_data = response.json()

        schema_validator.assert_valid_response(
            response_data,
            'plastilin_db/species_table/create_response.json',
            'Создание записи с максимальной длиной',
        )

        assert response_data['english_name'] == max_length_string
        assert response_data['russian_name'] == max_length_string.capitalize()

    def test_create_species_table_required_fields_only(
        self, get_token, plastilin_db_api, schema_validator, data_helper
    ):
        """
        Тест создания записи только с обязательными полями
        """
        token = get_token()

        response = plastilin_db_api.create_species_table(
            token=token,
            russian_name=data_helper.generate_random_string(name='Культура_'),
            english_name=None,
        )

        assert response.status == HTTPStatus.CREATED

        response_data = response.json()

        schema_validator.assert_valid_response(
            response_data,
            'plastilin_db/species_table/create_response.json',
            'Создание записи с обязательными полями',
        )

        assert response_data['english_name'] is None


class TestSpeciesTableGet:
    """
    Тесты получения данных из таблицы видов (species_table)
    """

    def test_get_species_table_list(
        self, get_token, plastilin_db_api, schema_validator, api_helper
    ):
        """
        Тест получения списка записей species_table
        """
        token = get_token()

        response = plastilin_db_api.get_species_table(token=token)

        assert response.status == HTTPStatus.OK

        response_data = response.json()

        schema_validator.assert_valid_response(
            response_data,
            'plastilin_db/species_table/list_response.json',
            'Получение списка записей',
        )
