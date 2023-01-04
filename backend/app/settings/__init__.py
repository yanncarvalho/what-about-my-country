
import os
from dotenv import load_dotenv
from pathlib import Path
profile = os.getenv('APP_ENVIRONMENT')


env_path = os.path.join(Path(__file__).parent.parent.parent,'.envs',profile)
load_dotenv(env_path)
from .base import *

if profile == 'prod':
   from .prod import *
else:
   from .dev import *

