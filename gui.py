from typing import Any, Optional
from nicegui import app, ui
from stuff import Dict
from functools import partial as wrap

from inspect import currentframe, getframeinfo
from colorama import Fore

class GUI():
	def __init__(i, vars: dict[str, Any], init: dict[str, Any]) -> None:
		from main import get_level, get_xp, handle_key
		# setup "variables"
		i.vars = Dict(vars)
		i.user = Dict(app.storage.user)
		i.user.update(init, overwrite=False)
		# setup ui element holder
		i.elms = Dict({
			'key': ui.keyboard(on_key=wrap(handle_key, i)),
			'xp': Dict(),
			'pop': Dict()
		})
		# body
		with ui.row().classes('w-full'):
			# left side
			with ui.column().classes('w-8/12'):
				with ui.card().props('square flat').classes('w-full flex-row flex-nowrap'):
					i.elms.xp.label = ui.label('Saana Online:').classes('flex-none')
					# xp bar
					with ui.linear_progress(size='20px', show_value=False).props('instant-feedback') as i.elms.xp.bar:
						i.elms.xp.bar.bind_value_from(i.user._target, 'xp', wrap(get_xp, i.vars))  # bind bar to xp value
						i.elms.xp.text = ui.label().classes('absolute-center text-sm text-white').bind_text_from(i.user._target, 'xp', lambda xp: get_level(i.vars.xp_showing, xp, True))
			# right side
			with ui.column().classes('w-3/12'):
				# stats box
				with ui.card().props('square flat').classes(('w-96 h-96')) as i.elms.stats:
					ui.label('character:')  # .set_visibility(False)
					ui.label('Class: None')
				# events box
				with ui.card().props('square flat').classes(('w-96 h-96')) as i.elms.events:
					ui.label('Events:')
					ui.separator()
				# quests box
				with ui.card().props('square flat').classes(('w-96 h-96')) as i.elms.quests:
					ui.label('Quests:')
					ui.separator()
				# dream fragments box
				with ui.card().props('square flat').classes(('w-96 h-96')) as i.elms.dreams:
					ui.label('Dream Fragments:')
					ui.separator()
		# setup popup
		with ui.dialog().props('persistent') as i.elms.pop, ui.card():
			i.elms.pop.text = ui.label('')
			i.elms.pop.but1 = ui.button('', on_click=wrap(i.elms.pop.submit, 1))
			i.elms.pop.but2 = ui.button('', on_click=wrap(i.elms.pop.submit, 0))
	def set_vol_0(i) -> None:
		i.elms.xp.label.set_text('Literature:')
		i.vars.xp_showing = 'l'
		# hiding not yet unlocked boxes
		i.elms.stats.set_visibility(False)
		i.elms.events.set_visibility(False)
		i.elms.quests.set_visibility(False)
		i.elms.dreams.set_visibility(False)
	def set_vol_1(i) -> None:
		pass

async def open_popup(pop: ui.dialog, text: str, but1: str, but2: Optional[str] = None) -> Any:
	'sets the text of label and button then opens the popup'
	pop.text.set_text(text)
	pop.but1.set_text(but1)
	# if second button is wanted
	if but2 is not None:
		pop.but2.set_text(but2)
		pop.but2.set_visibility(True)
	else:
		pop.but2.set_visibility(False)
	pop.open()
	return await pop
