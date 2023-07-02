from typing import Any
import mountains as m
from gui import GUI, ui, open_popup
from functools import partial as wrap
from math import e
from nicegui import Client
from nicegui.events import KeyEventArguments
from stuff import Dict

vars: dict[str, Any] = {
	# 'tick_speed': 1e-3,
	'tick_speed': 1,  # for debugging
	'max_xp': {
		'm': lambda i, level: e ** level * 1e6 / 1e3,
	},
	'levels': {
		's': {},
		'l': {-1: 1e9},
		'm': {},
	},
	'xp_showing': 's',
	# 'zero': 1e-9,
}
default = {
	'vol': -1,
	'xp': {
		's': 999.999,
		'l': -1.1,
		'm': 0,
	},
}

def json_filter(folder: str = '.') -> None:
	import glob, json, os
	for file in glob.glob(folder + '*.json'):
		try:
			with open(file, 'r') as f:
				json.load(f)
		except json.decoder.JSONDecodeError:
			os.remove(file)
def get_level(xp_showing: str, xp: dict[str, int], process=False) -> int | str:
	level = int(xp[xp_showing])
	if process and level < 0:
		return ''
	return int(xp[xp_showing])
def get_xp(vars: Dict, xp: dict[str, int]) -> float:
	return abs(xp[vars.xp_showing]) % 1
def gain_xp(vol: 'str', i: GUI, xp: int = 1) -> None:
	'increment xp by 1 / xp required to level up'
	level = get_level(i.vars.xp_showing, i.user.xp)
	# if xp required to level up has not been calculated, calculate
	if level not in i.vars.levels[vol]:
		i.vars.levels[vol][level] = i.vars.max_xp[vol](level)
	# increment xp
	i.user.xp[vol] += xp / i.vars.levels[vol][level]
	# # update bar
	# i.elms.xp.set_value(get_xp(vol, i.user.xp))
	# i.elms.xp.text.set_text(get_level(vol, i.user.xp))
def handle_key(i: GUI, e: KeyEventArguments):
	if e.modifiers.ctrl and e.action.repeat and e.key == 'c':
		print('resetting progress')
		i.user.update(default)
@ui.page('/')
async def main(client: Client) -> None:
	i = GUI(vars, default)
	await client.connected()
	# print(Fore.BLUE, getframeinfo(currentframe()).filename.split('\\')[-1], getframeinfo(currentframe()).lineno, Fore.RESET)  # type: ignore

	if i.user.vol == -1:
		# print(Fore.BLUE, getframeinfo(currentframe()).filename.split('\\')[-1], getframeinfo(currentframe()).lineno, Fore.RESET)  # type: ignore
		await open_popup(i.elms.pop, m.story_0, 'Okay?')
		# await i.elms.pop.but1.clicked()
		# i.elms.pop.close()
		await i.elms.pop
		i.user.vol = 0

	# print(Fore.BLUE, getframeinfo(currentframe()).filename.split('\\')[-1], getframeinfo(currentframe()).lineno, Fore.RESET)  # type: ignore
	i.set_vol_0()
	# print(Fore.BLUE, getframeinfo(currentframe()).filename.split('\\')[-1], getframeinfo(currentframe()).lineno, Fore.RESET)  # type: ignore
	if i.user.vol == 0: vol_0(i)

	# print(Fore.BLUE, getframeinfo(currentframe()).filename.split('\\')[-1], getframeinfo(currentframe()).lineno, Fore.RESET)  # type: ignore

def vol_0(i: GUI) -> None:
	# print(Fore.BLUE, getframeinfo(currentframe()).filename.split('\\')[-1], getframeinfo(currentframe()).lineno, Fore.RESET)  # type: ignore
	i.elms.ticker = ui.timer(i.vars.tick_speed, wrap(gain_xp, i.vars.xp_showing, i))


if __name__ in {"__main__", "__mp_main__"}:
	# for debugging
	import tracemalloc, colorama
	tracemalloc.start()
	from inspect import currentframe, getframeinfo
	from colorama import just_fix_windows_console, Fore
	just_fix_windows_console()
	# end debugging
	# print(Fore.RED, '--------------------------------------------STARTING--------------------------------------------', Fore.RESET)
	json_filter('.nicegui/')
	ui.run(dark=True, storage_secret='secret')
	ui.open(main)
	# print(Fore.BLUE, getframeinfo(currentframe()).filename.split('\\')[-1], getframeinfo(currentframe()).lineno, Fore.RESET)  # type: ignore
