# Trivago File Format Converter

A Command Line data file format converter. It accepts a data file, converts and saves in other file formats.

## Installation

The tool can be setup on a virtual environment using `virtualenv` or in a `docker` container using `docker-compose`.

**Mandatory** Grant execute permission to the executable files

```bash
chmod +x ./scripts/run_local.sh ./scripts/docker_start.sh ./converter/convert-cli.py
```

### Virtual Environment

**Note:** Make sure you have [pip3](https://pip.pypa.io/en/stable/) installed on your computer.

From the root directory, run the following script in your terminal:

```bash
./scripts/run_local.sh
```

**Note:** If you get a `Permission Denied` error trying to run the shell file, **grant premission** to the script file using:

```bash
chmod +x ./scripts/run_local.sh
```

Activate the created environment using

```bash
source ./venv/bin/activate
cd converter
```

And we are done!


### Docker-Compose

**Note:** Make sure you have [docker-compose](https://docs.docker.com/compose/install/) installed on your computer.

From the root directory, run the following script in your terminal:

```bash
./scripts/docker_start.sh
```

**Note:** If you get a `Permission Denied` error trying to run the shell file. Grant access to the script file using:

```bash
chmod +x ./scripts/docker_start.sh
```
This will build the docker container, start it, and attach to it's shell instance.

And we are done!



## Usage


```bash
convert-cli.py -in [-out] [-format] [-force] [-error-file]
```

Options:

  - `-in`           | `-i`      (string) path to input file to convert **Mandatory** (supported formats: `csv`, `json`).
  - `-out`          | `-o`      (string) path to output directory where exported files will be stored (optional) | default: `./files/output`.
  - `-format`       | `-format` (string) export format. Available formats `json`, `xml`.
  - `-force`        | `-force`  (bool) force export of records, including records that failed validation.
  - `-error-file`   | `-e`      (string) path to file where error logs are stored on failed validations. | default: `./files/output/error.json`.


## Development

The tool is structured to allow developers plugin any import and/or export logic of any file format. Also develop custom validations to be used while processing data. This is achieved by modularizing major components of the tool. The diagram below shows the break-down.

+---------+       +------------------------+    +----------+
| Importer|       |       Processor        |    | Exporter |
|         |       |                        |    |          |
|         |       |                        |    | json     |
| csv     |       |   {                    |    | xml      |
| json    +------->     'prop1': 'value1', +----> ...      |
| ...     |       |     'prop2': 'value2'  |    |          |
|         |       |   }                    |    |          |
|         |       |                        |    |          |
|         |       |                        |    |          |
|         |       +----------+-------------+    |          |
+---------+                  ^                  +----------+
                             |
                     +-------v--------+
                     |                |
                     |   Validators   |
                     |                |
                     |                |
                     +----------------+

### Importers

The importer class `./converter/importer.py` accepts a `custom_importers` argument that allows you add import functions for specific file formats.
The requirements for the import function are:
-   Read data from file
-   Extract headers or keys from file
-   Return an array of data rows as `dict` (use of generators are advised for better performance)

**Note** Register the import functions and pass as `custom_importers`

example:
```python
    import json
    from importer import Importer

    # Json import function
    def json_importer(file):
        with open(file, 'r') as f:
            data = json.load(f)
            if not isinstance(data, list):
                raise ValueError('Data is not a collection of rows')
            for row in data:
                yield row

    # Registering the importer
    custom_importers = {
        'json': json_importer
    }

    # Initialize importer object with custom importers
    importer = Importer(custom_importers=custom_importers)

    # Import json file
    data = importer.load('/path/to/json/file')
```

### Exporters

The exporter class `./converter/exporter.py` accepts a `custom_exporters` argument that allows you add export functions for specific file formats.
The requirements for the export function are:
-   Accept `data` and `folder` arguments (`data` `array [dict]`: dictionary array of data to be exported, `folder` `string`: path to the output folder)
-   Write data to file in specified format
-   Return the path of the output file as `string`

**Note** Register the export functions and pass as `custom_exporters`

example:
```python
    import csv
    from datetime import datetime
    from exporter import Exporter

    def csv_exporter(data, folder):
        file_name = f'{folder}/trivago-{datetime.today().strftime("%Y-%m-%d-%H-%M-%S")}.csv'
        with open(file_name, 'w') as csv_file:
            props = []
            csv_writer = csv.writer(csv_file)
            for item in data:
                if not len(props):
                    props = item.keys()
                    csv_writer.writerow(props)
                csv_writer.writerow(item.values())
        return file_name

    # Registering the importer
    custom_exporters = {
        'csv': csv_exporter
    }

    # Initialize importer object with custom importers
    exporter = Exporter(custom_exporters=custom_exporters)

    # Export csv file
    data = exporter.write(data, '/path/to/output/dir', 'csv')
```

### Validators

The validator class `./converter/validator.py` allows development of custom validators based on this class. Override the `validate` method to include your validation logic.
The requirements of this class are:
- Initialize base class in your `__init__` method
- Call the `keep_count()` method at the start of your `validate` method.
- In the validate method, concatenate list of generated errors and assign to `self.errors`

Exmaple:
> `./converter/custom_validators/hotel_validator.py`


## Developed by

-   Name    :   Lord-Mallam Nugwan
-   Email   :   lordy002000@gmail.com
-   GitHub  :   [http://github.com/lordmallam](http://github.com/lordmallam/)
