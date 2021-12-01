# Creator : Kingtebe
# Date : 11-11-2021, 11:33 WIB
# Note : Follow my github https://github.com/Musk-ID
import os,re,sys,ini,json,base64,requests
try:
	from time import sleep
	from datetime import datetime
	from bs4 import BeautifulSoup
except:
	exit("# Sorry! module not installed !")

c = '\033[1;36m'
p = '\033[1;37m'
h = '\033[1;32m'
k = '\033[1;33m'
m = '\033[1;31m'
q = '\033[1;30m'
z = '\033[101m'
o = '\033[0m'
t = '\033[0;32m';

class Goqash:
	def __init__(self):
		self.config = ini.parse(open("cfg.ini").read())
		self.headers = {
			"user-agent":self.config["data"]["user-agent"],
			"cookie":self.config["data"]["cookie"]}
		self.time = datetime.now().strftime("%H.%M.%S")
		self.date = datetime.now().strftime("%d/%m/%Y")
		self.req = requests.Session()
		self.find = self.req.get("https://api.myip.com").json()

	def message(self,katakan):
		for j in katakan + "\n":
			sys.stdout.write(j)
			sys.stdout.flush()
			sleep(0.001)

	def waktu(self,second):
		while second:
			mins,secs = divmod(second,60)
			timer = "  \033[1;33m▶ \033[1;37mWaiting\033[1;37m \033[37m⟨\033[0;36m{:02d}:{:02d}\033[1;37m⟩".format(mins,secs)
			print(timer,end="\r")
			sleep(1)
			second -= 1

	def get_balance(self):
		req = self.req.get("https://qashbits.com/",headers=self.headers)
		if "login" in req.text:
			exit("\n# Cookie has expired !\n")
		bits = re.search('<div class="text-primary"><b>(.*?)</b></div></div>',req.text).group(1)
		btc = re.search('<div class="text-warning"><b>(.*?)</b></div></div>',req.text).group(1)
		username = re.search('<font class="text-success">(.*?)</font>',req.text).group(1)
		return username,bits,btc

	def Ptc_ads(self):
		while True:
			try:
				url = self.req.get("https://qashbits.com/?page=ptc",headers=self.headers)
				if "is no website available" in url.text:
					print(f"  {p}PTC ads no available now {m}!\n")
					return
			except requests.exceptions.ConnectionError:
				print(f"  {p}Error connection internet {m}! ",flush=True,end="\r")
				continue
			par = BeautifulSoup(url.text,"html.parser")
			adsID = par.find("div",attrs={"class":"website_block"}).get("id")
			pageKey = re.search("'&key\=(.*?)'",url.text).group(1)
			print(f"  {m}▶ {p}Visit ads site            ",flush=True,end="\r")
			sleep(1.5)
			try:
				req = self.req.get("https://qashbits.com/surf.php",headers=self.headers,params={"sid":adsID,"key":pageKey})
			except requests.exceptions.ConnectionError:
				print(f"  {p}Error connection internet {m}! ",flush=True,end="\r")
				continue
			secs = re.search("var\ssecs\s=\s(.*?);",req.text).group(1)
			toKen = re.search("var\stoken\s=\s'(.*?)';",req.text).group(1)
			self.waktu(int(secs))
			while True:
				print(f"  {m}▶ {p}Trying bypass captcha ",flush=True,end="\r")
				headers={
					"user-agent":self.config["data"]["user-agent"],
					"cookie":self.config["data"]["cookie"],
					"x-requested-with":"XMLHttpRequest",
					"content-type":"application/x-www-form-urlencoded; charset=UTF-8"
				}
				url = "https://qashbits.com/system/libs/captcha/request.php"
				try:
					req = self.req.post(url,headers=headers,data={"cID": "0","rT": "1","tM": "light"}).json()
					satu = req[0];dua = req[1];tiga = req[2];empat = req[3];lima = [4]
					req = self.req.post(url,headers=headers,data={"cID":"0","pC":satu,"rT":"2"})
				except requests.exceptions.ConnectionError:
					print(f"  {p}Error connection internet {m}! ",flush=True,end="\r")
					continue
				if req.status_code != 200:
					continue
				try:
					req = self.req.post("https://qashbits.com/system/ajax.php",headers=headers,data={"a":"proccessPTC","data":adsID,"token":toKen,"captcha-idhf":"0","captcha-hf":satu}).json()
				except requests.exceptions.ConnectionError:
					print(f"  {p}Error connection internet {m}! ",flush=True,end="\r")
					continue
				if req["status"] != 200:
					print(f"  {m}▶ {p}Bypass captcha failed {m}! ",flush=True,end="\r")
					continue
				elif req["status"] == 200:
					earn = re.search('</b> (.*?)</div>',req["message"]).group(1)
					detail = self.get_balance()
					print(f"  {t}{earn} {q}- {t}{detail[1]} {q}- {t}{detail[2]}")
					break

	def bypass(self):
		while True:
			solve = self.req.get("https://api-secure.solvemedia.com/papi/_challenge.js?k=1yqk3nHfy5Px58G81cXjL7frVWm8h.KL;f=_ACPuzzleUtil.callbacks%5B0%5D;l=en;t=img;s=standard;c=js,h5c,h5ct,svg,h5v,v/h264,v/webm,h5a,a/mp3,a/ogg,ua/chrome,ua/chrome76,os/android,os/android8.1,fwv/BfyRWw.qgut49,jslib/jquery,htmlplus;am=t7dyT9ELVKOyS-Au0QtUow;ca=ajax;ts=1636431166;ct=1636431364;th=white;r=0.15729434621940186",headers=self.headers)
			chall = re.search('"challenge":"(?P<chal>[^>]+?)"',solve.text).group(1)
			solve = self.req.get(f"https://api-secure.solvemedia.com/papi/media?c={chall};w=300;h=150;fg=000000;bg=f8f8f8",headers=self.headers)
			with open("img.png","wb") as cap:
				cap.write(solve.content)
			Img = base64.b64encode(open("img.png","rb").read()).decode()
			try:
				page = page = self.req.post("https://vision.googleapis.com/v1/images:annotate?key=AIzaSyC3y-Em42htSB8UEZPqptJ78rlvL58_h6Y",data=json.dumps({"requests":[{"image":{"content": Img},"features":[{"type":"TEXT_DETECTION","maxResults":1}]}]}),headers={"Content-Type":"application/json"}).json()
				textImg = " ".join(page['responses'][0]['fullTextAnnotation']['text'].splitlines()[1:])
			except KeyError:
				continue
			req = self.req.get("https://qashbits.com/",headers=self.headers)
			print(f"  {k}▶ {p}Trying bypass captcha ",flush=True,end="\r")
			toKen = re.search("var\stoken\s=\s'(.*?)';",req.text).group(1)
			data = {
				"a":"getFaucet",
				"token":toKen,
				"captcha":"0",
				"challenge":chall,
				"response":textImg
			}
			try:
				req = self.req.post("https://qashbits.com/system/ajax.php",headers={"user-agent":self.config["data"]["user-agent"],"cookie":self.config["data"]["cookie"],"x-requested-with":"XMLHttpRequest","content-type":"application/x-www-form-urlencoded; charset=UTF-8"},data=data).json()
			except requests.exceptions.ConnectionError:
				print(f"  {p}Error connenction internet {m}!{p}\n")
				continue
			if req["status"] != 200:
				print(f"  {m}▶ Bypass captcha failed {m}!",flush=True,end="\r")
				continue
			else:
				earn= " ".join(BeautifulSoup(req["message"],"html.parser").text.strip().split()[3:])
				detail = self.get_balance()
				print(f"  {t}{earn} {q}- {t}{detail[2]}")
				self.waktu(int(60*5))

	def manual_bypass(self):
		while True:
			solve = self.req.get("https://api-secure.solvemedia.com/papi/_challenge.js?k=1yqk3nHfy5Px58G81cXjL7frVWm8h.KL;f=_ACPuzzleUtil.callbacks%5B0%5D;l=en;t=img;s=standard;c=js,h5c,h5ct,svg,h5v,v/h264,v/webm,h5a,a/mp3,a/ogg,ua/chrome,ua/chrome76,os/android,os/android8.1,fwv/BfyRWw.qgut49,jslib/jquery,htmlplus;am=t7dyT9ELVKOyS-Au0QtUow;ca=ajax;ts=1636431166;ct=1636431364;th=white;r=0.15729434621940186",headers=self.headers)
			chall = re.search('"challenge":"(?P<chal>[^>]+?)"',solve.text).group(1)
			solve = self.req.get(f"https://api-secure.solvemedia.com/papi/media?c={chall};w=300;h=150;fg=000000;bg=f8f8f8",headers=self.headers)
			with open("img.png","wb") as cap:
				cap.write(solve.content)
			try:
				Img = base64.b64encode(open("img.png","rb").read()).decode()
			except:
				continue
			req = self.req.get("https://qashbits.com/",headers=self.headers)
			toKen = re.search("var\stoken\s=\s'(.*?)';",req.text).group(1)
			os.popen("termux-open img.png")
			cap = input(f"  {k}▶ {p}Input Captcha {k}: {p}")
			data = {
				"a":"getFaucet",
				"token":toKen,
				"captcha":"0",
				"challenge":chall,
				"response":cap
			}
			try:
				req = self.req.post("https://qashbits.com/system/ajax.php",headers={"user-agent":self.config["data"]["user-agent"],"cookie":self.config["data"]["cookie"],"x-requested-with":"XMLHttpRequest","content-type":"application/x-www-form-urlencoded; charset=UTF-8"},data=data).json()
			except requests.exceptions.ConnectionError:
				print(f"  {p}Error connenction internet {m}!{p}\n")
				continue
			if req["status"] != 200:
				print(f"  {m}▶ {p}Text captcha wrong {m}!{p}     ",flush=True,end="\r")
				continue
			else:
				earn= " ".join(BeautifulSoup(req["message"],"html.parser").text.strip().split()[3:])
				detail = self.get_balance()
				print(f"  {t}{earn} {q}- {t}{detail[2]}")
				self.waktu(int(60*5))

	def Execute(self):
		info = self.get_balance()
		os.system('cls' if os.name=='nt' else 'clear')
		self.message(f"\n  {p}Time : {self.time}                 Date : {self.date}\n {m}╔{c}═════════════════════════════════════════════════{m}╗\n {c}║ {m}███████{c}╗ {m}█████{c}╗  {m}█████{c}╗ {m}██{c}╗  {m}████████{c}╗{m}██{c}╗   {m}██{c}╗ ║\n {c}║ {m}██{c}╔════╝{m}██{c}╔══{m}██{c}╗{m}██{c}╔══{m}██{c}╗{m}██{c}║  {c}╚══{m}██{c}╔══╝{m}██{c}║   {m}██{c}║ ║\n {c}║ {m}█████{c}╗  {m}███████{c}║{m}███████{c}║{m}██{c}║     {m}██{c}║   {m}██{c}║   {m}██{c}║ ║\n {c}║ {m}██{c}╔══╝  {m}██{c}╔══{m}██{c}║{m}██{c}╔══{m}██{c}║{m}██{c}║     {m}██{c}║   {c}╚{m}██{c}╗ {m}██{c}╔╝ ║\n {c}║ {m}██{c}║     {m}██{c}║  {m}██{c}║{m}██{c}║  {m}██{c}║{m}███████{c}╗{m}██{c}║    {c}╚{m}████{c}╔╝  ║\n {c}║ ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝     ╚═══╝   ║\n {c}║{k}-------------------------------------------------{c}║\n {c}║ {k}▶ {p}Author {k}: {p}Kingtebe                             {c}║\n {c}║ {k}▶ {p}Github {k}: {p}github.clom/Musk-ID        {m}[{p}ONLINE{m}]  {c}║\n {m}╚{c}═════════════════════════════════════════════════{m}╝\n {q}<══════════════[{k}{z} • FREE SCRIPT • {o}{q}]════════════════>\n  {c}▶ {p}Youtube {k}: {p}FaaL TV\n  {c}▶ {p}IP Kamu {k}: {h}{self.find['ip']}\n  {c}▶ {p}Group   {k}: {p}https://t.me/Kapten_bulls\n {q}<═════════════════════════════════════════════════>\n  {p}Account Login as {c}{info[0]} {p}with balance {h}{info[1]}\n {q}<═════════════════════════════════════════════════>")
		self.message(f"\t{m}[{p}1{m}] {p}Auto bypass captcha\n\t{m}[{p}2{m}] {p}Manual bypass captcha\n\t{m}[{p}3{m}] {p}Ptc earn\n\t{m}[{p}4{m}] {p}Exit")
		choise= input(f"  {p}>> ")
		self.message(f" {q}<═════════════════════════════════════════════════>")
		if choise in ["1","01"]:
			self.bypass()
		elif choise in ["2","02"]:
			self.manual_bypass()
		elif choise in ["3","03"]:
			self.Ptc_ads()
		else:
			exit(f"  {p}Your selection no available {m}!{p}")

try:
	Main = Goqash()
	Main.Execute()

except KeyboardInterrupt:
	exit()
