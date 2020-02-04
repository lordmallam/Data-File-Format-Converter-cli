from datetime import datetime
import json
import os

class Exporter():

    def __init__(self, custom_exporters=None):
        '''
        Initializes the Exporter class. Custom export functions can be passed in as Dict

        Parameters:
            custom_importer (dict): A custom file exporter specifing the file extension and the function as a key, value pair
                example: { 'file_ext' : custom_function }
        '''

        self.export_formats = {
            'json': self.write_json,
            'xml': self.write_xml
        }
        if isinstance(custom_exporters, dict):
            self.export_formats.update(custom_exporters)

    def write(self, data, folder, output_format):
        if not os.path.isdir(folder):
            raise IOError(f'Directory is not accessible: {folder}')
        if output_format in self.export_formats:
            return self.export_formats[output_format](data, folder)
        raise ValueError(f'Unsupported export format. Available formats: {[f for f in self.export_formats]}')

    def write_json(self, data, folder):
        file_name = f'{folder}/trivago-{datetime.today().strftime("%Y-%m-%d-%H-%M-%S")}.json'
        is_first = True
        with open(file_name, 'w') as json_file:
            json_file.write('[')
            for item in data:
                if is_first:
                    json_file.write(json.dumps(item))
                    is_first = False
                else:
                    json_file.write(',' + json.dumps(item))
            json_file.write(']')
        return file_name

    def write_xml(self, data, folder):
        file_name = f'{folder}/trivago-{datetime.today().strftime("%Y-%m-%d-%H-%M-%S")}.xml'
        with open(file_name, 'w') as xml_file:
            props = []
            xml_file.write('<root>')
            for item in data:
                if not len(props):
                    props = item.keys()
                children = ''
                for prop in props:
                    children += f'<{prop}>{item[prop]}</{prop}>'
                el = f'<row>{children}</row>'
                xml_file.write(el)
            xml_file.write('</root>')
        return file_name
