# -*- coding: utf-8 -*-
# Copyright: Olivier Binda <olivier.binda@wanadoo.fr>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# ---------------------------------------------------------------------------
# This file is a plugin for the "anki" flashcard application http://repose.cx/anki/
# ---------------------------------------------------------------------------
Jx__Entry_Source_Target__Default = [
(u"Word recall",u"""D:%(Reading)s""",u"""${Css}<div style="float:left"><div>${W:JLPT}</div><div>${W:Freq}</div></div><div><center>${Expression}<br />${Reading}</center></div>"""),
(u"Word recognition",u"""D:%(Reading)s<br>%(Meaning)s""",u"""${Css}<div style="float:left;"><div>${W:JLPT}</div><div>${W:Freq}</div></div><div><center>${Reading}<br \>${Meaning}</center></div>"""),
(u"Kanji recall",u"""K:%(Reading)s""",u"""${Css}<div class="K">${K:Stroke}<div>${K:JLPT}</div><div>${K:Jouyou}</div><div>${K:Freq}</div></div><center>${OnYomi}<br />${KunYomi}</center><center>${K:Words}</center>"""),
(u"Kanji recognition",u"""K:%(Reading)s<br>%(Meaning)s""",u"""${Css}<div class="K">${K:Stroke}<div>${K:JLPT}</div><div>${K:Jouyou}</div><div>${K:Freq}</div></div><center>${K:Words}</center>"""),
(u"Kanji/Word recall",u"""KW:%(Reading)s""",u"""${Css}<div class="K">${K:Stroke}<div>${K:JLPT}</div><div>${K:Jouyou}</div><div>${K:Freq}</div></div><center>${OnYomi}<br />${KunYomi}</center><center>${K:Words}</center>"""),
(u"Kanji/Word recognition",u"""KW:%(Reading)s<br>%(Meaning)s""",u"""${Css}<div class="K">${K:Stroke}<div>${K:JLPT}</div><div>${K:Jouyou}</div><div>${K:Freq}</div></div><center>${K:Words}</center>"""),
(u"Sentence recall",u"""S:%(Reading)s""",u"""<center>${Expression}<br />${Reading}<br />${W:Stroke}</center>"""),
(u"Sentence recognition",u"""S:%(Reading)s<br>%(Meaning)s""",u"""<center>${Reading}<br \>${Meaning}</center>"""),
(u"Grammar recall",u"""G:%(Reading)s""",u"""${Expression}<br />${Reading}</center>"""),
(u"Grammar recognition",u"""G:%(Reading)s<br>%(Meaning)s""",u"""<center>${Reading}<br \>${Meaning}</center>"""),
(u"Kanji character",u"""K:%(Kanji)s""",u"""${Css}<div class="K">${K:Stroke}<div>${K:JLPT}</div><div>${K:Jouyou}</div><div>${K:Freq}</div></div><center>${K:Words}</center>"""),
(u"Kanji meanings",u"""K:%(Meaning)s""",u"""${Css}<div class="K">${K:Stroke}<div>${K:JLPT}</div><div>${K:Jouyou}</div><div>${K:Freq}</div></div><center>${Meaning}</center><center>${K:Words}</center>"""),
(u"Kanji readings",u"""K:%(OnYomi)s<br>%(KunYomi)s""",u"""${Css}<div class="K">${K:Stroke}<div>${K:JLPT}</div><div>${K:Jouyou}</div><div>${K:Freq}</div></div><center>${OnYomi}<br />${KunYomi}</center><center>${K:Words}</center>""")]


