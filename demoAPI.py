from flask import Flask, request
from flask_restful import Resource, Api
from config import Config
import textai
import random
import AITester

app = Flask(__name__)
api = Api(app)


class Generate(Resource):
    def get(self):
        auth = request.args.get('key')
        config = Config()
        if auth == config.restKey:
            return textai.getText(config.prompt, int(config.maxTokens), float(config.temp), config.model, config.apiKey,
                                  config.loglevel)
        else:
            return "Unauthorized", 401


class GenerateReal(Resource):
    def get(self):
        auth = request.args.get('key')
        config = Config()
        if auth != config.restKey:
            return "Unauthorized", 401
        # Grab random twewt from real dataset
        with open(config.real, 'r', errors='ignore') as f:
            dataset = f.read().splitlines()
        return random.choice(dataset)


class classify(Resource):
    def get(self):
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
