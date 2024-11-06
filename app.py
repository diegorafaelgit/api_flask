from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost:3306/my_bd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Produto(db.Model):
    __tablename__ = 'produtos'
    id_serial = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    custo = db.Column(db.Float, nullable=False)
    
    def to_dict(self):
        return {"id_serial": self.id_serial, "descricao": self.descricao, "custo": self.custo}

class Loja(db.Model):
    __tablename__ = 'lojas'
    id_serial = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    
    def to_dict(self):
        return {"id_serial": self.id_serial, "descricao": self.descricao}

db = SQLAlchemy(app)

@app.route('/produtos', methods=['GET'])
def get_produtos():
    produtos = Produto.query.all()
    return jsonify([produto.to_dict() for produto in produtos])

@app.route('/lojas', methods=['GET'])
def get_lojas():
    lojas = Loja.query.all()
    return jsonify([loja.to_dict() for loja in lojas])

# @app.route('/produtos', methods=['GET'])
# def get_produtos():
#     return jsonify(produtos) 

# @app.route('/lojas', methods=['GET'])
# def get_lojas():
#     return jsonify(lojas) 

# @app.route('/produtos', methods=['POST'])
# def create_produto():
#     produto = request.json
#     produtos.append(produto)
#     return produto

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)