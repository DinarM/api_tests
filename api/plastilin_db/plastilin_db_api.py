from api.plastilin_db.field_year import FieldYearAPI
from api.plastilin_db.species_table import SpeciesTableAPI

class PlastilinDbApi(SpeciesTableAPI, FieldYearAPI):
    """Общий клиент, собирающий все части plastilin_db API."""
    pass