#!/usr/bin/env python
# author: d.koch
# coding: utf-8
# naming: pep-0008
# typing: pep-0484
# docstring: pep-0257
# indentation: tabulation

""" canp_view_mpl.py
	Math Plot Lib view
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

# python3 -m pip install --upgrade matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt

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

class canp_view_mpl:
	""" CAN view
	"""

	@staticmethod
	def display(
				i_list_narr,	# all the lists in one package
				i_int_tmp,		# time index
				i_int_pos,		# pos index
			) -> None:
		# Display data in matplotlib windows
		plt.style.use('seaborn')

		plt.figure()

		plt.title("Capture CAN vs. Trajectoire référence")
		plt.xlabel("Temps (s)")
		plt.ylabel("Position (mm)")
		plt.legend(loc = "upper left")

		# Display x axis
		plt.plot(
			i_list_narr[CANP_ENUM__IDX_X_CAN][:, i_int_tmp],
			i_list_narr[CANP_ENUM__IDX_X_CAN][:, i_int_pos],
			color = "r",
			label = "x_can")
		plt.plot(
			i_list_narr[CANP_ENUM__IDX_X_REF][:, i_int_tmp],
			i_list_narr[CANP_ENUM__IDX_X_REF][:, i_int_pos],
			color = "m",
			label = "x_ref")

		# Display y axis
		plt.plot(
			i_list_narr[CANP_ENUM__IDX_Y_CAN][:, i_int_tmp],
			i_list_narr[CANP_ENUM__IDX_Y_CAN][:, i_int_pos],
			color = "g",
			label = "y_can")
		plt.plot(
			i_list_narr[CANP_ENUM__IDX_Y_REF][:, i_int_tmp],
			i_list_narr[CANP_ENUM__IDX_Y_REF][:, i_int_pos],
			color = "y",
			label = "y_ref")

		# Display z axis
		plt.plot(
			i_list_narr[CANP_ENUM__IDX_Z_CAN][:, i_int_tmp],
			i_list_narr[CANP_ENUM__IDX_Z_CAN][:, i_int_pos],
			color = "b",
			label = "z_can")
		plt.plot(
			i_list_narr[CANP_ENUM__IDX_Z_REF][:, i_int_tmp],
			i_list_narr[CANP_ENUM__IDX_Z_REF][:, i_int_pos],
			color = "c",
			label = "z_ref")

		plt.show()

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
