from functools import partial as wrap
from nicegui import ui
from gui import GUI, gain_xp

class Task():
	def __init__(self, i: GUI, name: str, diff: str = 'normal', rate: str = 'exp') -> None:
		# setup vars
		self.name, self.diff, self.rate, self.tick_speed, self.i = name, diff, rate, i.vars.tick_speed, i
		self.xp = 0
		self.timer = ui.timer(self.tick_speed, self.tick)
		# create gui elements
		with ui.row().classes('w-full flex-row flex-nowrap'):
			ui.label(name)
			with ui.linear_progress(size='20px', show_value=False).props('instant-feedback') as self.bar:
				ui.label().bind_text_from(self, 'xp', int).classes('absolute-center text-sm text-white')
			ui.label('+ 001').classes('flex-none')
		# calculate xp required
		self.calc_xp()
	def calc_xp(self) -> None:
		if self.rate == 'const':
			if self.diff == 'easy':
				self.xp_required = 10 / self.tick_speed
				return
		assert False, 'not yet implemented'
	def tick(self) -> None:
		'runs every tick'
		level = int(self.xp)
		self.xp += gain_xp(self.xp_required, self.bar)
		# if level up
		if int(self.xp) != level:
			self.effect()
			self.calc_xp()
	def effect(self) -> None:
		if self.name == 'Revisiting <i>Infinite Leaves</i>':
			gain_xp(self.i.vars.xp_required['literature'], None, self.i.user.xp, 'literature')  # for debugging
			# gain_xp(self.i.vars.xp_required['literature'], None, self.i.user.xp, 'literature', xp=5e7)


story_0 = 'Having finally surmounted the mountain that was Saana Online, the climber may now finally retire at the age of 17 to pursue what really matters. The climb that is the all-encompassing, all-synthesizing exploration of the world of literatu—'
events = {
	'The Card': {
		'title': 'The Card:',
		'text': '''
			"holy crap just agree already!!!! what's taking so long!! here’s the deal: if u get 1st in the 1v1, i won’t pull that card again."\n
			The card, the climber's attention honed in on this.\n
			The card!\n
			What was the card? Long ago the frenemy had helped his family out in a massive way when the climber's mother had fallen ill. Since then, it'd been reminders of this favour that'd motivated the climber to put up with the frenemy's nonsense.\n
			In a way, the card was the last thing binding them together. Once it was removed, it'd really be over...the climber would be retired for good.\n
			So that was tonight's wager: first place in his own recruitment tournament in exchange for eternal freedom, the warm bliss that lay beyond the mountain's frosty slopes.\n
			The climber, leaned back to contemplate the offer while, across from him, his long-time comrade feigned indifference sawing through a piece of pork.\n
			The Card...\n
			The Card...the Car—\n
		''',
		'buttons': ['It was only two weeks, Deal!', 'Isnt\'t this underhanded scheming too much?'],
	},
}
quests = {
	'The Card': {
		'title': 'Accept The Challenge: (tmp, probably)',
		'text': 'The Climber\'s frenemy has proposed a challenge. Accept it so the story my continue .',
		'buttons': ['Fine', 'Not Doing'],
	},
}
insights = {
	'Wu Wei': {
		'title': 'Wu Wei:',
		'text': '''
			What had the climber ever done to deserve this treatment? Had it really been too much to ask for a 17-year-old man to retire quietly in peace? Had he not put in enough work for one lifetime?\n
			It seemed so silly to him.\n
			Recently, in the spirit of retirement, he'd been doing much reading about his new non-vocation. The greatest insights had come from the bearded philosophers of ancient China, who'd captured the essence of quitting perfectly with the principle of Wu-Wei, or non-doing.\n
			Non-doing, one might argue that this was the secret spice to all human advancement. Just as the life of an individual required offsetting its more active, doing parts with more restful, non-doing parts to maintain a functional balance, so too might this greater life which we call civilization require offsetting its more active, doing people with more restful, non-doing people. Man was a creature of comparison, and without the low achiever, could anyone truly be a high achiever? Behind every great man of action, the climber would assert there was another man—much less great but no less important—a man of inaction, a man whose inert, flabby example terrified the great man and drove him to strive on to ever-higher altitudes. And who were we, the non-doers, to strip this great man of his vital motivation? Ask yourself, if the next Einstein walked through the door right now, would you deny him his potential? Henry could never be so selfish. For the greater good of society, he would leap in front of the lazy bullet. He would sacrifice himself by becoming one of those men who dare, boldly, to do nothing. As for his great man, he could be any one of the souls brimming with untapped potential around him - he could be the waiter, he could be an anonymous diner, and, why of course, he could even be you.\n
\n
			Effect: tick speed multiplier\n
		''',
	},
}
