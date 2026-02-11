from flask import Flask, request, render_template_string
import unicodedata
import os

app = Flask(__name__)


# ====== ALGORITMOS =======

def digitsSum(inputInt: int) -> int:
    return sum(int(d) for d in str(abs(inputInt)))


def isPalindrome(inputStr: str) -> bool:
    # Normalizar texto
    inputStr = inputStr.lower()

    inputStr = ''.join(
        c for c in unicodedata.normalize('NFD', inputStr)
        if unicodedata.category(c) != 'Mn'
    )

    # Mantener solo letras y números
    inputStr = ''.join(c for c in inputStr if c.isalnum())

    return inputStr == inputStr[::-1]


def integerSort(inputArray):
    if len(inputArray) <= 1:
        return inputArray

    mid = len(inputArray) // 2
    left = integerSort(inputArray[:mid])
    right = integerSort(inputArray[mid:])

    return merge(left, right)


def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

# ====== FRONTEND =========


HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Clever Internship Challenge</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background-color: #0f0f0f;
            color: white;
            text-align: center;
            padding: 40px;
        }

        h1 {
            color: #ff1e1e;
            margin-bottom: 30px;
        }

        .card {
            background: #1a1a1a;
            padding: 40px;
            margin: auto;
            width: 420px;
            border-radius: 15px;
            box-shadow: 0 0 20px rgba(255, 0, 0, 0.3);
        }

        button {
            padding: 12px 20px;
            margin: 8px;
            border: none;
            background-color: #ff1e1e;
            color: white;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            transition: 0.3s ease;
        }

        button:hover {
            background-color: #cc0000;
            transform: scale(1.05);
        }

        input {
            padding: 10px;
            width: 85%;
            margin: 10px;
            border-radius: 6px;
            border: 1px solid #333;
            background-color: #2a2a2a;
            color: white;
        }

        .result {
            margin-top: 20px;
            padding: 15px;
            background-color: #111;
            border-left: 4px solid #ff1e1e;
            border-radius: 8px;
            font-weight: bold;
        }

        .menu {
            margin-bottom: 20px;
        }
    </style>
</head>
<body>

<h1>Clever Internship - Desafíos</h1>

<div class="card">

    <div class="menu">
        <form method="POST">
            <button name="challenge" value="sum">Suma de Dígitos</button>
            <button name="challenge" value="palindrome">Palíndromo</button>
            <button name="challenge" value="sort">Ordenamiento</button>
        </form>
    </div>

    {% if selected == "sum" %}
        <h3>Suma de Dígitos</h3>
        <form method="POST">
            <input type="hidden" name="challenge" value="sum">
            <input type="number" name="number" placeholder="Ingresa un número" required>
            <br>
            <button type="submit">Calcular</button>
        </form>
    {% endif %}

    {% if selected == "palindrome" %}
        <h3>Verificar Palíndromo</h3>
        <form method="POST">
            <input type="hidden" name="challenge" value="palindrome">
            <input type="text" name="text" placeholder="Ingresa un texto" required>
            <br>
            <button type="submit">Verificar</button>
        </form>
    {% endif %}

    {% if selected == "sort" %}
        <h3>Ordenamiento</h3>
        <form method="POST">
            <input type="hidden" name="challenge" value="sort">
            <input type="text" name="numbers" placeholder="Ej: 5,-2,10,0,3,-7" required>
            <br>
            <button type="submit">Ordenar</button>
        </form>
    {% endif %}

    {% if result is not none %}
        <div class="result">
            Resultado: {{ result }}
        </div>
    {% endif %}

</div>

</body>
</html>
"""


# ====== ROUTE ============


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    selected = None

    if request.method == "POST":
        selected = request.form.get("challenge")

        try:
            if selected == "sum" and "number" in request.form:
                number = int(request.form["number"])
                result = digitsSum(number)

            elif selected == "palindrome" and "text" in request.form:
                text = request.form["text"]
                result = isPalindrome(text)

            elif selected == "sort" and "numbers" in request.form:
                numbers = request.form["numbers"]
                number_list = [int(n.strip()) for n in numbers.split(",")]
                result = integerSort(number_list)

        except Exception:
            result = "Entrada inválida"

    return render_template_string(HTML_TEMPLATE, result=result, selected=selected)



# ====== PRODUCCIÓN =======

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
