import math
from rest_framework.response import Response
from rest_framework.pagination import CursorPagination


class BlogPagination(CursorPagination):
    """Custom pagination class for blog posts."""

    page_size = 10
    max_page_size = 100
    ordering = "-score"  # Order by score, descending
    page_size_query_param = "page_size"

    # pylint: disable=R0801
    def get_paginated_response(self, data):
        """Prepare the paginated response."""
        total_count = self.page.paginator.count
        total_pages = math.ceil(total_count / self.get_page_size(self.request))
        return Response(
            {
                "count": total_count,
                "total_pages": total_pages,  # Total number of pages
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )
