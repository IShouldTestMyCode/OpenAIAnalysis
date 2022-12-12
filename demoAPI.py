"""
Demo API - An API to preform demos.
Please no I don't really know how this works or how to fix it :P
"""


from flask import Flask, request
from flask_restful import Resource, Api
from config import Config
import textai
import random
import AITester

app = Flask(__name__)
api = Api(app)


# noinspection PyMethodMayBeStatic
class Generate(Resource):
    """
    Generates a new text based on the prompt
    """

    def get(self):
        """
        Generates a new text based on the prompt
        """
        auth = request.args.get('key')
        config = Config()
        if auth == config.restKey:
            return textai.getText(config.prompt, int(config.maxTokens), float(config.temp), config.model, config.apiKey,
                                  config.loglevel)
        else:
            return "Unauthorized", 401


# noinspection PyMethodMayBeStatic
class GenerateReal(Resource):
    """
    Selects a new text based on the prompt
    """

    def get(self):
        """
        Randomly select a real text from the dataset
        """
        auth = request.args.get('key')
        config = Config()
        if auth != config.restKey:
            return "Unauthorized", 401
        # Grab random tweets from real dataset
        with open(config.real, 'r', errors='ignore') as f:
            dataset = f.read().splitlines()
        return random.choice(dataset)


# noinspection PyMethodMayBeStatic,PyPep8Naming
class classify(Resource):
    """
    Classify a text
    """

    def get(self):
        """
        Classify a text
        """
        auth = request.args.get('key')
        text = request.args.get('text')
        full = request.args.get('full')
        config = Config()
        if auth != config.restKey:
            return "Unauthorized", 401

        if full != "true":
            return AITester.parsePrediction(AITester.predict(config, text), config)
        else:
            return str(AITester.predict(config, text))


api.add_resource(Generate, '/api/v1/gen/fake')
api.add_resource(GenerateReal, '/api/v1/gen/real')
api.add_resource(classify, '/api/v1/classify')
