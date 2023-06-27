import asyncio
from nicegui import app, ui
from stuff import Binder, Dict, wrap

class GUI():
	def __init__(i, vars: dict, init: dict) -> None:
		from main import get_level, get_xp, handle_key
		# setup "variables"
		i.vars = Dict(vars)
		i.user = Binder(app.storage.user)
		i.user.update(init, overwrite=False)

		# setup ui element holder
		i.elms = Dict({
			'key': ui.keyboard(on_key=wrap(handle_key, i))
		})
		# add maxed out xp bar and label
		with ui.row().classes('w-full'):
			with ui.column().classes('w-1/2'):
				i.elms.level = ui.label()
				with ui.linear_progress(size='20px', show_value=False).props('instant-feedback').classes('w-1/2').bind_value_from(i.user._target, 'xp', wrap(get_xp, i.vars.xp_showing)) as i.elms.xp:
					i.elms.xp.text = ui.label().classes('absolute-center text-sm text-white').bind_text_from(i.user._target, 'xp', wrap(get_level, i.vars.xp_showing))
			with ui.column():
				ui.label().bind_text_from(i.user._target, 'xp', wrap(get_level, i.vars.xp_showing))
				ui.label().bind_text_from(i.user._target, 'xp', wrap(get_xp, i.vars.xp_showing))
		# setup popup
		with ui.dialog().props('persistent') as i.elms.pop, ui.card():
			i.elms.pop.text = ui.label('')
			i.elms.pop.but = ui.button('', on_click=i.elms.pop.close)
	def set_stage_0(i) -> None:
		i.elms.level.set_text('Saana Online:')
		i.elms.xp.text.set_text('999')
	def open_popup(i, text: str, but: str) -> None:
		'sets the text of label and button then opens the popup'
		i.elms.pop.text.set_text(text)
		i.elms.pop.but.set_text(but)
		i.elms.pop.open()
	def set_stage_1(i) -> None:
		i.elms.level.set_text('Literature:')
		i.elms.xp.text.set_text('')
		i.vars.xp_showing = 'l'
	def set_stage_2(i) -> None:
		pass


# def tmp(i, num):
# 	print('-------------------------------------------------------')
# 	print(num)
# 	print(i.vars.xp_showing)
# 	print(num[i.vars.xp_showing] % 1)
# 	print('-------------------------------------------------------')
# 	return (num[i.vars.xp_showing] - i.vars.zero) % 1

# def tmp2(i, num):
# 	print(num, i.vars.tmp, int(num[i.vars.tmp]))
# 	return int(num[i.vars.tmp])
