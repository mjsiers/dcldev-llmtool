import logging
from typing import Dict, Optional

import fsspec
import toml

# configure logging
logger = logging.getLogger(__name__)

# define and set the default log level setting
default_loglevel = logging.INFO

# define and set the default ollama model names
ollama_model_embed = "nomic-embed-text"
ollama_model_chat = "mistral:7b"

# define and set the default database table names
lancedb_database_path = "./data/vectors/lancedb"
lancedb_database_name = "dcl-llmtool"
lancedb_assessment_table = "dcl-assessment"
lancedb_section_table = "dcl-section"


def load_config() -> None:
    config_filepath: str = "./config.toml"
    config: Optional[Dict] = None

    # check to see if there is a local configuration file
    if config_filepath is not None:
        fs = fsspec.filesystem("file")
        file_exists = fs.exists(config_filepath)
        file_valid = fs.isfile(config_filepath)
        if not file_exists or not file_valid:
            logger.error("load_config: [%s] was not found.", config_filepath)
            return None

        # read in the toml configuration file
        with open(config_filepath, "r") as f:
            config = toml.load(f)

    # no configuration specified
    if config is None:
        logger.info("load_config: Using default configuration values.")
        return

    # load the ollama model configuration values
    logger.info("load_config: Using [%s] configuration values.", config_filepath)
    if "models" in config:
        if "embedding" in config["models"]:
            ollama_model_embed = config["models"]["embedding"]
            logger.debug("load_config: %s: %s", "ollama_model_embed", ollama_model_embed)
        if "chat" in config["models"]:
            ollama_model_chat = config["models"]["chat"]
            logger.debug("load_config: %s: %s", "ollama_model_chat", ollama_model_chat)

    # load the lancedb vector database configuration values
    if "lancedb" in config:
        if "database_path" in config["lancedb"]:
            lancedb_database_path = config["lancedb"]["database_path"]
            logger.info("load_config: %s: %s", "lancedb_database_path", lancedb_database_path)
        if "database_name" in config["lancedb"]:
            lancedb_database_name = config["lancedb"]["database_name"]
            logger.info("load_config: %s: %s", "lancedb_database_name", lancedb_database_name)
        if "assessment_table" in config["lancedb"]:
            lancedb_assessment_table = config["lancedb"]["assessment_table"]
            logger.info("load_config: %s: %s", "lancedb_assessment_table", lancedb_assessment_table)
        if "section_table" in config["lancedb"]:
            lancedb_section_table = config["lancedb"]["section_table"]
            logger.info("load_config: %s: %s", "lancedb_section_table", lancedb_section_table)
