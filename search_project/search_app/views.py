import json
from decimal import Decimal

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from.models import Cart, Product, Category # Product モßデルをインポート
from .forms import ProductForm, SearchForm # フォームのインポート
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse  # reverseをインポート




def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST,)
        if form.is_valid():
            product = form.save()  # 保存したProductインスタンスを取得
            # 生成したproductの詳細ページへリダイレクト
            return redirect(reverse('product_detail', args=[product.pk]))
    else:
        form = ProductForm()  # GETリクエストや、POSTが無効な場合、新しいフォームを表示

    return render(request, 'product_form.html', {'form': form})

# def product_create(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('product_list')
#         else:
#             form = ProductForm()
#         return render(request, 'product_form.html', {'form': form})
    
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})
    
def product_update(request, pk): 
    product = get_object_or_404(Product, pk=pk) 
    if request.method == 'POST': 
        form = ProductForm(request.POST, instance=product) 
        if form.is_valid(): 
            form.save() 
            return redirect('product_detail', pk=product.pk) 
    else: 
        form = ProductForm(instance=product) 
    # product オブジェクトをテンプレートに渡す
    return render(request, 'product_form.html', {'form': form, 'product': product})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'product_confirm_delete.html', {'product': product})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def search_view(request):
    form = SearchForm(request.GET or None)
    results = Product.objects.all() # クエリセットの初期化
    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            results = results.filter(name__icontains=query)
    # カテゴリフィルタリング
    category_name = request.GET.get('category')
    if category_name:
        try:
            # カテゴリ名に基づいてカテゴリ ID を取得
            category = Category.objects.get(name=category_name)
            results = results.filter(category_id=category.id)
        except Category.DoesNotExist:
            results = results.none() # 存在しないカテゴリの場合、結果を空にする
            category = None
    # 価格のフィルタリング (最低価格・最高価格)
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        results = results.filter(price__gte=min_price)
    if max_price:
        results = results.filter(price__lte=max_price)
    
    # 並び替え処理
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price_asc':
        results = results.order_by('price')
    elif sort_by == 'price_desc':
        results = results.order_by('-price')

    #商品数の取得
    total_results = results.count()
    
    # クエリセットをリストに変換せず、直接Paginatorに渡す
    paginator = Paginator(results, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'search.html', {'form': form, 'page_obj': page_obj, 'total_results': total_results})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    print(f"Cart item saved: {cart_item}")
    print(f"Cart item quantity: {cart_item.quantity}")
    return redirect('cart_detail')


def cart_detail(request):
    cart_items = Cart.objects.filter(user=request.user)
    for item in cart_items:
        item.total_price = item.product.price * item.quantity  # 合計金額を計算
    return render(request, 'cart_detail.html', {'cart_items': cart_items})


def serialize_cart(cart_items):
    return json.dumps([
        {
            'name': item.product.name,
            'price': float(item.product.price),
            'quantity': item.quantity
        } for item in cart_items
    ])