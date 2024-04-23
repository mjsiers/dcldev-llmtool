import logging
from enum import Enum, unique

# configure logging
logger = logging.getLogger(__name__)


@unique
class SectionEnum(Enum):
    AAA = "aaa"
    BBB = "bbb"
    CCC = "ccc"
