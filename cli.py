import os
import sys
from bill import BillAgent
from config import load_config
from prompts import opening_sentence

def first_sentence():
    opening = opening_sentence()
    print("\033[97mBill: " + opening + "\033[0m")

def main():
    config = load_config()
    
    if not config['api_key'] or not config['api_url']:
        print("Error: Please configure your API settings in config.json")
        print("Example configuration:")
        print('''{
  "api_url": "https://api.example.com/v1/chat/completions",
  "api_key": "your-api-key-here",
  "model_name": "gpt-4o"
}''')
        return
        
    print("Chat started. Type 'exit' to quit, or 'clear' to clear chat history.")
    first_sentence()

    agent = BillAgent(config)
    while True:
        try:
            user_input = input("\033[90mYou: ")
            if user_input.lower() == 'exit':
                break
            elif user_input.lower() == 'clear':
                agent.clear_history()
                print("\033[0m历史对话已清除。")
                first_sentence()
                continue
                
            print("\033[97mBill: ", end="", flush=True)
            agent.chat(user_input)
            print("\033[0m")
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    # change chcp
    if sys.platform == "win32":
        import os
        os.system("chcp 65001")
    

    main()
