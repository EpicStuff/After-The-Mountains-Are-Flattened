from typing import Any, Callable, Mapping, MutableMapping
from functools import partial as wrap
from math import e
from nicegui.events import KeyEventArguments
class Binder():
	def __init__(self, target: MutableMapping) -> None:
		self._target = target
	def __getattr__(self, __name: str) -> Any:
		if __name[0] == '_':
			return super().__getattribute__(__name)
		else:
			return self._target[__name]
	def __setattr__(self, __name: str, __value: Any) -> None:
		if __name[0] == '_':
			super().__setattr__(__name, __value)
		else:
			self._target[__name] = __value
	def __contains__(self, __key: object) -> bool:
		return self._target.__contains__(__key)
	def update(self, __map: Mapping = {}, overwrite=True, **kwargs) -> None:
		if overwrite:
			self._target.update(__map | kwargs)
		else:
			for key, value in (__map | kwargs).items():
				self._target.setdefault(key, value)
class Dict(dict):
	def __init__(self, __map: Mapping = {}, **kwargs) -> None:
		self.__dict__.update(__map | kwargs)
	def __repr__(self) -> str:
		return self.__dict__.__repr__()