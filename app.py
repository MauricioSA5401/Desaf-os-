from flask import Flask, request, render_template_string
import unicodedata

app = Flask(__name__)

# =========================
# ====== ALGORITMOS =======
# =========================

def digitsSum(inputInt: int) -> int:
    inputInt = abs(inputInt)
    suma = 0
    while inputInt > 0:
        suma += inputInt % 10
        inputInt //= 10
    return suma


def isPalindrome(inputStr: str) -> bool:
    # Convertir a minúsculas
    inputStr = inputStr.lower()

    # Eliminar acentos
    inputStr = ''.join(
        c for c in unicodedata.normalize('NFD', inputStr)
        if unicodedata.category(c) != 'Mn'
    )

    # Eliminar espacios
    inputStr = inputStr.replace(" ", "")

    left = 0
    right = len(inputStr) - 1

    while left < right:
        if inputStr[left] != inputStr[right]:
            return False
        left += 1
        right -= 1

    return True


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


# =========================
# ====== FRONTEND =========
# =========================

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Clever Internship Challenge</title>
    <style>
        body {
            font-family: Arial;
            background-color: #f4f4f4;
            text-align: center;
            padding: 40px;
        }
        .card {
            background: white;
            padding: 30px;
            margin: auto;
            width: 400px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        button {
            padding: 10px 20px;
            margin: 10px;
            border: none;
            background-color: #007BFF;
            color: white;
            border-radius: 5px;
            cursor: pointer;
        }
        input {
            padding: 8px;
            width: 80%;
            margin: 10px;
        }
    </style>
</head>
<body>

<h1>Clever Internship - Desafíos</h1>

<div class="card">

    <form method="POST">
        <button name="challenge" value="sum">Suma de Dígitos</button>
        <button name="challenge" value="palindrome">Palíndromo</button>
        <button name="challenge" value="sort">Ordenamiento</button>
    </form>

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
        <h2>Resultado:</h2>
        <p>{{ result }}</p>
    {% endif %}

</div>

</body>
</html>
"""

# =========================
# ====== ROUTE ============
# =========================

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    selected = None

    if request.method == "POST":
        selected = request.form.get("challenge")

        if selected == "sum" and "number" in request.form:
            number = int(request.form["number"])
            result = digitsSum(number)

        elif selected == "palindrome" and "text" in request.form:
            text = request.form["text"]
            result = isPalindrome(text)

        elif selected == "sort" and "numbers" in request.form:
            numbers = request.form["numbers"]
            number_list = list(map(int, numbers.split(",")))
            result = integerSort(number_list)

    return render_template_string(HTML_TEMPLATE, result=result, selected=selected)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
