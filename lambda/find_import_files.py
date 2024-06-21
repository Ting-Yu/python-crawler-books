import logging
import requests
import botocore.exceptions
import bs4
import time
import psutil
import os
import random
from datetime import datetime
import pandas as pd
import humanfriendly
import boto3
from urllib.parse import urlparse
import charset_normalizer

modules = [logging, requests, botocore.exceptions, bs4, time, psutil, os, random, datetime, pd, humanfriendly, boto3, urlparse, charset_normalizer]

for module in modules:
    if hasattr(module, '__file__'):
        print(f"{module.__name__} is installed in: {os.path.dirname(module.__file__)}")
    else:
        print(f"{module.__name__} is a built-in module.")