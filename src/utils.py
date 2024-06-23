import logging
from loguru import logger
import sentry_sdk
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from sentry_sdk.integrations.logging import LoggingIntegration

# def get_logger(name: str):
#     logger = logging.getLogger(name)
#     logger.setLevel(logging.INFO)
#
#     handler = logging.StreamHandler()
#     formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
#     handler.setFormatter(formatter)
#
#     if not logger.handlers:
#         logger.addHandler(handler)
#         logger.propagate = False
#
#     return logger


# Setup Sentry
sentry_logging = LoggingIntegration(
    level=logging.INFO,        # Capture info and above as breadcrumbs
    event_level=logging.ERROR  # Send errors as events
)
sentry_sdk.init(
    dsn="https://108cf956032577b7b2f4514cdeb7cb43@o4507482987167744.ingest.de.sentry.io/4507482988871760",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    integrations=[sentry_logging]
)

# Setup Loguru
logger.info("Loguru and Sentry are setup and ready to go!")


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )
