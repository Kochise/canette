#!/usr/bin/env python
# author: d.koch
# coding: utf-8
# naming: pep-0008
# typing: pep-0484
# docstring: pep-0257
# indentation: tabulation

""" canp_path.py
	Path tools
"""

#  --- IMPORT ---

# Standard libraries (installed with python)

import enum
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

from canp_enum import CANP_ENUM__HEAD_MAIN

from canp_enum import CANP_ENUM__STR_ASLASH
from canp_enum import CANP_ENUM__STR_DOT
from canp_enum import CANP_ENUM__STR_EMPTY
from canp_enum import CANP_ENUM__STR_SLASH
from canp_enum import CANP_ENUM__STR_SPACE

from canp_args import canp_args

#  --- GLOBAL ---

CANP_PATH__IDX_DRIVE = 0
CANP_PATH__IDX_FILE = -2
CANP_PATH__IDX_EXT = -1

#  --- CLASS ---

class canp_path:
	""" CAN path converter
	"""

	@staticmethod
	def list_str(
				i_str_path: str
			) -> List[str]:
		""" List from string
		"""
		l_list_ret: List[str] = []
		l_str_file: str = CANP_ENUM__STR_EMPTY
		l_str_name: str = CANP_ENUM__STR_EMPTY
		l_str_ext: str = CANP_ENUM__STR_EMPTY

		if (i_str_path != CANP_ENUM__STR_EMPTY):
			# Beware of escaped characters
			i_str_path = i_str_path.replace(CANP_ENUM__STR_SLASH, CANP_ENUM__STR_ASLASH)
			l_list_ret = CANP_ENUM__STR_SPACE.join(i_str_path.split(CANP_ENUM__STR_ASLASH)).split()

			if (i_str_path[-1] != CANP_ENUM__STR_ASLASH):
				# Last element is filename (for sure)
				l_str_file = l_list_ret[-1]
				l_str_name = CANP_ENUM__STR_DOT.join(l_str_file.split(CANP_ENUM__STR_DOT)[:CANP_PATH__IDX_EXT])
				l_str_ext = l_str_file.split(CANP_ENUM__STR_DOT)[CANP_PATH__IDX_EXT]
				if (l_str_name == CANP_ENUM__STR_EMPTY) and (l_str_ext != CANP_ENUM__STR_EMPTY):
					# Hidden 'dot' file
					l_str_name = l_str_file
					l_str_ext = CANP_ENUM__STR_EMPTY
				l_list_ret = l_list_ret[:-1]

			l_list_ret.append(l_str_name)
			l_list_ret.append(l_str_ext)

		return l_list_ret

#  --- MAIN ---

def __main__(i_list_args: List = []):
	""" Basic self test (debugging)
	"""
	if True:
		EDS_FILE = "PAC-P3_v1.0.eds"
		l_list_path = canp_path.list_str(i_str_path = "c:/toto/titi")
	else:
		pass

if __name__ == CANP_ENUM__HEAD_MAIN:
	""" Routine selector
	"""
	canp_args.dispatch(i_list_globals = globals())
