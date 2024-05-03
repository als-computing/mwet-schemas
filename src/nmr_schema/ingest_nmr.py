import glob
import logging
import os
import pathlib

from dotenv import load_dotenv
from ingest import ingest

load_dotenv()
logger = logging.getLogger(__name__)

ROOT_FOLDER = os.getenv("ROOT_FOLDER")
SCICAT_URL = os.getenv("SCICAT_URL")
USERNAME = os.getenv("USERNAME")
INGEST_USER = os.getenv("INGEST_USER")
PASSWORD = os.getenv("PASSWORD")
INGEST_SPEC = os.getenv("INGEST_SPEC")
DERIVED_FOLDER = os.getenv("DERIVED_FOLDER")

logger.info("env file loaded")

assert type(ROOT_FOLDER) is str and len(ROOT_FOLDER) != 0
assert type(SCICAT_URL) is str and len(SCICAT_URL) != 0
assert type(USERNAME) is str and len(USERNAME) != 0
assert type(PASSWORD) is str and len(PASSWORD) != 0
assert type(INGEST_USER) is str and len(INGEST_USER) != 0
assert type(INGEST_SPEC) is str and len(INGEST_SPEC) != 0

is_derived_folder = False

ROOT_FOLDER = pathlib.Path(ROOT_FOLDER)

pattern = None
ingestor_location = None
override_iterator = False
ingest_files_iter = []
if INGEST_SPEC == "als_nmr":
    pattern = f"{ROOT_FOLDER}/*.csv"
    ingestor_location = pathlib.Path(os.getcwd(), "als_nmr.py")
else:
    raise Exception("Environment variable 'INGEST_SPEC' is invalid.")

if override_iterator is False:
    ingest_files_iter = glob.iglob(pattern)

for ingest_file_str in ingest_files_iter:
    ingest_file_path = pathlib.Path(ingest_file_str)
    if ingest_file_path.exists():
        # print(ingest_file_path)
        logger.info(ingest_file_path)
        if is_derived_folder is False:
            ingest(
                ingestor_location,
                ingest_file_path,
                None,
                INGEST_USER,
                SCICAT_URL,
                token=None,
                username=USERNAME,
                password=PASSWORD,
            )
        else:
            ingest(
                ingestor_location,
                ingest_file_path,
                pathlib.Path(DERIVED_FOLDER),
                INGEST_USER,
                SCICAT_URL,
                token=None,
                username=USERNAME,
                password=PASSWORD,
            )
