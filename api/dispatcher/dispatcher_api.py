from api.dispatcher.teams import DispatcherTeamAPI
from api.dispatcher.jobs import DispatcherJobsAPI

class DispatcherAPI(DispatcherTeamAPI, DispatcherJobsAPI):
    """Общий клиент, собирающий все части диспетчерского API."""
    pass