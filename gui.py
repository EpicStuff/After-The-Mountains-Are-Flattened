import mountains as m
from typing import Any, Optional, Callable
from nicegui import app, ui
from stuff import Dict
from functools import partial as wrap

from inspect import currentframe, getframeinfo
from colorama import Fore

class GUI():
	def __init__(i, vars: dict[str, Any], init: dict[str, Any]) -> None:
		from main import get_level, get_xp
		# setup "variables"
		i.vars = Dict(vars)
		i.user = Dict(app.storage.user)
		i.user.update(init, overwrite=False)
		# setup ui element holder
		i.elms = Dict({
			'xp': Dict(),
			'pop': Dict()
		})
		# body
		with ui.row().classes('w-full flex-row'):
			# left side
			with ui.column().classes('w-8/12'):
				with ui.card().props('square flat').classes('w-full flex-row flex-nowrap'):
					i.elms.xp.label = ui.label('Saana Online:').classes('flex-none')
					# xp bar
					with ui.linear_progress(size='20px', show_value=False).props('instant-feedback') as i.elms.xp.bar:
						i.elms.xp.bar.bind_value_from(i.user._target, 'xp', wrap(get_xp, i.vars))  # bind bar to xp value
						i.elms.xp.text = ui.label().classes('absolute-center text-sm text-white').bind_text_from(i.user._target, 'xp', lambda xp: get_level(i.vars.xp_showing, xp, True))
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
		with ui.dialog().props('persistent') as i.elms.pop, ui.card():
			i.elms.pop.title = ui.label('')
			ui.separator().bind_visibility_from(i.elms.pop.title, 'visible')
			i.elms.pop.text = ui.label('')
			with ui.row():
				i.elms.pop.but1 = ui.button('', on_click=wrap(i.elms.pop.submit, 1)).props('no-caps')
				i.elms.pop.but2 = ui.button('', on_click=wrap(i.elms.pop.submit, 0)).props('no-caps')
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
				i.vars.events[name] = (wrap(i.elms.events.remove, container)), ui.button('View').props('size="xs"').style('margin-left: auto; margin-right: 0;')  # , on_click=wrap(i.elms.events.remove, card))
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
				i.vars.quests[name] = wrap(i.elms.quests.remove, container), ui.button('View').props('size="xs"').style('margin-left: auto; margin-right: 0;')
	async def view_event(i, name: str) -> int:
		open_popup(i.elms.pop, m.events[name]['text'], m.events[name]['buttons'][0], m.events[name]['buttons'][1], m.events[name]['title'])
		return await i.elms.pop
	async def view_quest(i, name: str) -> int:
		open_popup(i.elms.pop, m.quests[name]['text'], m.quests[name]['buttons'][0], m.quests[name]['buttons'][1], m.quests[name]['title'])
		return await i.elms.pop
	async def view_insight(i, name: str) -> None:
		open_popup(i.elms.pop, m.insights[name]['text'], 'Close', title=m.insights[name]['title'])
		await i.elms.pop
	def set_vol_0(i) -> None:
		'setup gui for vol 0'
		i.user.vol = 0
		# hiding not yet unlocked boxes
		i.user.stats_unlocked = False
		i.user.events_unlocked = False
		i.user.quests_unlocked = False
		i.user.insights_unlocked = False
		i.user.dreams_unlocked = False
	def set_vol_1(i) -> None:
		'setup gui for vol 0'
		i.user.vol = 1

def open_popup(pop: ui.dialog, text: str, but1: str, but2: Optional[str] = None, title: Optional[str] = None) -> None:
	'sets up the popup to be opened'
	pop.text.set_text(text)
	pop.but1.set_text(but1)
	# if second button is wanted
	if but2 is not None:
		pop.but2.set_text(but2)
		pop.but2.set_visibility(True)
	else:
		pop.but2.set_visibility(False)
	# if title is wanted
	if title is not None:
		pop.title.set_text(title)
		pop.title.set_visibility(True)
	else:
		pop.title.set_visibility(False)
