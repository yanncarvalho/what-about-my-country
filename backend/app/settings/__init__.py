"""Django settings init"""

import os
from pathlib import Path
from dotenv import load_dotenv
profile = os.getenv('APP_ENVIRONMENT')

env_path = os.path.join(Path(__file__).parent.parent.parent, '.envs', profile)
load_dotenv(env_path)
# pylint: disable=wrong-import-position
from .base import *
if profile == 'prod':
    from .prod import *
else:
    from .dev import *
