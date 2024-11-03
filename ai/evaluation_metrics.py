"""Evaluation Metrics Module for Eagle Terminal's AI System.

This module provides functions to calculate various evaluation metrics
for the AI model used in Eagle Terminal. It includes functions for
calculating accuracy, precision, recall, F1 score, and perplexity.

Note: Some functions require scikit-learn, which is optional. If not
available, a warning will be printed and those functions will return
an error message instead of actual metrics.
"""

from typing import Any, Dict, List, Union

import numpy as np

try:
    from sklearn.metrics import accuracy_score, precision_recall_fscore_support
except ImportError:
    print("Warning: sklearn not found. Some evaluation metrics may not be available.")
    accuracy_score = precision_recall_fscore_support = None


def calculate_metrics(
    predictions: List[Any], labels: List[Any]
) -> Dict[str, Union[float, str]]:
    """Calculate evaluation metrics including accuracy, precision, recall, and
    F1 score.

    Args:
        predictions (List[Any]): Predicted labels from the model.
        labels (List[Any]): True labels.

    Returns:
        Dict[str, Union[float, str]]: A dictionary containing the calculated metrics.
    """
    if accuracy_score is None:
        return {"error": "sklearn not available for metric calculation"}

    accuracy = accuracy_score(labels, predictions)
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, predictions, average="weighted"
    )
    return {"accuracy": accuracy, "precision": precision, "recall": recall, "f1": f1}


def calculate_perplexity(model: Any, eval_dataset: Any) -> float:
    """Calculate the perplexity of the model on the given evaluation dataset.

    Args:
        model (Any): The language model to evaluate.
        eval_dataset (Any): The evaluation dataset.

    Returns:
        float: The calculated perplexity.
    """
    # This is a placeholder implementation
    # we need to adjust this based on our specific model and dataset structure
    total_loss = 0
    total_tokens = 0
    for batch in eval_dataset:
        inputs = batch["input_ids"]
        labels = batch["labels"]
        outputs = model(input_ids=inputs, labels=labels)
        total_loss += outputs.loss.item() * inputs.size(0)
        total_tokens += inputs.ne(model.config.pad_token_id).sum().item()

    avg_loss = total_loss / total_tokens
    perplexity = np.exp(avg_loss)
    return perplexity


if __name__ == "__main__":
    # Example usage
    sample_predictions = [1, 0, 1, 1, 0]
    sample_labels = [1, 1, 1, 0, 0]
    metrics = calculate_metrics(sample_predictions, sample_labels)
    print("Sample metrics:", metrics)

    # Note: calculate_perplexity cannot be demonstrated without actual model and dataset
    print("Perplexity calculation requires a model and evaluation dataset.")
