"""Configuration to connect to a PostgreSQL database."""

# Standard Python Libraries
from configparser import ConfigParser
import platform

# Third-Party Libraries
from importlib_resources import files

myplatform = platform.system()

REPORT_DB_CONFIG = files("dkplastics").joinpath("data/dbconfig.config")


def config(filename=REPORT_DB_CONFIG, section="postgreslocal"):
    """Parse Postgres configuration details from database configuration file."""
    parser = ConfigParser()

    parser.read(filename, encoding="utf-8")

    db = dict()

    if parser.has_section(section):
        for key, value in parser.items(section):
            db[key] = value

    else:
        raise Exception(f"Section {section} not found in {filename}")

    return db

