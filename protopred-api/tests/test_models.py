"""Unit tests for ProtoPRED models"""

import pytest
from protopred.models import (
    Module, InputType, OutputType, Molecule,
    PredictionResult, PredictionResponse
)


class TestModels:
    
    def test_module_enum(self):
        assert Module.PROTOPHYSCHEM == "ProtoPHYSCHEM"
        assert Module.PROTOADME == "ProtoADME"
    
    def test_input_type_enum(self):
        assert InputType.SMILES_TEXT == "SMILES_TEXT"
        assert InputType.SMILES_FILE == "SMILES_FILE"
    
    def test_output_type_enum(self):
        assert OutputType.JSON == "JSON"
        assert OutputType.XLSX == "XLSX"
    
    def test_molecule_creation(self):
        mol = Molecule(
            SMILES="CCCCC",
            CAS="109-66-0",
            chemical_name="Pentane"
        )
        assert mol.SMILES == "CCCCC"
        assert mol.CAS == "109-66-0"
        assert mol.chemical_name == "Pentane"
    
    def test_molecule_to_dict(self):
        mol = Molecule(
            SMILES="CCCCC",
            CAS="109-66-0",
            chemical_name="Pentane",
            EC_number="203-692-4"
        )
        
        result = mol.to_dict()
        expected = {
            "SMILES": "CCCCC",
            "CAS": "109-66-0",
            "Chemical name": "Pentane",
            "EC number": "203-692-4"
        }
        assert result == expected
    
    def test_prediction_result_from_dict(self):
        data = {
            "ID": "mol_1",
            "SMILES": "CCCCC",
            "Predicted value": "0.066 g/L",
            "Predicted numerical": 0.066,
            "Predicted value (model units)": "-3.04 log mol/L",
            "Predicted numerical (model units)": -3.04,
            "Applicability domain**": "Inside (T/L/E/R)",
            "Chemical name": "Pentane",
            "CAS": "109-66-0"
        }
        
        result = PredictionResult.from_dict(data)
        assert result.ID == "mol_1"
        assert result.SMILES == "CCCCC"
        assert result.predicted_value == "0.066 g/L"
        assert result.predicted_numerical == 0.066
        assert result.chemical_name == "Pentane"
        assert result.CAS == "109-66-0"
    
    def test_prediction_response_from_json(self):
        data = {
            "Water solubility": [{
                "ID": "mol_1",
                "SMILES": "CCCCC",
                "Predicted value": "0.066 g/L",
                "Predicted numerical": 0.066,
                "Predicted value (model units)": "-3.04 log mol/L",
                "Predicted numerical (model units)": -3.04,
                "Applicability domain**": "Inside (T/L/E/R)",
                "Chemical name": "-",
                "CAS": "-"
            }]
        }
        
        response = PredictionResponse.from_json(data)
        assert "Water solubility" in response.predictions
        assert len(response.predictions["Water solubility"]) == 1
        assert response.predictions["Water solubility"][0].ID == "mol_1"
    
    def test_prediction_response_get_model_results(self):
        data = {
            "Water solubility": [{
                "ID": "mol_1",
                "SMILES": "CCCCC",
                "Predicted value": "0.066 g/L",
                "Predicted numerical": 0.066,
                "Predicted value (model units)": "-3.04 log mol/L",
                "Predicted numerical (model units)": -3.04,
                "Applicability domain**": "Inside (T/L/E/R)",
                "Chemical name": "-",
                "CAS": "-"
            }]
        }
        
        response = PredictionResponse.from_json(data)
        results = response.get_model_results("Water solubility")
        assert len(results) == 1
        assert results[0].ID == "mol_1"
        
        # Test non-existent model
        empty_results = response.get_model_results("Non-existent model")
        assert len(empty_results) == 0