import logging
import os
import json
from itertools import tee
from importer import Importer
from validator import Validator
from custom_validators.hotels_validator import HotelValidator
from exporter import Exporter
from custom_importers.json_importer import json_importer
from custom_exporters.csv_exporter import csv_exporter
import traceback

LOG = logging.getLogger('PROCESSOR')
LOG.setLevel(os.environ.get('LOGGING_LEVEL', logging.INFO))

class Processor():

    def convert(
        self,
        input_file,
        output_dir=None,
        output_format='json',
        export_with_errors=False,
        errors_file='./files/output/errors.json'
    ):

        #  Register custom importers
        c_importers = {
            'json': json_importer
        }

         #  Register custom exporters
        c_exporters = {
            'csv': csv_exporter
        }

        importer = Importer(custom_importers=c_importers)
        validator = HotelValidator()
        exporter = Exporter(custom_exporters=c_exporters)

        try:
            data =  importer.load(input_file)
            data, data_backup = tee(data)

            # Validate data
            for row in data:
                validator.validate(row)

            error_count = len(validator.errors)
            LOG.warning(f'Validated {validator.count} records. Found {error_count} errors.')
            if error_count:
                with open(errors_file, 'w') as error_file:
                    error_file.write(json.dumps(validator.errors))
                if export_with_errors:
                   LOG.debug(f'Export to {output_format} started.')
                   output = exporter.write(data_backup, output_dir, output_format)
                   LOG.warning(f'Exported successfully. View file: {os.path.abspath(output)}')
                else:
                    LOG.error(f'Errors identified. Export process stopped. You can view the error logs at {os.path.abspath(errors_file)}')
        except Exception as e:
            LOG.error(str(e))