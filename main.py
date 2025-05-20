from openai import OpenAI
import json
from ftplib import FTP_TLS
import ssl

DEEPSEEK_API_KEY="Your key"



client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com/v1"  # DeepSeek-compatible endpoint
)


FTP_HOST = "FTPHost"
FTP_PORT = 21
FTP_USER = "Ftpuser"
FTP_PASS = "FTP pass"

players_json = '''
[
  {"player": "Mitchell Starc", "matches": 96, "role": "bowler"},
  {"player": "Mushfiqur Rahim", "matches": 96, "role": "batsman"},
  {"player": "Kraigg Brathwaite", "matches": 98, "role": "batsman"}
]
'''

players=json.loads(players_json)
print(players)


HTML_FILENAME = "cricket_100_tests.html"
def generate_prompt():
  intro="Write an article in HTML format about these international cricketers who are about to complete 100 Test matches this year:\n"
  player_descriptions = "\n".join([
        f"{p['player']} is a {p['role']} who has played {p['matches']} Tests."
        for p in players
    ])
  closing = "\nCan you write a good content with given input"
  return intro+player_descriptions+closing
 
def generate_html_article(prompt):
  response=client.chat.completions.create(
  model='deepseek-chat',
  messages=[{"role": "user", "content": prompt}],
  temperature=0.7
  )
  return response.choices[0].message.content
 
 
def save_to_html(html_content,filename=HTML_FILENAME):
  with open(filename,'w',encoding="utf-8") as f:
    f.write(html_content)
   
def upload_to_ftp(filename):
    context = ssl.create_default_context()
    context.set_ciphers("DEFAULT:@SECLEVEL=1")  # ✅ Allow weak DH keys

    ftp = FTP_TLS(context=context)
    ftp.connect(FTP_HOST , FTP_PORT)
    ftp.login(FTP_USER, FTP_PASS)
    ftp.prot_p()  # Secure data connection

    ftp.cwd("htdocs")  # Change to public folder

    with open(filename, "rb") as f:
        ftp.storbinary(f"STOR " + filename, f)

    ftp.quit()
    print(f"✅ Uploaded '{filename}' to /htdocs/")
       


if __name__=="__main__":
  prompt=generate_prompt()
  print(prompt)
  html_content=generate_html_article(prompt)
  print(html_content)
  save_to_html(html_content,HTML_FILENAME)
  upload_to_ftp(HTML_FILENAME)
