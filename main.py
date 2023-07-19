import mountains as m, random, asyncio
from typing import Any, Callable
from gui import GUI, ui, open_popup
from functools import partial as wrap
from math import e
from nicegui import Client
from nicegui.events import KeyEventArguments
from stuff import Dict


default = {
	'vol': -1,
	'xp': {
		'saana': 999.999,
		'literature': 0.1,
		'martial': 0,
	},
	'tasks': {'Writing': 0},
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
vars = {
	'tick_speed': 1e-3,
	# 'tick_speed': 1,  # for debugging
	'xp_required': {  # xp required to level up, level: xp_required
		'literature': 1e9,
		'martial': 0,
	},
	'tasks': {},
	'events': {},
	'quests': {},
	'insights': {},
}
equations = {
	'xp_required': {
		'martial': lambda i, level: e ** level * 1e6 / 1e3,
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
@ui.page('/')
async def main(client: Client) -> None:
	i = GUI(vars, default)
	await client.connected()

	if i.user.vol == -1:
		# open then wait for into popup
		open_popup(i.elms.diag, m.story_0, 'Okay?')
		await i.elms.diag.container
		# hiding not yet unlocked boxes
		i.user.stats_unlocked = i.user.events_unlocked = i.user.quests_unlocked = i.user.insights_unlocked = i.user.dreams_unlocked = False
		# set vol to 0
		i.user.vol = 0

	if i.user.vol == 0:
		# setup gui for vol 0
		i.set_vol_0()
		await vol_0(i)


async def vol_0(i: GUI) -> None:
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
