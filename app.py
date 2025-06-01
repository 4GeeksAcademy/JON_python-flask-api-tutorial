from flask import Flask, jsonify, request, abort, send_from_directory

app = Flask(__name__, static_folder='static')
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

# 1) Servir el frontend (index.html) en la ruta raíz
@app.route('/', methods=['GET'])
def serve_homepage():
    return send_from_directory(app.static_folder, 'index.html')

# 2) Datos en memoria (lista de tareas)
todos = [
    {"label": "Sample Todo 1", "done": True},
    {"label": "Sample Todo 2", "done": False}
]

# 3) GET /todos → devuelve la lista de tareas
@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos), 200

# 4) POST /todos → crea una tarea nueva
@app.route('/todos', methods=['POST'])
def add_todo():
    if not request.is_json:
        abort(400, description="El cuerpo de la petición debe ser JSON")
    data = request.get_json()
    if 'label' not in data or 'done' not in data:
        abort(400, description="Faltan campos 'label' o 'done'")
    if not isinstance(data['label'], str) or not isinstance(data['done'], bool):
        abort(400, description="'label' debe ser string y 'done' booleano")

    todos.append({"label": data['label'], "done": data['done']})
    return jsonify(todos), 201

# 5) DELETE /todos/<int:position> → elimina la tarea en la posición dada
@app.route('/todos/<int:position>', methods=['DELETE'])
def delete_todo(position):
    if position < 0 or position >= len(todos):
        abort(404, description="Posición fuera de rango")
    todos.pop(position)
    return jsonify(todos), 200

# 6) Arrancar el servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
