#!/usr/bin/env python
# author: d.koch
# coding: utf-8
# naming: pep-0008
# typing: pep-0484
# docstring: pep-0257
# indentation: tabulation

""" canp_conv.py
	Conversion
"""

#  --- IMPORT ---

# Standard libraries (installed with python)

import logging
import os
import struct
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

from canp_enum import CANP_ENUM__BASE_DECI
from canp_enum import CANP_ENUM__BASE_HEXA

from canp_enum import CANP_ENUM__BYTE_BIG
from canp_enum import CANP_ENUM__BYTE_LITTLE

from canp_enum import CANP_ENUM__HEAD_MAIN
from canp_enum import CANP_ENUM__HEAD_NAME

from canp_enum import CANP_ENUM__STR_EMPTY
from canp_enum import CANP_ENUM__STR_ZERO

from canp_enum import dict_SIZE_TYPE

from canp_enum import enum_ACCS
from canp_enum import enum_OBJT
from canp_enum import enum_TYPE

from canp_enum import list_TYPE_BOOL
from canp_enum import list_TYPE_INT, list_TYPE_SINT
from canp_enum import list_TYPE_REAL
from canp_enum import list_TYPE_STRING
from canp_enum import list_TYPE_TIME


from canp_args import canp_args
from canp_logs import canp_logs

#  --- GLOBAL ---


#  --- CLASS ---

class canp_conv:
	""" CAN data type converter
	"""

	# Logger object
	m_logs = canp_logs.logger(CANP_ENUM__APP_NAME).getChild("conv")

	@staticmethod
	def any_str(
				i_enum_typ: int,
				i_str_val: str = CANP_ENUM__STR_EMPTY
			) -> Any:
		""" DataType value from string
			DataType returned is the closest from the requested 'i_enum_typ'
		"""
		l_any_ret: Any = None

		l_any_ret = i_str_val

		if i_enum_typ in list_TYPE_BOOL:
			# Boolean
			l_any_ret = bool(int(CANP_ENUM__STR_ZERO + i_str_val))
		elif i_enum_typ in list_TYPE_INT:
			# Integer
			if i_str_val[:2] == '0x':
				l_any_ret = int(i_str_val, CANP_ENUM__BASE_HEXA)
			else:
				l_any_ret = int(CANP_ENUM__STR_ZERO + i_str_val, CANP_ENUM__BASE_DECI)
		elif i_enum_typ in list_TYPE_REAL:
			# Real
			l_any_ret = float(CANP_ENUM__STR_ZERO + i_str_val)
		elif i_enum_typ in list_TYPE_STRING:
			# String
			if i_enum_typ == enum_TYPE.OctetString:
				try:
					# If proper format (hex str)
					l_any_ret = bytearray.fromhex(i_str_val)
					# - except ValueError -
				except ValueError:
					# Otherwise...
					l_any_ret = bytearray(i_str_val.encode("utf-8"))
			else:
				# VisibleString - UnicodeString
				l_any_ret = i_str_val
		elif i_enum_typ in list_TYPE_TIME:
			# TODO : Time
			l_any_ret = i_str_val
		else:
			# Go figure...
			l_any_ret = i_str_val

		return l_any_ret

	@staticmethod
	def bytes_any(
				i_enum_typ: int,
				i_any_val: Any
			) -> Any:
		""" Bytes from DataType value
			Bytes returned are the closest conversion from the requested 'i_enum_typ'
		"""
		l_bytes_ret: bytearray = b""
		l_bool_sign: bool = False
		l_int_len: int = 0
		l_str_fun: str = CANP_ENUM__STR_EMPTY

		l_int_len = dict_SIZE_TYPE[i_enum_typ]
		l_str_fun = sys._getframe().f_code.co_name

		if i_enum_typ in list_TYPE_BOOL:
			# Boolean
			if i_any_val == 0:
				l_bytes_ret = bytearray(b"\x00")
			else:
				l_bytes_ret = bytearray(b"\x01")
		elif i_enum_typ in list_TYPE_INT:
			# Integer
			if i_enum_typ in list_TYPE_SINT:
				# OverflowError if True on 0x80000000
				l_bool_sign = False
			else:
				l_bool_sign = False

			try:
				l_bytes_ret = bytearray(
					i_any_val.to_bytes(
						l_int_len,
						byteorder = CANP_ENUM__BYTE_LITTLE,
						signed = l_bool_sign))
				# - except OverflowError -
			except OverflowError:
				m_logs.error("conv.bytes_any.int.overflow")
		elif i_enum_typ in list_TYPE_REAL:
			# Real
			if i_enum_typ == enum_TYPE.Real32:
				l_bytes_ret = bytearray(
					struct.pack(
						'f',
						i_any_val))
			elif i_enum_typ == enum_TYPE.Real64:
				l_bytes_ret = bytearray(
					struct.pack(
						'd',
						i_any_val))
			else:
				m_logs.error("conv.bytes_any.datatype.real.unknown")
		elif i_enum_typ in list_TYPE_STRING:
			# String (mostly)
			if i_enum_typ == enum_TYPE.OctetString:
				l_bytes_ret = i_any_val
			else:
				l_bytes_ret = bytearray(i_any_val.encode("utf-8"))
		elif i_enum_typ in list_TYPE_TIME:
			# TODO : Time
			m_logs.error("conv.bytes_any.datatype.time.unknown")
			l_bytes_ret = bytearray(b'\x00')
		else:
			# Go figure...
			m_logs.error("conv.bytes_any.datatype.unknown")
			l_bytes_ret = bytearray(b'\x00')

		return l_bytes_ret

	@staticmethod
	def any_bytes(
				i_enum_typ: int,
				i_bytes_val: bytearray = b""
			) -> Any:
		""" Value from DataType bytes
			Value returned are the closest conversion from the requested 'i_enum_typ'
		"""
		l_any_ret: Any = None
		l_int_len: int = 0
		l_str_fun: str = CANP_ENUM__STR_EMPTY

		l_any_ret = i_bytes_val
		l_int_len = dict_SIZE_TYPE[i_enum_typ]
		l_str_fun = sys._getframe().f_code.co_name

		if l_int_len <= len(i_bytes_val) or l_int_len < 0:
			if i_enum_typ in list_TYPE_BOOL:
				# Boolean
				l_any_ret = struct.unpack("?", i_bytes_val)
			elif i_enum_typ in list_TYPE_INT:
				# Integer
				l_any_ret = int.from_bytes(i_bytes_val, byteorder = CANP_ENUM__BYTE_LITTLE)
			elif i_enum_typ in list_TYPE_REAL:
				# Real
				if i_enum_typ == enum_TYPE.Real32:
					l_any_ret = struct.unpack("f", i_bytes_val)
				elif i_enum_typ == enum_TYPE.Real64:
					l_any_ret = struct.unpack("d", i_bytes_val)
				else:
					m_logs.error("conv.any_bytes.datatype.real.unknown")
			elif i_enum_typ in list_TYPE_STRING:
				# String (mostly)
				l_any_ret = i_bytes_val.decode("utf-8")
			elif i_enum_typ in list_TYPE_TIME:
				# TODO : Time
				m_logs.error("conv.any_bytes.datatype.time.unknown")
				l_any_ret = b'\x00'
			else:
				# Go figure...
				m_logs.error("conv.any_bytes.datatype.unknown")
				l_any_ret = b'\x00'
		else:
			m_logs.error("conv.any_bytes.size.mismatch")

		return l_any_ret

	@staticmethod
	def int_bytes(
				i_bool_bytes: bytes,
				i_str_enc: str = CANP_ENUM__BYTE_LITTLE,
				i_bool_sign: bool = False
			) -> int:
		""" Integer from bytes
		"""
		return int.from_bytes(
			i_bool_bytes,
			byteorder = i_str_enc,
			signed = i_bool_sign)

	@staticmethod
	def bytes_int(
				i_int_val: int,
				i_str_enc: str = CANP_ENUM__BYTE_LITTLE,
				i_bool_sign: bool = False
			) -> bytes:
		""" Bytes from integer
		"""
		return i_int_val.to_bytes(
			(i_int_val.bit_length() + 7) // 8,
			byteorder = i_str_enc,
			signed = i_bool_sign)

	@staticmethod
	def str_hex(
				i_str_hex: str,
				i_str_enc1: str,
				i_str_enc2: str
			) -> str:
		""" String from hex string
		"""
		return canp_conv.bytes_int(
			int.from_bytes(
				bytes.fromhex(i_str_hex),
				i_str_enc1),
			i_str_enc2).hex()

	@staticmethod
	def swap_hex(i_str_hex: str) -> str:
		""" Swap string characters
		"""
		return canp_conv.str_hex(
			i_str_hex,
			CANP_ENUM__BYTE_BIG,
			CANP_ENUM__BYTE_LITTLE)

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
