# import requests
# # {"mode":"search","type":"html","data":{"srch-term":""}}
# body = {"mode":"search"}
#
# for i in range(200):
#     try:
#         print(i)
#         # r = requests.get(f"http://127.0.0.1:9191/sim_udpated?g={body}")
#         # sess = requests.Session()
#         # adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
#         # sess.mount('http://', adapter)
#
#         r = requests.get(f"http://127.0.0.1:9191/sim_udpated?g={body}")
#         print(r.text)
#     except requests.exceptions.RequestException as e:
#         raise SystemExit(e)
#         # pass
#

from flask import Flask, jsonify, make_response, request
app = Flask(__name__)
@app.route('/api/v1.0/qanda/', methods=['POST'])
def people_api():
    text = request.json.get('text')
    if text is None:
       make_response(jsonify({'error': 'Missing text parameter'}), 400)
    return '<html><body> Hello! </body> </html>'
app.run()

text = "Inshorts invites applications for its Inshorts Inclusives Campus Program Inshorts is looking for young enthusiastic and innovative minds for its campus program – The Inshorts Inclusives Program. The Inshorts Inclusives is a community of like-minded students working towards Inshorts’ umbrella mission of #Stay Informed. The Inclusives being the torchbearers of the mission, are responsible for designing and executing plans and strategies to keep people informed of and connected to, their surroundings and the world at a larger level. Through this journey, an Inclusive gets exposed to the fields of marketing, content-writing, business development and strategy and gets a hands on experience in these areas. WHAT WOULD BE THE WORK OF AN INSHORTS INCLUSIVE? The main task of an Inclusive would be to come-up with innovative solutions to the given problem - of keeping people informed and creating awareness of the Inshorts app amongst the masses. With this problem statement in mind, an Inclusive would need to be on a constant look out for all possible modes and ways of tackling it. An Inclusive would be responsible for both the ideation and execution of such solutions. Along with this, the Inclusives will also drive the initiative of connecting campuses across the country by creating and managing a common content platform for college students on the Inshorts app. For this they will need to ensure and manage their college’s presence on the app by collating all relevant news and information from their college."

import requests
r = requests.post("http://127.0.0.1:5000/api/v1.0/qanda/", json={"text": text})
r.text