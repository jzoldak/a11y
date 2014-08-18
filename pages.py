# -*- coding: utf-8 -*-
from bok_choy.page_object import PageObject
from bs4 import BeautifulSoup
from pdb import set_trace


class TenonIoTestNowPage(PageObject):
    """
    Tenon.io's Test Now Page
    Used to find violations in the pages
    """

    url = 'http://www.tenon.io/#testnow'

    def is_browser_on_page(self):
        return self.q(css='h2.focusFirst').text[0] == 'What to test'

    def _fill_text(self, text):
        """
        Fill the text into the CodeMirror input block
        """
        script = """
        var cm = $('div.CodeMirror').get(0).CodeMirror;
        CodeMirror.signal(cm, "focus", cm);
        cm.setValue(arguments[0]);
        CodeMirror.signal(cm, "blur", cm);
        """
        self.browser.execute_script(script, str(text))

    def submit_data(self, text):
        """
        Submit the data for evaluation
        and wait for the results
        """
        self._fill_text(text)
        self.q(css='input#submit').click()

        # wait for the results to be returned
        self.wait_for_element_visibility('#results', 'Results are visible.')

    @property
    def results(self):
        """
        Get the results after submitting data
        """
        return self.q(css='#results').html[0]

    def get_score(self):
        """
        The results score, returned as a dict
        """
        soup = BeautifulSoup(self.results)
        score = {}
        scorelist = soup.find(id='scoreList')
        items = scorelist.find_all('li')
        for item in items:

            data = item.text.split()
            score[data[1]] = data[0]

        return score
