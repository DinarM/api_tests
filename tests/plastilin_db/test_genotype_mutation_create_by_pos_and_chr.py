from http import HTTPStatus

from utils.api.constants import FIELDS, TEST_CULTURES


# TODO доделать тест после фиксов на стейдже
class TestGenotypeMutationCreateByPosAndChr:
    def test_genotype_mutation_create_by_pos_and_chr_success(
        self, get_token, plastilin_db_api, data_helper, schema_validator
    ):
        token = get_token('company_1.head_of_company')
        _, _, year_id = data_helper.get_or_create_spec_field_year_id(
            token=token,
            spec_name=TEST_CULTURES['barley']['russian_name'],
            field_name=FIELDS['field_3']['field_name'],
            year=FIELDS['field_3']['year'],
            region=FIELDS['field_3']['region'],
        )

        response = plastilin_db_api.genotype_mutation_create_by_pos_and_chr(
            token=token,
            plot_id=206471,
            in_plot_created=False,
            chr='123456',
            pos='12451',
            mut_name=data_helper.generate_random_string(name='mut_name'),
            first_allele="йцвйasdSa112",
            second_allele="йцвйasdSa112",
        )
        assert response.status == HTTPStatus.CREATED

        response_data = response.json()
        
        schema_validator.assert_valid_response(
            response_data,
            'plastilin_db/genotype_mutation_create_by_pos_and_chr/create_response.json'
        )