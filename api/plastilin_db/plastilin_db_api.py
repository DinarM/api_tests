from api.plastilin_db.cross_avg_values_multiple import CrossAvgValuesMultipleAPI
from api.plastilin_db.field_maps import FieldMapsAPI
from api.plastilin_db.field_table import FieldTableApi
from api.plastilin_db.field_year import FieldYearAPI
from api.plastilin_db.field_year_add import FieldYearAddApi
from api.plastilin_db.field_year_permissions import FieldYearPermissionsApi
from api.plastilin_db.perform_t_test_multiple import PerformTTestMultipleAPI
from api.plastilin_db.species_table import SpeciesTableAPI
from api.plastilin_db.user_groups_with_fields import UserGroupsWithFieldsApi


class PlastilinDbApi(
    SpeciesTableAPI,
    FieldYearAPI,
    FieldYearPermissionsApi,
    UserGroupsWithFieldsApi,
    FieldTableApi,
    FieldYearAddApi,
    PerformTTestMultipleAPI,
    CrossAvgValuesMultipleAPI,
    FieldMapsAPI,
):
    """Общий клиент, собирающий все части plastilin_db API."""

    pass
