from api.plastilin_db.field_year import FieldYearAPI
from api.plastilin_db.species_table import SpeciesTableAPI
from api.plastilin_db.field_year_permissions import FieldYearPermissionsApi

class PlastilinDbApi(SpeciesTableAPI, FieldYearAPI, FieldYearPermissionsApi):
    """Общий клиент, собирающий все части plastilin_db API."""
    pass