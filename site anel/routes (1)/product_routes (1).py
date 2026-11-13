from flask import Blueprint, flash, render_template, request, redirect, url_for, session
from services.product_service import (create_product, get_products, get_product_by_id,
                                      get_products_by_user, update_product, delete_product,
                                      CATEGORIAS_DISPONIVEIS, MATERIAIS_DISPONIVEIS)
from .auth_decorator import login_required

product_bp = Blueprint('product', __name__, url_prefix='/produto', template_folder='templates')

@product_bp.route('/cadastro', methods=['GET', 'POST'])
@login_required
def cadastrar_produto():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        categoria = request.form.get('categoria', 'Acessório').strip()
        material = request.form.get('material', '').strip()
        tamanho = request.form.get('tamanho', '').strip()
        descricao = request.form.get('descricao', '').strip()
        preco = request.form.get('preco')
        quantidade = request.form.get('quantidade')
        usuario_id = session['user_id']

        try:
            create_product(nome, categoria, material, tamanho, descricao, float(preco), int(quantidade), usuario_id)
            flash("Acessório cadastrado com sucesso!", "success")
            return redirect(url_for('product.listar_produtos'))
        except (ValueError, KeyError) as e:
            flash(f"Erro ao cadastrar: {e}", "danger")
            return redirect(url_for('product.cadastrar_produto'))

    return render_template('cadastro_produto.html',
                           categorias=CATEGORIAS_DISPONIVEIS,
                           materiais=MATERIAIS_DISPONIVEIS)

@product_bp.route('/listar', methods=['GET'])
@login_required
def listar_produtos():
    usuario_id = session['user_id']
    produtos = get_products_by_user(usuario_id)
    return render_template('listar_produtos.html', produtos=produtos)

@product_bp.route('/editar/<int:produto_id>', methods=['GET', 'POST'])
@login_required
def editar_produto(produto_id):
    produto = get_product_by_id(produto_id)
    if not produto:
        flash("Acessório não encontrado.", "danger")
        return redirect(url_for('product.listar_produtos'))

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        categoria = request.form.get('categoria', produto.categoria).strip()
        material = request.form.get('material', '').strip()
        tamanho = request.form.get('tamanho', '').strip()
        descricao = request.form.get('descricao', '').strip()
        preco = request.form.get('preco')
        quantidade = request.form.get('quantidade')

        try:
            update_product(produto_id, nome, categoria, material, tamanho, descricao, float(preco), int(quantidade))
            flash("Acessório atualizado com sucesso!", "success")
            return redirect(url_for('product.listar_produtos'))
        except (ValueError, KeyError) as e:
            flash(f"Erro ao atualizar: {e}", "danger")
            return redirect(url_for('product.editar_produto', produto_id=produto_id))

    return render_template('editar_produto.html',
                           produto=produto,
                           categorias=CATEGORIAS_DISPONIVEIS,
                           materiais=MATERIAIS_DISPONIVEIS)

@product_bp.route('/deletar/<int:produto_id>', methods=['GET', 'POST'])
@login_required
def deletar_produto(produto_id):
    try:
        delete_product(produto_id)
        flash("Acessório removido com sucesso.", "success")
    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for('product.listar_produtos'))
