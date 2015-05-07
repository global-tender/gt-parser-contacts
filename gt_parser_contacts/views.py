from django.conf import settings
from django.http import StreamingHttpResponse
from django.template import RequestContext, loader

def index(request):
    template = loader.get_template('index.html')
    template_args = {
        'content': 'index_content.html',
        'request': request,
        'title': '',
    }
    context = RequestContext(request, template_args)
    return StreamingHttpResponse(template.render(context))