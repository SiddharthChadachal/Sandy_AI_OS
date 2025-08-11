import os
import requests
from dotenv import load_dotenv
from colorama import init, Fore, Style
import textwrap

load_dotenv()

#-------------------
#Initialisation
#-------------------


API_KEY = os.getenv("GROQ_API_KEY")
API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.1-8b-instant"


#-------------------
#API_KEY check
#-------------------
if not API_KEY:
	raise ValueError("No API key found.")

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
	print(Fore.CYAN + "\n\n\tSandy 0.2\t\n\n ------------------------\n Now with memory context\n ------------------------\n\n" + Style.RESET_ALL)
	
	try:
		intro = question("")
		print(Fore.CYAN + format_ai_message("Sandy: " + intro)+ Style.RESET_ALL+ "\n\n")
	except Exception as e:
		print(Fore.RED + f"[Error] {e}" + Style.RESET_ALL)
	
	while True:
		
		user_inp = input(Fore.YELLOW + "You: " + Style.RESET_ALL).strip()
		if user_inp.lower() in ["exit", "quit", "bye", "thank you bye !", "goodnight !", "goodbye", "let me sleep !!"]:
			print(Fore.CYAN + format_ai_message("Sandy: Goodbye!") + Style.RESET_ALL)
			break
		try:
			reply = question(user_inp)
			print(Fore.CYAN + format_ai_message(f"Sandy: {reply}\n") + Style.RESET_ALL)
		except Exception as e:
			print(Fore.RED + f"[Error] {e}" + Style.RESET_ALL)
