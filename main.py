import mountains as m, random, asyncio
from typing import Any
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
	'events': {},
	'quests': {},
	'insights': {},
}
default = {
	'vol': -1,
	'xp': {
		's': 999.999,
		'l': -1.1,
		'm': 0,
	},
	'stats_unlocked': True,
	'events_unlocked': True,
	'events': {},
	'quests_unlocked': True,
	'quests': {},
	'insights_unlocked': True,
	'insights': {},
	'dreams_unlocked': True,
	'dreams': {},
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
@ui.page('/')
async def main(client: Client) -> None:
	i = GUI(vars, default)
	await client.connected()

	if i.user.vol == -1:
		open_popup(i.elms.pop, m.story_0, 'Okay?')
		await i.elms.pop
		i.set_vol_0()

	if i.user.vol == 0:
		await vol_0(i)


async def vol_0(i: GUI) -> None:
	# setup vars for vol 0
	i.elms.xp.label.set_text('Literature:')
	i.vars.xp_showing = 'l'
	# if 'The Card' event has not been activated, activate in 5-10 seconds
	if 'The Card' not in i.user.events and 'The Card' not in i.user.quests:
		# await asyncio.sleep(random.randint(5, 10))
		await asyncio.sleep(1)  # for debugging
		i.new_event('The Card')
	# if the player has not yet viewed The Card event
	if 'The Card' in i.user.events:
		# wait for user to click The Card event and get response
		await i.vars.events['The Card'][1].clicked()
		ans = await i.view_event('The Card')
		# remove The Card event
		i.vars.events['The Card'][0]()
		del i.user.events['The Card']
		# if user clicked yes
		if ans:
			# start vol 1
			i.set_vol_1()
			return
		# if user clicked no: add The Card quest and Wu Wei insight
		i.new_quest('The Card')
		i.new_insight('Wu Wei')
		await i.view_insight('Wu Wei')
	# wait for user to click The Card quest and get response, repeat till user clicks yes
	while True:
		await i.vars.quests['The Card'][1].clicked()
		ans = await i.view_quest('The Card')
		# if user clicked yes
		if ans:
			# remove quest and start vol 1
			i.vars.quests['The Card'][0]()
			del i.user.quests['The Card']
			return
		# if user clicked no: close popup (do nothing)


if __name__ in {"__main__", "__mp_main__"}:
	# for debugging
	import tracemalloc
	tracemalloc.start()
	json_filter('.nicegui/')

	ui.run(dark=True, storage_secret='secret')
	ui.open(main)
