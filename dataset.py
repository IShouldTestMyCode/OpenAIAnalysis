"""
Dataset stuff
"""

import textai
import logging


def generateDataset(config):
    """
    Generates a dataset from OpenAI. Uses Config. Populates dataset.
    :param config: Configuration. Object Config
    """
    logging.basicConfig(level=config.loglevel)
    logging.info("Generating dataset...")
    for i in range(int(config.iter)):
        logging.info("Generated " + str(i + 1) + " of " + config.iter + " documents.")
        response = textai.getText(config.prompt, int(config.maxTokens), float(config.temp), config.model, config.apiKey,
                                  config.loglevel)
        with open(config.dataset, 'a', errors="ignore") as f:
            f.write(response + "\n")


def createImportable(config, intent, clean):
    """
    Populates a file, output (config), with data that is importable to VertexAI (CSV).
    :param config: Configuration. Object Config
    :param intent: Label
    :param clean: Whether to clean up the dataset or not.
    :return: None
    """
    logging.basicConfig(level=config.loglevel)
    # Create an importable dataset of real tweets, for Vertex AI
    # Read dataset
    logging.info("Creating importable dataset...")
    with open(config.dataset, 'r', errors='ignore') as f:
        dataset = f.read().splitlines()
        logging.debug("Dataset read.")

    for i in range(len(dataset)):
        logging.info("Processed " + str(i + 1) + " of " + str(len(dataset)) + " documents to an importable dataset.")
        txt = dataset[i]
        if clean:
            txt = txt.replace("\"", "")
            if txt == "" or len(txt) < 6:
                continue

        # Remove non-ascii characters
        txt = ''.join([i if ord(i) < 128 else ' ' for i in txt])
        # Prepend and append with quotes
        txt = '"' + txt + '"'
        # Append label
        txt = txt + ',' + intent
        # Write to file
        with open(config.output, 'a') as f:
            f.write(txt + "\n")
