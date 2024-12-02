from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    is_librarian = models.BooleanField(default=False)
    profile_image = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'user'

class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField()
    genre = models.CharField(max_length=50)
    published_date = models.DateField()
    cover_image = models.CharField(max_length=255, null=True, blank=True)
    available_copies = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.author}"
    
    class Meta:
        db_table = 'book'

class Shelf(models.Model):
    shelf_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shelf_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'shelf'
        unique_together = ['user', 'shelf_type']

    def __str__(self):
        return f"{self.user.username}'s {self.shelf_type} shelf"

class ShelfBook(models.Model):
    shelf_book_id = models.AutoField(primary_key=True)
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'shelf_book'
        unique_together = ['shelf', 'book']

    def __str__(self):
        return f"{self.book.title} in {self.shelf.user.username}'s {self.shelf.shelf_type}"

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'review'
        unique_together = ['user', 'book']

    def __str__(self):
        return f"{self.user.username}'s review of {self.book.title}"