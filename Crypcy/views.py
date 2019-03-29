from django.http import HttpResponse

def home(request):
	return HttpResponse("Hello from crypcy. What’s Satoshi’s favorite brand of sneakers? <br> \
			<img src='https://images.cointelegraph.com/images/740_Ly9jb2ludGVsZWdyYXBoLmNvbS9zdG9yYWdlL3VwbG9hZHMvdmlldy8wNmY3YTk1MDNiOWZiODg1ZGNlMjQ5ZDU3ZjA4OWIwMy5qcGc=.jpg'>  ")

