from rest_framework.pagination import PageNumberPagination


class FilePagination(PageNumberPagination):
    page_size = 5  # Number of items per page
    page_size_query_param = 'page_size'  # Allow the client to specify a page size
    max_page_size = 100  # Max page size limit
