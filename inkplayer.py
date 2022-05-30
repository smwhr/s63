from device import S63
from playsound import playsound
from hashlib import md5
import requests
from os.path import isfile

phone = S63()


def ink_continue(**kwargs):
  url = 'http://192.168.0.8:3000/continue%s' % ('?choice=%s' % kwargs['choice'] if 'choice' in kwargs else '')
  print(url)
  r = requests.get(url)
  json_response = r.json()
  for t in json_response['paragraphs']:
    print(t)
    dig = md5(t.strip().encode()).hexdigest()
    f = "numbergame/sounds/%s.wav" % dig
    if(isfile(f)):
      playsound(f)
    else:
      print('no sound found for «%s» [%s]' % (t,dig))

def compose(n):
  ink_continue(choice=n)

phone.on_compose = compose

ink_continue()
print("Phone is ready")
phone.run()
