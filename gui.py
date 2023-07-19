from multiprocessing import process
import mountains as m
from typing import Any, MutableMapping
from nicegui import app, ui
from stuff import Dict
from functools import partial as wrap


class GUI():
	def __init__(i, vars: dict[str, Any], init: dict[str, Any]) -> None:
		# setup "variables"
		i.vars = Dict(vars)
		i.user = Dict(app.storage.user)
		i.user.update(init, overwrite=False)
		# setup ui element holder
		i.elms = Dict({
			'xp': Dict(),
			'diag': Dict(),
		})
		# body
		with ui.row().classes('w-full h-full flex-row'):
			# left side
			with ui.column().classes('w-8/12'):
				# xp box
				with ui.card().props('square flat').classes('w-full flex-row flex-nowrap'):
					i.elms.xp.label = ui.label('Saana Online:')
					# xp bar
					with ui.linear_progress(1, size='20px', show_value=False).props('instant-feedback') as i.elms.xp.bar:
						i.elms.xp.text = ui.label('999').classes('absolute-center text-sm text-white')
				# task box
				with ui.card().props('square flat').classes('w-2/3') as i.elms.tasks:
					ui.label('Skills:')
					ui.separator()
			# right side
			with ui.column().classes('flex-grow flex-col'):
				# stats box
				with ui.card().props('square flat').classes(('w-full shrink')).bind_visibility_from(i.user._target, 'stats_unlocked') as i.elms.stats:
					ui.label('character:')  # .set_visibility(False)
					ui.label('Class: None')
				# events box
				with ui.card().props('square flat').classes(('w-full shrink')).bind_visibility_from(i.user._target, 'events_unlocked') as i.elms.events:
					ui.label('Events:')
					ui.separator()
				# quests box
				with ui.card().props('square flat').classes(('w-full shrink')).bind_visibility_from(i.user._target, 'quests_unlocked') as i.elms.quests:
					ui.label('Quests:')
					ui.separator()
				# insights box
				with ui.card().props('square flat').classes(('w-full shrink')).bind_visibility_from(i.user._target, 'insights_unlocked') as i.elms.insights:
					ui.label('Insights:')
					ui.separator()
				# dream fragments box
				with ui.card().props('square flat').classes(('w-full shrink')).bind_visibility_from(i.user._target, 'dreams_unlocked') as i.elms.dreams:
					ui.label('Dream Fragments:')
					ui.separator()
		# setup popup
		with ui.dialog().props('persistent') as i.elms.diag.container, ui.card():
			i.elms.diag.title = ui.label('')
			ui.separator().bind_visibility_from(i.elms.diag.title, 'visible')
			i.elms.diag.text = ui.column()
			with ui.row():
				i.elms.diag.but1 = ui.button('', on_click=wrap(i.elms.diag.container.submit, 1)).props('no-caps')
				i.elms.diag.but2 = ui.button('', on_click=wrap(i.elms.diag.container.submit, 0)).props('no-caps')
		# (re)add events
		for event in i.user.events:
			i.new_event(event)
		# (re)add quests
		for quest in i.user.quests:
			i.new_quest(quest)
		# (re)add insights
		for insight in i.user.insights:
			i.new_insight(insight)
	def new_event(i, name: str) -> None:
		i.user.events[name] = 1
		# if first event unlocked
		if not i.user.events_unlocked:
			i.user.events_unlocked = True
		with i.elms.events:
			with ui.row().classes('w-full') as container:
				ui.label(name)
				i.vars.events[name] = (wrap(i.elms.events.remove, container)), ui.button('View').props('square size="xs"').style('margin-left: auto; margin-right: 0;')  # , on_click=wrap(i.elms.events.remove, card))
	def new_insight(i, name: str) -> None:
		i.user.insights[name] = 0
		# if first insight unlocked
		if not i.user.insights_unlocked:
			i.user.insights_unlocked = True
		with i.elms.insights:
			with ui.row().classes('w-full flex-row flex-nowrap'):
				ui.label(name).classes('flex-none')
				i.vars.insights[name] = ui.linear_progress().props('instant-feedback')
	def new_quest(i, name: str) -> None:
		i.user.quests[name] = 1
		# if first quest unlocked
		if not i.user.quests_unlocked:
			i.user.quests_unlocked = True
		with i.elms.quests:
			with ui.row().classes('w-full') as container:
				ui.label(name)
				i.vars.quests[name] = wrap(i.elms.quests.remove, container), ui.button('View').props('square size="xs"').style('margin-left: auto; margin-right: 0;')
	async def view_event(i, name: str) -> int:
		open_popup(i.elms.diag, m.events[name]['text'], m.events[name]['buttons'][0], m.events[name]['buttons'][1], m.events[name]['title'])
		return await i.elms.diag.container
	async def view_quest(i, name: str) -> int:
		open_popup(i.elms.diag, m.quests[name]['text'], m.quests[name]['buttons'][0], m.quests[name]['buttons'][1], m.quests[name]['title'])
		return await i.elms.diag.container
	async def view_insight(i, name: str) -> None:
		open_popup(i.elms.diag, m.insights[name]['text'], 'Close', title=m.insights[name]['title'])
		await i.elms.diag.container
	def set_vol_0(i) -> None:
		'setup gui for vol 0'
		# setup writing task
		with i.elms.tasks:
			i.vars.tasks['Writing'] = m.Task(i, 'Revisiting <i>Infinite Leaves</i>', 'easy', 'const')
		# setup vars for vol 0
		i.elms.xp.label.set_text('Literature:')
		# binding bars
		i.elms.xp.text.bind_text_from(i.user._target, 'xp', wrap(get_level, 'literature', process=True))
		i.elms.xp.bar.bind_value_from(i.user._target, 'xp', wrap(get_xp, 'literature'))  # bind bar to xp value

	def set_vol_1(i) -> None:
		'setup gui for vol 0'
		i.user.vol = 1

def open_popup(diag: Dict, text: str, but1: str, but2: str | None = None, title: str | None = None) -> None:
	'sets up the popup to be opened'
	# clear the popup text container
	diag.text.clear()
	with diag.text:
		# add separate label for each line of text
		for line in text.split('\n'):
			ui.label(line)
	diag.but1.set_text(but1)
	# if second button is wanted
	if but2 is not None:
		diag.but2.set_text(but2)
		diag.but2.set_visibility(True)
	else:
		diag.but2.set_visibility(False)
	# if title is wanted
	if title is not None:
		diag.title.set_text(title)
		diag.title.set_visibility(True)
	else:
		diag.title.set_visibility(False)

def gain_xp(xp_required: int, bar: ui.linear_progress | None = None, data: MutableMapping | None = None, key: str | None = None, xp: float = 1) -> float:
	'increment xp by 1 / xp required to level up'
	assert bar or data and key, 'either bar or data and key must be provided'
	# convert xp to fraction of xp required
	xp = xp / xp_required
	# increment xp [bar or data]
	if bar:
		bar.value = get_xp(0, (bar.value + xp,))
	elif data:
		data[key] += xp
	# return xp
	return xp

def get_level(key: str | int, data, process: bool = False) -> int | str:
	level = int(data[key])
	if process and level == 0:
		return ''
	return level
def get_xp(key: str, data: MutableMapping) -> float:
	return abs(data[key]) % 1
