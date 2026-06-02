"""Unit test file for nexthink_api."""
from nexthink_api import NxtEndpoint


class TestNxtEndpoint:

    #  get_api_name returns correct enum name for valid path
    def test_get_api_name_valid_path(self) -> None:
        assert NxtEndpoint.get_api_name('/api/v1/enrichment/data/fields') == 'Enrichment'
        assert NxtEndpoint.get_api_name('/api/v1/act/execute') == 'Act'
        assert NxtEndpoint.get_api_name('/api/v1/euf/campaign/trigger') == 'Engage'
        assert NxtEndpoint.get_api_name('/api/v1/workflows/execute') == 'Workflow'
        assert NxtEndpoint.get_api_name('/api/v2/workflows/execute') == 'WorkflowV2'
        assert NxtEndpoint.get_api_name('/api/v1/workflows/workflows/id/execution/id/trigger') == (
            'WorkflowThinkletTrigger'
        )
        assert NxtEndpoint.get_api_name('/api/v1/workflows/details') == 'WorkflowDetails'
        assert NxtEndpoint.get_api_name('/api/v1/workflows') == 'Workflows'
        assert NxtEndpoint.get_api_name('/api/v1/spark/handoff') == 'SparkHandoff'
        assert NxtEndpoint.get_api_name('/api/v1/data-management/device/deletions') == 'DataManagement'
        assert NxtEndpoint.get_api_name('/api/v1/act/remote-action') == 'RemoteActions'
        assert NxtEndpoint.get_api_name('/api/v1/act/remote-action/details') == 'RemoteActionsDetails'
        assert NxtEndpoint.get_api_name('/api/v1/nql/execute') == 'Nql'
        assert NxtEndpoint.get_api_name('/api/v2/nql/execute') == 'NqlV2'
        assert NxtEndpoint.get_api_name('/api/v1/nql/export') == 'NqlExport'
        assert NxtEndpoint.get_api_name('/api/v1/nql/status') == 'NqlStatus'
        assert NxtEndpoint.get_api_name('/api/v1/token') == 'Token'

    def test_data_management_endpoint_routing(self) -> None:
        assert NxtEndpoint.get_api_name('/api/v1/data-management/device/deletions') == 'DataManagement'
        assert NxtEndpoint.get_api_name('/api/v1/data-management/device/deletions/extra') == 'DataManagement'
        assert NxtEndpoint.get_api_name('/api/v1/data-management/device') is None

    #  all enum values are correctly assigned to their respective paths
    def test_enum_values_assigned_correctly(self) -> None:
        assert NxtEndpoint.Enrichment == '/api/v1/enrichment/data/fields'
        assert NxtEndpoint.Act == '/api/v1/act/execute'
        assert NxtEndpoint.Engage == '/api/v1/euf/campaign/trigger'
        assert NxtEndpoint.Workflow == '/api/v1/workflows/execute'
        assert NxtEndpoint.WorkflowV2 == '/api/v2/workflows/execute'
        assert NxtEndpoint.WorkflowThinkletTrigger == '/api/v1/workflows/workflows'
        assert NxtEndpoint.WorkflowDetails == '/api/v1/workflows/details'
        assert NxtEndpoint.Workflows == '/api/v1/workflows'
        assert NxtEndpoint.SparkHandoff == '/api/v1/spark/handoff'
        assert NxtEndpoint.DataManagement == '/api/v1/data-management/device/deletions'
        assert NxtEndpoint.RemoteActions == '/api/v1/act/remote-action'
        assert NxtEndpoint.RemoteActionsDetails == '/api/v1/act/remote-action/details'
        assert NxtEndpoint.Nql == '/api/v1/nql/execute'
        assert NxtEndpoint.NqlV2 == '/api/v2/nql/execute'
        assert NxtEndpoint.NqlExport == '/api/v1/nql/export'
        assert NxtEndpoint.NqlStatus == '/api/v1/nql/status'
        assert NxtEndpoint.Token == '/api/v1/token'

    def test_number_of_endpoints(self) -> None:
        expected = 17
        assert len(NxtEndpoint) == expected, f"Number of endpoints should be {expected}"

    def test_get_api_name_prefers_longest_matching_path(self) -> None:
        """Routing resolves nested Remote Actions paths to the most specific endpoint."""
        assert NxtEndpoint.get_api_name('/api/v1/act/remote-action/details') == 'RemoteActionsDetails'
        assert NxtEndpoint.get_api_name('/api/v1/workflows/details') == 'WorkflowDetails'
        assert NxtEndpoint.get_api_name('/api/v1/workflows/workflows/id/execution/id/trigger') == (
            'WorkflowThinkletTrigger'
        )

    #  get_api_name returns None for invalid path
    def test_get_api_name_invalid_path(self) -> None:
        assert NxtEndpoint.get_api_name('/invalid/path') is None

    #  get_api_name with empty string as path
    def test_get_api_name_empty_string(self) -> None:
        assert NxtEndpoint.get_api_name('') is None

    #  get_api_name with path not starting with '/'
    def test_get_api_name_no_leading_slash(self) -> None:
        assert NxtEndpoint.get_api_name('api/v1/enrichment/data/fields') is None

    #  get_api_name with path containing special characters
    def test_get_api_name_special_characters(self) -> None:
        assert NxtEndpoint.get_api_name('/api/v1/enrichment/data/fields/!@#') == 'Enrichment'

    #  get_api_name with path having trailing slashes
    def test_get_api_name_trailing_slashes(self) -> None:
        assert NxtEndpoint.get_api_name('/api/v1/enrichment/data/fields/') == 'Enrichment'
