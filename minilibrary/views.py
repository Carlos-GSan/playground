from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Review
from django.db.models import Q
from django.core.paginator import Paginator 
from .forms import ReviewSimpleForm, ReviewForm
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()
# Create your views here.
def index(request):
    try:
        books = Book.objects.all()
        query = request.GET.get("query_search")
        date_start = request.GET.get("start")
        date_end = request.GET.get("end")
        if query:
            books = books.filter(
                Q(title__icontains=query) | Q(author__name__icontains=query)                
            )
        if date_start and date_end:
            books = books.filter(publication_date__range=[date_start, date_end])
            
        paginator = Paginator(books, 5)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number) # ya vienen los libros paginados
        
        query_params = request.GET.copy() #copia los query_params para de filtros
        if "page" in query_params:
            query_params.pop("page")
        query_string = query_params.urlencode()
        
        return render(request, "minilibrary/minilibrary.html",{
            "page_obj": page_obj,
            "query": query,
            "query_string": query_string
        })
    except Exception:
        return HttpResponseNotFound("Página no encontrada")
    
def add_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    form = ReviewForm(request.POST or None)
    
    if request.method == "POST":
        if form.is_valid():
            review = form.save(commit=False) # commit=false, para el guardado de forma automática
            review.book = book # dato faltante
            review.user = request.user # dato faltante
            review.save() # ahora si guardamos
            messages.success(request, "Gracias por la reseña")
            return redirect("recommend_book", book_id=book.id)
        else:
            messages.error(request, "Corrige los errores del formulario")
            
    return render(request, "minilibrary/add_review.html", {
        "form": form,
        "book": book
    })