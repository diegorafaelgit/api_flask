from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost:3306/cadastroprodutos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Produto(db.Model):
    __tablename__ = 'produto'
    id_serial = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=True)
    custo = db.Column(db.Float, nullable=False)
    
    def to_dict(self):
        return {"id_serial": self.id_serial, "descricao": self.descricao, "custo": self.custo}

class Loja(db.Model):
    __tablename__ = 'loja'
    id_serial = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=True)
    
    def to_dict(self):
        return {"id_serial": self.id_serial, "descricao": self.descricao}
    
class ProdutoLoja(db.Model):
    __tablename__ = 'produtoloja'
    id_serial = db.Column(db.Integer, primary_key=True)
    idProduto = db.Column(db.Integer, nullable=True)
    idLoja = db.Column(db.Integer, nullable=True)
    precoVenda = db.Column(db.Float, nullable=False)
    
    def to_dict(self):
        return {"id_serial": self.id_serial, "idProduto": self.idProduto, "idLoja": self.idLoja, "precoVenda": self.precoVenda}

@app.route('/produtos', methods=['GET'])
def get_produtos():
    produtos = Produto.query.all()
    return jsonify([produto.to_dict() for produto in produtos])

@app.route('/produtos', methods=['POST'])
def adicionar_produto():
    data = request.get_json()
  
    if not data.get('descricao'):
        return jsonify({'error': 'Campo Descrição é de preenchimento obrigatório'}), 400

    descricao = data['descricao']
    custo = data['custo']
    
    novo_produto = Produto(descricao=descricao, custo=custo)
    db.session.add(novo_produto)
    db.session.commit()

    return jsonify(novo_produto.to_dict()), 201

@app.route('/produtos/<int:id_serial>', methods=['PUT'])
def atualizar_produto(id_serial):
    produto = Produto.query.get(id_serial)
    if not produto:
        return jsonify({'error': 'Produto não encontrado'}), 404

    data = request.get_json()

    if 'descricao' in data:
        produto.descricao = data['descricao']
    if 'custo' in data:
        produto.custo = data['custo']
    
    db.session.commit()
    return jsonify(produto.to_dict())

@app.route('/produtos/<int:id_serial>', methods=['DELETE'])
def deletar_produto(id_serial):
    produto = Produto.query.get(id_serial)
    if not produto:
        return jsonify({'error': 'Produto não encontrado'}), 404

    db.session.delete(produto)
    db.session.commit()
    return jsonify({'message': 'Produto excluído com sucesso'}), 200

@app.route('/lojas', methods=['GET'])
def get_lojas():
    lojas = Loja.query.all()
    return jsonify([loja.to_dict() for loja in lojas])

@app.route('/produto_lojas/<int:idProduto>', methods=['GET'])
def get_produto_lojas(idProduto):
    produto_lojas = ProdutoLoja.query.filter_by(idProduto=idProduto).all()
    return jsonify([produto_loja.to_dict() for produto_loja in produto_lojas])

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)