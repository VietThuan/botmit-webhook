import pycommon.patterns
from pycommon import ConfigBase


@pycommon.patterns.singleton
class WebhookConfig(ConfigBase):
    FANPAGE_TOKEN = None
    GENDER_U = None
    GENDER_L = None
    THREAD_TIMEOUT = None
    CACHE_MAXSIZE = None
    CACHE_TTL = None


cfg = WebhookConfig()
cfg.merge_file(pycommon.get_callee_path() + "/config.ini")
cfg.merge_env()
