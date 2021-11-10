#!/usr/bin/env python
# author: d.koch
# coding: utf-8
# naming: pep-0008
# typing: pep-0484
# docstring: pep-0257
# indentation: tabulation

""" canp_card.py
	Card
	CARD-chan-node-conf
"""

#  --- IMPORT ---

# Standard libraries (installed with python)

import logging
import os
import re
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

import can

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

# Included libraries (this module, local files)

from canp_chan import canp_chan


from canp_enum import CANP_ENUM__APP_NAME
from canp_enum import CANP_ENUM__BASE_HEXA
from canp_enum import CANP_ENUM__EOL_LF

from canp_enum import CANP_ENUM__HEAD_MAIN
from canp_enum import CANP_ENUM__HEAD_NAME

from canp_enum import CANP_ENUM__STR_ASLASH
from canp_enum import CANP_ENUM__STR_DOT
from canp_enum import CANP_ENUM__STR_EMPTY
from canp_enum import CANP_ENUM__STR_HASHTAG
from canp_enum import CANP_ENUM__STR_PARENTC
from canp_enum import CANP_ENUM__STR_PARENTO
from canp_enum import CANP_ENUM__STR_PIPE
from canp_enum import CANP_ENUM__STR_SPACE
from canp_enum import CANP_ENUM__STR_ZERO


from canp_args import canp_args
from canp_logs import canp_logs


from canp_path import canp_path
from canp_path import CANP_PATH__IDX_EXT

#  --- GLOBAL ---

CANP_CARD__BAUD_1K = 1000
CANP_CARD__BAUD_1M = 1000 * CANP_CARD__BAUD_1K
CANP_CARD__BAUD_800K = 800 * CANP_CARD__BAUD_1K
CANP_CARD__BAUD_500K = 500 * CANP_CARD__BAUD_1K
CANP_CARD__BAUD_250K = 250 * CANP_CARD__BAUD_1K
CANP_CARD__BAUD_125K = 125 * CANP_CARD__BAUD_1K
CANP_CARD__BAUD_50K = 50 * CANP_CARD__BAUD_1K
CANP_CARD__BAUD_20K = 20 * CANP_CARD__BAUD_1K
CANP_CARD__BAUD_10K = 10 * CANP_CARD__BAUD_1K

dict_CANP_CARD__BAUD = {
		"1m": int(CANP_CARD__BAUD_1M),
		#"800k": int(CANP_CARD__BAUD_800K),
		"500k": int(CANP_CARD__BAUD_500K),
		"250k": int(CANP_CARD__BAUD_250K),
		"125k": int(CANP_CARD__BAUD_125K),
		#"50k": int(CANP_CARD__BAUD_50K),
		#"20k": int(CANP_CARD__BAUD_20K),
		#"10k": int(CANP_CARD__BAUD_10K),
	}

CANP_CARD__STR_RE_FRAME = "\(|\)| |\#|\n"
#	CANP_ENUM__STR_PARENTO + CANP_ENUM__STR_PIPE +
#	CANP_ENUM__STR_PARENTC + CANP_ENUM__STR_PIPE +
#	CANP_ENUM__STR_SPACE + CANP_ENUM__STR_PIPE +
#	CANP_ENUM__STR_HASHTAG + CANP_ENUM__STR_PIPE +
#	CANP_ENUM__EOL_LF
CANP_CARD__RE_FRAME = re.compile(CANP_CARD__STR_RE_FRAME)

# Local settings (might be present in other files yet with different values)

CANP_LOG__IDX_TIME = 0
CANP_LOG__IDX_CHAN = 1
CANP_LOG__IDX_COBID = 2
CANP_LOG__IDX_DATA = 3

#  --- CLASS ---

class canp_card:
	""" CAN bus
	"""

	# Channel objects (key = chan number, not necessarily starting at 0)
	m_dict_chans: Dict[int, Any] = {}

	# Logger object
	m_logs = canp_logs.logger(CANP_ENUM__APP_NAME).getChild("card")

	def __init__(self,
				**i_dict_args: Any
			) -> None:
		""" Constructor
		"""
		super().__init__(**i_dict_args)

	def __getitem__(self,
				i_int_index
			) -> Any:
		""" Get at (key = chan index, if present)
		"""
		l_any_ret: Any = None

		try:
			l_any_ret = self.m_dict_chans[i_int_index]
			# - except KeyError -
		except KeyError:
			pass

		return l_any_ret


	def __len__(self):
		""" Size of (number of chans)
			Beware, no actual chan ids
		"""
		return len(self.m_dict_chans)

	def chan_list(self,
			) -> None:
		""" Chan ids list
		"""
		return self.m_dict_chans.keys()

	def chan_set(self,
				i_int_chan: int = 0,
				i_bool_force: bool = False
			) -> None:
		""" Channel set
		"""
		if i_int_chan >= 0:
			try:
				if i_bool_force == True:
					# Overwrite channel
					self.m_dict_chans[i_int_chan] = canp_chan()
				else:
					# Check channel
					self.m_dict_chans[i_int_chan]
					# - except KeyError -
			except KeyError:
				self.m_dict_chans[i_int_chan] = canp_chan()

	def node_conf(self,
				i_int_chan: int = 0,
				i_int_node: int = 0,
				i_str_file: str = CANP_ENUM__STR_EMPTY
			) -> None:
		""" Conf set (through chan)
		"""
		if i_int_chan >= 0:
			self.chan_set(i_int_chan)

			try:
				self.m_dict_chans[i_int_chan].node_conf(
					i_int_node,
					i_str_file)
				# - except KeyError -
			except KeyError:
				self.m_logs.error(f"card.node_conf.chan[{i_int_chan}].unknown")

	def frame_parse(self,
				i_list_frame: List[Any] = [],
				i_float_time: float = 0.0,
				i_int_chan: int = 0,
				i_int_cobid: int = 0,
				i_any_data: bytearray = b'',
			) -> None:
		""" Frame parser (through chan)
			Dual mode operation : via list (if provided) or via args
			Chan and Node should already be configured first
		"""
		# List format expected :
		# [142.844095, 2, 897, b'\x6c\x4e\x00\x00\xfe\xff\xff\xff']
		# 0 : timestamp (float)
		# 1 : channel (int)
		# 2 : cobid (int)
		# 3 : frame (bytearray, dlc = len)
		l_bool_frame: bool = False

		if len(i_list_frame) >= (CANP_LOG__IDX_DATA + 1):
			# Via list
			l_bool_frame = True
			i_int_chan = i_list_frame[CANP_LOG__IDX_CHAN]

		try:
			self.m_dict_chans[i_int_chan]
			# - except KeyError -
		except KeyError:
			# Create channel (beware of chan id)
			self.chan_set(i_int_chan)

		try:
			if l_bool_frame == True:
				# Via list
				self.m_dict_chans[i_int_chan].frame_parse(
					[i_list_frame[CANP_LOG__IDX_TIME],
					i_list_frame[CANP_LOG__IDX_COBID],
					i_list_frame[CANP_LOG__IDX_DATA]])
				# [142.844095, 897, b'\x6c\x4e\x00\x00\xfe\xff\xff\xff']
			else:
				# Via args
				self.m_dict_chans[i_int_chan].frame_parse(
					i_float_time = i_float_time,
					i_int_cobid = i_int_cobid,
					i_any_data = i_any_data)
			# - except KeyError -
		except KeyError:
			self.m_logs.error(f"card.frame_parse.chan[{i_int_chan}].unknown")

	def log_parse(self,
				i_str_file: str = CANP_ENUM__STR_EMPTY
			) -> None:
		""" Log reader
			Read file line by line (might be made async)
			Chan and Node should already be configured first
		"""
		if isinstance(i_str_file, str) and i_str_file != CANP_ENUM__STR_EMPTY:
			l_str_ext = canp_path.list_str(i_str_path = i_str_file)[CANP_PATH__IDX_EXT]
			with open(i_str_file, newline = None) as l_obj_file:
				for l_num_line, l_str_line in enumerate(l_obj_file, 1):
					if l_str_ext == "asc" and l_num_line <= 3:
						# Skip 3 lines header (time, format and reference)
						pass
					else:
						l_str_line.strip()
						# '(142.844095) 2 381#6C4E0000FEFFFFFF'

						l_list_line = CANP_CARD__RE_FRAME.split(l_str_line)
						l_list_line = CANP_ENUM__STR_SPACE.join(l_list_line).split()
						#        0             1    2      3
						# log : ['142.844095', '2', '381', '6C4E0000FEFFFFFF']
						# asc : ['0.000288', '2', '381', 'Rx', 'd', '8', '00', '44', '07', '00', 'E7', 'FF', 'FF', 'FF']
						#        0           1    2      3     4    5    6     7     8     9     10    11    12    13

						if l_str_ext == "asc":
							del l_list_line[3:6]	# Remove ['Rx', 'd', '8']
							# ['0.000288', '2', '381', '00', '44', '07', '00', 'E7', 'FF', 'FF', 'FF']
							l_list_line = l_list_line[0:3] + [CANP_ENUM__STR_EMPTY.join(l_list_line[3:])]
							# ['0.000288', '2', '381', '00440700E7FFFFFF']

						try:
							# Check if empty data (, '']) has been removed from the list
							l_list_line[CANP_LOG__IDX_DATA]
							# - except IndexError -
						except IndexError:
							# Complete the list
							l_list_line.append(CANP_ENUM__STR_EMPTY)

						# Extract fields (with proper casting)
						l_float_time = float(CANP_ENUM__STR_ZERO + l_list_line[CANP_LOG__IDX_TIME])
						l_int_chan = int(CANP_ENUM__STR_ZERO + l_list_line[CANP_LOG__IDX_CHAN])
						l_int_cobid = int(CANP_ENUM__STR_ZERO + l_list_line[CANP_LOG__IDX_COBID], CANP_ENUM__BASE_HEXA)
						l_any_data = bytearray.fromhex(l_list_line[CANP_LOG__IDX_DATA])

						if False:
							# Reformat list with numbers and bytes instead of strings
							l_list_line = [
								l_float_time,
								l_int_chan,
								l_int_cobid,
								l_any_data]
							# [142.844095, 2, 897, b'\x6c\x4e\x00\x00\xfe\xff\xff\xff']

							# Via list (convenient but slightly slower)
							self.frame_parse(
								i_list_frame = l_list_line)
						else:
							# Via args
							self.frame_parse(
								i_float_time = l_float_time,
								i_int_chan = l_int_chan,
								i_int_cobid = l_int_cobid,
								i_any_data = l_any_data)
		else:
			self.m_logs.error(f"card.log_parse.file[{i_str_file}].unknown")

	def can_parse(self,
				i_str_card: str = CANP_ENUM__STR_EMPTY,
				i_str_chan: str = CANP_ENUM__STR_EMPTY,
				i_int_baud: int = CANP_CARD__BAUD_1M,
				i_int_count: int = 0
			) -> None:
		""" Can reader
			Read data from a 'python-can' adapter (might be made async)
			Chan and Node should already be configured
		"""
		l_int_count: int = 0

		try:
			with can.interface.Bus(
						bustype = i_str_card,
						channel = i_str_chan,
						bitrate = i_int_baud
					) as l_obj_bus:
				try:
					while i_int_count == 0 or l_int_count < i_int_count:
						# Read one frame at a time (beware of buffer occupation)
						l_obj_msg = l_obj_bus.recv(1)
						if l_obj_msg is not None:
							# Parse the can frame
							if False:
								# Compose the list (only needed attributes)
								l_list_line = [
									l_obj_msg.timestamp,
									l_obj_msg.channel,
									l_obj_msg.arbitration_id,
									l_obj_msg.data]
								# [142.844095, 2, 897, b'\x6c\x4e\x00\x00\xfe\xff\xff\xff']

								# Via list (convenient but slightly slower)
								self.frame_parse(
									i_list_frame = l_list_line)
							else:
								# Via args
								self.frame_parse(
									i_float_time = l_obj_msg.timestamp,
									i_int_chan = l_obj_msg.channel,
									i_int_cobid = l_obj_msg.arbitration_id,
									i_any_data = l_obj_msg.data)

							# Limiter
							l_int_count += 1
					else:
						self.m_logs.info(f"card.can_parse.limit_reached ({i_int_count})")
				except:
					self.m_logs.error("card.can_parse.error.unknown")
		except:
			self.m_logs.error("card.can_parse.error.connection")

#  --- MAIN ---

def __main__(i_list_args: List = []):
	""" Basic self test (debugging)
	"""
	if False:
		pass
	else:
		pass

if __name__ == CANP_ENUM__HEAD_MAIN:
	""" Routine selector
	"""
	canp_args.dispatch(i_list_globals = globals())
