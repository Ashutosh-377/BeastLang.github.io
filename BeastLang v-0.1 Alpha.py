def tokenize(code) :
    tokens = []
    words = code.split()

    for word in words:
        if word == "print" or word == "make":
            tokens.append(("keyword", word))
        elif word == "=":
            tokens.append(("equal", word))
        elif word in {"+", "-", "*", "/"}:
            tokens.append(("operator", word))
        elif word.startswith('"') and word.endswith('"'):
            tokens.append(("string", word.strip('"')))
        elif word.isdigit():
            tokens.append(("number", word))
        else:
            tokens.append(("identifier", word))

    return tokens

def parse(tokens):
    ast = []
    i = 0

    while i < len(tokens):
        token_type, token_value = tokens[i]

        if token_type == "keyword" and token_value == "print":
            token_string = tokens[i + 1]
            ast.append({
                "type": "print",
                "value": token_string[1]  
            })
            i += 2

        elif token_type == "keyword" and token_value == "make":
            var_name = tokens[i + 1][1]  
            if tokens[i + 2][0] != "equal": 
                raise Exception('Expected "=" after variable')
            
            if i + 5 < len(tokens) and tokens[i + 4][0] == "operator":
                value_var_left = tokens[i + 3][1]
                op = tokens[i + 4][1]
                value_var_right = tokens[i + 5][1]

                ast.append({
                    "type": "assignment",
                    "name": var_name,
                    "left": value_var_left,
                    "op": op,
                    "right": value_var_right
                })
                i += 6 

            else:
                value_var = tokens[i + 3][1]
                ast.append({
                    "type": "assignment",
                    "name": var_name,
                    "value": value_var
                })
                i += 4  

        else:
            raise Exception(f"Unknown syntax at token: {tokens[i]}")

    return ast


def interpret(ast):
    env = {}

    for node in ast:
        if node["type"] == "print":
            value = node["value"]
            if value in env:
                print(env[value])
            else:
                print(value)

        elif node["type"] == "assignment":
            var_name = node["name"]

            if "value" in node:
                value = node["value"]
                if value.isdigit():
                    env[var_name] = int(value)
                elif value in env:
                    env[var_name] = env[value]
                else:
                    env[var_name] = value
            else:
                left = node["left"]
                op = node["op"]
                right = node["right"]

                left_val = int(env[left]) if left in env else int(left)
                right_val = int(env[right]) if left in env else int(right)

                if op == "+":
                    result = left_val + right_val
                elif op == "-":
                    result = left_val - right_val
                elif op == "*":
                    result = left_val * right_val
                elif op == "/":
                    result = left_val / right_val
                else:
                    raise Exception(f"Unknown operator {op}")
                env[var_name] = result
            
    return env
    

codes = '''make x = 15 make y = 10 make z =  x + y print z'''

tokens = tokenize(codes)
ast = parse(tokens)
inter = interpret(ast)

print(inter)