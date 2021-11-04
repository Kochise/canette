#!/usr/bin/env python
# author: d.koch
# coding: utf-8
# naming: pep-0008
# typing: pep-0484
# docstring: pep-0257
# indentation: tabulation

""" canp_conf.py
	Configuration
	card-chan-node-CONF
"""

#  --- IMPORT ---

# Standard libraries (installed with python)

import enum
import logging
import os
import re
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from configparser import ConfigParser

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

from canp_conv import canp_conv


from canp_enum import CANP_ENUM__APP_NAME
from canp_enum import CANP_ENUM__BASE_HEXA

from canp_enum import CANP_ENUM__HEAD_LIST
from canp_enum import CANP_ENUM__HEAD_MAIN
from canp_enum import CANP_ENUM__HEAD_NAME

from canp_enum import CANP_ENUM__STR_ASLASH
from canp_enum import CANP_ENUM__STR_DOT
from canp_enum import CANP_ENUM__STR_EMPTY
from canp_enum import CANP_ENUM__STR_SPACE

from canp_enum import CANP_ENUM__VAL_DEFAULT

from canp_enum import enum_ACCS, enum_OBJT, enum_TYPE


from canp_args import canp_args
from canp_logs import canp_logs


from canp_path import canp_path

from canp_path import CANP_PATH__IDX_EXT
from canp_path import CANP_PATH__IDX_FILE

#  --- GLOBAL ---

class enum_CANP_CONF__TYPE(enum.Enum):
	""" Parameters of configuration files (EDS)
	"""

	AccessType = "accesstype"
	BaudRate_10 = "baudrate_10"
	BaudRate_1000 = "baudrate_1000"
	BaudRate_125 = "baudrate_125"
	BaudRate_20 = "baudrate_20"
	BaudRate_250 = "baudrate_250"
	BaudRate_50 = "baudrate_50"
	BaudRate_500 = "baudrate_500"
	BaudRate_800 = "baudrate_800"
	Baudrate = "baudrate"
	CANopenManager = "canopenmanager"
	CompactPDO = "compactpdo"
	CompactSubObj = "compactsubobj"
	CreatedBy = "createdby"
	CreationDate = "creationdate"
	CreationTime = "creationtime"
	DataType = "datatype"
	DefaultValue = "defaultvalue"
	Description = "description"
	DynamicChannelsSupported = "dynamicchannelssupported"
	EDSVersion = "edsversion"
	FileName = "filename"
	FileRevision = "filerevision"
	FileVersion = "fileversion"
	Granularity = "granularity"
	GroupMessaging = "groupmessaging"
	HighLimit = "highlimit"
	LSS_SerialNumber = "lss_serialnumber"
	LSS_Supported = "lss_supported"
	LastEDS = "lasteds"
	Lines = "lines"
	List = CANP_ENUM__HEAD_LIST			# Special case for sections [Comments], [*Objects], ...
	LowLimit = "lowlimit"
	ModificationDate = "modificationdate"
	ModificationTime = "modificationtime"
	ModifiedBy = "modifiedby"
	NetNumber = "netnumber"
	NodeID = "nodeid"
	NodeName = "nodename"
	NrOfEntries = "nrofentries"
	NrOfRXPDO = "nrofrxpdo"
	NrOfTXPDO = "nroftxpdo"
	ObjFlags = "objflags"
	ObjectType = "objecttype"
	OrderCode = "ordercode"
	PDOMapping = "pdomapping"
	ParameterName = "parametername"
	ParameterValue = "parametervalue"
	ProductName = "productname"
	ProductNumber = "productnumber"
	RevisionNumber = "revisionnumber"
	SimpleBootUpMaster = "simplebootupmaster"
	SimpleBootUpSlave = "simplebootupslave"
	SubNumber = "subnumber"
	SupportedObjects = "supportedobjects"
	VendorName = "vendorname"
	VendorNumber = "vendornumber"

# Type from Configuration Enum
dict_CANP_CONF__TYPE = {
		enum_CANP_CONF__TYPE.AccessType: enum_TYPE.VisibleString,
		enum_CANP_CONF__TYPE.BaudRate_10: enum_TYPE.Boolean,
		enum_CANP_CONF__TYPE.BaudRate_1000: enum_TYPE.Boolean,
		enum_CANP_CONF__TYPE.BaudRate_125: enum_TYPE.Boolean,
		enum_CANP_CONF__TYPE.BaudRate_20: enum_TYPE.Boolean,
		enum_CANP_CONF__TYPE.BaudRate_250: enum_TYPE.Boolean,
		enum_CANP_CONF__TYPE.BaudRate_50: enum_TYPE.Boolean,
		enum_CANP_CONF__TYPE.BaudRate_500: enum_TYPE.Boolean,
		enum_CANP_CONF__TYPE.BaudRate_800: enum_TYPE.Boolean,
		enum_CANP_CONF__TYPE.Baudrate: enum_TYPE.Unsigned16,
		enum_CANP_CONF__TYPE.CANopenManager: enum_TYPE.Unsigned16,
		enum_CANP_CONF__TYPE.CompactPDO: enum_TYPE.Unsigned16,
		enum_CANP_CONF__TYPE.CompactSubObj: enum_TYPE.Unsigned8,
		enum_CANP_CONF__TYPE.CreatedBy: enum_TYPE.VisibleString,
		#enum_CANP_CONF__TYPE.CreationDate: enum_TYPE.TimeDifference,		# Currently unsupported
		enum_CANP_CONF__TYPE.CreationDate: enum_TYPE.VisibleString,
		#enum_CANP_CONF__TYPE.CreationTime: enum_TYPE.TimeOfDay,			# Currently unsupported
		enum_CANP_CONF__TYPE.CreationTime: enum_TYPE.VisibleString,
		enum_CANP_CONF__TYPE.DataType: enum_TYPE.Unsigned16,
		enum_CANP_CONF__TYPE.DefaultValue: enum_TYPE.VisibleString,
		enum_CANP_CONF__TYPE.Description: enum_TYPE.VisibleString,
		enum_CANP_CONF__TYPE.DynamicChannelsSupported: enum_TYPE.Unsigned8,
		enum_CANP_CONF__TYPE.EDSVersion: enum_TYPE.Real32,
		enum_CANP_CONF__TYPE.FileName: enum_TYPE.VisibleString,
		enum_CANP_CONF__TYPE.FileRevision: enum_TYPE.Unsigned16,
		enum_CANP_CONF__TYPE.FileVersion: enum_TYPE.Unsigned16,
		enum_CANP_CONF__TYPE.Granularity: enum_TYPE.Unsigned8,
		enum_CANP_CONF__TYPE.GroupMessaging: enum_TYPE.Unsigned8,
		enum_CANP_CONF__TYPE.HighLimit: enum_TYPE.Unsigned32,
		enum_CANP_CONF__TYPE.LSS_SerialNumber: enum_TYPE.Unsigned8,
		enum_CANP_CONF__TYPE.LSS_Supported: enum_TYPE.Unsigned8,
		enum_CANP_CONF__TYPE.LastEDS: enum_TYPE.VisibleString,
		enum_CANP_CONF__TYPE.Lines: enum_TYPE.Unsigned16,
		enum_CANP_CONF__TYPE.LowLimit: enum_TYPE.Unsigned32,
		#enum_CANP_CONF__TYPE.ModificationDate: enum_TYPE.TimeDifference,	# Currently unsupported
		enum_CANP_CONF__TYPE.ModificationDate: enum_TYPE.VisibleString,
		#enum_CANP_CONF__TYPE.ModificationTime: enum_TYPE.TimeOfDay,		# Currently unsupported
		enum_CANP_CONF__TYPE.ModificationTime: enum_TYPE.VisibleString,
		enum_CANP_CONF__TYPE.ModifiedBy: enum_TYPE.VisibleString,
		enum_CANP_CONF__TYPE.NetNumber: enum_TYPE.Unsigned8,
		enum_CANP_CONF__TYPE.NodeID: enum_TYPE.Unsigned8,
		enum_CANP_CONF__TYPE.NodeName: enum_TYPE.VisibleString,
		enum_CANP_CONF__TYPE.NrOfEntries: enum_TYPE.Unsigned8,
		enum_CANP_CONF__TYPE.NrOfRXPDO: enum_TYPE.Unsigned8,
		enum_CANP_CONF__TYPE.NrOfTXPDO: enum_TYPE.Unsigned8,
		enum_CANP_CONF__TYPE.ObjFlags: enum_TYPE.Unsigned32,
		enum_CANP_CONF__TYPE.ObjectType: enum_TYPE.Unsigned8,
		enum_CANP_CONF__TYPE.OrderCode: enum_TYPE.VisibleString,
		enum_CANP_CONF__TYPE.PDOMapping: enum_TYPE.Unsigned8,
		enum_CANP_CONF__TYPE.ParameterName: enum_TYPE.VisibleString,
		enum_CANP_CONF__TYPE.ParameterValue: enum_TYPE.VisibleString,
		enum_CANP_CONF__TYPE.ProductName: enum_TYPE.VisibleString,
		enum_CANP_CONF__TYPE.ProductNumber: enum_TYPE.Unsigned32,
		enum_CANP_CONF__TYPE.RevisionNumber: enum_TYPE.Unsigned16,
		enum_CANP_CONF__TYPE.SimpleBootUpMaster: enum_TYPE.Boolean,
		enum_CANP_CONF__TYPE.SimpleBootUpSlave: enum_TYPE.Boolean,
		enum_CANP_CONF__TYPE.SubNumber: enum_TYPE.Unsigned16,
		enum_CANP_CONF__TYPE.SupportedObjects: enum_TYPE.Unsigned8,
		enum_CANP_CONF__TYPE.VendorName: enum_TYPE.VisibleString,
		enum_CANP_CONF__TYPE.VendorNumber: enum_TYPE.Unsigned32,
	}

# Communication PArameter (CPA)
CANP_CONF__CPA_SSDO_CP = 0x1200
CANP_CONF__CPA_CSDO_CP = 0x1280
CANP_CONF__CPA_RPDO_CP = 0x1400
CANP_CONF__CPA_RPDO_MP = 0x1600
CANP_CONF__CPA_TPDO_CP = 0x1800
CANP_CONF__CPA_TPDO_MP = 0x1A00
CANP_CONF__CPA__CP_LEN = 0x0200

list_CANP_CONF__CPA = [
		CANP_CONF__CPA_SSDO_CP,
		CANP_CONF__CPA_CSDO_CP,
		CANP_CONF__CPA_RPDO_CP,
		CANP_CONF__CPA_RPDO_MP,
		CANP_CONF__CPA_TPDO_CP,
		CANP_CONF__CPA_TPDO_MP,
	]

# Process Data Object (PDO)
CANP_CONF__PDO_COB_FRAME = 0x40000000
CANP_CONF__PDO_COB_FRAME__11BITS = 0
CANP_CONF__PDO_COB_RTR = 0x40000000
CANP_CONF__PDO_COB_RTR__ALLOWED = 0
CANP_CONF__PDO_COB_VALID = 0x80000000
CANP_CONF__PDO_COB_VALID__VALID = 0

CANP_CONF__PDO_RX = 0
CANP_CONF__PDO_TX = 1

# Service Data Object (SDO)
CANP_CONF__SDO_RX = 0
CANP_CONF__SDO_TX = 1

#  --- CLASS ---

class canp_conf:
	""" CAN configuration
	"""

	# Parameter
	m_dict_par: Dict[str, Any] = {}
	# Object (key = index, sub-indexes)
	m_dict_obj: Dict[int, Any] = {}
	# PDO mapper
	m_list_pdo: List[Dict[int, int]] = []
	# SDO mapper
	m_list_sdo: List[int] = []
	# Configuration file name (if loaded successfully)
	m_str_name: str = CANP_ENUM__STR_EMPTY

	# Logger object
	m_logs = canp_logs.logger(CANP_ENUM__APP_NAME).getChild("conf")

	def __init__(self,
				i_str_file: str,
				**i_dict_args: Any
			) -> None:
		""" Constructor
		"""
		super().__init__(**i_dict_args)

		if i_str_file != CANP_ENUM__STR_EMPTY:
			l_list_path = canp_path.list_str(i_str_path = i_str_file)
			l_str_ext = l_list_path[CANP_PATH__IDX_EXT].lower()

			if l_str_ext == "eds" or l_str_ext == "dcf":
				self.load_eds(i_str_file)
			else:
				self.m_logs.error(f"init.file.format[{l_str_ext}].unknown")

	def __getitem__(self,
				i_int_index
			) -> Any:
		""" Get at (key = object index, if present)
		"""
		return self.m_dict_obj[i_int_index]

	def __len__(self):
		""" Size of (number of objects)
		"""
		return len(self.m_dict_obj)

	@staticmethod
	def conv_cnf(
				i_enum_cnf: enum_CANP_CONF__TYPE,
				i_str_val: str
			) -> Any:
		""" Type converter
		"""
		l_any_ret: Any = 0
		l_enum_typ: enum_TYPE = enum_TYPE.VisibleString

		try:
			l_enum_typ = dict_CANP_CONF__TYPE[i_enum_cnf]
			# - except KeyError -
		except KeyError:
			# Use default type (not the brightest idea)
			pass

		l_any_ret = canp_conv.any_str(
			l_enum_typ,
			i_str_val)

		# Specific conversion (from integers)
		if i_enum_cnf is enum_CANP_CONF__TYPE.AccessType:
			l_any_ret = enum_ACCS(l_any_ret)
		elif i_enum_cnf is enum_CANP_CONF__TYPE.DataType:
			l_any_ret = enum_TYPE(l_any_ret)
		elif i_enum_cnf is enum_CANP_CONF__TYPE.ObjectType:
			l_any_ret = enum_OBJT(l_any_ret)

		return l_any_ret

	def conv_obj(self,
				i_int_idx: int = 0,
				i_int_sub: int = 0,
				i_bytes_data: bytearray = b''
			) -> Any:
		""" Type converter
		"""
		l_any_ret: Any = None
		l_dict_idx: Any = None
		l_dict_sub: Any = None
		l_int_max: int = 0
		l_enum_typ: int = 0

		l_any_ret = i_bytes_data

		if isinstance(i_bytes_data, bytearray) and len(i_bytes_data) > 0:
			try:
				# Object index
				l_dict_idx = self.m_dict_obj[i_int_idx]
				# - except KeyError -
				# ParameterName=
				# SubNumber=
				# ObjectType=
				# ...

				try:
					# Object sub-index
					l_dict_sub = l_dict_idx[i_int_sub]
					# - except KeyError -
					# ParameterName=
					# ObjectType=
					# DataType=
					# AccessType=
					# PDOMapping=
					# DefaultValue=
					# ...

				except KeyError:
					try:
						l_dict_sub = l_dict_idx[CANP_ENUM__VAL_DEFAULT]
					except KeyError:
						# Handle the error below (== None)
						pass

				if l_dict_sub is not None:
					try:
						l_enum_typ = l_dict_sub[enum_CANP_CONF__TYPE.DataType]
						# - except KeyError -
						l_any_ret = canp_conv.any_bytes(
							l_enum_typ,
							i_bytes_data)
					except KeyError:
						self.m_logs.error(f"conv_obj.idx[{i_int_idx:#x}].sub[{i_int_sub:#x}].data.type.unknown")
				else:
					self.m_logs.error(f"conv_obj.idx[{i_int_idx:#x}].sub[{i_int_sub:#x}].unknown")
			except KeyError:
				self.m_logs.error(f"conv_obj.idx[{i_int_idx:#x}].unknown")

		return l_any_ret

	def check_obj(self,
				i_int_idx: int = 0,
				i_str_err: str = CANP_ENUM__STR_EMPTY,
				i_str_chk: str = CANP_ENUM__STR_EMPTY
			) -> None:
		""" Check object integrity
		"""
		l_bool_ok: bool = False
		l_any_data: Any = 0
		l_int_max: int = 0
		l_int_map: int = 0
		l_int_len: int = 0
		l_str_err: str = CANP_ENUM__STR_EMPTY

		l_str_err = f"{i_str_err}.idx[{i_int_idx:#x}]"

		# Maximum sub-index
		try:
			l_int_max = self.m_dict_obj[i_int_idx][CANP_ENUM__VAL_DEFAULT][enum_CANP_CONF__TYPE.SubNumber]
			# - except KeyError -
			if l_int_max > 0:
				# Subtract CANP_ENUM__VAL_DEFAULT
				l_int_len = len(self.m_dict_obj[i_int_idx]) - 1
				if l_int_max > l_int_len:
					pass
					self.m_logs.error(f"{l_str_err}.sub[{l_int_max}].len[{l_int_len}].mismatch {i_str_chk}".rstrip())

				l_bool_ok = False
				# Number of mapped objects (variable)
				try:
					# Parameter value
					l_any_data = self.m_dict_obj[i_int_idx][0][enum_CANP_CONF__TYPE.ParameterValue]
					# - except KeyError -
					l_bool_ok = True
				except KeyError:
					try:
						# Default value
						l_any_data = self.m_dict_obj[i_int_idx][0][enum_CANP_CONF__TYPE.DefaultValue]
						# - except KeyError -
						l_bool_ok = True
					except KeyError:
						pass

				if l_bool_ok == True:
					if isinstance(l_any_data, bytearray):
						l_int_map = canp_conv.int_bytes(l_any_data)
					elif isinstance(l_any_data, int):
						l_int_map = l_any_data

					if l_int_map > 0:
						# Subtract 0 ("Number of mapped objects")
						l_int_len -= 1
						if l_int_map < l_int_len:
							pass
							self.m_logs.warning(f"{l_str_err}.len[{l_int_len}].map[{l_int_map}].useless {i_str_chk}".rstrip())
						elif l_int_map != l_int_len:
							pass
							self.m_logs.error(f"{l_str_err}.len[{l_int_len}].map[{l_int_map}].mismatch {i_str_chk}".rstrip())
				else:
					pass
					self.m_logs.error(f"{l_str_err}.map.unknown {i_str_chk}".rstrip())
			else:
				self.m_logs.error(f"{l_str_err}.sub.zero {i_str_chk}".rstrip())
		except KeyError:
			pass

	def load_eds(self,
				i_str_file: str
			) -> None:
		""" Load EDS/DCF configuration file
		"""
		if isinstance(i_str_file, str) and i_str_file != CANP_ENUM__STR_EMPTY:
			self.m_dict_par = {}
			self.m_dict_obj = {}
			self.m_list_pdo = [{}, {}]
			self.m_list_sdo = [0, 0]

			l_str_file: str = CANP_ENUM__STR_EMPTY
			l_str_err: str = CANP_ENUM__STR_EMPTY
			l_str_sub: str = CANP_ENUM__STR_EMPTY
			l_str_chk: str = CANP_ENUM__STR_EMPTY
			l_int_old: int = CANP_ENUM__VAL_DEFAULT

			l_list_path = canp_path.list_str(i_str_path = i_str_file)
			l_str_file = CANP_ENUM__STR_DOT.join(l_list_path[CANP_PATH__IDX_FILE:])

			l_re_sub = re.compile(r"[0-9a-fA-F]+sub[0-9a-fA-F]+")
			l_re_val = re.compile(r"[0-9a-fA-F]+value")

			# Load EDS/INI file
			l_obj_load: Optional[ConfigParser] = ConfigParser()
			l_obj_load.read(i_str_file)

			l_str_err = f"load_eds[{l_str_file}]"
			l_str_chk = ""

			# Explore sections
			for l_str_sect in l_obj_load.sections():
				# 'l_str_sect' should be left untouched (case sensitive)
				# Comments
				# FileInfo
				# DeviceInfo
				# 1018sub0
				# ...

				l_int_obj: int = CANP_ENUM__VAL_DEFAULT
				l_int_sub: int = CANP_ENUM__VAL_DEFAULT
				l_int_acc: int = 0
				l_any_val: Any = 0
				l_str_obj: str = CANP_ENUM__STR_EMPTY
				l_str_sub: str = CANP_ENUM__STR_EMPTY
				l_str_val: str = CANP_ENUM__STR_EMPTY
				l_enum_key: int = 0
				l_enum_lst: int = 0
				l_enum_val: int = 0
				l_list_acc: List[str] = []

				# Using heavy duck-typing to identify sections (fuzzy logic)
				# False positives are filtered out below

				# Check Obj[Sub]
				if l_re_sub.search(l_str_sect.lower()):
					# Sub-object (most probably)
					[l_str_obj, l_str_sub] = l_str_sect.lower().split("sub")
				elif l_re_val.search(l_str_sect.lower()):
					# List of compact sub-objects
					[l_str_obj, l_str_sub] = l_str_sect.lower().split("value")
					# Flagging compact object
					l_any_val = 1
				else:
					# Object or parameter (maybe)
					l_str_obj = l_str_sect

				# Check if really an object
				try:
					l_int_obj = int(l_str_obj, CANP_ENUM__BASE_HEXA)
					# - except ValueError -
					# Object (mostly)
					if l_str_sub != CANP_ENUM__STR_EMPTY:
						try:
							l_int_sub = int(l_str_sub, CANP_ENUM__BASE_HEXA)
							# - except ValueError -
							# Object (most probably)
						except ValueError:
							# Parameter (false positive)
							l_str_obj = l_str_sect
							l_str_sub = CANP_ENUM__STR_EMPTY
					else:
						# Object (forced)
						l_str_sub = CANP_ENUM__STR_DOT
				except ValueError:
					# Parameter (now for sure)
					pass

				if l_str_sub == CANP_ENUM__STR_EMPTY:
					# Parameter (for sure now)
					self.m_dict_par[l_str_sect] = {}

					if l_str_sect.lower() == "comments":
						l_enum_lst = enum_CANP_CONF__TYPE.Lines
						l_enum_val = enum_CANP_CONF__TYPE.Description
					else:
						l_enum_lst = enum_CANP_CONF__TYPE.SupportedObjects
						l_enum_val = enum_CANP_CONF__TYPE.SubNumber

					# Explore sub-keys
					for l_str_key in l_obj_load[l_str_sect]:
						l_str_key.lower()
						# ParameterName
						# ObjectType
						# DataType
						# ...

						l_str_val = l_obj_load[l_str_sect][l_str_key]
						l_str_sub = f"{l_str_err}.list[{l_str_sect}].line[{l_str_key}]"

						if len(l_list_acc) == 0:
							# No list scanning
							try:
								# Simple copy
								l_enum_key = enum_CANP_CONF__TYPE(l_str_key)
								# - except ValueError -
								if l_enum_key == enum_CANP_CONF__TYPE.DefaultValue \
								or l_enum_key == enum_CANP_CONF__TYPE.ParameterValue:
									try:
										l_enum_val = self.m_dict_par[l_str_sect][enum_CANP_CONF__TYPE.DataType]
										# - except KeyError -
										l_any_val = canp_conv.any_str(l_enum_val, l_str_val)
									except KeyError:
										l_any_val = l_str_val
								else:
									l_any_val = self.conv_cnf(l_enum_key, l_str_val)

								self.m_dict_par[l_str_sect][l_enum_key] = l_any_val
							except ValueError:
								# List scanning (startup)
								try:
									l_int_max = int(self.m_dict_par[l_str_sect][l_enum_lst])
									# - except KeyError -
									l_any_val = self.conv_cnf(l_enum_val, l_str_val)
									l_list_acc.append(l_any_val)
									l_int_acc += 1
								except KeyError:
									# No more a list (obviously)
									self.m_logs.error(f"{l_str_sub}.unknown")
						else:
							# List scanning (continuation)
							try:
								l_int_max = int(self.m_dict_par[l_str_sect][l_enum_lst])
								# - except KeyError -
								if l_int_acc < l_int_max:
									l_any_val = self.conv_cnf(l_enum_val, l_str_val)
									l_list_acc.append(l_any_val)
									l_int_acc += 1

								if l_int_acc == l_int_max:
									# Store list
									self.m_dict_par[l_str_sect][enum_CANP_CONF__TYPE.List] = l_list_acc

								if l_int_acc > l_int_max:
									# Problem there
									self.m_logs.error(f"{l_str_sub}.overshoot")
							except KeyError:
								# No more a list (obviously)
								self.m_logs.error(f"{l_str_sub}.unknown")
				else:
					# Object (by default)
					try:
						# Check index
						self.m_dict_obj[l_int_obj]
						# - except KeyError -
					except KeyError:
						self.m_dict_obj[l_int_obj] = {}

					try:
						# Check sub-index
						self.m_dict_obj[l_int_obj][l_int_sub]
						# - except KeyError -
					except KeyError:
						self.m_dict_obj[l_int_obj][l_int_sub] = {}

					# Check previous object integrity
					if l_int_old != l_int_obj:
						if l_int_old != CANP_ENUM__VAL_DEFAULT:
							self.check_obj(l_int_old, l_str_err, l_str_chk)

						l_int_old = l_int_obj

					if l_any_val == 1:
						# Compact sub-object
						l_enum_lst = enum_CANP_CONF__TYPE.NrOfEntries
						try:
							l_int_max = self.m_dict_obj[l_int_obj][CANP_ENUM__VAL_DEFAULT][enum_CANP_CONF__TYPE.CompactSubObj]
							# - except KeyError -
						except KeyError:
							self.m_logs.error(f"{l_str_err}.obj[{l_str_sect}].compact.unknown (possible orphan?)")

					for l_str_key in l_obj_load[l_str_sect]:
						l_str_val = l_obj_load[l_str_sect][l_str_key]
						try:
							# Simple copy
							l_enum_key = enum_CANP_CONF__TYPE(l_str_key)
							# - except ValueError -
							if l_enum_key == enum_CANP_CONF__TYPE.DefaultValue \
							or l_enum_key == enum_CANP_CONF__TYPE.ParameterValue:
								# Convert using proper DataType
								try:
									l_enum_val = self.m_dict_obj[l_int_obj][l_int_sub][enum_CANP_CONF__TYPE.DataType]
									# - except KeyError -
									# Specific cases (cleaning up the dirt)
									l_str_val = l_str_val.replace('$NODEID+', CANP_ENUM__STR_EMPTY)
									l_any_val = canp_conv.any_str(l_enum_val, l_str_val)
								except KeyError:
									# Store as string (later conversion needed)
									l_any_val = l_str_val
							else:
								l_any_val = self.conv_cnf(l_enum_key, l_str_val)

							# Store (using the proper data type)
							self.m_dict_obj[l_int_obj][l_int_sub][l_enum_key] = l_any_val

							if l_enum_lst == l_enum_key:
								# Compact sub-object
								if l_any_val != l_int_max:
									# NrOfEntries != CompactSubObj (not a big deal)
									self.m_logs.error(f"{l_str_err}.obj[{l_str_sect}].compact.entries.mismatch")
						except ValueError:
							if l_enum_lst == enum_CANP_CONF__TYPE.NrOfEntries:
								# Compact sub-object
								l_int_sub = self.conv_cnf(l_enum_lst, l_str_key)
								try:
									# Copy reference object
									self.m_dict_obj[l_int_obj][l_int_sub] = self.m_dict_obj[l_int_obj][CANP_ENUM__VAL_DEFAULT]
									# - except KeyError -
									try:
										l_enum_val = self.m_dict_obj[l_int_obj][l_int_sub][enum_CANP_CONF__TYPE.DataType]
										# - except KeyError -
										l_any_val = canp_conv.any_str(l_enum_val, l_str_val)
										# Store as right type (beware for later conversion)
										self.m_dict_obj[l_int_obj][l_int_sub][enum_CANP_CONF__TYPE.ParameterValue] = l_any_val
									except KeyError:
										self.m_logs.error(f"{l_str_err}.obj[{l_str_sect}].compact.datatype.missing")
										# Store as string (later conversion needed, maybe)
										self.m_dict_obj[l_int_obj][l_int_sub][enum_CANP_CONF__TYPE.ParameterValue] = l_str_val
								except KeyError:
									pass

			if l_str_sub != CANP_ENUM__STR_EMPTY:
				# Check last object integrity
				if l_int_old != CANP_ENUM__VAL_DEFAULT:
					self.check_obj(l_int_old, l_str_err, l_str_chk)

			# Store file name (provided everything went right)
			if False:
				self.m_str_name = l_list_path[CANP_PATH__IDX_FILE]
			else:
				self.m_str_name = l_str_file

			# Filter configured pdos
			for l_int_pdo in self.m_dict_obj:
				l_bool_ok: bool = False
				l_int_val: int = 0

				if l_int_pdo == CANP_CONF__CPA_SSDO_CP:
					# sdo : 0x1200
					try:
						l_int_val = self.m_dict_obj[l_int_pdo][1][enum_CANP_CONF__TYPE.DefaultValue]
						# - except KeyError - index
						if l_int_val & CANP_CONF__PDO_COB_VALID == CANP_CONF__PDO_COB_VALID__VALID:
							# Activated
							l_bool_ok = False
							while l_bool_ok == False:
								try:
									self.m_list_sdo[CANP_CONF__SDO_RX] = l_int_val
									# - except KeyError - index
									# - except TypeError - None
									l_bool_ok = True
								except KeyError:
									self.m_list_sdo = [0, 0]
								except TypeError:
									self.m_list_sdo = [0, 0]
					except KeyError:
						pass
					try:
						l_int_val = self.m_dict_obj[l_int_pdo][2][enum_CANP_CONF__TYPE.DefaultValue]
						# - except KeyError - index
						if l_int_val & CANP_CONF__PDO_COB_VALID == CANP_CONF__PDO_COB_VALID__VALID:
							# Activated
							l_bool_ok = False
							while l_bool_ok == False:
								try:
									self.m_list_sdo[CANP_CONF__SDO_TX] = l_int_val
									# - except KeyError - index
									# - except TypeError - None
									l_bool_ok = True
								except KeyError:
									self.m_list_sdo = [0, 0]
								except TypeError:
									self.m_list_sdo = [0, 0]
					except KeyError:
						pass
				elif l_int_pdo >= CANP_CONF__CPA_TPDO_CP and l_int_pdo < (CANP_CONF__CPA_TPDO_CP + CANP_CONF__CPA__CP_LEN):
					# Tpdo : 0x1800 / 0x1A00
					try:
						l_int_val = self.m_dict_obj[l_int_pdo][1][enum_CANP_CONF__TYPE.DefaultValue]
						# - except KeyError - index
						if l_int_val & CANP_CONF__PDO_COB_VALID == CANP_CONF__PDO_COB_VALID__VALID:
							# Activated
							l_bool_ok = False
							while l_bool_ok == False:
								try:
									self.m_list_pdo[CANP_CONF__PDO_TX][l_int_val] = l_int_pdo + CANP_CONF__CPA__CP_LEN
									# - except KeyError - index
									# - except TypeError - None
									l_bool_ok = True
								except KeyError:
									self.m_list_pdo = [{}, {}]
								except TypeError:
									self.m_list_pdo = [{}, {}]
					except KeyError:
						pass
				elif l_int_pdo >= CANP_CONF__CPA_RPDO_CP and l_int_pdo < (CANP_CONF__CPA_RPDO_CP + CANP_CONF__CPA__CP_LEN):
					# Rpdo : 0x1400 / 0x1600
					try:
						l_int_val = self.m_dict_obj[l_int_pdo][1][enum_CANP_CONF__TYPE.DefaultValue]
						# - except KeyError - index
						if l_int_val & CANP_CONF__PDO_COB_VALID == CANP_CONF__PDO_COB_VALID__VALID:
							# Activated
							l_bool_ok = False
							while l_bool_ok == False:
								try:
									self.m_list_pdo[CANP_CONF__PDO_RX][l_int_val] = l_int_pdo + CANP_CONF__CPA__CP_LEN
									# - except KeyError - index
									# - except TypeError - None
									l_bool_ok = True
								except KeyError:
									self.m_list_pdo = [{}, {}]
								except TypeError:
									self.m_list_pdo = [{}, {}]
					except KeyError:
						pass

#  --- MAIN ---

def __main__(i_list_args: List = []):
	""" Basic self test (debugging)
	"""
	DCF_FILE = "carteGripper_config_01.dcf"
	EDS_FILE = "PAC-P3_v1.0.eds"

	if False:
		print("--- INI file ---")
		dict_eds = ConfigParser()
		dict_eds.read(EDS_FILE)
		print(dict_eds.sections())
		print(dict_eds["31FF"])
		for key in dict_eds["31FF"]:
			print(key)
		print(dict_eds["31FF"]["ObjectType"])
	else:
		print("--- EDS/DCF file ---")
		conf = canp_conf(i_str_file = DCF_FILE)

if __name__ == CANP_ENUM__HEAD_MAIN:
	""" Routine selector
	"""
	canp_args.dispatch(i_list_globals = globals())
