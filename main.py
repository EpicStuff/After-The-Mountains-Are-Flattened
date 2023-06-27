import mountains as m
from gui import GUI, ui
from stuff import e, wrap, KeyEventArguments

vars = {
	'tick_speed': 1e-3,
	# 'tick_speed': 1,  # for debugging
	'max_xp': lambda i, level: e ** level * 1e6 / 1e3,
	'levels': {
		's': {999: 1e9},
	},
	'xp_showing': 's',
	# 'zero': 1e-9,
}
default = {
	'stage': 0,
	'xp': {
		's': 999.999,
		'l': 1 / 10,
		'm': 0,
	},
}

def json_filter(folder='.') -> None:
	import glob, json, os
	for file in glob.glob(folder + '*.json'):
		try:
			with open(file, 'r') as f:
				json.load(f)
		except json.decoder.JSONDecodeError:
			os.remove(file)
def get_level(xp: dict, stage: 'str') -> int | str:
	return int(xp[stage]) if int(xp[stage]) != 0 else ''
def get_xp(stage: 'str', xp: dict) -> float:
	return xp[stage] % 1
def gain_xp(stage: 'str', i: GUI) -> None:
	'increment xp by 1 / xp required to level up'
	level = get_level(i.user.xp, stage)
	# if xp required to level up has not been calculated, calculate
	if level not in i.vars.levels[stage]:
		i.vars.levels[stage][level] = i.vars.max_xp[stage](level)
	# increment xp
	i.user.xp[stage] += 1 / i.vars.levels[stage][level]
def handle_key(i: GUI, e: KeyEventArguments):
	if e.modifiers.ctrl and e.action.repeat and e.key == 'c':
		print('resetting progress')
		i.user.update(default)
@ui.page('/')
async def main() -> None:
	i = GUI(vars, default)

	i.set_stage_0()
	if i.user.stage == 0: await stage_0(i)

	i.set_stage_1()
	if i.user.stage == 1: await stage_1(i)

async def stage_0(i: GUI) -> None:
	# open popup
	i.open_popup(m.story_0, 'Okay?')
	# wait for button to be clicked
	await i.elms.pop.but.clicked()
	i.user.stage = 1
	i.user.level = ''
	i.user.xp = 1 / 5
async def stage_1(i: GUI) -> None:
	i.elms.ticker = ui.timer(i.vars.tick_speed, wrap(gain_xp, i, i.vars.xp_showing))


if __name__ in {"__main__", "__mp_main__"}:
	# import tracemalloc; tracemalloc.start()
	json_filter('.nicegui/')
	ui.run(dark=True, storage_secret='secret')
	ui.open(main)
