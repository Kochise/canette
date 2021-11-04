#!/usr/bin/env python
# author: d.koch
# coding: utf-8
# naming: pep-0008
# typing: pep-0484
# docstring: pep-0257
# indentation: tabulation

""" canp_view_enaml.py
	Enaml view
"""

#  --- IMPORT ---

# Standard libraries (installed with python)

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

# python3 -m pip install --upgrade pyqtgraph
# python3 -m pip install --upgrade QScintilla
# python3 -m pip install --upgrade enamlx
#import enamlx
#enamlx.install()

# python3 -m pip install --upgrade rtree
# python3 -m pip install --upgrade intervaltree
# python3 -m pip install --upgrade enaml
import enaml
from enaml.qt.qt_application import QtApplication

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

# Included libraries (this module, local files)

from canp_enum import CANP_ENUM__HEAD_MAIN

from canp_enum import CANP_ENUM__IDX_X_CAN
from canp_enum import CANP_ENUM__IDX_X_REF
from canp_enum import CANP_ENUM__IDX_Y_CAN
from canp_enum import CANP_ENUM__IDX_Y_REF
from canp_enum import CANP_ENUM__IDX_Z_CAN
from canp_enum import CANP_ENUM__IDX_Z_REF

from canp_args import canp_args
from canp_logs import canp_logs

#  --- GLOBAL ---

# Local settings (might be present in other files yet with different values)

#  --- CLASS ---

class canp_view_enaml:
	""" CAN view
		CANNOT be used alone, but be fed some data
	"""

	@staticmethod
	def display(
				i_list_narr,	# All the lists in one package
				i_int_tmp,		# Time index in each list (usually 0)
				i_int_pos,		# Pos index in each list (usually 1)
				i_obj_can,		# Can card object (chan, node, conf, ...)
			) -> None:
		# Display data in Enaml windows
		with enaml.imports():
			from canp_view_enaml_main import Main

		app = QtApplication()

		view = Main(
			i_list_narr = i_list_narr,
			i_int_tmp = i_int_tmp,
			i_int_pos = i_int_pos,
			i_obj_can = i_obj_can,
			)
		view.show()

		app.start()

#  --- MAIN ---

def __main__(i_list_args: List = []):
	""" Basic self test (debugging)
	"""
	if True:
		with enaml.imports():
			from canp_view_enaml_main import Main

		app = QtApplication()

		view = Main()
		view.show()

		app.start()
	else:
		pass

if __name__ == CANP_ENUM__HEAD_MAIN:
	""" Routine selector
	"""
	canp_args.dispatch(i_list_globals = globals())
