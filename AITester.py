"""
Testing Vertex AI Model
"""
import logging
import google.auth.exceptions

from textpred import predict_text_classification_single_label_sample
import os


def predict(config, text):
    """
    Predicts the label of a text.
    """
    logging.basicConfig(level=config.loglevel)
    os.environ["GOOGLE_CLOUD_PROJECT"] = config.project

    try:
        logging.info("Predicting " + text)
        return predict_text_classification_single_label_sample(
            project=config.project,
            endpoint_id=config.endpoint,
            location=config.location,
            content=text
        )

    except google.auth.exceptions.DefaultCredentialsError:
        logging.critical("You need to authenticate to GCP. https://cloud.google.com/sdk/gcloud/reference/auth"
                         "/application-default")
        logging.critical("Execute this to log in: gcloud auth application-default login")
        exit(1)


def parsePrediction(prediction, config):
    """
    Parses the prediction into a string.
    """
    logging.basicConfig(level=config.loglevel)
    logging.info("Parsing prediction...")
    # Get the labels
    labels = prediction["displayNames"]
    # Get the scores
    scores = prediction["confidences"]
    # Get the highest score
    highest = max(scores)
    # Get the index of the highest score
    index = scores.index(highest)
    # Get the label of the highest score
    label = labels[index]
    # Return the label
    return label
