from random import choice

randoms = {
  "task_name": [
    "Rydderunde",
    "Panterunde",
    "Crewtøy",
  ],
  "task_description": ["Det er viktig at denne oppgaven blir gjort! Ta kontakt med xyz for å gjøre endringer."],
  "reminder_info": ["Husk å ta med deg abc og møt opp hos xyz ved Logistikk!"],
}

def get_random(type): return choice(randoms[type])
