from random import choice

randoms = {
  "task_name": [
    "Rydderunde",
    "Panterunde",
    "Crewtøy",
  ],
  "task_description": ["Møt opp hos xyz! Ta med deg abc!"],
}

def get_random(type): return choice(randoms[type])
