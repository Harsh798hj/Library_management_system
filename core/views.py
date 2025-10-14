from rest_framework import generics, permissions, status
from .models import  User, Book, CartItem, IssuedBook, SavedForLater
from rest_framework.response import Response
from datetime import timedelta
from django.utils import timezone
from .serializers import BookSerializer, UserSerializer, CartItemSerializer, IssuedBookSerializer, SavedForLaterSerializer


class BookReportView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        # Sirf librarian ko allow karna
        if user.role != 'librarian':
            return Book.objects.none()

        sort = self.request.query_params.get('sort')
        author = self.request.query_params.get('author')
        if author:
            qs = qs.filter(author__icontains=author)
        if sort == 'most_issued':
            qs = qs.order_by('-total_issued_count')
        elif sort == 'least_issued':
            qs = qs.order_by('total_issued_count')
        return qs
    
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        sort = self.request.query_params.get('sort')
        author = self.request.query_params.get('author')
        if author:
            qs = qs.filter(author__icontains=author)
        if sort == 'most_issued':
            qs = qs.order_by('-total_issued_count')
        elif sort == 'least_issued':
            qs = qs.order_by('total_issued_count')
        return qs

class AddBookView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        if self.request.user.role != 'librarian':
            raise PermissionError("Only librarians can add books.")
        serializer.save()

class DeleteBookView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if self.request.user.role != 'librarian':
            raise PermissionError("Only librarians can delete books.")
        instance.delete()

class CartItemView(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
class CheckoutView(generics.CreateAPIView):
    serializer_class = IssuedBookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response(
                {"msg": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        issued_books = []
        total_price = 0

        for item in cart_items:
            issued = IssuedBook.objects.create(
                user=request.user,
                book=item.book,
                issue_date=timezone.now(),
                return_date=timezone.now() + timedelta(days=14),
                price_at_issue=item.book.price
            )
            issued_books.append(issued)
            total_price += float(item.book.price)
            item.book.total_issued_count += 1
            item.book.save()

      
        cart_items.delete()
        
        bill_summary = {
            "customer": request.user.username,
            "total_books": len(issued_books),
            "total_amount": total_price,
            "issue_date": timezone.now().date(),
            "return_date": (timezone.now() + timedelta(days=14)).date(),
        }

        return Response(
            {
                "msg": "Books issued successfully!",
                "bill_summary": bill_summary,
                "issued_books": IssuedBookSerializer(issued_books, many=True).data,
            },
            status=status.HTTP_201_CREATED,
        )


class SavedForLaterView(generics.ListCreateAPIView):
    serializer_class = SavedForLaterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavedForLater.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class IssuedBooksListView(generics.ListAPIView):
    serializer_class = IssuedBookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "librarian":
            return IssuedBook.objects.select_related("book", "user").all().order_by("-issue_date")
        else:
            return IssuedBook.objects.filter(user=user).select_related("book").order_by("-issue_date")

