from api.users.companies import CompaniesApi
from api.users.users_by_company_id import UsersByCompanyIdApi
from api.users.company_structure import CompanyStructureApi
from api.users.users_groups import UsersGroupsApi
from api.users.profile import ProfileApi

class UsersApi(CompaniesApi, UsersByCompanyIdApi, CompanyStructureApi, UsersGroupsApi, ProfileApi):
    """Общий клиент, собирающий все части users API."""
    pass