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
def handle_key(i: GUI, e: KeyEventArguments):
	if e.modifiers.ctrl and e.action.repeat and e.key == 'c':
		print('resetting progress')
		i.user.update(default)
@ui.page('/')
async def main(client: Client) -> None:
	i = GUI(vars, default)
	await client.connected()

	if i.user.vol == -1:
		await open_popup(i.elms.pop, m.story_0, 'Okay?')
		i.user.vol = 0

	i.set_vol_0()
	if i.user.vol == 0: vol_0(i)


def vol_0(i: GUI) -> None:
	i.elms.ticker = ui.timer(i.vars.tick_speed, wrap(gain_xp, i.vars.xp_showing, i))


if __name__ in {"__main__", "__mp_main__"}:
	# for debugging
	import tracemalloc
	tracemalloc.start()
	json_filter('.nicegui/')

	ui.run(dark=True, storage_secret='secret')
	ui.open(main)
