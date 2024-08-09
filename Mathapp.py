import ast
import operator
import math
from rich.console import Console
from rich.text import Text



#nltk.download("stopwords")
console = Console()

def safe_eval(expr):
    # Define operators
    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
        'Factorial': math.factorial
    }

    def eval_(node):
        if isinstance(node, ast.Constant):  # <number>
            return node.value
        elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
            return operators[type(node.op)](eval_(node.left), eval_(node.right))
        elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
            return operators[type(node.op)](eval_(node.operand))
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'Factorial':
            arg = eval_(node.args[0])
            return operators['Factorial'](arg)
        elif isinstance(node, ast.Expression):
            return eval_(node.body)
        else:
            raise TypeError(node)

    def parse_factorial(expression):
        while '!' in expression:
            idx = expression.index('!')
            start = idx - 1
            while start >= 0 and expression[start].isdigit():
                start -= 1
            start += 1
            number = int(expression[start:idx])
            fact_result = math.factorial(number)
            expression = expression[:start] + str(fact_result) + expression[idx+1:]
        return expression

    try:
        # Replace '^' with '**' for exponentiation
        expr = expr.replace('^', '**')
        # Handle factorials
        expr = parse_factorial(expr)
        # Parse and evaluate the expression
        node = ast.parse(expr, mode='eval')
        return eval_(node)
    except Exception as e:
        return f"Error: {e}"

custom_responses = {
    "hi": "Hello! How can I assist you today?",
    "hey": "Hey there! What can I do for you?",
    "hello": "Hi! Need any help?",
    "yo": "Yo! What's going on? Need a hand?",
    "sup": "Sup! How can I help?",
    "what's up": "What's up? Need anything?",
    "good morning": "Good morning! How can I help you start your day?",
    "good afternoon": "Good afternoon! What can I do for you today?",
    "good evening": "Good evening! How can I assist you this evening?",
    "how do you do": "How do you do? It's a pleasure to assist you.",
    "pleased to meet you": "Pleasure's mine! How can I help?",
    "nice to meet you": "Nice to meet you too! Let's get started.",
    "can you help me": "Absolutely! What do you need help with?",
    "what can you do": "I can do many things! searches, analyzes, and summarizes content from the web",
    "how do I": "Let's figure it out together! How can I help?",
    "tell me about": "I'd be happy to! Tell me what you're interested in.",
    "do you know": "Let's find out! Ask away.",
    "how are you": "I'm doing well, thanks for asking! How can I help you?",
    "thank you": "You're welcome! Is there anything else I can do for you?",
    "see you later": "See you later! Don't hesitate to contact me.",
    "thanks for your help": "You're very welcome! Let me know if you need anything else.",
    "help": "You can type any number query .",
    "about": "I am  Simple Math chatbot Develpoed by Shiva in year 2024, that functions !,*,-,+,/."
}


# Main execution
if __name__ == "__main__":
    # Welcome message
    console.print("Hi, welcome! I am Simple Math bot", style="bold cyan")
    console.print(f"[bold yellow]> Bot:[/bold yellow] Hi, how can i help you ? [bold red](Hint : enter bye to exit)[/bold red] (!,*,-,+,/,^)", style="bold cyan")

    while True:
        query = console.input("[bold yellow]> You: [/bold yellow]").lower()
        if query == 'bye':
            console.print("[bold yellow]> Bot:[/bold yellow] Goodbye! Have a great day.", style="bold green")
            break
        elif query in custom_responses:
            console.print(f"[bold yellow]> Bot:[/bold yellow] {custom_responses[query]}", style="bold green")
        else:
            results = safe_eval(query)
            if not results:
                console.print("[bold yellow]> Bot:[/bold yellow] No results found.", style="bold red")
            else:
                    console.print(f"[bold yellow]> Bot:[/bold yellow] {results}", style="bold green")
                    console.print("\n" + "="*100 + "\n")
