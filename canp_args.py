#!/usr/bin/env python
# author: d.koch
# coding: utf-8
# naming: pep-0008
# typing: pep-0484
# docstring: pep-0257
# indentation: tabulation

""" canp_args.py
	Arguments
"""

#  --- IMPORT ---

# Standard libraries (installed with python)

#import enum
#import logging
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

#from canp_enum import CANP_ENUM__HEAD_MAIN
CANP_ENUM__HEAD_MAIN = "__main__"

#  --- GLOBAL ---


#  --- CLASS ---

class canp_args:
	""" CAN arguments
	"""

	@staticmethod
	def dispatch(
				i_list_args: List[str] = sys.argv,
				i_list_globals: List[str] = globals(),
			) -> None:
		""" Args dispatcher
		"""
		if len(i_list_args) > 1:
			# 'function'(args)
			i_list_globals[i_list_args[1]](*i_list_args[2:])
		else:
			if True:
				# '__main__'()
				i_list_globals[CANP_ENUM__HEAD_MAIN]()
			else:
				# 'filename'()
				l_str_name = os.path.splitext(os.path.split(i_list_args[0])[1])[0]
				i_list_globals[l_str_name]()
				#ASYNC_RUN(i_list_globals[l_str_name](), debug = True)

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
