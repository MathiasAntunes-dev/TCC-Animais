import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from models.database import inicializar_banco
from models.usuario import (
    criar_usuario,
    verificar_login
)

from models.pet import (
    listar_pets,
    criar_pet,
    buscar_pet_por_id
)

from models.match import curtir_pet, listar_matches_usuario

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

# Cria as tabelas automaticamente
inicializar_banco()


# =========================
# HOME
# =========================
@app.route("/")
def home():
    return render_template("home.html")


# =========================
# CADASTRO
# =========================
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":

        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        sucesso = criar_usuario(
            nome,
            email,
            senha
        )

        if sucesso:
            flash("Cadastro realizado com sucesso!")
            return redirect(url_for("login"))

        flash("E-mail já cadastrado!")

    return render_template("cadastro.html")


# =========================
# LOGIN
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        senha = request.form["senha"]

        usuario = verificar_login(
            email,
            senha
        )

        if usuario:

            session["usuario_id"] = usuario["id"]
            session["usuario_nome"] = usuario["nome"]

            return redirect(url_for("feed"))

        flash("Email ou senha inválidos.")

    return render_template("login.html")


# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))


# =========================
# FEED DOS PETS
# =========================
@app.route("/feed")
def feed():

    pets = listar_pets()

    return render_template(
        "feed.html",
        pets=pets
    )

@app.route("/cadastrar_pet", methods=["GET", "POST"])
def cadastrar_pet():

    if "usuario_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        nome = request.form["nome"]
        idade = request.form["idade"]
        especie = request.form["especie"]
        raca = request.form["raca"]
        sexo = request.form["sexo"]
        descricao = request.form["descricao"]
        whatsapp = request.form["whatsapp"]

        arquivo = request.files.get("foto")

        foto = ""

        if arquivo and arquivo.filename:

            nome_arquivo = secure_filename(
                arquivo.filename
            )

            caminho = os.path.join(
                "static",
                "uploads",
                nome_arquivo
            )

            arquivo.save(caminho)

            foto = f"uploads/{nome_arquivo}"

        criar_pet(
            nome,
            idade,
            especie,
            raca,
            sexo,
            descricao,
            foto,
            whatsapp,
            session["usuario_id"]
        )

        flash("Pet cadastrado com sucesso!")

        return redirect(url_for("feed"))

    return render_template("cadastrar_pet.html")


@app.route("/perfil_pet/<int:pet_id>")
def perfil_pet(pet_id):

    pet = buscar_pet_por_id(pet_id)

    if not pet:
        return "Pet não encontrado", 404

    return render_template(
        "perfil_pet.html",
        pet=pet
    )

@app.route("/curtir/<int:pet_id>")
def curtir(pet_id):

    if "usuario_id" not in session:
        return redirect(url_for("login"))

    sucesso = curtir_pet(
        session["usuario_id"],
        pet_id
    )

    if sucesso:
        flash("❤️ Pet curtido com sucesso!")
    else:
        flash("⚠️ Você já curtiu este pet.")

    return redirect(
        url_for(
            "perfil_pet",
            pet_id=pet_id
        )
    )
    

@app.route("/meus_matches")
def meus_matches():

    if "usuario_id" not in session:
        return redirect(url_for("login"))

    matches = listar_matches_usuario(
        session["usuario_id"]
    )

    return render_template(
        "meus_matches.html",
        matches=matches
    )


if __name__ == "__main__":
    app.run(debug=True)