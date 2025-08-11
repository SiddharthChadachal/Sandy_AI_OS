import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
	raise ValueError("No API key found.")

API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-8b-8192"

def question(prompt):
	headers = {
	"Authorization": f"Bearer {API_KEY}",
	"Content-Type": "application/json"
	}
	data = {
	"model": MODEL,
	"messages": [
			{"role": "system","content": "You are Sandy, a helpful Linux terminal assistant"},
			{"role": "user", "content": prompt}
		]
	}
	
	response = requests.post(API_URL, headers=headers, json=data)
	if response.status_code != 200:
		raise Exception(f"Error {response.status_code}: {response.text}")
	return response.json()["choices"][0]["message"]["content"]
	
if __name__ == "__main__":
	while True:
		try:
			user_inp = input("You: ")
			if user_inp.lower() in ["exit", "quit","bye"]:
				print("Sandy: Goodbye!")
				break
			answer = question(user_inp)
			print("Sandy: ", answer)			
		except KeyboardInterrupt:
			print("\n Sandy: GoodBye!")
			break

