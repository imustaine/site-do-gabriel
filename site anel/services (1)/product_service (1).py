from models.models import Produto, db

CATEGORIAS_DISPONIVEIS = [
    "Jóia",
    "Anel",
    "Piercing",
    "Colar / Corrente",
    "Brinco",
    "Pulseira / Bracelete",
    "Tornozeleira",
    "Outro Acessório"
]

MATERIAIS_DISPONIVEIS = [
    "Prata 925",
    "Ouro 18k",
    "Ouro Branco",
    "Titânio Grau Implante (ASTM F-136)",
    "Aço Cirúrgico 316L",
    "Folheado a Ouro",
    "Ouro Rosé",
    "Outro"
]

def create_product(nome: str, categoria: str, material: str, tamanho: str, descricao: str, preco: float, quantidade: int, usuario_id: int) -> Produto:
    if not nome or preco is None or quantidade is None:
        raise ValueError("Por favor, preencha todos os campos obrigatórios.")

    produto = Produto(
        nome=nome,
        categoria=categoria or "Jóia / Acessório",
        material=material,
        tamanho=tamanho,
        descricao=descricao,
        preco=preco,
        quantidade=quantidade,
        usuario_id=usuario_id
    )
    db.session.add(produto)
    db.session.commit()
    return produto

def get_products() -> list[Produto]:
    return db.session.query(Produto).limit(50).all()

def get_product_by_id(produto_id: int) -> Produto:
    return db.session.query(Produto).filter_by(id=produto_id).first()

def get_products_by_user(usuario_id: int) -> list[Produto]:
    return db.session.query(Produto).filter_by(usuario_id=usuario_id).order_by(Produto.id.desc()).all()

def update_product(produto_id: int, nome: str, categoria: str, material: str, tamanho: str, descricao: str, preco: float, quantidade: int) -> Produto:
    produto = get_product_by_id(produto_id)
    if not produto:
        raise ValueError("Produto/Acessório não encontrado.")

    if not nome or preco is None or quantidade is None:
        raise ValueError("Por favor, preencha todos os campos obrigatórios.")

    produto.nome = nome
    produto.categoria = categoria or produto.categoria or "Jóia / Acessório"
    produto.material = material
    produto.tamanho = tamanho
    produto.descricao = descricao
    produto.preco = preco
    produto.quantidade = quantidade
    db.session.commit()
    return produto

def delete_product(produto_id: int) -> None:
    produto = get_product_by_id(produto_id)
    if not produto:
        raise ValueError("Produto/Acessório não encontrado.")

    db.session.delete(produto)
    db.session.commit()
