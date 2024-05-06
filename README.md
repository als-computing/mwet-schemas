# NMR metadata schema using LinkML

This repository contains code to help manage schemas and workflows for managing data for the MWET project. There are several workflows supported:

1. Maintian an publish a list metadata fields that are collected for various techniques. For this, the [LinkML](https://linkml.io/) and its expressive schema definition format is used. In this repository, we manage the LinkML schema.

2. Using LinkML, produce [JSON Schema](https://json-schema.org/) files for the LinkML Schemas. These published JSON Schemas will be maintained in GitHub and re-built whenever the accompanying LinkML schema changes in this repostiory.

3. The MWET repsotory uses [SciCat](https://scicatproject.github.io/) to manage datasets. SciCat has a very flexible "Scientific Metadata" dictionary for each collected dataset. JSON Schemas can be used by the ingestion code to validate incoming Scientific Metadata on ingest.


<!-- For more information about the workflow, check out this [gitlab](https://gitlab.desy.de/ric/opendata-metadata) tutorial. -->


## Getting started

### 0. Setup environment

[LinkML](https://linkml.io/linkml/intro/tutorial.html) if you wish to work directly with these files. The [Quick Install Guide](https://linkml.io/linkml/intro/install.html) page gives more detailed information.

1. Create a new conda environment called "linkml"

```
conda create -n linkml python=3.10
conda activate linkml
```

2. Install packages as specified in ```pyproject.toml```

```
python -m pip install -e .
```

3. If you are interested in ingesting example data to the SciCat database

```
python -m pip install -e ".[ingest]"
```

This command will install ingesting required packages, as specified in the ```pyproject.toml``` file.


### 1. Schemasheets

Schemasheets is part of the LinkML toolset that allows a LinkML data description to be converted to a spreadsheet and vice versa. See install guide [here](https://github.com/linkml/schemasheets).

Generation of spreadsheet through linkml schemasheets

```
linkml2schemasheets-template -i src/nmr_schema/nmr_schema.yaml -o nmr_concise.tsv -s concise
```
or
```
linkml2schemasheets-template -i src/nmr_schema/nmr_schema.yaml -o nmr_exhaustive.tsv -s exhaustive
```
[exhaustive|concise] represents report style.

### 2. Generate json schema

Generating a corresponding JSON-Schema definition (`nmr.schema.json`) for the NMR datasets:

```
gen-json-schema --closed src/nmr_schema/nmr_schema.yaml  >nmr.schema.json
```

### 3. Simple working examples to validate the csv input metadata

Check ("valdate") that example csv metadata (`src/example_data/example-nmr-metadata.csv`) complies with the SFX metadata defintion (`nmr_schema.yaml`):

```
linkml-validate -s src/nmr_schema/nmr_schema.yaml src/example_data/example-nmr-metadata.csv
```

### 4. Convert validated csv file to json
Specify the input csv file an output json file.
```
linkml-convert -s src/nmr_schema/nmr_schema.yaml -o src/nmr_schema/metadata.json --index-slot datasets src/example_data/example-nmr-metadata.csv
```
For more information on converting between different representations, visit this [linkmk documentation](https://linkml.io/linkml/data/conversion.html#cmdoption-linkml-convert-S).

### 5. Ingest NMR data and metadata
An example metadata file named ```example-nmr-metadata.csv``` is provided, as well as an example data file named ```example-nmr-metadata.csv``` for ingesting to [SciCat](https://github.com/SciCatProject/pyscicat) database. This data was acquired at University of California, Santa Barbara by Leo Gordon and Raphaële Clément.

To ingest the nmr data and metadata to [local SciCat](https://github.com/SciCatProject/scicatlive) database:

1. install packages as described in step 0:

```
python -m pip install -e ".[ingest]"
```

3. create an ```.env``` file at the linkml_nmr folder following the pattern in ```.env.example``` file

4. run the following command in terminal to to ingest the example data
```
cd src/nmr_schema
python ingest_nmr.py
```

## Next Step
- schema for 2d NMR data
- github action that generate the json schema and puts it in a public location -> github page


## Developer Setup
If you are developing this library, there are a few things to note.

1. Install development dependencies:

```
python -m pip install ".[dev]"
```

2. Install pre-commit
This step will setup the pre-commit package. After this, commits will get run against flake8, black, isort.

```
pre-commit install
```

3. (Optional) If you want to check what pre-commit would do before commiting, you can run:

```
pre-commit run --all-files
```
