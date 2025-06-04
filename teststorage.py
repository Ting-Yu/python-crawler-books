import sys
import os
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages')

from dobby_storage.storage import FileStorage
import json
from pathlib import Path

config_path = 'storage.json'

file_storage = FileStorage()

file_storage.save(config_path, 'destination.json')