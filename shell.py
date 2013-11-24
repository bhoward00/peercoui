#!/usr/bin/env python
import os
import readline
from pprint import pprint

from flask import *
from app import *
from app import db
from app.records.models import Records
from app.users.models import User

os.environ['PYTHONINSPECT'] = 'True'
