#!/usr/bin/env python
# author: d.koch
# coding: utf-8
# naming: pep-0008
# typing: pep-0484
# docstring: pep-0257
# indentation: tabulation

""" canp_enum.py
	Enums for CANette
"""

#  --- IMPORT ---

# Standard libraries (installed with python)

import enum
import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

#from typing import Any
#from typing import Callable
#from typing import Dict
from typing import List
#from typing import Optional
#from typing import Union

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

# External libraries (installed with pip, conda, setup.py, ...)

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

# Included libraries (this module, local files)

from canp_args import canp_args

#  --- GLOBAL ---

CANP_ENUM__APP_NAME = "canp"

# End Of Line (EOL)
CANP_ENUM__EOL_CR = "\r"
CANP_ENUM__EOL_LF = "\n"
CANP_ENUM__EOL_CRLF = "\r\n"

# Common characters
CANP_ENUM__STR_DOT = "."
CANP_ENUM__STR_PIPE = "|"
CANP_ENUM__STR_ZERO = "0"
CANP_ENUM__STR_EMPTY = ""
CANP_ENUM__STR_SPACE = " "
CANP_ENUM__STR_SLASH = "/"
CANP_ENUM__STR_ASLASH = "\\"
CANP_ENUM__STR_HASHTAG = "#"
CANP_ENUM__STR_PERCENT = "%"

# Grouping characters
CANP_ENUM__STR_ANGLEO = "<"
CANP_ENUM__STR_ANGLEC = ">"
CANP_ENUM__STR_CURLYO = "{"
CANP_ENUM__STR_CURLYC = "}"
CANP_ENUM__STR_PARENTO = "("
CANP_ENUM__STR_PARENTC = ")"
CANP_ENUM__STR_SQUAREO = "["
CANP_ENUM__STR_SQUAREC = "]"

# Section names (python and other)
CANP_ENUM__HEAD_ATTR = "__attr__"
CANP_ENUM__HEAD_CARD = "__card__"
CANP_ENUM__HEAD_CURR = "__curr__"
CANP_ENUM__HEAD_DATA = "__data__"
CANP_ENUM__HEAD_DICT = "__dict__"
CANP_ENUM__HEAD_DONE = "__done__"
CANP_ENUM__HEAD_INIT = "__init__"
CANP_ENUM__HEAD_LAST = "__last__"
CANP_ENUM__HEAD_LIST = "__list__"
CANP_ENUM__HEAD_MAIN = "__main__"
CANP_ENUM__HEAD_NAME = "__name__"
CANP_ENUM__HEAD_PROC = "__proc__"
CANP_ENUM__HEAD_READ = "__read__"
CANP_ENUM__HEAD_REPL = "__repl__"
CANP_ENUM__HEAD_REPR = "__repr__"
CANP_ENUM__HEAD_VOID = "__void__"

# Byte order
CANP_ENUM__BYTE_BIG = "big"
CANP_ENUM__BYTE_LITTLE = "little"
CANP_ENUM__BYTE_ENDIAN = CANP_ENUM__BYTE_LITTLE

# Url addresses
CANP_ENUM__URL_LOCALHOST = "127.0.0.1"

# Numeric base
CANP_ENUM__BASE_DECI = 10
CANP_ENUM__BASE_HEXA = 16

# Node identifier
CANP_ENUM__NODE_MIN = 0					# Broadcast
CANP_ENUM__NODE_MAX = (128 - 1)

# Default values
CANP_ENUM__VAL_DEFAULT = -1				# Last index
CANP_ENUM__VAL_LOGGING = logging.INFO

# Data indexes
CANP_ENUM__IDX_LAST = -1

# Arrays list indexes (currently for debugging purpose only)
CANP_ENUM__IDX_X_CAN = 0
CANP_ENUM__IDX_X_REF = 1
CANP_ENUM__IDX_Y_CAN = 2
CANP_ENUM__IDX_Y_REF = 3
CANP_ENUM__IDX_Z_CAN = 4
CANP_ENUM__IDX_Z_REF = 5

#  --- CLASS ---

# Access rights
class enum_ACCS(enum.Enum):
	""" CAN access types (AccessType)
	"""

	const = "const"						# Constant (ro)
	ro = "ro"							# Read only
	rw = "rw"							# Read write
	rwr = "rwr"							# Read write, reading immediate (Tpdo)
	rww = "rww"							# Read write, writing immediate (Rpdo)
	wo = "wo"							# Write only

# Object identifiers
class enum_OBJT(enum.Enum):
	""" CAN object types (ObjectType)
	"""

	Null = 0
	#Reserved1 = 1						# Currently unsupported
	Domain = 2
	#Reserved3 = 3						# Currently unsupported
	#Reserved4 = 4						# Currently unsupported
	Deftype = 5
	Defstruct = 6
	Var = 7
	Array = 8
	Record = 9

# Type identifiers
class enum_TYPE(enum.Enum):
	""" CAN data types (DataType)
	"""

	Boolean = 1
	Integer8 = 2
	Integer16 = 3
	Integer32 = 4
	Unsigned8 = 5
	Unsigned16 = 6
	Unsigned32 = 7
	Real32 = 8
	VisibleString = 9
	OctetString = 10
	UnicodeString = 11
	TimeOfDay = 12
	TimeDifference = 13
	#Reserved14 = 14					# Currently unsupported
	Domain = 15
	Integer24 = 16
	Real64 = 17
	Integer40 = 18
	Integer48 = 19
	Integer56 = 20
	Integer64 = 21
	Unsigned24 = 22
	#Reserved23 = 23					# Currently unsupported
	Unsigned40 = 24
	Unsigned48 = 25
	Unsigned56 = 26
	Unsigned64 = 27
	#Reserved28 = 28					# Currently unsupported
	#Reserved29 = 29					# Currently unsupported
	#Reserved30 = 30					# Currently unsupported
	#Reserved31 = 31					# Currently unsupported
	PdoCommParam = 32
	PdoMapParam = 33
	SdoParam = 34
	Identity = 35

# Booleans
list_TYPE_BOOL = [
		enum_TYPE.Boolean,
	]

# Signed integers
list_TYPE_SINT = [
		enum_TYPE.Integer8,
		enum_TYPE.Integer16,
		enum_TYPE.Integer32,
		enum_TYPE.Integer24,
		enum_TYPE.Integer40,
		enum_TYPE.Integer48,
		enum_TYPE.Integer56,
		enum_TYPE.Integer64,
	]

# Unsigned integers
list_TYPE_UINT = [
		enum_TYPE.Unsigned8,
		enum_TYPE.Unsigned16,
		enum_TYPE.Unsigned32,
		enum_TYPE.Unsigned24,
		enum_TYPE.Unsigned40,
		enum_TYPE.Unsigned48,
		enum_TYPE.Unsigned56,
		enum_TYPE.Unsigned64,
	]

# Integers
list_TYPE_INT = list_TYPE_SINT + list_TYPE_UINT

# Reals
list_TYPE_REAL = [
		enum_TYPE.Real32,
		enum_TYPE.Real64,
	]

# Strings
list_TYPE_STRING = [
		enum_TYPE.VisibleString,
		enum_TYPE.OctetString,
		enum_TYPE.UnicodeString,
	]

# Times
list_TYPE_TIME = [
		enum_TYPE.TimeOfDay,
		enum_TYPE.TimeDifference,
	]

# Size in byte(s)
dict_SIZE_TYPE = {
		enum_TYPE.Boolean: 1,
		enum_TYPE.Integer8: 1,
		enum_TYPE.Integer16: 2,
		enum_TYPE.Integer32: 4,
		enum_TYPE.Unsigned8: 1,
		enum_TYPE.Unsigned16: 2,
		enum_TYPE.Unsigned32: 4,
		enum_TYPE.Real32: 4,
		enum_TYPE.VisibleString: -1,	# Variable length
		enum_TYPE.OctetString: -1,		# Variable length
		enum_TYPE.UnicodeString: -1,	# Variable length
		enum_TYPE.TimeOfDay: 6,
		enum_TYPE.TimeDifference: 6,
		enum_TYPE.Domain: -1,			# Specific case (currently unsupported)
		enum_TYPE.Integer24: 3,
		enum_TYPE.Real64: 8,
		enum_TYPE.Integer40: 5,
		enum_TYPE.Integer48: 6,
		enum_TYPE.Integer56: 7,
		enum_TYPE.Integer64: 8,
		enum_TYPE.Unsigned24: 3,
		enum_TYPE.Unsigned40: 5,
		enum_TYPE.Unsigned48: 6,
		enum_TYPE.Unsigned56: 7,
		enum_TYPE.Unsigned64: 8,
	}

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
