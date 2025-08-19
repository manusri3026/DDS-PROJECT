# ---------------------------
# Expression Calculator
# ---------------------------

# Function to define operator precedence
def precedence(op):
    if op == '+' or op == '-':
        return 1
    if op == '*' or op == '/':
        return 2
    if op == '^':
        return 3
    return 0

# Function to check if character is an operator
def is_operator(c):
    return c in ['+', '-', '*', '/', '^']

# Convert Infix → Postfix using stack
def infix_to_postfix(expression):
    stack = []
    result = []
    
    for char in expression:
        if char.isalnum():  # Operand (number/variable)
            result.append(char)
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                result.append(stack.pop())
            stack.pop()  # remove '('
        elif is_operator(char):
            while (stack and precedence(stack[-1]) >= precedence(char)):
                result.append(stack.pop())
            stack.append(char)
    
    while stack:
        result.append(stack.pop())
    
    return "".join(result)

# Evaluate a Postfix expression
def evaluate_postfix(expression):
    stack = []
    
    for char in expression:
        if char.isdigit():  # Single-digit operand
            stack.append(int(char))
        elif is_operator(char):
            b = stack.pop()
            a = stack.pop()
            if char == '+': stack.append(a + b)
            elif char == '-': stack.append(a - b)
            elif char == '*': stack.append(a * b)
            elif char == '/': stack.append(a // b)  # integer division
            elif char == '^': stack.append(a ** b)
    
    return stack[-1]

# ---------------------------
# Main
# ---------------------------
def main():
    infix_expr = input("Enter an infix expression: ")
    
    postfix_expr = infix_to_postfix(infix_expr.replace(" ", ""))
    print("✅ Postfix Expression:", postfix_expr)
    
    result = evaluate_postfix(postfix_expr)
    print("🎯 Evaluated Result:", result)

if __name__ == "__main__":
    main()
