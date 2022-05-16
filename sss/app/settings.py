class GitSettingsRequests:
    HEADERS = {
        "Acccept": "application/vnd.github.v3+json"
    }
    VERIFY = False

class LocalSettings:
    DEBUG = True
    GIT_API_URL = "https://api.github.com"
    GIT_ORG = "MAEJER"
    GIT_TOKEN = "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"
    GIT_REQUESTS_HEADER = {
                "Acccept": "application/vnd.github.v3+json"
            }
    GIT_REQUESTS_VERIFY = False
    REPO_WHITELIST = "MAEJER/MAEJER-whitelists"
    FILE_PATH_SERVERCLASS = "serverclass/serverclass.conf"
    DIR_PATH_WHITELIST = "whitelists"
    PREFIX_REPO_FWD_APPS = "MAEJER-MyCluster-fwd-"
    PREFIX_DEP_APPS = "mj-d-"
