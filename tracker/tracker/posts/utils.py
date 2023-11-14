from django.core.paginator import Paginator

POSTS_PEG_PAGE = 10


def pagination(request, obj):
    paginator = Paginator(obj, POSTS_PEG_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj