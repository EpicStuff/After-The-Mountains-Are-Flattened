import mountains as m, math
from gui import GUI, app, ui
from stuff import wrap

consts = {
	'tick_speed': .01,
	'xp': lambda level: math.e ** level * 100000 / 10000,
	'levels': {},
}

@ui.page('/')
async def main() -> None:
	gui = GUI()
	if gui.data['stage'] == 0: await stage0(gui)
	if gui.data['stage'] == 1: await stage1(gui)

async def stage0(gui) -> None:
	gui.dialog(m.story0, 'Okay')
	await gui.elms.pop.but.clicked()
	gui.data['stage'] = 1
	gui.data['xp'] = gui.data['level'] = 0
async def stage1(gui) -> None:
	gui.stage1()
	ui.timer(consts['tick_speed'], wrap(gain_xp, gui))
def gain_xp(gui) -> None:
	# if xp required to level up has not been calculated, calculate
	if gui.data['level'] not in consts['levels']:
		consts['levels'][gui.data['level']] = consts['xp'](gui.data['level'])
	gui.data['xp'] += 1 / consts['levels'][gui.data['level']]
	# if should level up
	if gui.data['xp'] > 1:
		gui.data['level'] += 1
		gui.data['xp'] = 0
		gui.elms.xp.text.set_text(gui.data['level'])
	gui.elms.xp.set_value(gui.data['xp'])

	# gui.data['xp'] += 1
	# if gui.data['xp'] > 100:
	# 	# gui.data['level'] += 1
	# 	gui.data['xp'] = 0
	# 	gui.elms.xp.text.set_text(gui.data['level'])
	# tmp = gui.data['xp'] / 100
	# gui.elms.xp.set_value(gui.data['xp'] / 100)


if __name__ in {"__main__", "__mp_main__"}:
	import tracemalloc, glob, json, os
	tracemalloc.start()

	for file in glob.glob('.nicegui/*.json'):
		try:
			with open(file, 'r') as f:
				json.load(f)
		except json.decoder.JSONDecodeError:
			os.remove(file)

	ui.run(dark=True, storage_secret='test')
	ui.open(main)
