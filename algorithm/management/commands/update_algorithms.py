# -*- coding: utf-8 -*-
from algorithm.controllers import *
from django.core.management.base import BaseCommand
import traceback
from algorithm.controllers import *
import json


class Command(BaseCommand):
    help = u"""Command to update algorithms on the database. Requires that either the extractor was used previously
                or that the classifications are updated"""

    def get_algorithms(self):
        algorithms = []
        extraction_path = 'extractor/temp/algorithms/'
        for extraction_file in os.listdir(extraction_path):
            with open(extraction_path + extraction_file) as data_file:
                algorithms.append(json.load(data_file))

        return algorithms

    def get_classifications(self):
        extraction_path = 'extractor/temp/'
        with open(extraction_path + 'classifications.json') as data_file:
            return json.load(data_file)

    def update_algorithms(self, algorithms):
        for algorithm in algorithms:
            insert_algorithm_db(algorithm['name'], algorithm['about'], get_classification_by_name(algorithm['classification']), algorithm['dbpedia_url'], True)

    def update_classifications(self, classifications):
        for classification in classifications:
            insert_classification_db(classification['classification'], classification['uri'])

    def handle(self, *args, **options):
        try:
            classifications = self.get_classifications()
            self.update_classifications(classifications)

            algorithms = self.get_algorithms()
            self.update_algorithms(algorithms)
        except:
            traceback.print_exc()
            pass