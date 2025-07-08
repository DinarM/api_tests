from api.plastilin_db.field_year import FieldYearAPI
from api.plastilin_db.species_table import SpeciesTableAPI
from api.plastilin_db.field_year_permissions import FieldYearPermissionsApi
from api.plastilin_db.user_groups_with_fields import UserGroupsWithFieldsApi

class PlastilinDbApi(SpeciesTableAPI, FieldYearAPI, FieldYearPermissionsApi, UserGroupsWithFieldsApi):
    """Общий клиент, собирающий все части plastilin_db API."""
    pass