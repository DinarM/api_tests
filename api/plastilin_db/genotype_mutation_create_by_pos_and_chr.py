from playwright.sync_api import APIResponse

from api.base_api import BaseAPI
from utils.api.api_helpers import APIHelper
from utils.api.constants import API_ENDPOINTS


class GenotypeMutationCreateByPosAndChrAPI(BaseAPI):
    def genotype_mutation_create_by_pos_and_chr(
        self, 
        token: str, 
        plot_id: int, 
        in_plot_created: bool, 
        chr: str, 
        pos: str, 
        mut_name: str, 
        first_allele: str, 
        second_allele: str
    ) -> APIResponse:
        headers = self.headers.copy()
        headers['Authorization'] = token
        
        payload = {
            'plot_id': plot_id,
            'in_plot_created': in_plot_created,
            'chr': chr,
            'pos': pos,
            'mut_name': mut_name,
            'first_allele': first_allele,
            'second_allele': second_allele,
        }
        payload = APIHelper.filter_none_values(payload)
        return self.context.post(
            API_ENDPOINTS['plastilin_db']['genotype_mutation_create_by_pos_and_chr'],
            data=payload,
            headers=headers,
        )