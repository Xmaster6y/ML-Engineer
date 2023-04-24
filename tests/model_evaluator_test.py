"""Tests for the model evaluator class."""

import pytest

from helpers import Evaluator

@pytest.fixture
def default_evaluator():
    """Returns a default evaluator."""
    return Evaluator()

class TestEvaluatorCreation:
    """Tests for the Evaluator class.
    
    Methods
    -------
    test_default_evaluator(default_evaluator)
        Tests the default evaluator.
    test_evaluator_with_model()
        Tests the evaluator with a model.
    """
    def test_default_evaluator(self, default_evaluator):
        """Tests the default evaluator.
        
        Parameters
        ----------
        default_evaluator : Evaluator
            The default evaluator.

        Raises
        ------
        AssertionError
            If the model is not None.
        """
        assert default_evaluator.model is None

    def test_evaluator_with_model(self):
        """Tests the evaluator with a model.
        
        Raises
        ------
        AssertionError
            If the model is not "model".
        """
        evaluator = Evaluator(model="model")
        assert evaluator.model == "model"