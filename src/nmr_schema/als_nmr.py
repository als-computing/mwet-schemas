import json
import logging
from collections import OrderedDict
from datetime import datetime
from pathlib import Path

from pyscicat.client import ScicatClient, get_file_mod_time, get_file_size
from pyscicat.model import (
    CreateDatasetOrigDatablockDto,
    DataFile,
    DatasetType,
    Ownable,
    RawDataset,
)

# from scicat_beamline.ingestors.common_ingestor_code import create_data_file, create_data_files_list
# from scicat_beamline.scicat_utils import encode_image_2_thumbnail
# from scicat_beamline.utils import Issue

ingest_spec = "als_nmr"

logger = logging.getLogger("scicat_ingest.NMR")

global_keywords = ["NMR"]

# Note: update the scicat_metadata based on the data you will upload
# scicat metadata is seperate from scientific_metadata (do not duplicate)
# note that this code requires the csv file only have one line for header, and one line for values
metadata_path = "metadata.json"
file = open(metadata_path)
data = json.load(file)
linkml_metadata = data["datasets"][0]
file.close()

scicat_metadata = {
    "owner": linkml_metadata["owner"],
    "email": linkml_metadata["owner_email"],
    "instrument_name": linkml_metadata["instrument_name"],
    "pi": linkml_metadata["principal_investigator"],
    "proposal": linkml_metadata["proposal"],
    "techniques": [linkml_metadata["instrument_name"]],
    "derived_techniques": [],
}


def ingest(
    scicat_client: ScicatClient,
    username: str,
    file_path: Path,
    thumbnail_dir: Path,
    issues,
) -> str:
    "Ingest a folder of 1d nmr files"

    now_str = datetime.isoformat(datetime.now()) + "Z"
    ownable = Ownable(
        owner="MWET",
        contactEmail="rjiang2@lbl.gov",
        createdBy="runboj",
        updatedBy="runboj",
        updatedAt=now_str,
        createdAt=now_str,
        ownerGroup="MWET",
        accessGroups=["MWET", "ingestor"],
        instrumentGroup="instrument-default",
    )

    # issues: List[Issue] = []
    issues = []

    # read scientific_metadata from the metadata.json file
    # only one row of metadata as of this protype (Apr 16)
    keys = list(linkml_metadata.keys())
    keys_to_keep = keys[5:]
    scientific_metadata = OrderedDict(
        {key: linkml_metadata[key] for key in keys_to_keep}
    )
    print(scientific_metadata)

    description = file_path.stem.replace("_", " ")
    filename = file_path.name

    dataset = RawDataset(
        owner="Leo Gordon",
        contactEmail="leo@gmail.com",
        creationLocation="ALS ?.?.?",
        datasetName=filename,
        type=DatasetType.raw,
        instrumentId="6.3.2",
        proposalId=scicat_metadata["proposal"],
        dataFormat="ALS BCS",
        principalInvestigator=scicat_metadata["pi"],
        sourceFolder=file_path.parent.as_posix(),
        scientificMetadata=scientific_metadata,
        sampleId=scientific_metadata["sample"],
        isPublished=False,
        description=description,
        keywords=["NMR", "1d"],
        creationTime=scientific_metadata["acquisition_date"],
        **ownable.dict(),
    )
    print(file_path)
    file_name = Path(file_path).name
    print(file_name)
    dataset_id = scicat_client.upload_new_dataset(dataset)
    data_file = DataFile(
        path=str(file_name),
        size=get_file_size(Path(file_path)),
        time=get_file_mod_time(Path(file_path)),
        type="RawDatasets",
    )

    data_block = CreateDatasetOrigDatablockDto(
        size=get_file_size(file_path),
        datasetId=dataset_id,
        dataFileList=[data_file],
        **ownable.dict(),
    )
    scicat_client.datasets_origdatablock_create(dataset_id, data_block)

    return dataset_id, issues
