from rest_framework.pagination import CursorPagination


class CreatedAtPaginator(CursorPagination):
    page_size = 16
    ordering = '-created_at'
