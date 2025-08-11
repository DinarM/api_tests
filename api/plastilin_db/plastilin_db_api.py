from api.plastilin_db.calculate_nsr_multiple import CalculateNSRMultipleAPI
from api.plastilin_db.combined_plot_field_line_genealogy import CombinedPlotFieldLineGenealogyAPI
from api.plastilin_db.cross_avg_values_multiple import CrossAvgValuesMultipleAPI
from api.plastilin_db.download_field_file import DownloadFieldFileAPI
from api.plastilin_db.download_plot_data import DownloadPlotDataAPI
from api.plastilin_db.download_selection_list import DownloadSelectionListAPI
from api.plastilin_db.export_to_excel import ExportToExcelAPI
from api.plastilin_db.field_map_coloring_data import FieldMapColoringDataAPI
from api.plastilin_db.field_maps import FieldMapsAPI
from api.plastilin_db.field_table import FieldTableApi
from api.plastilin_db.field_year import FieldYearAPI
from api.plastilin_db.field_year_add import FieldYearAddApi
from api.plastilin_db.field_year_permissions import FieldYearPermissionsApi
from api.plastilin_db.perform_t_test_multiple import PerformTTestMultipleAPI
from api.plastilin_db.plot_result import PlotResultAPI
from api.plastilin_db.plot_table import PlotTableAPI
from api.plastilin_db.sowing_list import SowingListAPI
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
    FieldMapColoringDataAPI,
    PlotTableAPI,
    CombinedPlotFieldLineGenealogyAPI,
    CalculateNSRMultipleAPI,
    PlotResultAPI,
    SowingListAPI,
    DownloadPlotDataAPI,
    DownloadSelectionListAPI,
    ExportToExcelAPI,
    DownloadFieldFileAPI,
):
    """Общий клиент, собирающий все части plastilin_db API."""
    pass
