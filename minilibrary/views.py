from email import message
from django.http import HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from .models import Book, Review
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model 
from .forms import ReviewForm
from django.contrib import messages
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import time

User = get_user_model()
# Create your views here.
class Hello(View):
    def get(self, request):
        return HttpResponse("Hola mundo de CBV")

class WelcomeView(TemplateView):
    template_name = "minilibrary/welcome.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_books'] = Book.objects.count()
        return context
    
class BookListView(ListView):
    model = Book
    template_name = "minilibrary/book_list.html"
    context_object_name = "books"
    paginate_by = 5

class BookDetailView(LoginRequiredMixin,DetailView):
    model = Book
    template_name = "minilibrary/book_detail.html"
    context_object_name = "book"
    # slug_field = "slug" ## en caso de que aplique con slug
    # slug_url_kwarg = "slug" 
    def get(self, request, *args, **kwargs):
        if request.user.has_perm('minilibrary.view_book'):
            response = super().get(request, *args, **kwargs)
            request.session['last_viewed_book'] = self.object.id
            return response
        else:
            return HttpResponseForbidden('Contenido no disponible')

class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "minilibrary/add_review.html"
    
    def form_valid(self, form):
        book_id = self.kwargs.get("pk")
        book = Book.objects.get(pk=book_id)
        form.instance.book = book
        form.instance.user_id = 1 ## para pruebas
        messages.success(self.request, "Gracias por tu reseña")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("book_detail", kwargs={"pk":self.kwargs.get("pk")})

class ReviewUpdateView(UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = "minilibrary/add_review.html"
    
    def get_queryset(self):
        return Review.objects.filter(user_id=self.request.user.id)
    
    def form_valid(self, form):
        messages.success(self.request, "Se actualizo tu reseña, correctamente")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al guardar los cambios")
    
    def get_success_url(self):
        return reverse_lazy("book_detail", kwargs={"pk":self.object.book.id})

class ReviewDeleteView(PermissionRequiredMixin,DeleteView):
    permission_required = "minilibrary.delete_review"
    model = Review
    template_name = "minilibrary/review_confirm_delete.html"
    success_url = reverse_lazy("book_list")
    
    def get_queryset(self):
        return Review.objects.filter(user_id=self.request.user.id)
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Tu reseña fue eliminada.")
        return super().delete(request, *args, **kwargs)

@login_required
def index(request):
    try:
        books = Book.objects.all()
        query = request.GET.get("query_search")
        date_start = request.GET.get("start")
        date_end = request.GET.get("end")
        book_id_recommend = request.session.get('last_viewed_book')
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
        
        if book_id_recommend:
            try:
                last_book=Book.objects.get(pk=book_id_recommend)
            except Book.DoesNotExist:
                    last_book=None
        else:
            last_book=None
        
        return render(request, "minilibrary/minilibrary.html",{
            "page_obj": page_obj,
            "query": query,
            "query_string": query_string,
            "last_book": last_book
        })
    except Exception:
        return HttpResponseNotFound("Página no encontrada")
    
@permission_required('minilibrary.add_review')
def add_review(request,book_id):
    book = get_object_or_404(Book, id=book_id)
    form = ReviewForm(request.POST or None)
    
    if request.method == "POST":
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            messages.success(request, "Gracias por la reseña")
            return redirect("recommend_book", book_id=book_id)
        else:
            messages.error(request, "Corrige los errores del formulario", "danger")
    return render(request, "minilibrary/add_review.html",{
        "form":form,
        "book":book
    })
    
def time_test(request):
    time.sleep(2)
    return HttpResponse("Esta vista tardo 2 segundos")

def visit_counter(request):
    visits = request.session.get("visitas", 0)
    visits +=1
    request.session["visitas"] = visits
    request.session.set_expiry(15)
    # 300 -> 10 minutos, 0-> Al cerrar navegador, None -> duración por defecto
    return HttpResponse(f"Has visitado esta página {visits}")