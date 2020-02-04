import os
import csv

class Importer():

    def __init__(self, custom_importers=None):
        '''
        Initializes the importer class. Custom import functions can be passed in as Dict

        Parameters:
            custom_importer (dict): A custom file importer specifing the file extension and the function as a key, value pair
                example: { 'file_ext' : custom_function }
        '''

        self.import_formats = {
            'csv': self.load_csv
        }
        if isinstance(custom_importers, dict):
            self.import_formats.update(custom_importers)

    def load(self, file):
        if not os.path.isfile(file):
            raise FileNotFoundError(f'File not accessible: {file}')
        _, ext = os.path.splitext(file)
        ext = ext[1:]
        if ext in self.import_formats:
            return self.import_formats[ext](file)
        raise ValueError(f'Unsupported import format. Available formats: {[f for f in self.import_formats]}')

    def load_csv(self, file):
        with open(file, 'r') as f:
            sniffer = csv.Sniffer()
            sample_bytes = 1024
            if not sniffer.has_header(f.read(sample_bytes)):
                raise ValueError('No headers identified on input file')

        with open(file, 'r') as f:
            reader = csv.reader(f)
            headers = next(reader)
            for row in reader:
                standardized_row = {}
                for header_index in range(len(headers)):
                    standardized_row[headers[header_index]] =  row[header_index]
                yield standardized_row
