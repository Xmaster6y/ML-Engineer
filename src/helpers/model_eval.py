"""This module contains the Evaluator class,
 which is used to evaluate the performance of a model.
 
 author: Yoann Poupart
 """

class Evaluator:
    """This class is used to evaluate the performance of a model.
    
    Attributes
    ----------
    model : str
        The model to be evaluated.

    Methods
    -------
    evaluate()
        This method evaluates the performance of a model.
    """
    def __init__(self, model=None):
        """This method initializes the Evaluator class.

        Parameters
        ----------
        model : str, optional
            The model to be evaluated, by default None
        """
        self.model = model

    def evaluate(self)->float:
        """This method evaluates the performance of a model.
        
        Returns
        --------
        float
            The performance of the model.
        """
        return 1.0

    def _check(self):
        """This method checks if the model is not None.
        
        Raises
        ------
        ValueError
            If the model is None.
        """
        if self.model is None:
            raise ValueError("The model is None.")
