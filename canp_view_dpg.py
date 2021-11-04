#!/usr/bin/env python
# author: d.koch
# coding: utf-8
# naming: pep-0008
# typing: pep-0484
# docstring: pep-0257
# indentation: tabulation

""" canp_view_mpl.py
	DearPyGui 0.6 view
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

# python3 -m pip install "dearpygui<0.7"
# /!\ Dear PyGui 0.6 *only*
from dearpygui.core import *
from dearpygui.simple import *

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

# Included libraries (this module, local files)

from canp_enum import CANP_ENUM__HEAD_MAIN

from canp_enum import CANP_ENUM__IDX_X_CAN
from canp_enum import CANP_ENUM__IDX_X_REF
from canp_enum import CANP_ENUM__IDX_Y_CAN
from canp_enum import CANP_ENUM__IDX_Y_REF
from canp_enum import CANP_ENUM__IDX_Z_CAN
from canp_enum import CANP_ENUM__IDX_Z_REF

#  --- GLOBAL ---

# Local settings (might be present in other files yet with different values)

#  --- CLASS ---

class canp_view_dpg:
	""" CAN view
	"""

	@staticmethod
	def display(
				i_list_farr,	# all the lists in one package
				i_int_tmp,		# time index
				i_int_pos,		# pos index
			) -> None:
		# Display data in DearPyGui 0.6 windows
		with window("Tutorial"):
			add_plot("Plot", height = -1)

			# Display x axis
			add_line_series(
				"Plot",
				"x_can",
				i_list_farr[CANP_ENUM__IDX_X_CAN][0],
				i_list_farr[CANP_ENUM__IDX_X_CAN][1],
				weight = 2,
				color = [255, 000, 255, 100])
			add_line_series(
				"Plot",
				"x_ref",
				i_list_farr[CANP_ENUM__IDX_X_REF][0],
				i_list_farr[CANP_ENUM__IDX_X_REF][1],
				weight = 2,
				color = [255, 000, 000, 100])

			# Display y axis
			add_line_series(
				"Plot",
				"y_can",
				i_list_farr[CANP_ENUM__IDX_Y_CAN][0],
				i_list_farr[CANP_ENUM__IDX_Y_CAN][1],
				weight = 2,
				color = [000, 255, 000, 100])
			add_line_series(
				"Plot",
				"y_ref",
				i_list_farr[CANP_ENUM__IDX_Y_REF][0],
				i_list_farr[CANP_ENUM__IDX_Y_REF][1],
				weight = 2,
				color = [255, 255, 000, 100])

			# Display z axis
			add_line_series(
				"Plot",
				"z_can",
				i_list_farr[CANP_ENUM__IDX_Z_CAN][0],
				i_list_farr[CANP_ENUM__IDX_Z_CAN][1],
				weight = 2,
				color = [000, 000, 255, 100])
			add_line_series(
				"Plot",
				"z_ref",
				i_list_farr[CANP_ENUM__IDX_Z_REF][0],
				i_list_farr[CANP_ENUM__IDX_Z_REF][1],
				weight = 2,
				color = [000, 255, 255, 100])

		start_dearpygui()

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
