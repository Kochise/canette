#!/usr/bin/env python
# author: d.koch
# coding: utf-8
# naming: pep-0008
# typing: pep-0484
# docstring: pep-0257
# indentation: tabulation

""" canp_logs.py
	Loggers
	/!\ f-string are always evaluated first regardless of setLevel (performance)
	.pylintrc:[logging] disable=logging-fstring-interpolation
"""

#  --- IMPORT ---

# Standard libraries (installed with python)

import enum
import inspect
import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

# External libraries (installed with pip, conda, setup.py, ...)

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

# Included libraries (this module, local files)

from canp_enum import CANP_ENUM__APP_NAME
from canp_enum import CANP_ENUM__EOL_LF
from canp_enum import CANP_ENUM__HEAD_MAIN

from canp_enum import CANP_ENUM__STR_CURLYO
from canp_enum import CANP_ENUM__STR_PERCENT

from canp_enum import CANP_ENUM__VAL_LOGGING

from canp_args import canp_args

#  --- GLOBAL ---

# https://docs.python.org/3/library/logging.html#logrecord-attributes
CANP_LOGS__STR_FORMAT = "%(process)s %(thread)s: %(message)s"
CANP_LOGS__STR_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
CANP_LOGS__STR_FORMAT = "[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s"
CANP_LOGS__STR_FORMAT = "[%(filename)s:%(lineno)s - %(funcName)15s] %(message)s"
CANP_LOGS__STR_FORMAT = "[%(filename)s:%(lineno)4s - %(funcName)12s:%(levelname)8s] %(message)s"
CANP_LOGS__STR_FORMAT = "%(message)s"

CANP_LOGS__STR_FORMAT = "{process} {thread}: {message}"
CANP_LOGS__STR_FORMAT = "{asctime} - {name} - {levelname} - {message}"
CANP_LOGS__STR_FORMAT = "[{asctime}] p{process} {pathname}:{lineno} {levelname} - {message}"
CANP_LOGS__STR_FORMAT = "[{filename}:{lineno} - {funcName:15}] {message}"
CANP_LOGS__STR_FORMAT = "[{filename}:{lineno:4} - {funcName:12}:{levelname:8}] {message}"
CANP_LOGS__STR_FORMAT = "{message}"

# Avoid doc-string detection
CANP_LOGS__STR_DQUOTE = ('"' * 3)

#  --- CLASS ---

class Filter(logging.Filter):
	def __init__(self, i_list_level):
		self.l_list_level = i_list_level

	def filter(self, i_record):
		return i_record.levelno in self.l_list_level

class FileHandler(logging.FileHandler):
	def l_open(self):
		return open(self.baseFilename,
				mode = self.mode,
				encoding = self.encoding,
				newline = CANP_ENUM__EOL_LF)

class canp_logs:
	""" CAN logger
	"""

	"""
	def __deferred_flog(i_cls_logger, i_enum_level, i_str_f, *i_list_args):
		if i_cls_logger.isEnabledFor(i_enum_level):
			l_frame = inspect.currentframe().f_back.f_back
			try:
				i_str_f = 'f' + CANP_LOGS__STR_DQUOTE + i_str_f + CANP_LOGS__STR_DQUOTE
				i_cls_logger.log(i_enum_level, eval(i_str_f, l_frame.f_globals, l_frame.f_locals))
			finally:
				del l_frame

	def __init__(self,
				**i_dict_args: Any
			) -> None:
		super().__init__(**i_dict_args)

		self.fdebug = lambda i_str_f, *i_list_args: __deferred_flog(self, logging.DEBUG, i_str_f, *i_list_args)
		self.finfo = lambda i_str_f, *i_list_args: __deferred_flog(self, logging.INFO, i_str_f, *i_list_args)
		self.fwarning = lambda i_str_f, *i_list_args: __deferred_flog(self, logging.WARNING, i_str_f, *i_list_args)
		self.ferror = lambda i_str_f, *i_list_args: __deferred_flog(self, logging.ERROR, i_str_f, *i_list_args)
		self.fcritical = lambda i_str_f, *i_list_args: __deferred_flog(self, logging.CRITICAL, i_str_f, *i_list_args)
	"""

	@staticmethod
	def logger(
				i_str_name: str = CANP_ENUM__APP_NAME,
				i_str_path: str = "./",
			) -> logging:
		""" Customized logger
		"""
		l_logger = logging.getLogger(i_str_name)
		l_logger.handlers.clear()

		# NOTSET=0 DEBUG=10 INFO=20 WARNING=30 ERROR=40 CRITICAL=50
		l_logger.setLevel(CANP_ENUM__VAL_LOGGING)
		#l_logger.setLevel(logging.DEBUG)

		#logging.basicConfig(level = logging.DEBUG, filename = 'example.log', encoding = 'utf-8')
		#logging.basicConfig(level = CANP_ENUM__VAL_LOGGING, format = '%(message)s')

		l_style = CANP_ENUM__STR_CURLYO if CANP_LOGS__STR_FORMAT.find(CANP_ENUM__STR_CURLYO) >=0 else CANP_ENUM__STR_PERCENT
		l_formatter = logging.Formatter(fmt = CANP_LOGS__STR_FORMAT, style = l_style, datefmt = '%m-%d %H:%M:%S')
		l_formatter = logging.Formatter(fmt = CANP_LOGS__STR_FORMAT, style = l_style)

		l_handler_out = logging.StreamHandler(sys.stdout)
		#l_handler_out.setLevel(CANP_ENUM__VAL_LOGGING)
		l_handler_out.setFormatter(l_formatter)
		#l_handler_out.addFilter(Filter([logging.ERROR, logging.CRITICAL]))
		l_logger.addHandler(l_handler_out)

		l_handler_err = logging.StreamHandler(sys.stderr)
		#l_handler_err.setLevel(CANP_ENUM__VAL_LOGGING)
		l_handler_err.setFormatter(l_formatter)
		#l_handler_err.addFilter(Filter([logging.ERROR, logging.CRITICAL]))
		l_logger.addHandler(l_handler_err)

		if i_str_path != "":
			l_handler_log = FileHandler(os.path.join(i_str_path, i_str_name + '.log'), mode = 'w')
			#l_handler_log.setLevel(CANP_ENUM__VAL_LOGGING)
			l_handler_log.setFormatter(l_formatter)
			#l_handler_log.terminator = CANP_ENUM__EOL_LF
			#l_handler_log.addFilter(Filter([logging.ERROR, logging.CRITICAL]))
			l_logger.addHandler(l_handler_log)

		return l_logger

#  --- MAIN ---

def __main__(i_list_args: List = []):
	""" Basic self test (debugging)
	"""
	if True:
		pass
	else:
		pass

if __name__ == CANP_ENUM__HEAD_MAIN:
	""" Routine selector
	"""
	canp_args.dispatch(i_list_globals = globals())
