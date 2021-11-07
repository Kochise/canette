#!/usr/bin/env python
# author: d.koch
# coding: utf-8
# naming: pep-0008
# typing: pep-0484
# docstring: pep-0257
# indentation: tabulation

""" canp_test.py
	Simple CAN interface tester
"""

#  --- IMPORT ---

# Standard libraries (installed with python)

import asyncio
#import atexit
#import json
#import logging
import os
#import random
#import re
import sys
#import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

#from math import cos, sin

#from typing import Any
#from typing import Callable
#from typing import Dict
from typing import List
#from typing import Optional
#from typing import Union

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

# External libraries (installed with pip, conda, setup.py, ...)

# python3 -m pip install --upgrade similaritymeasures
import similaritymeasures

# python3 -m pip install --upgrade numpy
import numpy as np

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

# Included libraries (this module, local files)

# canp_conv : data type conversion
# canp_enum : enum values
# canp_path : path parser
# canp_logs : logs logger
# canp_args : args dispatcher

# canp_card : card level (selection of the adapter and its speed)
#	canp_chan : channel splitter (redirect frame on the right node)
#		canp_node : node manager (most of the work is done there)
#			canp_conf : configuration objects (from EDS/DCF file)

from canp_card import canp_card

from canp_card import CANP_CARD__BAUD_500K
from canp_card import CANP_CARD__RE_FRAME


from canp_enum import CANP_ENUM__APP_NAME

from canp_enum import CANP_ENUM__HEAD_LIST
from canp_enum import CANP_ENUM__HEAD_MAIN
from canp_enum import CANP_ENUM__HEAD_NAME

from canp_enum import CANP_ENUM__STR_SPACE


from canp_args import canp_args
from canp_logs import canp_logs


from canp_view_mpl import canp_view_mpl
from canp_view_dpg import canp_view_dpg
from canp_view_enaml import canp_view_enaml
from canp_view_flexx import canp_view_flexx

#  --- GLOBAL ---

# Local settings (might be present in other files yet with different values)

ASYNC_RUN = asyncio.run
ASYNC_LOOP = asyncio.get_event_loop()
ASLEEP = asyncio.sleep

# Card (see can.interfaces.BACKENDS)
CANP_TEST__CARD = "neovi"

# Channel
CANP_TEST__CHAN = 2

# Nodes
CANP_TEST__NODE_AXIS_X = 1
CANP_TEST__NODE_AXIS_Y = 2
CANP_TEST__NODE_AXIS_Z = 3
CANP_TEST__NODE_GRIP = 4

# Configuration files
# /!\ Use v1.0, not v1.2 despite looking more recent
CANP_TEST__FILE_EDS = "PAC-P3_v1.0.eds"
CANP_TEST__FILE_DCF = "carteGripper_config_01.dcf"

# Log file (beware of format, must be supported to be parser correctly)
CANP_TEST__FILE_LOG = "python_can.logger_c_2_all_axis_rot.log"
#CANP_TEST__FILE_LOG = "cycle U 8u20 9-16-2021 11-58-56 am.asc"

# Array indexes
CANP_TEST__ARR_TMP = 0
CANP_TEST__ARR_POS = 1

# Can object index for Position (depends on configuration file because PDO)
CANP_TEST__POS_OBJ = 0x6064
CANP_TEST__POS_SUB = 0

# Setting global wide logger (used in sub classes as well, hopefully)
g_logs = canp_logs.logger(CANP_ENUM__APP_NAME)

#  --- CLASS ---


#  --- MAIN ---

def __main__(i_list_args: List = []):
	""" Basic self test (debugging)
	"""
	global g_logs

	if False:
		# Display log file (line by line)
		g_logs.debug("--- CAN LOG DISPLAY ---")
		with open(str(CANP_TEST__FILE_LOG)) as obj_file_:
			for num_line_, str_line_ in enumerate(obj_file_, 1):
				str_line_.strip()
				# '(142.844095) 2 381#6C4E0000FEFFFFFF'
				g_logs.debug(f"{num_line_}:'{str_line_}'")
				l_list_line = CANP_CARD__RE_FRAME.split(str_line_)
				l_list_line = CANP_ENUM__STR_SPACE.join(l_list_line).split()
				g_logs.debug(f"{num_line_}:{l_list_line}\n")
				# ['142.844095', '2', '381', '6C4E0000FEFFFFFF']

	else:
		# Creating "card" object (to connect to CAN or parse LOG files)
		l_obj_can = canp_card()

		# Configure channel and its nodes (using EDS/DCF description file)
		l_obj_can.node_conf(
			i_int_chan = CANP_TEST__CHAN,
			i_int_node = CANP_TEST__NODE_AXIS_X,
			i_str_file = CANP_TEST__FILE_EDS)
		l_obj_can.node_conf(
			i_int_chan = CANP_TEST__CHAN,
			i_int_node = CANP_TEST__NODE_AXIS_Y,
			i_str_file = CANP_TEST__FILE_EDS)
		l_obj_can.node_conf(
			i_int_chan = CANP_TEST__CHAN,
			i_int_node = CANP_TEST__NODE_AXIS_Z,
			i_str_file = CANP_TEST__FILE_EDS)

		l_obj_can.node_conf(
			i_int_chan = CANP_TEST__CHAN,
			i_int_node = CANP_TEST__NODE_GRIP,
			i_str_file = CANP_TEST__FILE_DCF)

		# Select the data source (LOG file or real time CAN data)
		if True:
			g_logs.debug("--- CAN LOG PARSE ---")
			l_obj_can.log_parse(
				i_str_file = CANP_TEST__FILE_LOG)
		else:
			g_logs.debug("--- CAN BUS PARSE ---")
			l_obj_can.can_parse(
				i_str_card = CANP_TEST__CARD,
				i_str_chan = str(CANP_TEST__CHAN),
				i_int_baud = CANP_CARD__BAUD_500K,
				i_int_count = 100000)

		# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

		# The hierarchy is as follow :
		#	CARD object
		#		CHAN object
		#			NODE object
		#				OBJS dict (all sub registers)
		#					SUBS dict
		#						DATA  (last data stored)
		#						LIST  (all data stored in (time, data) format)

		g_logs.debug("Testing...")
		#l_obj_can.m_dict_chans[2].m_dict_nodes[2].m_dict_objs[0x6064][0]
		#l_obj_can[2][2][0x6064][0]

		# Doing some math (rotor increment into mm)
		l_float_pos_ratio = 1.0
		l_float_pos_ratio = (4096 * 10) / 204

		# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

		# Extracting X axis data (with numpy conversion)
		l_list_x_can = l_obj_can[CANP_TEST__CHAN][CANP_TEST__NODE_AXIS_X][CANP_TEST__POS_OBJ][CANP_TEST__POS_SUB][CANP_ENUM__HEAD_LIST]
		l_narr_x_can = np.zeros((len(l_list_x_can), 2))
		l_narr_x_can[:, CANP_TEST__ARR_TMP] = [f[CANP_TEST__ARR_TMP] for f in l_list_x_can]
		l_narr_x_can[:, CANP_TEST__ARR_POS] = [f[CANP_TEST__ARR_POS] / l_float_pos_ratio for f in l_list_x_can]

		# Starting timestamp (exact or manual value)
		l_float_tmp_start = l_list_x_can[0][CANP_TEST__ARR_TMP]
		l_float_tmp_start = 143.0	# Time base for "reference" curve

		# Offsetting time and position (plus zipping them)
		l_list_x_ref_tmp = [ts + l_float_tmp_start for ts in [0.0, 6.93, 10.15, 10.8, 14.02, 53.0]]
		l_list_x_ref_pos = [ps / l_float_pos_ratio for ps in [20075, 20075, 107450, 107450, 20075, 20075]]
		l_zipr_x_ref = zip(l_list_x_ref_tmp, l_list_x_ref_pos)

		# Converting time and position to numpy format
		l_narr_x_ref = np.zeros((6, 2))
		l_narr_x_ref[:, CANP_TEST__ARR_TMP] = l_list_x_ref_tmp
		l_narr_x_ref[:, CANP_TEST__ARR_POS] = l_list_x_ref_pos

		# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

		# Extracting Y axis data (with numpy conversion)
		l_list_y_can = l_obj_can[CANP_TEST__CHAN][CANP_TEST__NODE_AXIS_Y][CANP_TEST__POS_OBJ][0][CANP_ENUM__HEAD_LIST]
		l_narr_y_can = np.zeros((len(l_list_y_can), 2))
		l_narr_y_can[:, CANP_TEST__ARR_TMP] = [f[CANP_TEST__ARR_TMP] for f in l_list_y_can]
		l_narr_y_can[:, CANP_TEST__ARR_POS] = [f[CANP_TEST__ARR_POS] / l_float_pos_ratio for f in l_list_y_can]

		# Offsetting time and position (plus zipping them)
		l_list_y_ref_tmp = [ts + l_float_tmp_start for ts in [0.0, 16.15, 19.86, 20.81, 24.51, 53.0]]
		l_list_y_ref_pos = [ps / l_float_pos_ratio for ps in [29050, 29050, 174300, 174300, 29050, 29050]]
		l_zipr_y_ref = zip(l_list_y_ref_tmp, l_list_y_ref_pos)

		# Converting time and position to numpy format
		l_narr_y_ref = np.zeros((6, 2))
		l_narr_y_ref[:, CANP_TEST__ARR_TMP] = l_list_y_ref_tmp
		l_narr_y_ref[:, CANP_TEST__ARR_POS] = l_list_y_ref_pos

		# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

		# Extracting Z axis data (with numpy conversion)
		l_list_z_can = l_obj_can[CANP_TEST__CHAN][CANP_TEST__NODE_AXIS_Z][CANP_TEST__POS_OBJ][0][CANP_ENUM__HEAD_LIST]
		l_narr_z_can = np.zeros((len(l_list_z_can), 2))
		l_narr_z_can[:, CANP_TEST__ARR_TMP] = [f[CANP_TEST__ARR_TMP] for f in l_list_z_can]
		l_narr_z_can[:, CANP_TEST__ARR_POS] = [f[CANP_TEST__ARR_POS] / l_float_pos_ratio for f in l_list_z_can]

		# Offsetting time and position (plus zipping them)
		l_list_z_ref_tmp = [ts + l_float_tmp_start for ts in [0.0, 26.38, 30.23, 30.71, 34.57, 53.0]]
		l_list_z_ref_pos = [ps / l_float_pos_ratio for ps in [15180, 15180, 94100, 94100, 15170, 15170]]
		l_zipr_z_ref = zip(l_list_z_ref_tmp, l_list_z_ref_pos)

		# Converting time and position to numpy format
		l_narr_z_ref = np.zeros((6, 2))
		l_narr_z_ref[:, CANP_TEST__ARR_TMP] = l_list_z_ref_tmp
		l_narr_z_ref[:, CANP_TEST__ARR_POS] = l_list_z_ref_pos

		# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

		# Partial Curve Mapping	: matches the area of a subset between the two curves
		# Discrete Frechet		: shortest distance in-between two curves, where you are allowed to very the speed at which you travel along each curve independently (walking dog problem)
		# Area					: algorithm for calculating the Area between two curves in 2D space
		# Curve Length			: assumes that the only true independent variable of the curves is the arc-length distance along the curve from the origin
		# Dynamic Time Warping	: non-metric distance between two time-series curves that has been proven useful for a variety of applications

		# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

		# Calculating stats for X axis
		l_float_x_pcm = similaritymeasures.pcm(l_narr_x_can, l_narr_x_ref)
		l_float_x_df = similaritymeasures.frechet_dist(l_narr_x_can, l_narr_x_ref)
		l_float_x_area = 0.0
		#l_float_x_area = similaritymeasures.area_between_two_curves(l_narr_x_can, l_narr_x_ref)
		l_float_x_cl = similaritymeasures.curve_length_measure(l_narr_x_can, l_narr_x_ref)
		l_float_x_dtw, l_float_x_d = similaritymeasures.dtw(l_narr_x_can, l_narr_x_ref)
		g_logs.debug(f"X :"
			f" pcm={l_float_x_pcm:.3f}/0,"
			f" df={l_float_x_df:.3f},"
			f" area={l_float_x_area:.3f}/m2,"
			f" cl={l_float_x_cl:.3f}/0,"
			f" dtw={l_float_x_dtw:.3f}")

		# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

		# Calculating stats for Y axis
		l_float_y_pcm = similaritymeasures.pcm(l_narr_y_can, l_narr_y_ref)
		l_float_y_df = similaritymeasures.frechet_dist(l_narr_y_can, l_narr_y_ref)
		l_float_y_area = 0.0
		#l_float_y_area = similaritymeasures.area_between_two_curves(l_narr_y_can, l_narr_y_ref)
		l_float_y_cl = similaritymeasures.curve_length_measure(l_narr_y_can, l_narr_y_ref)
		l_float_y_dtw, l_float_y_d = similaritymeasures.dtw(l_narr_y_can, l_narr_y_ref)
		g_logs.debug(f"Y :"
			f" pcm={l_float_y_pcm:.3f}/0,"
			f" df={l_float_y_df:.3f},"
			f" area={l_float_y_area:.3f}/m2,"
			f" cl={l_float_y_cl:.3f}/0,"
			f" dtw={l_float_y_dtw:.3f}")

		# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

		# Calculating stats for Z axis
		l_float_z_pcm = similaritymeasures.pcm(l_narr_z_can, l_narr_z_ref)
		l_float_z_df = similaritymeasures.frechet_dist(l_narr_z_can, l_narr_z_ref)
		l_float_z_area = 0.0
		#l_float_z_area = similaritymeasures.area_between_two_curves(l_narr_z_can, l_narr_z_ref)
		l_float_z_cl = similaritymeasures.curve_length_measure(l_narr_z_can, l_narr_z_ref)
		l_float_z_dtw, l_float_z_d = similaritymeasures.dtw(l_narr_z_can, l_narr_z_ref)
		g_logs.debug(f"Z :"
			f" pcm={l_float_z_pcm:.3f}/0,"
			f" df={l_float_z_df:.3f},"
			f" area={l_float_z_area:.3f}/m2,"
			f" cl={l_float_z_cl:.3f}/0,"
			f" dtw={l_float_z_dtw:.3f}")

		# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

		if False:
			# Display data in matplotlib window
			canp_view_mpl.display([
				l_narr_x_can, l_narr_x_ref,
				l_narr_y_can, l_narr_y_ref,
				l_narr_z_can, l_narr_z_ref],
				CANP_TEST__ARR_TMP,
				CANP_TEST__ARR_POS,)
			print("canp_view_mpl done")

		if False:
			# Display data in DearPyGui (0.6.x) window
			canp_view_dpg.display([
				# Separate series (time / pos) and adapt them for DPG
				[[f[CANP_TEST__ARR_TMP] for f in l_list_x_can],
				[f[CANP_TEST__ARR_POS] / l_float_pos_ratio for f in l_list_x_can]],
				[l_list_x_ref_tmp,
				l_list_x_ref_pos],
				[[f[CANP_TEST__ARR_TMP] for f in l_list_y_can],
				[f[CANP_TEST__ARR_POS] / l_float_pos_ratio for f in l_list_y_can]],
				[l_list_y_ref_tmp,
				l_list_y_ref_pos],
				[[f[CANP_TEST__ARR_TMP] for f in l_list_z_can],
				[f[CANP_TEST__ARR_POS] / l_float_pos_ratio for f in l_list_z_can]],
				[l_list_z_ref_tmp,
				l_list_z_ref_pos]],
				CANP_TEST__ARR_TMP,
				CANP_TEST__ARR_POS,)
			print("canp_view_dpg done")

		if False:
			# Display data in Flexx (browser) window
			# Create a browser window (problem with Firefox)
			canp_view_flexx.display([
				l_narr_x_can, l_narr_x_ref,
				l_narr_y_can, l_narr_y_ref,
				l_narr_z_can, l_narr_z_ref],
				CANP_TEST__ARR_TMP,
				CANP_TEST__ARR_POS,)
			print("canp_view_flexx done")

		if True:
			# Display data in Enaml (0.12+.0) window
			canp_view_enaml.display([
				l_narr_x_can, l_narr_x_ref,
				l_narr_y_can, l_narr_y_ref,
				l_narr_z_can, l_narr_z_ref],
				CANP_TEST__ARR_TMP,
				CANP_TEST__ARR_POS,
				l_obj_can,)
			print("canp_view_enaml done")

if __name__ == CANP_ENUM__HEAD_MAIN:
	""" Routine selector
	"""
	canp_args.dispatch(i_list_globals = globals())
