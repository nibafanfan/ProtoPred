"""Unit tests for ProtoPRED client"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from protopred import ProtoPREDClient
from protopred.exceptions import ValidationError, AuthenticationError
from protopred.models import Module, PredictionResponse


class TestProtoPREDClient:
    
    @pytest.fixture
    def client(self):
        return ProtoPREDClient(
            account_token="test_token",
            account_secret_key="test_secret",
            account_user="test_user"
        )
    
    def test_client_initialization(self):
        client = ProtoPREDClient(
            account_token="token",
            account_secret_key="secret",
            account_user="user"
        )
        assert client.account_token == "token"
        assert client.account_secret_key == "secret"
        assert client.account_user == "user"
        assert client.base_url == "https://protopred.protoqsar.com/API/v2"
    
    def test_validate_models_valid(self, client):
        # Should not raise any exception
        client._validate_models(
            Module.PROTOPHYSCHEM,
            "model_phys:water_solubility, model_phys:melting_point"
        )
    
    def test_validate_models_invalid_format(self, client):
        with pytest.raises(ValidationError, match="Invalid model format"):
            client._validate_models(
                Module.PROTOPHYSCHEM,
                "model_phys-water_solubility"
            )
    
    def test_validate_models_invalid_model_type(self, client):
        with pytest.raises(ValidationError, match="Unknown model type"):
            client._validate_models(
                Module.PROTOPHYSCHEM,
                "invalid_type:water_solubility"
            )
    
    def test_validate_models_invalid_model_name(self, client):
        with pytest.raises(ValidationError, match="Unknown model"):
            client._validate_models(
                Module.PROTOPHYSCHEM,
                "model_phys:invalid_model"
            )
    
    @patch('protopred.client.requests.post')
    def test_predict_single_success(self, mock_post, client):
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {
            "Water solubility": [{
                "ID": "ID_1",
                "SMILES": "CCCCC",
                "Predicted value": "0.066 g/L",
                "Predicted numerical": 0.066,
                "Predicted value (model units)": "-3.04 log mol/L",
                "Predicted numerical (model units)": -3.04,
                "Applicability domain**": "Inside (T/L/E/R)",
                "Chemical name": "-",
                "CAS": "-",
                "EC number": "-",
                "Structural formula": "-"
            }]
        }
        mock_response.raise_for_status = Mock()
        mock_response.headers = {"Content-Type": "application/json"}
        mock_post.return_value = mock_response
        
        result = client.predict_single(
            smiles="CCCCC",
            module="ProtoPHYSCHEM",
            models=["model_phys:water_solubility"]
        )
        
        assert isinstance(result, PredictionResponse)
        assert "Water solubility" in result.predictions
        assert len(result.predictions["Water solubility"]) == 1
        assert result.predictions["Water solubility"][0].SMILES == "CCCCC"
    
    @patch('protopred.client.requests.post')
    def test_authentication_error(self, mock_post, client):
        # Mock 401 response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = Exception()
        mock_post.return_value = mock_response
        
        with pytest.raises(Exception):
            client.predict_single(
                smiles="CCCCC",
                module="ProtoPHYSCHEM",
                models=["model_phys:water_solubility"]
            )