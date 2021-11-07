#!/usr/bin/env python
# author: d.koch
# coding: utf-8
# naming: pep-0008
# typing: pep-0484
# docstring: pep-0257
# indentation: tabulation

""" canp_node.py
	Node
	card-chan-NODE-conf
"""

#  --- IMPORT ---

# Standard libraries (installed with python)

#import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import date, timedelta

from typing import Any
#from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
#from typing import Union

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

# External libraries (installed with pip, conda, setup.py, ...)

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

# Included libraries (this module, local files)

from canp_conf import canp_conf

from canp_conf import CANP_CONF__CPA_RPDO_MP
from canp_conf import CANP_CONF__CPA_TPDO_MP

from canp_conf import CANP_CONF__PDO_RX
from canp_conf import CANP_CONF__PDO_TX

from canp_conf import CANP_CONF__SDO_RX
from canp_conf import CANP_CONF__SDO_TX

from canp_conf import enum_CANP_CONF__TYPE


from canp_conv import canp_conv


from canp_enum import CANP_ENUM__APP_NAME
from canp_enum import CANP_ENUM__BYTE_LITTLE

from canp_enum import CANP_ENUM__HEAD_DATA
from canp_enum import CANP_ENUM__HEAD_LIST
from canp_enum import CANP_ENUM__HEAD_MAIN
#from canp_enum import CANP_ENUM__HEAD_NAME

from canp_enum import CANP_ENUM__NODE_MAX

#from canp_enum import CANP_ENUM__STR_ASLASH
#from canp_enum import CANP_ENUM__STR_DOT
from canp_enum import CANP_ENUM__STR_EMPTY
#from canp_enum import CANP_ENUM__STR_SPACE

from canp_enum import CANP_ENUM__VAL_DEFAULT

from canp_enum import enum_TYPE


from canp_args import canp_args
from canp_logs import canp_logs

#  --- GLOBAL ---

# CiA 301
CANP_NODE__COB_NMT = 0x000
CANP_NODE__COB_RES1 = 0x000
CANP_NODE__COB_SYNC = 0x080
CANP_NODE__COB_EMCY = 0x080
CANP_NODE__COB_TIME = 0x100
CANP_NODE__COB_TPDO1 = 0x180
CANP_NODE__COB_RPDO1 = 0x200
CANP_NODE__COB_TPDO2 = 0x280
CANP_NODE__COB_RPDO2 = 0x300
CANP_NODE__COB_TPDO3 = 0x380
CANP_NODE__COB_RPDO3 = 0x400
CANP_NODE__COB_TPDO4 = 0x480
CANP_NODE__COB_RPDO4 = 0x500
CANP_NODE__COB_TSDO = 0x580
CANP_NODE__COB_RSDO = 0x600
CANP_NODE__COB_RES2 = 0x680
CANP_NODE__COB_ECP = 0x700
CANP_NODE__COB_RES3 = 0x780

list_CANP_NODE__COB_TPDO = [
		CANP_NODE__COB_TPDO1,
		CANP_NODE__COB_TPDO2,
		CANP_NODE__COB_TPDO3,
		CANP_NODE__COB_TPDO4,
	]

list_CANP_NODE__COB_RPDO = [
		CANP_NODE__COB_RPDO1,
		CANP_NODE__COB_RPDO2,
		CANP_NODE__COB_RPDO3,
		CANP_NODE__COB_RPDO4,
	]


# CiA 30x (specific cases)
CANP_NODE__COB_GFC = 0x001				# CiA 302
CANP_NODE__COB_FLYM = 0x071				# CiA 302-2
CANP_NODE__COB_IAI = 0x07F				# CiA 302-6
CANP_NODE__COB_DSDO = 0x6E0				# CiA 302-5
CANP_NODE__COB_LSS = 0x7E4				# CiA 305

# CiA 4xx (specific cases)
CANP_NODE__COB_NCP1 = 0x6E1				# CiA 416-1
CANP_NODE__COB_NCP2 = 0x6F0				# CiA 416-1


# Frame indexes
CANP_LOG__IDX_TIME = 0
CANP_LOG__IDX_COBID = 1
CANP_LOG__IDX_DATA = 2


CANP_NODE__NMT_OP = 0x01				# Operational (1)
CANP_NODE__NMT_STOP = 0x02				# Stopped (2)
CANP_NODE__NMT_PREOP = 0x80				# Pre-Op. (128)
CANP_NODE__NMT_RSTNODE = 0x81			# Reset Node (129)
CANP_NODE__NMT_RSTCOMM = 0x82			# Reset Comm. (130)
CANP_NODE__NMT__DLC = 2

# NTM Finite State Machine (FSM)
list_CANP_NODE__NMT_FSM = [
		CANP_NODE__NMT_OP,
		CANP_NODE__NMT_STOP,
		CANP_NODE__NMT_PREOP,
		CANP_NODE__NMT_RSTNODE,
		CANP_NODE__NMT_RSTCOMM,
	]

dict_CANP_NODE__NMT_FSM = {
		CANP_NODE__NMT_OP: [CANP_NODE__NMT_STOP, CANP_NODE__NMT_PREOP, CANP_NODE__NMT_RSTNODE, CANP_NODE__NMT_RSTCOMM],
		CANP_NODE__NMT_STOP: [CANP_NODE__NMT_OP, CANP_NODE__NMT_PREOP, CANP_NODE__NMT_RSTNODE, CANP_NODE__NMT_RSTCOMM],
		CANP_NODE__NMT_PREOP: [CANP_NODE__NMT_OP, CANP_NODE__NMT_STOP, CANP_NODE__NMT_RSTNODE, CANP_NODE__NMT_RSTCOMM],
		CANP_NODE__NMT_RSTNODE: [CANP_NODE__NMT_RSTCOMM],
		CANP_NODE__NMT_RSTCOMM: [CANP_NODE__NMT_PREOP],
	}


CANP_NODE__EMCY__DLC = 8


CANP_NODE__TIME__DLC = 8


CANP_NODE__TSDO_RECVBLK = 0x00			# Receiving '...' (0x00-0x1F )
CANP_NODE__TSDO_RECVX = 0x41			# Receiving 'x bytes'
CANP_NODE__TSDO_RECV4 = 0x43			# Receive '4 bytes'
CANP_NODE__TSDO_RECV3 = 0x47			# Receive '3 bytes'
CANP_NODE__TSDO_RECV2 = 0x4B			# Receive '2 bytes'
CANP_NODE__TSDO_RECV1 = 0x4F			# Receive '1 byte'
CANP_NODE__TSDO_SENDACK = 0x60			# Send ACK
CANP_NODE__TSDO_SENDERR = 0x80			# Send ERROR
CANP_NODE__TSDO__DLC = 8

list_CANP_NODE__TSDO_CMD = [
		CANP_NODE__TSDO_RECVX,
		CANP_NODE__TSDO_RECV4,
		CANP_NODE__TSDO_RECV3,
		CANP_NODE__TSDO_RECV2,
		CANP_NODE__TSDO_RECV1,
		CANP_NODE__TSDO_SENDACK,
		CANP_NODE__TSDO_SENDERR,
	]


CANP_NODE__RSDO_SEND4 = 0x23			# Send '4 bytes'
CANP_NODE__RSDO_SEND3 = 0x27			# Send '3 bytes'
CANP_NODE__RSDO_SEND2 = 0x2B			# Send '2 bytes'
CANP_NODE__RSDO_SEND1 = 0x2F			# Send '1 byte'
CANP_NODE__RSDO_RDOBJ = 0x40			# Read 'object'
CANP_NODE__RSDO_RDTGL0 = 0x60			# Read '...' (toggle 0)
CANP_NODE__RSDO_RDTGL1 = 0x70			# Read '...' (toggle 1)
CANP_NODE__RSDO_SENDABRT = 0x80			# Send ABORT
CANP_NODE__RSDO__DLC = 8

list_CANP_NODE__RSDO_CMD = [
		CANP_NODE__RSDO_SEND4,
		CANP_NODE__RSDO_SEND3,
		CANP_NODE__RSDO_SEND2,
		CANP_NODE__RSDO_SEND1,
		CANP_NODE__RSDO_RDOBJ,
		CANP_NODE__RSDO_RDTGL0,
		CANP_NODE__RSDO_RDTGL1,
		CANP_NODE__RSDO_SENDABRT,
	]


CANP_NODE__ECP_BOOT = 0x00				# Bootup
CANP_NODE__ECP_STOP = 0x04				# Stopped
CANP_NODE__ECP_OP = 0x05				# Operational
CANP_NODE__ECP_PREOP = 0x7F				# Pre-operational
CANP_NODE__ECP_TOGGLE = 0x80			# Toggle (0x8x : at each Tx)
CANP_NODE__ECP__DLC = 1

list_CANP_NODE__ECP_CMD = [
		CANP_NODE__ECP_BOOT,
		CANP_NODE__ECP_STOP,
		CANP_NODE__ECP_OP,
		CANP_NODE__ECP_PREOP,
		CANP_NODE__ECP_TOGGLE,
	]


CANP_NODE__INDEX_DTA = 0x0000			# 0x0000 – 0x0FFF		Data Types Area (DTA)
										# 0x0000 - 0x0000 : reserved
										# 0x0001 – 0x025F : Data types
										# 0x0260 – 0x0FFF : reserved
CANP_NODE__INDEX_CPA = 0x1000			# 0x1000 – 0x1FFF		Communication Profile Area (CPA)
CANP_NODE__INDEX_MSPA = 0x2000			# 0x2000 – 0x5FFF		Manufacturer Specific Profile Area (MSPA)
CANP_NODE__INDEX_SDPA = 0x6000			# 0x6000 – 0x9FFF		Standardised Device Profile Area (SDPA)
										# 0x6000 - 0x67FF		Device 1
										# 0x6800 - 0x6FFF		Device 2 (same as Device 1, but offset)
										# 0x7000 - 0x77FF		Device 3 (same as Device 1, but offset)
										# 0x7800 - 0x7FFF		Device 4 (same as Device 1, but offset)
										# 0x8000 - 0x87FF		Device 5 (same as Device 1, but offset)
										# 0x8800 - 0x8FFF		Device 6 (same as Device 1, but offset)
										# 0x9000 - 0x97FF		Device 7 (same as Device 1, but offset)
										# 0x9800 - 0x9FFF		Device 8 (same as Device 1, but offset)
CANP_NODE__INDEX_SNVA = 0xA000			# 0xA000 – 0xAFFF		Standardised Network Variable Area (SNVA)
CANP_NODE__INDEX_SSVA = 0xB000			# 0xB000 – 0xBFFF		Standardised System Variable Area (SSVA)
CANP_NODE__INDEX_RES = 0xC000			# 0xC000 – 0xFFFF		reserved

# EMCY error_code (0x00xx : 00 = code below)
dict_CANP_NODE__EMCY_SERR: Dict[int, str] = {
		0x00: "no error or reset",
		0x10: "generic error",
		0x20: "current",
		0x21: "current, canopen device input side",
		0x22: "current inside the canopen device",
		0x23: "current, canopen device output side",
		0x30: "voltage",
		0x31: "mains",
		0x32: "voltage inside the canopen device",
		0x33: "output voltage",
		0x40: "temperature",
		0x41: "ambient temperature",
		0x42: "canopen device temperature",
		0x50: "canopen device hardware",
		0x60: "canopen device software",
		0x61: "internal software",
		0x62: "user software",
		0x63: "data set",
		0x70: "additional modules",
		0x80: "monitoring",
		0x81: "communication",
		0x82: "protocol",
		0x90: "external",
		0xF0: "additional functions",
		0xFF: "canopen device specific"
	}

# CANP_NODE__TSDO_SENDERR error_code
# CANP_NODE__RSDO_SENDABRT error_code
dict_CANP_NODE__SDO_SERR: Dict[int, str] = {
		0x05030000: "toggle bit not changed",
		0x05040001: "command specifier unknown",
		0x06010000: "unsupported access",
		0x06010002: "read only entry",
		0x06020000: "object not existing",
		0x06040041: "object cannot be pdo mapped",
		0x06040042: "mapped pdo exceed pdo",
		0x06070012: "parameter length too long",
		0x06070013: "parameter length too short",
		0x06090011: "subindex not existing",
		0x06090031: "value too great",
		0x06090032: "value too small",
		0x08000000: "general error",
		0x08000022: "data cannot be read or stored in this state"
	}

# Configuration files (key = filename)
g_dict_confs: Optional[Dict[str, canp_conf]] = None

#  --- CLASS ---

class canp_node:
	""" CAN node
	"""

	# Configuration object (for 'raw frame' into 'object' conversion)
	m_cls_cnfs: Optional[canp_conf] = None
	# Frames analysed (key = timestamp)
	m_dict_raws: Optional[Dict[float, Any]] = None
	# Objects stored (key = index, sub-indexes)
	m_dict_objs: Optional[Dict[int, Any]] = None

	# Logger object
	m_logs = canp_logs.logger(CANP_ENUM__APP_NAME).getChild("node")

	m_int_date: int = 0
	m_int_time: int = 0
	m_int_nmt: int = 0x0
	m_int_idx: int = 0
	m_int_sub: int = 0
	m_int_cmd: int = 0
	m_int_acc: int = 0
	m_byte_acc: bytearray = b""

	def __init__(self,
				**i_dict_args: Any
			) -> None:
		""" Constructor
		"""
		super().__init__(**i_dict_args)

	def __getitem__(self,
				i_int_index: int = -1
			) -> Any:
		""" Get at (key = object index, if present)
		"""
		l_any_ret: Any = None

		try:
			l_any_ret = self.m_dict_objs[i_int_index]
			# - except KeyError -
		except KeyError:
			pass

		return l_any_ret

	def __len__(self) -> int:
		""" Size of (number of objects)
		"""
		l_int_ret: int = 0

		if self.m_dict_objs is not None:
			l_int_ret = len(self.m_dict_objs)

		return l_int_ret

	def obj_list(self,
			) -> None:
		""" Object list
		"""
		l_list_ret: list = []

		if self.m_dict_objs is not None:
			l_list_ret = self.m_dict_objs.keys()

		return l_list_ret

	def obj_store(self,
				i_int_idx: int = 0,
				i_int_sub: int = 0,
				i_any_data: Any = CANP_ENUM__STR_EMPTY,
				i_float_time: float = 0.0,
				i_bool_bytes: bool = False
			) -> None:
		""" Object storing
		"""
		l_any_data: Any = None

		l_any_data = i_any_data

		if self.m_dict_objs is None:
			self.m_dict_objs = {}

		try:
			# Check index
			self.m_dict_objs[i_int_idx]
			# - except KeyError -
		except KeyError:
			# Create dict
			self.m_dict_objs[i_int_idx] = {}

		try:
			# Check sub-index
			self.m_dict_objs[i_int_idx][i_int_sub]
			# - except KeyError -
		except KeyError:
			# Create dict
			self.m_dict_objs[i_int_idx][i_int_sub] = {}

		try:
			# Check accumulator (special index)
			self.m_dict_objs[i_int_idx][i_int_sub][CANP_ENUM__HEAD_LIST]
			# - except KeyError -
		except KeyError:
			# Create list
			self.m_dict_objs[i_int_idx][i_int_sub][CANP_ENUM__HEAD_LIST] = []

		if i_bool_bytes == False:
			if isinstance(i_any_data, bytearray) or isinstance(i_any_data, bytes):
				if self.m_cls_cnfs is not None:
					# Trying to decode using conf
					l_any_data = self.m_cls_cnfs.conv_obj(
						i_int_idx,
						i_int_sub,
						i_any_data)

		# Storing raw data (last value)
		self.m_dict_objs[i_int_idx][i_int_sub][CANP_ENUM__HEAD_DATA] = l_any_data

		# Encapsulate for storage (tuple)
		l_any_data = (i_float_time, l_any_data)
		self.m_dict_objs[i_int_idx][i_int_sub][CANP_ENUM__HEAD_LIST].append(l_any_data)

	def pdo_dispatch(self,
				i_int_pdo: int = 0,
				i_bytes_data: bytearray = b"",
				i_float_time: float = 0.0
			) -> None:
		""" Object dispatching
		"""
		if i_int_pdo > 0 and isinstance(i_bytes_data, bytearray) and len(i_bytes_data) > 0:
			#l_enum_typ: enum_TYPE = enum_TYPE.VisibleString
			l_any_data: Any = CANP_ENUM__STR_EMPTY
			l_int_data: int = 0
			l_int_mask: int = 0
			l_int_dlc: int = 0
			l_int_idx: int = 0
			l_int_sub: int = 0
			l_int_max: int = 0
			l_int_len: int = 0
			l_str_err: str = CANP_ENUM__STR_EMPTY
			l_str_chk: str = CANP_ENUM__STR_EMPTY

			if self.m_cls_cnfs is not None:
				l_str_err = f"node.pdo_dispatch.pdo.map[{i_int_pdo:#x}]"
				l_str_chk = "(check config file)"

				try:
					# Configuration object
					l_dict_idx = self.m_cls_cnfs.m_dict_obj[i_int_pdo]
					# - except KeyError -
					# ParameterName=
					# SubNumber=
					# ObjectType=
					# ...

					# Check object integrity ---------------------
					# TODO DUPLICATE START : canp_conf.check_obj
					try:
						# Maximum sub-index
						l_int_max = l_dict_idx[CANP_ENUM__VAL_DEFAULT][enum_CANP_CONF__TYPE.SubNumber]
						# - except KeyError -
						if l_int_max > 0:
							l_int_len = len(self.m_dict_objs[i_int_pdo])
							if l_int_max > l_int_len:
								pass
								#self.m_logs.error(f"{l_str_err}.sub[{l_int_max}].map[{l_int_len}].inconsistent {l_str_chk}".rstrip())

							try:
								# Number of mapped objects (variable)
								l_any_data = self.m_dict_objs[i_int_pdo][0][CANP_ENUM__HEAD_DATA]
								# - except KeyError -
								if isinstance(l_any_data, bytearray):
									l_int_map = canp_conv.int_bytes(l_any_data)
								elif isinstance(l_any_data, int):
									l_int_map = l_any_data

								if l_int_map > 0:
									l_int_len -= 1
									if l_int_map < l_int_len:
										pass
										#self.m_logs.error(f"{l_str_err}.max[{l_int_map}].map[{l_int_len}].unmapped {l_str_chk}".rstrip())
									elif l_int_map != l_int_len:
										pass
										self.m_logs.error(f"{l_str_err}.max[{l_int_map}].map[{l_int_len}].inconsistent {l_str_chk}".rstrip())

									# DUPLICATE END : canp_conf.check_obj
									# Check object integrity ---------------------

									l_int_data = canp_conv.int_bytes(i_bool_bytes = i_bytes_data)
									l_int_dlc = len(i_bytes_data) * 8

									for l_int_loop in range(1, l_int_map + 1):
										# Each mapped object (1 to 64 bits)
										l_str_map = f"map[{i_int_pdo:#x}].sub[{l_int_loop}]"
										try:
											# Pdo register
											l_dict_pdo = self.m_dict_objs[i_int_pdo][l_int_loop]
											# - except KeyError -
											try:
												# Mapped cobid+len
												l_any_data = l_dict_pdo[CANP_ENUM__HEAD_DATA]
												# - except KeyError -
												if isinstance(l_any_data, bytearray):
													l_int_idx = canp_conv.int_bytes(l_any_data)
												elif isinstance(l_any_data, int):
													l_int_idx = l_any_data

												# Target object
												l_int_len = (l_int_idx >> 0) & 0xFF
												l_int_sub = (l_int_idx >> 8) & 0xFF
												l_int_idx = (l_int_idx >> 16) & 0xFFFF

												if l_int_len > 0:
													l_int_mask = (2 ** l_int_len) - 1
													l_any_data = l_int_data & l_int_mask
													l_int_data >>= l_int_len
													l_int_dlc -= l_int_len

													# Byte sized
													if l_int_len >= 8:
														l_int_len //= 8
													else:
														l_int_len = 1

													# Type conversion is done by the store
													l_any_data = bytearray(
														l_any_data.to_bytes(
															l_int_len,
															byteorder = CANP_ENUM__BYTE_LITTLE))

													self.obj_store(
														i_int_idx = l_int_idx,
														i_int_sub = l_int_sub,
														i_any_data = l_any_data,
														i_float_time = i_float_time)
											except KeyError:
												self.m_logs.error(f"{l_str_err}.data.unknown")
										except KeyError:
											self.m_logs.error(f"{l_str_err}.unknown")

									if l_int_dlc > 0:
										pass
										#self.m_logs.error(f"{l_str_err}.data.dlc.leftover[{l_int_dlc}] {l_str_chk}".rstrip())
									elif l_int_dlc < 0:
										pass
										self.m_logs.error(f"{l_str_err}.data.dlc.overshoot[{l_int_dlc}] {l_str_chk}".rstrip())
								else:
									self.m_logs.error(f"{l_str_err}.map.zero")
							except KeyError:
								self.m_logs.error(f"{l_str_err}.map.unknown")
						else:
							self.m_logs.error(f"{l_str_err}.max.zero")
					except KeyError:
						self.m_logs.error(f"{l_str_err}.max.unknown")
				except KeyError:
					self.m_logs.error(f"{l_str_err}.unknown")

	def conf_load(self,
				i_str_file: str = CANP_ENUM__STR_EMPTY,
				i_bool_force: bool = False,
				i_bool_bytes: bool = False
			) -> None:
		""" Node configuration
		"""
		if i_str_file != CANP_ENUM__STR_EMPTY:
			l_enum_typ: enum_TYPE = enum_TYPE.VisibleString
			l_bool_ok: bool = False
			l_any_data: Any = 0
			l_int_idx: int = 0
			l_int_sub: int = 0

			# Access global bank
			global g_dict_confs

			if g_dict_confs is None:
				g_dict_confs = {}

			try:
				# Check if configuration already loaded (key = filename)
				g_dict_confs[i_str_file]
				# - except TypeError - None
				# - except KeyError - index
			except KeyError:
				# Load configuration
				g_dict_confs[i_str_file] = canp_conf(i_str_file)

			# Set configuration
			self.m_cls_cnfs = g_dict_confs[i_str_file]

			# Import parameter/default values (creation / reset)
			if i_bool_force == True or self.m_dict_objs is None:
				for l_int_idx, l_dict_idx in self.m_cls_cnfs.m_dict_obj.items():
					for l_int_sub, l_dict_sub in l_dict_idx.items():
						# Check object integrity ---------------------
						# TODO DUPLICATE START : canp_conf.check_obj
						l_bool_ok = False
						try:
							# Parameter value (from DCF file)
							l_any_data = l_dict_sub[enum_CANP_CONF__TYPE.ParameterValue]
							# - except KeyError -
							l_bool_ok = True
						except KeyError:
							try:
								# Default value (from EDS file)
								l_any_data = l_dict_sub[enum_CANP_CONF__TYPE.DefaultValue]
								# - except KeyError -
								l_bool_ok = True
							except KeyError:
								pass

						if l_bool_ok == True:
							try:
								# Data type
								l_enum_typ = l_dict_sub[enum_CANP_CONF__TYPE.DataType]
								# - except KeyError -
								if isinstance(l_any_data, str):
									# Conversion (if needed)
									l_any_data = canp_conv.any_str(
										l_enum_typ,
										l_any_data)

								if i_bool_bytes == True:
									# Convert and store into bytes (later conversion needed)
									l_any_data = canp_conv.bytes_any(
										l_enum_typ,
										l_any_data)

								if l_int_sub < 0:
									l_int_sub = 0

								self.obj_store(
									i_int_idx = l_int_idx,
									i_int_sub = l_int_sub,
									i_any_data = l_any_data,
									i_bool_bytes = i_bool_bytes)
							except KeyError:
								# No data type ?
								pass

	def frame_parse(self,
				i_list_frame: List[Any] = [],
				i_float_time: float = 0.0,
				i_int_cobid: int = 0,
				i_any_data: bytearray = b'',
			) -> None:
		""" Frame parser
		"""
		# [142.844095, 897, b'\x6c\x4e\x00\x00\xfe\xff\xff\xff']
		# 0 : timestamp (float)
		# 1 : cobid (int)
		# 2 : frame (bytearray, dlc = len)
		l_byte_data: bytearray = b''
		#l_float_time: float = 0.0
		l_bool_toggle: bool = False
		l_bool_store: bool = False
		l_int_cobid: int = 0
		l_int_node: int = 0
		l_int_data: int = 0
		l_int_dlc: int = 0
		l_int_cmd: int = 0
		l_int_pdo: int = 0
		l_int_idx: int = 0
		l_int_sub: int = 0
		l_int_chk: int = 0
		l_str_err: str = CANP_ENUM__STR_EMPTY

		if len(i_list_frame) >= (CANP_LOG__IDX_DATA + 1):
			# Via list
			i_float_time = i_list_frame[CANP_LOG__IDX_TIME]
			i_int_cobid = i_list_frame[CANP_LOG__IDX_COBID]
			i_any_data = i_list_frame[CANP_LOG__IDX_DATA]
		else:
			# Via args
			pass

		l_int_cobid = i_int_cobid
		l_int_node = l_int_cobid & CANP_ENUM__NODE_MAX
		l_int_cobid -= l_int_node
		l_int_dlc = len(i_any_data)

		l_str_err = "node.frame_parse"

		if l_int_cobid == CANP_NODE__COB_NMT and l_int_node == 0:
			# nmt (0x000 / 0)
			if l_int_dlc == CANP_NODE__NMT__DLC:
				l_int_cmd = canp_conv.int_bytes(
					i_bool_bytes = i_any_data[0:1])
				if l_int_cmd in list_CANP_NODE__NMT_FSM:
					if self.m_int_nmt == 0x0:
						self.m_logs.info(f"{l_str_err}.nmt.fsm.init")
						self.m_int_nmt = l_int_cmd
					if self.m_int_nmt != l_int_cmd:
						if l_int_cmd in dict_CANP_NODE__NMT_FSM[self.m_int_nmt]:
							self.m_int_nmt = l_int_cmd
							# transition() callback

							l_bool_store = True
						else:
							self.m_logs.error(f"{l_str_err}.nmt.fsm.error")
					else:
						self.m_logs.error(f"{l_str_err}.nmt.fsm.same")
				else:
					self.m_logs.error(f"{l_str_err}.nmt.cmd.unlisted")
			else:
				self.m_logs.error(f"{l_str_err}.nmt.dlc.mismatch")
		elif l_int_cobid == CANP_NODE__COB_RES1 and l_int_node != 0:
			# reserved (0x000 / 0)
			self.m_logs.info(f"{l_str_err}.res1")
		elif l_int_cobid == CANP_NODE__COB_SYNC and l_int_node == 0:
			# synchro (0x080 / 128)
			if l_int_dlc == 0:
				l_bool_store = True
			else:
				self.m_logs.error(f"{l_str_err}.sync.dlc.mismatch")
		elif l_int_cobid == CANP_NODE__COB_EMCY and l_int_node != 0:
			# emergency (0x080 / 128) -> 0x1014-0x1015
			if l_int_dlc == CANP_NODE__EMCY__DLC:
				# EMCY l_error_code
				l_int_data = canp_conv.int_bytes(
					i_bool_bytes = i_any_data[0:2])
				# l_error_register (0x1001:0)
				l_int_data = canp_conv.int_bytes(
					i_bool_bytes = i_any_data[2:3])
				# MANUFACTURER l_error_code
				l_int_data = canp_conv.int_bytes(
					i_bool_bytes = i_any_data[3:8])

				l_bool_store = True
			else:
				self.m_logs.error(f"{l_str_err}.emcy.dlc.mismatch")
		elif l_int_cobid == CANP_NODE__COB_TIME and l_int_node != 0:
			# time (0x100 / 256)
			if l_int_dlc == CANP_NODE__TIME__DLC:
				# time (ms since midnight)
				l_int_data = canp_conv.int_bytes(
					i_bool_bytes = i_any_data[0:4])
				self.m_int_time = l_int_data
				l_int_h = l_int_data // 3600000
				l_int_m = l_int_data % 3600000
				l_int_s = l_int_m % 60000
				l_int_ms = l_int_s % 1000
				l_int_s = l_int_s // 1000
				l_int_m = l_int_m // 60000
				self.m_logs.info(f"{l_str_err}.time.time={l_int_h}h{l_int_m}m{l_int_s}s{l_int_ms}ms")

				# days (since 01/01/84)
				l_int_data = canp_conv.int_bytes(
					i_bool_bytes = i_any_data[4:6])
				self.m_int_date = l_int_data
				l_obj_epoch = date(1984, 1, 1)
				l_obj_delta = timedelta(days = l_int_data)
				l_obj_date = l_obj_epoch + l_obj_delta
				self.m_logs.info(f"{l_str_err}.time.date={l_obj_date.year}y{l_obj_date.month}m{l_obj_date.day}d")

				# byte 6-7 = 0
				l_int_chk = canp_conv.int_bytes(
					i_bool_bytes = i_any_data[6:8])

				l_bool_store = True
			else:
				self.m_logs.error(f"{l_str_err}.time.dlc.mismatch")
		elif ((self.m_cls_cnfs is not None and l_int_cobid in self.m_cls_cnfs.m_list_pdo[CANP_CONF__PDO_TX]) \
			or l_int_cobid in list_CANP_NODE__COB_TPDO):
			# Tpdo (pdo lookup)
			l_bool_store = True

			if (self.m_cls_cnfs is not None and l_int_cobid in self.m_cls_cnfs.m_list_pdo[CANP_CONF__PDO_TX]):
				# Same as above, yet shall be cached by the interpreter/compiler
				try:
					l_int_pdo = self.m_cls_cnfs.m_list_pdo[CANP_CONF__PDO_TX][l_int_cobid]
					# - except KeyError -
				except KeyError:
					pass
			else:
				l_int_pdo = l_int_cobid
				l_int_pdo -= 0x080
				l_int_pdo //= 0x100
				# CANP_NODE__COB_TPDO1 : (0x180 / 384) -> 0x1800 / 0x1A00
				# CANP_NODE__COB_TPDO2 : (0x280 / 640) -> 0x1801 / 0x1A01
				# CANP_NODE__COB_TPDO3 : (0x380 / 896) -> 0x1802 / 0x1A02
				# CANP_NODE__COB_TPDO4 : (0x480 / 1152) -> 0x1803 / 0x1A03
				l_int_pdo = CANP_CONF__CPA_TPDO_MP + l_int_pdo - 1

			#self.m_logs.warning(f"{l_str_err}.tpdo[{l_int_pdo:#x}]=...")
			self.pdo_dispatch(
				i_int_pdo = l_int_pdo,
				i_bytes_data = i_any_data,
				i_float_time = i_float_time)
		elif ((self.m_cls_cnfs is not None and l_int_cobid in self.m_cls_cnfs.m_list_pdo[CANP_CONF__PDO_RX]) \
			or l_int_cobid in list_CANP_NODE__COB_RPDO):
			# Rpdo (pdo lookup)
			l_bool_store = True

			if (self.m_cls_cnfs is not None and l_int_cobid in self.m_cls_cnfs.m_list_pdo[CANP_CONF__PDO_RX]):
				# Same as above, yet shall be cached by the interpreter/compiler
				try:
					l_int_pdo = self.m_cls_cnfs.m_list_pdo[CANP_CONF__PDO_RX][l_int_cobid]
					# - except KeyError -
				except KeyError:
					pass
			else:
				l_int_pdo = l_int_cobid
				l_int_pdo -= 0x080
				l_int_pdo //= 0x100
				# CANP_NODE__COB_RPDO1 : (0x200 / 512) -> 0x1400 / 0x1600
				# CANP_NODE__COB_RPDO2 : (0x300 / 768) -> 0x1401 / 0x1601
				# CANP_NODE__COB_RPDO3 : (0x400 / 1024) -> 0x1402 / 0x1602
				# CANP_NODE__COB_RPDO4 : (0x500 / 1280) -> 0x1403 / 0x1603
				l_int_pdo = CANP_CONF__CPA_RPDO_MP + l_int_pdo - 1

			#self.m_logs.warning(f"{l_str_err}.rsdo[{l_int_pdo:#x}]=...")
			self.pdo_dispatch(
				i_int_pdo = l_int_pdo,
				i_bytes_data = i_any_data,
				i_float_time = i_float_time)
		elif ((self.m_cls_cnfs is not None and l_int_cobid == self.m_cls_cnfs.m_list_sdo[CANP_CONF__SDO_TX]) \
			or l_int_cobid == CANP_NODE__COB_TSDO) and l_int_node != 0:
			# Tsdo (0x580 / 1408) (conf lookup) -> 0x1200:2
			if l_int_dlc == CANP_NODE__TSDO__DLC:
				l_int_cmd = canp_conv.int_bytes(
					i_bool_bytes = i_any_data[0:1])
				if l_int_cmd in list_CANP_NODE__TSDO_CMD:
					l_int_idx = canp_conv.int_bytes(
						i_bool_bytes = i_any_data[1:3])
					l_int_sub = canp_conv.int_bytes(
						i_bool_bytes = i_any_data[3:4])
					l_int_chk = 0

					# Default state for now
					l_bool_store = True

					if l_int_cmd == CANP_NODE__TSDO_RECVX:
						# 0x41 : Receiving 'x bytes'
						l_int_data = canp_conv.int_bytes(
							i_bool_bytes = i_any_data[4:8])
						if self.m_int_acc == 0:
							self.m_int_idx = l_int_idx
							self.m_int_sub = l_int_sub
							self.m_int_acc = l_int_data
						else:
							self.m_int_acc = 0	# debug
							l_bool_store = False
							self.m_logs.error(f"{l_str_err}.tsdo.recvx.unfinished")
					elif l_int_cmd == CANP_NODE__TSDO_RECV4:
						# 0x43 : Receive '4 bytes'
						l_byte_data = i_any_data[4:8]
						l_int_data = canp_conv.int_bytes(
							i_bool_bytes = l_byte_data)
						self.obj_store(
							i_int_idx = l_int_idx,
							i_int_sub = l_int_sub,
							i_any_data = l_byte_data,
							i_float_time = i_float_time)
					elif l_int_cmd == CANP_NODE__TSDO_RECV3:
						# 0x47 : Receive '3 bytes'
						l_byte_data = i_any_data[4:7]
						l_int_data = canp_conv.int_bytes(
							i_bool_bytes = l_byte_data)
						l_int_chk = canp_conv.int_bytes(
							i_bool_bytes = i_any_data[7:8])
						if l_int_chk == 0:
							self.obj_store(
								i_int_idx = l_int_idx,
								i_int_sub = l_int_sub,
								i_any_data = l_byte_data,
								i_float_time = i_float_time)
						else:
							l_bool_store = False
							self.m_logs.error(f"{l_str_err}.tsdo.recv3.chk")
					elif l_int_cmd == CANP_NODE__TSDO_RECV2:
						# 0x4B : Receive '2 bytes'
						l_byte_data = i_any_data[4:6]
						l_int_data = canp_conv.int_bytes(
							i_bool_bytes = l_byte_data)
						l_int_chk = canp_conv.int_bytes(
							i_bool_bytes = i_any_data[6:8])
						if l_int_chk == 0:
							self.obj_store(
								i_int_idx = l_int_idx,
								i_int_sub = l_int_sub,
								i_any_data = l_byte_data,
								i_float_time = i_float_time)
						else:
							l_bool_store = False
							self.m_logs.error(f"{l_str_err}.tsdo.recv2.chk")
					elif l_int_cmd == CANP_NODE__TSDO_RECV1:
						# 0x4F : Receive '1 byte'
						l_byte_data = i_any_data[4:5]
						l_int_data = canp_conv.int_bytes(
							i_bool_bytes = l_byte_data)
						l_int_chk = canp_conv.int_bytes(
							i_bool_bytes = i_any_data[5:8])
						if l_int_chk == 0:
							self.obj_store(
								i_int_idx = l_int_idx,
								i_int_sub = l_int_sub,
								i_any_data = l_byte_data,
								i_float_time = i_float_time)
						else:
							l_bool_store = False
							self.m_logs.error(f"{l_str_err}.tsdo.recv1.chk")
					elif l_int_cmd == CANP_NODE__TSDO_SENDACK:
						# 0x60 : Send ACK
						l_int_chk = canp_conv.int_bytes(
							i_bool_bytes = i_any_data[4:8])
						if l_int_chk == 0:
							self.m_logs.info(f"{l_str_err}.tsdo.sendack")
						else:
							l_bool_store = False
							self.m_logs.error(f"{l_str_err}.tsdo.sendack.chk")
					elif l_int_cmd == CANP_NODE__TSDO_SENDERR:
						# 0x80 : Send ERROR
						l_int_data = canp_conv.int_bytes(
							i_bool_bytes = i_any_data[4:8])
					else:
						l_bool_store = False
						self.m_logs.error(f"{l_str_err}.tsdo.cmd.unknown")
				else:
					if l_int_cmd >= 0x00 and l_int_cmd <= 0x1F:
						# 0x00-0x1F : Receiving '...'
						if l_int_cmd == 0x00:
							self.m_int_cmd = 0
							self.m_byte_acc = b''

						if l_int_cmd == self.m_int_cmd:
							if self.m_int_acc >= 7:
								self.m_byte_acc.append(
									i_any_data[1:8])
								self.m_int_acc -= 7
							elif self.m_int_acc > 0:
								self.m_byte_acc.append(
									i_any_data[1:(self.m_int_acc + 1)])
								self.m_int_acc = 0
							else:
								pass

							if self.m_int_acc == 0:
								self.obj_store(
									i_int_idx = self.m_int_idx,
									i_int_sub = self.m_int_sub,
									i_any_data = self.m_byte_acc,
									i_float_time = i_float_time)

							self.m_int_cmd += 1
							l_bool_store = True
						else:
							self.m_logs.error(f"{l_str_err}.tsdo.recvx.unordered")

						if self.m_int_acc == 0:
							self.m_int_idx = 0
							self.m_int_sub = 0
							self.m_byte_acc = b''
					else:
						self.m_logs.error(f"{l_str_err}.tsdo.cmd.unlisted")
			else:
				self.m_logs.error(f"{l_str_err}.tsdo.dlc.mismatch")
		elif ((self.m_cls_cnfs is not None \
				and l_int_cobid == self.m_cls_cnfs.m_list_sdo[CANP_CONF__SDO_RX]) \
			or l_int_cobid == CANP_NODE__COB_RSDO) and l_int_node != 0:
			# Rsdo (0x600 / 1536) (conf lookup) -> 0x1200:1
			if l_int_dlc == CANP_NODE__RSDO__DLC:
				l_int_cmd = canp_conv.int_bytes(
					i_bool_bytes = i_any_data[0:1])
				if l_int_cmd in list_CANP_NODE__RSDO_CMD:
					l_int_idx = canp_conv.int_bytes(
						i_bool_bytes = i_any_data[1:3])
					l_int_sub = canp_conv.int_bytes(
						i_bool_bytes = i_any_data[3:4])
					l_int_chk = 0

					# Default state for now
					l_bool_store = True

					if l_int_cmd == CANP_NODE__RSDO_SEND4:
						# 0x23 : Send '4 bytes'
						l_byte_data = i_any_data[4:8]
						l_int_data = canp_conv.int_bytes(
							i_bool_bytes = l_byte_data)
						self.obj_store(
							i_int_idx = l_int_idx,
							i_int_sub = l_int_sub,
							i_any_data = l_byte_data)
							# i_float_time = i_float_time)
					elif l_int_cmd == CANP_NODE__RSDO_SEND3:
						# 0x27 : Send '3 bytes'
						l_byte_data = i_any_data[4:7]
						l_int_data = canp_conv.int_bytes(
							i_bool_bytes = l_byte_data)
						l_int_chk = canp_conv.int_bytes(
							i_bool_bytes = i_any_data[7:8])
						if l_int_chk == 0:
							self.obj_store(
								i_int_idx = l_int_idx,
								i_int_sub = l_int_sub,
								i_any_data = l_byte_data,
								i_float_time = i_float_time)
						else:
							l_bool_store = False
							self.m_logs.error(f"{l_str_err}.rsdo.send3.chk")
					elif l_int_cmd == CANP_NODE__RSDO_SEND2:
						# 0x2B : Send '2 bytes'
						l_byte_data = i_any_data[4:6]
						l_int_data = canp_conv.int_bytes(
							i_bool_bytes = l_byte_data)
						l_int_chk = canp_conv.int_bytes(
							i_bool_bytes = i_any_data[6:8])
						if l_int_chk == 0:
							self.obj_store(
								i_int_idx = l_int_idx,
								i_int_sub = l_int_sub,
								i_any_data = l_byte_data,
								i_float_time = i_float_time)
						else:
							l_bool_store = False
							self.m_logs.error(f"{l_str_err}.rsdo.send2.chk")
					elif l_int_cmd == CANP_NODE__RSDO_SEND1:
						# 0x2F : Send '1 byte'
						l_byte_data = i_any_data[4:5]
						l_int_data = canp_conv.int_bytes(
							i_bool_bytes = l_byte_data)
						l_int_chk = canp_conv.int_bytes(
							i_bool_bytes = i_any_data[5:8])
						if l_int_chk == 0:
							self.obj_store(
								i_int_idx = l_int_idx,
								i_int_sub = l_int_sub,
								i_any_data = l_byte_data,
								i_float_time = i_float_time)
						else:
							l_bool_store = False
							self.m_logs.error(f"{l_str_err}.rsdo.send1.chk")
					elif l_int_cmd == CANP_NODE__RSDO_RDOBJ:
						# 0x40 : Read 'object'
						l_int_chk = canp_conv.int_bytes(
							i_bool_bytes = i_any_data[4:8])
						if l_int_chk == 0:
							self.m_logs.info(f"{l_str_err}.rsdo.rdobj")
						else:
							l_bool_store = False
							self.m_logs.error(f"{l_str_err}.rsdo.rdobj.chk")
					elif l_int_cmd == CANP_NODE__RSDO_RDTGL0:
						# 0x60 : Read '...' (toggle 0)
						l_int_chk = canp_conv.int_bytes(
							i_bool_bytes = i_any_data[4:8])
						if l_int_chk == 0:
							self.m_logs.info(f"{l_str_err}.rsdo.rdtgl0")
						else:
							l_bool_store = False
							self.m_logs.error(f"{l_str_err}.rsdo.rdtgl0.chk")
					elif l_int_cmd == CANP_NODE__RSDO_RDTGL1:
						# 0x70 : Read '...' (toggle 1)
						l_int_chk = canp_conv.int_bytes(
							i_bool_bytes = i_any_data[4:8])
						if l_int_chk == 0:
							self.m_logs.info(f"{l_str_err}.rsdo.rdtgl1")
						else:
							l_bool_store = False
							self.m_logs.error(f"{l_str_err}.rsdo.rdtgl1.chk")
					elif l_int_cmd == CANP_NODE__RSDO_SENDABRT:
						# 0x80 : Send ABORT (l_error_code)
						l_int_data = canp_conv.int_bytes(
							i_bool_bytes = i_any_data[4:8])
					else:
						l_bool_store = False
						self.m_logs.error(f"{l_str_err}.rsdo.cmd.unknown")
				else:
					self.m_logs.error(f"{l_str_err}.rsdo.cmd.unlisted")
			else:
				self.m_logs.error(f"{l_str_err}.rsdo.dlc.mismatch")
		elif l_int_cobid == CANP_NODE__COB_RES2:
			# reserved (0x680 / 1664)
			# May be be configured as PDO (aka 0x1815:TPDOXpar / 0x1A15:TPDOXmap)
			self.m_logs.error(f"{l_str_err}.res2 (unmapped xpdo?)")
			# TODO
		elif l_int_cobid == CANP_NODE__COB_ECP and l_int_node != 0:
			# ecp (0x700 / 1792) -> 0x1016-0x1017
			if l_int_dlc == CANP_NODE__ECP__DLC:
				l_int_cmd = canp_conv.int_bytes(
					i_bool_bytes = i_any_data[0:1])
				if l_int_cmd >= CANP_NODE__ECP_TOGGLE:
					# 0x8x : Toggle (at each Tx)
					l_int_cmd -= CANP_NODE__ECP_TOGGLE
					l_bool_toggle = True
					# TODO : handle toggle bit
				if l_int_cmd in list_CANP_NODE__ECP_CMD:
					l_bool_store = True
					if l_int_cmd == CANP_NODE__ECP_BOOT:
						# 0x00 : Bootup
						self.m_logs.warning(f"{l_str_err}.ecp.cmd.bootup")
						pass
						# TODO
					elif l_int_cmd == CANP_NODE__ECP_STOP:
						# 0x04 : Stopped
						self.m_logs.warning(f"{l_str_err}.ecp.cmd.stop")
						pass
						# TODO
					elif l_int_cmd == CANP_NODE__ECP_OP:
						# 0x05 : Operational
						self.m_logs.warning(f"{l_str_err}.ecp.cmd.op")
						pass
						# TODO
					elif l_int_cmd == CANP_NODE__ECP_PREOP:
						# 0x7F : Pre-operational
						self.m_logs.warning(f"{l_str_err}.ecp.cmd.preop")
						pass
						# TODO
					else:
						l_bool_store = False
						self.m_logs.error(f"{l_str_err}.ecp.cmd.unknown")
				else:
					self.m_logs.error(f"{l_str_err}.ecp.cmd.unlisted")
			else:
				self.m_logs.error(f"{l_str_err}.ecp.dlc.mismatch")
		elif l_int_cobid == CANP_NODE__COB_RES3:
			# reserved (0x780 / 1920)
			self.m_logs.error(f"{l_str_err}.res3 (unmapped xpdo?)")
		else:
			# unknown COBID
			self.m_logs.error(f"{l_str_err}.cobid.unknown")

		if l_bool_store == True:
			l_any_data: Any = (i_int_cobid, i_any_data)
			try:
				# Store raw data (key = timestamp, beware of overwrite)
				self.m_dict_raws[i_float_time] = l_any_data
				# - except KeyError - index
				# - except TypeError - None
			except TypeError:
				# Create dict
				self.m_dict_raws = {i_float_time: l_any_data}

#  --- MAIN ---

def __main__(i_list_args: List = []):
	""" Basic self test (debugging)
	"""
	if True:
		print("--- EDS OBJ ---")
		EDS_FILE = "PAC-P3_v1.0.eds"
		caneton = canp_node()
		caneton.conf_load(i_str_file = EDS_FILE)
	else:
		pass

if __name__ == CANP_ENUM__HEAD_MAIN:
	""" Routine selector
	"""
	canp_args.dispatch(i_list_globals = globals())
