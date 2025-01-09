import json
import requests
from prompts import load_prompts

class BillAgent:
    def __init__(self, config):
        self.config = config
        self.init_prompts(load_prompts())
        self.active_agent = 'Bill'
        self.history = []

    def init_prompts(self, prompts):
        self.prompts = prompts
        self.general_prompt = prompts['general']
        self.agents_prompts = {}
        for agent in prompts['agents']:
            self.agents_prompts[agent['name']] = agent['prompt']
        self.active_agent = prompts['agents'][0]['name']

    def get_tools(self):
        tools = []
        for agent in self.prompts['agents']:
            if agent['name'] == self.active_agent:
                continue
            tools.append({
                "type": "function",
                "function": {
                    "name": f'switch_to_agent_{agent["name"]}',
                    "description": agent["condition"],
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "description": ""
                    }
                }
            })
        return tools
        
    def chat(self, message):
        system_prompt = self.general_prompt + self.agents_prompts[self.active_agent]

        messages = []
        messages.append({"role": "system", "content": system_prompt})

        if message:
            self.history.append({"role": "user", "content": message})

        for history in self.history:
            messages.append(history)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config['api_key']}"
        }
    
        data = {
            "model": self.config["model_name"],
            "messages": messages,
            "stream": True,
            "tools": self.get_tools()
        }

        print("=", end="", flush=True)
        
        try:
            with requests.post(
                self.config["api_url"],
                headers=headers,
                json=data,
                stream=True
            ) as response:
                if response.status_code != 200:
                    print(f"\033[31mError: {response.status_code} - {response.text}\033[0m")
                    return
                
                assistant_message = ""
                print("\b", end="", flush=True)
                for chunk in response.iter_lines():
                    if chunk:
                        decoded_chunk = chunk.decode('utf-8')
                        if decoded_chunk.startswith("data: "):
                            try:
                                chunk_data = json.loads(decoded_chunk[6:])

                                if "choices" in chunk_data:
                                    choice_delta = chunk_data["choices"][0]["delta"]

                                    content = choice_delta.get("content", None)
                                    if content:
                                        print(content, end="", flush=True)
                                        assistant_message += content
                                    elif "tool_calls" in choice_delta:
                                        tool_calls = choice_delta["tool_calls"]
                                        for tool_call in tool_calls:
                                            tool_name = tool_call["function"]["name"]
                                            if tool_name.startswith("switch_to_agent_"):
                                                agent_name = tool_name[16:]
                                                self.switch_agent(agent_name, message)
                                                return
                            except json.JSONDecodeError:
                                continue
                if assistant_message:
                    self.history.append({"role": "assistant", "content": assistant_message})
        except Exception as e:
            print(f"\033[31mError: {str(e)}\033[0m")

    def switch_agent(self, agent_name, message):
        if self.config['easy_mode']:
            print(f"Switching to agent {agent_name}")
        if agent_name in self.agents_prompts:
            self.active_agent = agent_name
            self.clear_history()
            return self.chat(message)
        else:
            print(f"Error: Agent {agent_name} not found.")
    
    def clear_history(self):
        self.history.clear()