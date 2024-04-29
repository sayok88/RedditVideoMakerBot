import random

import requests
from utils import settings
import json

from utils.console import print_substep


def get_gender(text):
    key = settings.config["settings"]["tts"]["uclassify_key"]
    m_p = random.choice([0, 1])
    f_p = 1 - m_p
    try:
        response = requests.post("https://api.uclassify.com/v1/uClassify/GenderAnalyzer_v5/classify",
                                 data=json.dumps({"texts": [text]}),
                                 headers={'Content-Type': 'application/json',
                                          'Authorization': f'Token {key}'
                                          })
        data = response.json()[0].get("classification", {})
        for p in data:
            if p.get('className', '') == 'female':
                f_p = p.get("p", f_p)
            else:
                m_p = p.get("p", m_p)
        print_substep(text + str(m_p) + str(f_p))
    except Exception as e:
        pass
    return 'M' if m_p > f_p else 'F'


if __name__ == '__main__':
    get_gender("Seems pretty straightforward, according to the docs on the page you linked (emphasis mine).")
