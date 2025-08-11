import os
import requests
from dotenv import load_dotenv
from colorama import init, Fore, Style
from pathlib import Path
import subprocess
import textwrap

load_dotenv()

#-------------------
#Initialisation
#-------------------

API_KEY = os.getenv("GROQ_API_KEY")
API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.1-8b-instant"

#-------------------
#Alias path setup
#-------------------

alias_name = "sandy"
command_to_run = f"gnome-terminal -- python3 {os.path.abspath(__file__)}"
bashrc_path = Path.home() / ".bashrc"

if bashrc_path.exists():
	with open(bashrc_path, "r") as file:
		bashrc_content = file.read()
	print(Style.BRIGHT + Fore.BLUE + "\n[INFO] printing bashrc content: \n\n\n" + bashrc_content + Style.RESET_ALL)
else:
	bashrc_content = ""



alias_line = f"alias {alias_name}='{command_to_run}'"

if alias_line not in bashrc_content:
	with open(bashrc_path, "a") as file:
		file.write(f"\n{alias_line}\n")
	print(Style.BRIGHT + Fore.BLUE + f"[SETUP] Alias '{alias_name}' added to {bashrc_path}. please run source ~/.bashrc\n"+ Style.RESET_ALL)
	subprocess.run(["bash", "-c", "source ~/.bashrc"], check=False)
else:
	print(Style.BRIGHT + Fore.BLUE + f"[INFO] found alias {alias_name}\n" + Style.RESET_ALL)
	print(Style.BRIGHT + Fore.BLUE + f"[INFO] checking API availability...\n" + Style.RESET_ALL)

#-------------------
#API_KEY check
#-------------------

if not API_KEY:
	raise ValueError(Style.BRIGHT + Fore.RED + "[ERROR] No API key found." + Style.RESET_ALL)

#-------------------
#Memory
#-------------------
Conversations = [{"role": "system", "content": "You are Sandy with nickname Sandy Boy, you are honest in giving opinions and no bias. You give solutions understand what arey my requriements from what i ask and try to fulfil them by helping me. You have good sense of humour and great sense of humour and give wise advices and not being robotic."}]

init(autoreset=True)

def format_ai_message(msg, width=80):
	wrapped = textwrap.fill(msg, width=width, subsequent_indent=" "* 4)
	return wrapped

def format_user_message(msg, width=80):
	wrapped = textwrap.fill(msg, width=width, initial_indent=" " * 40, subsequent_indent=" " * 40)
	return wrapped

def question(prompt):
	Conversations.append({"role":"user", "content": prompt})
	payload = {
	"model": MODEL,
	"messages": Conversations
	}
	headers = {
	"Authorization": f"Bearer {API_KEY}",
	"Content-Type": "application/json"
	}
	
	response = requests.post(API_URL, headers=headers, json=payload)
	response.raise_for_status()
	if response.status_code != 200:
		raise Exception(f"Error {response.status_code}: {response.text}")
	
	data = response.json()
	reply = data["choices"][0]["message"]["content"].strip()
	Conversations.append({"role": "assistant", "content": reply})
	return reply
	
if __name__ == "__main__":

	
	ascii_art = r"""
		                                                        

		 .oooooo..o                             .o8              
		d8P'    `Y8                            "888              
		Y88bo.       .soooo.   ooo. .oo.    .oooo888  oooo    ooo 
		 `"Y8888o.  `P  )88b  `888P"Y88b  d88' `888   `88.  .8'  
		     `"Y88b  .oP"888   888   888  888   888    `88..8'   
		oo     .d8P d8(  888   888   888  888   888     `888'    
		8""88888P'  `Y888""8o o888o o888o `Y8bod88P"     .8'     
				                             .o..P'      
				                     V0.2    `Y8P'	                                         
	"""
		
	print(Style.BRIGHT + Fore.CYAN   + ascii_art + Style.RESET_ALL)
	print(Fore.CYAN + "\t\t-------------------------------------------------------\n" + Style.RESET_ALL)
	print(Style.BRIGHT + Fore.CYAN + "\t\t\t\tNow with memory context\n" + Style.RESET_ALL)
	print(Style.BRIGHT + Fore.CYAN + "\t\t-------------------------------------------------------\n\n" + Style.RESET_ALL)
	
	"""
	try:
		intro = question("")
		print(Fore.CYAN + format_ai_message("Sandy: " + intro)+ Style.RESET_ALL+ "\n\n")
	except Exception as e:
		print(Style.BRIGHT + Fore.RED + f"[Error] {e}" + Style.RESET_ALL)
	"""
	while True:
		
		user_inp = input(Fore.YELLOW + "You: " + Style.RESET_ALL).strip()
		if user_inp.lower() in ["exit", "quit", "bye", "thank you bye", "goodnight !", "goodbye", "let me sleep !!", "end", "let me sleep !"]:
			print(Style.BRIGHT + Fore.CYAN + format_ai_message("Sandy: Goodbye!") + Style.RESET_ALL)
			break
		try:
			reply = question(user_inp)
			print(Style.BRIGHT + Fore.CYAN + format_ai_message(f"Sandy: {reply}\n") + Style.RESET_ALL)
		except Exception as e:
			print(Style.BRIGHT + Fore.RED + f"[ERROR] {e}" + Style.RESET_ALL)
