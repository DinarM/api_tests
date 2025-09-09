from api.plastilin_db.ancova import AncovaAPI
from api.plastilin_db.anova import AnovaAPI
from api.plastilin_db.calculate_nsr_multiple import CalculateNSRMultipleAPI
from api.plastilin_db.combined_plot_field_line_genealogy import CombinedPlotFieldLineGenealogyAPI
from api.plastilin_db.correlation import CorrelationAPI
from api.plastilin_db.cross_avg_values_multiple import CrossAvgValuesMultipleAPI
from api.plastilin_db.delete_fastqc_file import DeleteFastqcFileAPI
from api.plastilin_db.download_fastqc_archive import DownloadFastqcArchiveAPI
from api.plastilin_db.download_field_file import DownloadFieldFileAPI
from api.plastilin_db.download_plot_data import DownloadPlotDataAPI
from api.plastilin_db.download_selection_list import DownloadSelectionListAPI
from api.plastilin_db.export_to_excel import ExportToExcelAPI
from api.plastilin_db.f1_analyze import F1AnalyzeAPI
from api.plastilin_db.field_map_coloring_data import FieldMapColoringDataAPI
from api.plastilin_db.field_maps import FieldMapsAPI
from api.plastilin_db.field_table import FieldTableApi
from api.plastilin_db.field_year import FieldYearAPI
from api.plastilin_db.field_year_add import FieldYearAddApi
from api.plastilin_db.field_year_permissions import FieldYearPermissionsApi
from api.plastilin_db.genotype_mutation_create_by_pos_and_chr import (
    GenotypeMutationCreateByPosAndChrAPI,
)
from api.plastilin_db.get_fastqc_archives import GetFastqcArchivesAPI
from api.plastilin_db.get_heat_map import GetHeatMapAPI
from api.plastilin_db.get_unique_harvest_technologies_from_field import (
    GetUniqueHarvestTechnologiesFromFieldAPI,
)
from api.plastilin_db.get_url_to_upload_fastq import GetUrlToUploadFastqAPI
from api.plastilin_db.harvest_technology_add_multiple import HarvestTechnologyAddMultipleAPI
from api.plastilin_db.perform_t_test_multiple import PerformTTestMultipleAPI
from api.plastilin_db.plot_final_results_add_multiple import PlotFinalResultsAddMultipleAPI
from api.plastilin_db.plot_result import PlotResultAPI
from api.plastilin_db.plot_stage import PlotStageAPI
from api.plastilin_db.plot_table import PlotTableAPI
from api.plastilin_db.qualitative_features import QualitativeFeaturesAPI
from api.plastilin_db.quantitative_features import QuantitativeFeaturesAPI
from api.plastilin_db.sowing_list import SowingListAPI
from api.plastilin_db.species_table import SpeciesTableAPI
from api.plastilin_db.statistics_visualisation import StatisticsVisualisationAPI
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
    StatisticsVisualisationAPI,
    QuantitativeFeaturesAPI,
    GetUniqueHarvestTechnologiesFromFieldAPI,
    CorrelationAPI,
    QualitativeFeaturesAPI,
    AnovaAPI,
    AncovaAPI,
    F1AnalyzeAPI,
    GetHeatMapAPI,
    PlotFinalResultsAddMultipleAPI,
    GenotypeMutationCreateByPosAndChrAPI,
    PlotStageAPI,
    HarvestTechnologyAddMultipleAPI,
    GetUrlToUploadFastqAPI,
    DownloadFastqcArchiveAPI,
    GetFastqcArchivesAPI,
    DeleteFastqcFileAPI,
):
    """Общий клиент, собирающий все части plastilin_db API."""
    pass
