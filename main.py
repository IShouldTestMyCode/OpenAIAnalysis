"""
OpenAIAnalysis
A software that provides tools to create a machine learning model to differentiate information about
"""

from config import Config
import demoAPI

config = Config()
if __name__ == '__main__':
    demoAPI.app.run()  # run our Flask app
