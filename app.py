import os

from flask import Flask, flash, jsonify, redirect, render_template, request, url_for

from database import get_connection, init_db

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "medtec-2026-chave-secreta")

init_db()


def ordenar_consultas_por_data_hora(consultas):
    """
    Algoritmo de ordenação (Bubble Sort) implementado em Python (UC30).
    Ordena a lista de consultas/pacientes por dia (data) e hora em ordem crescente.
    """
    lista = list(consultas)
    n = len(lista)

    for i in range(n):
        trocou = False
        for j in range(0, n - i - 1):
            atual = (lista[j]["data"], lista[j]["hora"])
            proximo = (lista[j + 1]["data"], lista[j + 1]["hora"])

            if atual > proximo:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                trocou = True

        if not trocou:
            break

    return lista


def formatar_data_br(data_iso):
    """Converte data YYYY-MM-DD para DD/MM/YYYY para exibição."""
    if not data_iso or "-" not in data_iso:
        return data_iso or ""
    partes = data_iso.split("-")
    if len(partes) == 3:
        return f"{partes[2]}/{partes[1]}/{partes[0]}"
    return data_iso


@app.route("/")
def index():
    """Página principal: lista pacientes por dia e hora de consulta, com filtro e formulário."""
    busca = request.args.get("busca", "").strip()
    data_filtro = request.args.get("data", "").strip()
    editar_id = request.args.get("editar", type=int)

    conn = get_connection()

    sql = """
        SELECT
            consultas.id,
            consultas.paciente_id,
            consultas.data,
            consultas.hora,
            consultas.motivo,
            pacientes.nome AS paciente_nome,
            pacientes.telefone AS paciente_telefone
        FROM consultas
        INNER JOIN pacientes ON consultas.paciente_id = pacientes.id
        WHERE 1 = 1
    """
    parametros = []

    if busca:
        sql += " AND (LOWER(pacientes.nome) LIKE ? OR LOWER(COALESCE(consultas.motivo, '')) LIKE ?)"
        termo = f"%{busca.lower()}%"
        parametros.extend([termo, termo])

    if data_filtro:
        sql += " AND consultas.data = ?"
        parametros.append(data_filtro)

    registros = conn.execute(sql, parametros).fetchall()
    consultas_lista = [dict(row) for row in registros]

    consultas_ordenadas = ordenar_consultas_por_data_hora(consultas_lista)

    for consulta in consultas_ordenadas:
        consulta["data_br"] = formatar_data_br(consulta["data"])

    pacientes = conn.execute(
        "SELECT id, nome, telefone FROM pacientes ORDER BY nome ASC;"
    ).fetchall()

    # Se estiver editando uma consulta, carrega os dados dela
    consulta_edicao = None
    if editar_id:
        consulta_edicao = conn.execute(
            "SELECT * FROM consultas WHERE id = ?;", (editar_id,)
        ).fetchone()

    conn.close()

    return render_template(
        "index.html",
        consultas=consultas_ordenadas,
        pacientes=pacientes,
        consulta_edicao=consulta_edicao,
        busca=busca,
        data_filtro=data_filtro,
    )


@app.route("/consultas/salvar", methods=["POST"])
def salvar_consulta():
    """Cria uma nova consulta ou atualiza uma existente."""
    consulta_id = request.form.get("id", "").strip()
    paciente_id = request.form.get("paciente_id", "").strip()
    data = request.form.get("data", "").strip()
    hora = request.form.get("hora", "").strip()
    motivo = request.form.get("motivo", "").strip()

    if not paciente_id or not data or not hora:
        flash("Preencha paciente, data e hora para agendar a consulta.", "erro")
        return redirect(url_for("index"))

    conn = get_connection()

    if consulta_id:
        conn.execute(
            """
            UPDATE consultas
            SET paciente_id = ?, data = ?, hora = ?, motivo = ?
            WHERE id = ?;
            """,
            (paciente_id, data, hora, motivo, consulta_id),
        )
        flash("Consulta atualizada com sucesso!", "sucesso")
    else:
        conn.execute(
            """
            INSERT INTO consultas (paciente_id, data, hora, motivo)
            VALUES (?, ?, ?, ?);
            """,
            (paciente_id, data, hora, motivo),
        )
        flash("Consulta agendada com sucesso!", "sucesso")

    conn.commit()
    conn.close()
    return redirect(url_for("index"))


@app.route("/consultas/excluir/<int:id>", methods=["POST"])
def excluir_consulta(id):
    """Exclui uma consulta pelo ID."""
    conn = get_connection()
    conn.execute("DELETE FROM consultas WHERE id = ?;", (id,))
    conn.commit()
    conn.close()

    flash("Consulta excluída com sucesso!", "sucesso")
    return redirect(url_for("index"))


@app.route("/pacientes")
def listar_pacientes():
    """Página de pacientes: lista cadastrados e permite cadastrar ou editar."""
    editar_id = request.args.get("editar", type=int)
    conn = get_connection()

    pacientes = conn.execute(
        "SELECT * FROM pacientes ORDER BY nome ASC;"
    ).fetchall()

    pacientes_lista = []
    for p in pacientes:
        item = dict(p)
        item["data_nascimento_br"] = formatar_data_br(item["data_nascimento"])
        pacientes_lista.append(item)

    paciente_edicao = None
    if editar_id:
        paciente_edicao = conn.execute(
            "SELECT * FROM pacientes WHERE id = ?;", (editar_id,)
        ).fetchone()

    conn.close()

    return render_template(
        "pacientes.html",
        pacientes=pacientes_lista,
        paciente_edicao=paciente_edicao,
    )


@app.route("/pacientes/salvar", methods=["POST"])
def salvar_paciente():
    """Cadastra um novo paciente ou atualiza um existente."""
    paciente_id = request.form.get("id", "").strip()
    nome = request.form.get("nome", "").strip()
    telefone = request.form.get("telefone", "").strip()
    data_nascimento = request.form.get("data_nascimento", "").strip()

    if not nome or not telefone:
        flash("Nome e telefone são obrigatórios.", "erro")
        return redirect(url_for("listar_pacientes"))

    conn = get_connection()

    if paciente_id:
        conn.execute(
            """
            UPDATE pacientes
            SET nome = ?, telefone = ?, data_nascimento = ?
            WHERE id = ?;
            """,
            (nome, telefone, data_nascimento, paciente_id),
        )
        flash("Paciente atualizado com sucesso!", "sucesso")
    else:
        conn.execute(
            """
            INSERT INTO pacientes (nome, telefone, data_nascimento)
            VALUES (?, ?, ?);
            """,
            (nome, telefone, data_nascimento),
        )
        flash("Paciente cadastrado com sucesso!", "sucesso")

    conn.commit()
    conn.close()
    return redirect(url_for("listar_pacientes"))


@app.route("/pacientes/excluir/<int:id>", methods=["POST"])
def excluir_paciente(id):
    """Exclui um paciente (e suas consultas vinculadas) pelo ID."""
    conn = get_connection()
    conn.execute("DELETE FROM pacientes WHERE id = ?;", (id,))
    conn.commit()
    conn.close()

    flash("Paciente excluído com sucesso!", "sucesso")
    return redirect(url_for("listar_pacientes"))


@app.route("/api/pacientes")
def api_pacientes():
    """Endpoint de API que retorna todos os pacientes em formato JSON."""
    conn = get_connection()
    registros = conn.execute(
        "SELECT id, nome, telefone, data_nascimento FROM pacientes ORDER BY nome ASC;"
    ).fetchall()
    conn.close()

    return jsonify([dict(row) for row in registros])


@app.route("/api/consultas")
def api_consultas():
    """Endpoint de API que retorna as consultas ordenadas por dia e hora em JSON."""
    conn = get_connection()
    registros = conn.execute(
        """
        SELECT
            consultas.id,
            consultas.paciente_id,
            pacientes.nome AS paciente_nome,
            pacientes.telefone AS paciente_telefone,
            consultas.data,
            consultas.hora,
            consultas.motivo
        FROM consultas
        INNER JOIN pacientes ON consultas.paciente_id = pacientes.id;
        """
    ).fetchall()
    conn.close()

    consultas_ordenadas = ordenar_consultas_por_data_hora([dict(row) for row in registros])
    return jsonify(consultas_ordenadas)


if __name__ == "__main__":
    porta = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=porta, debug=True)
