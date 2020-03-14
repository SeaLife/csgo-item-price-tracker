import requests
import json
import os
import logging

log = logging.getLogger("error")


def check_version():
    local_version = os.getenv('APP_VERSION', 'SNAPSHOT')

    try:
        data = requests.get('https://git.r3ktm8.de/api/v4/projects/228/repository/tags')
        resolved = json.loads(data.content)

        newest_version = resolved[0]["release"]["tag_name"]

        if newest_version != local_version:
            return False, newest_version
        return True, None
    except Exception as e:
        log.error(e.args)
        return True, None
