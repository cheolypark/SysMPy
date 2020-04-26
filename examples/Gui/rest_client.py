import requests
# {"mode":"search","type":"html","data":{"srch-term":""}}
body = {"mode":"search"}

r = requests.get(f"http://127.0.0.1:9191/sim_udpated?g={body}")


print(r.text)