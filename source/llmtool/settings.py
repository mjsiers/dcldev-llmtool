import dataclasses
import logging
from typing import Dict, Optional

import dacite
import fsspec
import toml

# configure logging
logger = logging.getLogger(__name__)


@dataclasses.dataclass
class ModelsConfig:
    embedding: str
    chat: str

    @classmethod
    def get_defaults(cls):
        return ModelsConfig("", "")


@dataclasses.dataclass
class LanceDbConfig:
    database_path: str
    database_name: str
    assessment_table: str
    section_table: str

    @classmethod
    def get_defaults(cls):
        return LanceDbConfig("", "", "", "")


@dataclasses.dataclass
class TemplateConfig:
    template_path: str
    template_keywords: str
    template_sections: str
    template_tables: str

    @classmethod
    def get_defaults(cls):
        return TemplateConfig("", "", "", "")


@dataclasses.dataclass
class CrewConfig:
    crew_path: str
    crew_agents: str

    @classmethod
    def get_defaults(cls):
        return CrewConfig("", "")


@dataclasses.dataclass
class AppConfig:
    models: ModelsConfig
    lancedb: LanceDbConfig
    template: TemplateConfig
    crew: CrewConfig

    @classmethod
    def get_defaults(cls):
        return AppConfig(
            models=ModelsConfig.get_defaults(),
            lancedb=LanceDbConfig.get_defaults(),
            template=TemplateConfig.get_defaults(),
            crew=CrewConfig.get_defaults(),
        )


def load_config() -> Optional[AppConfig]:
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

    # load the configuration values
    logger.info("load_config: Using [%s] configuration values.", config_filepath)
    app_config = AppConfig.get_defaults()  # type: ignore
    for k, v in config.items():
        key = k.lower()
        if key == "models":
            app_config.models = dacite.from_dict(data_class=ModelsConfig, data=v)
        elif key == "lancedb":
            app_config.lancedb = dacite.from_dict(data_class=LanceDbConfig, data=v)
        elif key == "template":
            app_config.template = dacite.from_dict(data_class=TemplateConfig, data=v)
        elif key == "crew":
            app_config.crew = dacite.from_dict(data_class=CrewConfig, data=v)
        else:
            logger.warning("load_config: Unknown configuration value [%s].", k)

    # ensure we have a valid configuration
    if (
        app_config.models is None
        or app_config.lancedb is None
        or app_config.template is None
        or app_config.crew is None
    ):
        logger.error("load_config: Missing required configuration values.")
        return None

    return app_config
