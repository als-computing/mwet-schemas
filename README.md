# NMR metadata schema using LinkML

This repository contains code to help manage schemas and workflows for managing data for the MWET project. There are several workflows supported:

1. Maintian an publish a list metadata fields that are collected for various techniques. For this, the [LinkML](https://linkml.io/) and its expressive schema definition format is used. In this repository, we manage the LinkML schema.

2. Using LinkML, produce [JSON Schema](https://json-schema.org/) files for the LinkML Schemas. These published JSON Schemas will be maintained in GitHub and re-built whenever the accompanying LinkML schema changes in this repostiory.

3. The MWET repsotory uses [SciCat](https://scicatproject.github.io/) to manage datasets. SciCat has a very flexible "Scientific Metadata" dictionary for each collected dataset. JSON Schemas can be used by the ingestion code to validate incoming Scientific Metadata on ingest.


<!-- For more information about the workflow, check out this [gitlab](https://gitlab.desy.de/ric/opendata-metadata) tutorial. -->


## Getting started

### 0. Setup environment

[LinkML](https://linkml.io/linkml/intro/tutorial.html) if you wish to work directly with these files. The [Quick Install Guide](https://linkml.io/linkml/intro/install.html) page gives more detailed information.

1. Create a new conda environment

```
conda create -n linkml python=3.10
conda activate linkml
```

2. Install linkml package

```
python -m pip install -e .
```

3. If you are interested in ingesting example data to the SciCat database

```
python -m pip install -e ".[ingest]"
```

This command will install ingesting required packages, as specify in the ```pyproject.toml``` file.


### 1. Schemasheets

Schemasheets is part of the LinkML toolset that allows a LinkML data description to be converted to a spreadsheet and vice versa. See install guide [here](https://github.com/linkml/schemasheets).

Generation of spreadsheet through linkml schemasheets

```
linkml2schemasheets-template -i nmr.yaml -o nmr_concise.tsv -s concise
```
or
```
linkml2schemasheets-template -i nmr.yaml -o nmr_exhaustive.tsv -s exhaustive
```

### 2. Generate json schema

Generating a corresponding (closed world) JSON-Schema definition (`nmr.schema.json`) for the NMR datasets:

```
gen-json-schema --closed nmr.yaml  >nmr.schema.json
```

### 3. Simple worked examples to validate the csv input metadata

Check ("valdate") that some csv metadata (`my-nmr-metadata.csv`) complies with the SFX metadata defintion (`nmr.yaml`):

```
linkml-validate -s nmr.yaml my-nmr-metadata.csv
```

### 4. Convert validated csv file to json
Specify the input csv file an output json file.
```
python script.py my-nmr-metadata.csv output.json
```

### 5. Ingest NMR data and metadata
An example metadata file named ```example-nmr-metadata.csv``` is provided, as well as an example data file named ```example-nmr-metadata.csv``` for ingesting to [SciCat](https://github.com/SciCatProject/pyscicat) database. This data was acquired at University of California, Santa Barbara by Leo Gordon and Raphaële Clément.

To ingest the nmr data and metadata to [local SciCat](https://github.com/SciCatProject/scicatlive) database:

1. install packages as described in step 0:

```
python -m pip install -e ".[ingest]"
```

3. create a ```.env``` file following the pattern in ```example_env.env``` in the nmr_schema folder
`
4. run ```python ingest_nmr.py ``` to ingest the example data

## Next Step
- schema for 2d NMR data
- github action that generate the json schema and puts it in a public location -> github page


## Developer Setup
If you are developing this library, there are a few things to note.

1. Install development dependencies:

```
pip install .[dev]
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
