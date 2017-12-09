import pycommon.patterns
from pycommon import ConfigBase


@pycommon.patterns.singleton
class WebhookConfig(ConfigBase):
    CACHE_MAXSIZE = None
    CACHE_TTL = None
    AMIS_TOKEN_SERVICE = None
    AMIS_URL_SERVICE = None
    DF_CLIENT_ACCESS_TOKEN = None
    DF_API_VERSION = None
    DF_API_TIMEZONE = None
    DF_API_LANG = None

cfg = WebhookConfig()
cfg.merge_file(pycommon.get_callee_path() + "/config.ini")
cfg.merge_env()
