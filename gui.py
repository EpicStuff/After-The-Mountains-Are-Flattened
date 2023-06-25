import asyncio
from typing import Callable
from nicegui import app, ui
class GUI():
	def __init__(self) -> None:
		# setup storage
		self.data = app.storage.user
		if 'stage' not in self.data: self.data['stage'] = 0
		# setup ui elements
		self.elms = type('Holder', (), {
			'pop': ui.dialog()
		})()
		with self.elms.pop, ui.card():
			self.elms.pop.text = ui.label('')
			self.elms.pop.but = ui.button('', on_click=self.elms.pop.close)
	def dialog(self, text: str, but: str) -> None:
		self.elms.pop.text.set_text(text)
		self.elms.pop.but.set_text(but)
		self.elms.pop.open()
	def stage1(self) -> None:
		with ui.row().classes('w-full'):
			self.elms.level = ui.label('Level:')
			with ui.linear_progress(self.data['xp'], size='20px', show_value=False).props('instant-feedback').classes('w-1/2') as self.elms.xp:
				self.elms.xp.text = ui.label(self.data['level']).classes('absolute-center text-sm text-white')


async def delay(func: Callable, secs: int) -> None:
	await asyncio.sleep(secs)
	func()
