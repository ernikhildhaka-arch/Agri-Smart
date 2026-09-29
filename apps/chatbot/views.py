from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .services import reply
@login_required
def chat(request):
    answer=None; message=''
    if request.method=='POST': message=request.POST.get('message','').strip(); answer=reply(message,request.user) if message else 'Please enter a question.'
    return render(request,'chatbot/chat.html',{'answer':answer,'message':message})
