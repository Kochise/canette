#!/usr/bin/env python
# author: d.koch
# coding: utf-8
# naming: pep-0008
# typing: pep-0484
# docstring: pep-0257
# indentation: tabulation

""" canp_chan.py
	Channel
	card-CHAN-node-conf
"""

#  --- IMPORT ---

# Standard libraries (installed with python)

#import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from typing import Any
#from typing import Callable
from typing import Dict
from typing import List
#from typing import Optional
#from typing import Tuple
#from typing import Union

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

# External libraries (installed with pip, conda, setup.py, ...)

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

# Included libraries (this module, local files)

from canp_conv import canp_conv


from canp_enum import CANP_ENUM__APP_NAME

from canp_enum import CANP_ENUM__HEAD_MAIN
#from canp_enum import CANP_ENUM__HEAD_NAME

from canp_enum import CANP_ENUM__NODE_MAX
from canp_enum import CANP_ENUM__NODE_MIN

#from canp_enum import CANP_ENUM__STR_ASLASH
#from canp_enum import CANP_ENUM__STR_DOT
from canp_enum import CANP_ENUM__STR_EMPTY
#from canp_enum import CANP_ENUM__STR_SPACE

from canp_enum import CANP_ENUM__VAL_DEFAULT


from canp_node import canp_node

from canp_node import CANP_NODE__COB_NMT
from canp_node import CANP_NODE__COB_SYNC


from canp_args import canp_args
from canp_logs import canp_logs

#  --- GLOBAL ---

# Local settings (might be present in other files yet with different values)

CANP_LOG__IDX_TIME = 0
CANP_LOG__IDX_COBID = 1
CANP_LOG__IDX_DATA = 2

#  --- CLASS ---

class canp_chan:
	""" CAN channel
	"""

	# Node objects (key = node index)
	m_dict_nodes: Dict[int, Any] = {}
	# Frames analysed (key = cobid, value = {timestamp, data})
	m_dict_raws: Dict[int, Any] = {}

	# Logger object
	m_logs = canp_logs.logger(CANP_ENUM__APP_NAME).getChild("chan")

	def __init__(self,
				**i_dict_args: Any
			) -> None:
		""" Constructor
		"""
		super().__init__(**i_dict_args)

	def __getitem__(self,
				i_int_index
			) -> Any:
		""" Get at (key = node index, if present)
		"""
		l_any_ret: Any = None

		try:
			l_any_ret = self.m_dict_nodes[i_int_index]
			# - except KeyError -
		except KeyError:
			pass

		return l_any_ret

	def __len__(self):
		""" Size of (number of nodes)
			Beware, no actual node ids
		"""
		return len(self.m_dict_nodes)

	def node_list(self,
			) -> None:
		""" Node ids list
		"""
		return self.m_dict_nodes.keys()

	def node_set(self,
				i_int_node: int = 0,
				i_bool_force: bool = False
			) -> None:
		""" Node parser
		"""
		if i_int_node >= CANP_ENUM__NODE_MIN and i_int_node <= CANP_ENUM__NODE_MAX:
			# Node 0 : Broadcast
			try:
				if i_bool_force == True:
					# Overwrite node
					self.m_dict_nodes[i_int_node] = canp_node()
				else:
					# Check node
					self.m_dict_nodes[i_int_node]
					# - except KeyError -
			except KeyError:
				# Create node
				self.m_dict_nodes[i_int_node] = canp_node()
		else:
			self.m_logs.error(f"chan.node_set.node[{i_int_node}].impossible")

	def node_conf(self,
				i_int_node: int = 0,
				i_str_file: str = CANP_ENUM__STR_EMPTY
			) -> None:
		""" Conf set
		"""
		self.node_set(i_int_node)

		try:
			self.m_dict_nodes[i_int_node].conf_load(
				i_str_file)
			# - except KeyError -
		except KeyError:
			self.m_logs.error(f"chan.node_conf.node[{i_int_node}].unknown")

	def frame_parse(self,
				i_list_frame: List[Any] = [],
				i_float_time: float = 0.0,
				i_int_cobid: int = 0,
				i_any_data: bytearray = b'',
			) -> None:
		""" Frame parser
			Node should already be configured first
		"""
		# List format expected :
		# [142.844095, 897, b'\x6c\x4e\x00\x00\xfe\xff\xff\xff']
		# 0 : timestamp (float)
		# 1 : cobid (int)
		# 2 : frame (bytearray, dlc = len)
		l_bool_frame: bool = False
		l_bool_store: bool = False
		#l_int_cobid: int = 0
		l_int_node: int = 0
		l_int_dlc: int = 0

		if len(i_list_frame) >= (CANP_LOG__IDX_DATA + 1):
			# Via list
			l_bool_frame = True
			i_int_cobid = i_list_frame[CANP_LOG__IDX_COBID]
			l_int_dlc = len(i_list_frame[CANP_LOG__IDX_DATA])
		else:
			# Via args
			l_int_dlc = len(i_any_data)

		l_int_node = i_int_cobid & CANP_ENUM__NODE_MAX

		if i_int_cobid == CANP_NODE__COB_NMT and l_int_node == 0 and l_int_dlc == 2:
			# Node from frame (byte 1)
			if l_bool_frame == True:
				l_int_node = i_list_frame[CANP_LOG__IDX_DATA][1:2]
			else:
				l_int_node = i_any_data[1:2]

			# Broadcast vs Node specific
			l_int_node = canp_conv.int_bytes(
				i_bool_bytes = l_int_node)

		if (i_int_cobid == CANP_NODE__COB_NMT and l_int_node == 0 and l_int_dlc == 2) \
		or (i_int_cobid == CANP_NODE__COB_SYNC and l_int_node == 0 and l_int_dlc == 0):
			# broadcast (only existing nodes)
			# sync (emit pdo, configurable)
			for l_int_node, l_obj_node in self.m_dict_nodes.items():
				if l_bool_frame == True:
					# Via list (convenient but slightly slower)
					l_obj_node.frame_parse(
						i_list_frame = i_list_frame)
				else:
					# Via args
					l_obj_node.frame_parse(
						i_float_time = i_float_time,
						i_int_cobid = i_int_cobid,
						i_any_data = i_any_data)

			l_bool_store = True
		elif i_int_cobid == CANP_NODE__COB_SYNC and l_int_node == 0 and l_int_dlc == 0:
			# sync (emit pdo, configurable)
			self.m_logs.warning("cobid.sync")
			pass
		else:
			# Node specific
			if l_int_node >= CANP_ENUM__NODE_MIN and l_int_node <= CANP_ENUM__NODE_MAX:
				# Node 0 : Broadcast
				self.node_set(l_int_node)

				try:
					if l_bool_frame == True:
						# Via list (convenient but slightly slower)
						self.m_dict_nodes[l_int_node].frame_parse(
							i_list_frame = i_list_frame)
					else:
						# Via args
						self.m_dict_nodes[l_int_node].frame_parse(
							i_float_time = i_float_time,
							i_int_cobid = i_int_cobid,
							i_any_data = i_any_data)
					# - except KeyError -
					l_bool_store = True
				except KeyError:
					self.m_logs.error(f"chan.frame_parse.node[{l_int_node}].unknown")
			else:
				self.m_logs.error(f"chan.frame_parse.node[{l_int_node}].impossible")

		if l_bool_store == True:
			if l_bool_frame == True:
				i_any_data = i_list_frame[CANP_LOG__IDX_DATA]

			try:
				self.m_dict_raws[i_int_cobid].append((i_float_time, i_any_data))
				# - except KeyError -
			except:
				self.m_dict_raws[i_int_cobid] = [(i_float_time, i_any_data)]
				pass

			self.m_dict_raws[CANP_ENUM__VAL_DEFAULT] = i_int_cobid

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
