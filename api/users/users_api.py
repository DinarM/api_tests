from api.users.companies import CompaniesApi
from api.users.users_by_company_id import UsersByCompanyIdApi

class UsersApi(CompaniesApi, UsersByCompanyIdApi):
    """Общий клиент, собирающий все части users API."""
    pass