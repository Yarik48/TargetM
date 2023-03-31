from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegisterUserForm, LoginUserForm, UserForm, ProfileForm
from .models import User, Group, Chat, Message


def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('index')
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'mainapp/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'mainapp/login.html'


    def get_success_url(self):
        return reverse_lazy('index')


def logout_user(request):
    logout(request)
    return redirect('login')

def index(request):
    # Получаем список чатов для пользователя
    chats = Chat.objects.filter(members=request.user)
    # Получаем список групп, в которых состоит пользователь
    groups = request.user.group_set.all().order_by('-id')
    return render(request, 'mainapp/index.html', {'chats': chats, 'groups': groups})

@login_required
def chat(request, chat_id):
    # Получаем чат по идентификатору
    chat = get_object_or_404(Chat, id=chat_id)
    # Проверяем, является ли пользователь участником чата
    if request.user not in chat.members.all():

        return redirect('index')
    # Получаем сообщения чата
    messages = chat.message_set.order_by('timestamp')
    return render(request, 'mainapp/chat.html', {'chat': chat, 'messages': messages})

@login_required
def group(request, group_id):
    # Получаем группу по идентификатору
    group = get_object_or_404(Group, id=group_id)
    # Проверяем, является ли пользователь участником группы
    if request.user not in group.members.all():
        messages.error(request, 'Вы не участник этой группы')
        return redirect('index')
    # Получаем чаты, связанные с группой
    chats = Chat.objects.filter(group=group).order_by('-id')
    return render(request, 'mainapp/group.html', {'group': group, 'chats': chats})

@login_required
def create_chat(request):
    if request.method == 'POST':
        # Получаем данные из формы
        name = request.POST['name']
        ava = request.FILES['ava']
        group_id = request.POST.get('group_id')
        members = request.POST.getlist('members')
        # Создаем новый чат
        chat = Chat.objects.create(name=name, ava=ava)
        # Добавляем пользователей в чат
        chat.members.add(request.user)
        for member_id in members:
            member = User.objects.get(id=member_id)
            chat.members.add(member)
        # Если чат создается для группы, связываем его с группой
        if group_id:
            group = Group.objects.get(id=group_id)
            chat.group = group
            chat.save()
            return redirect('group', group_id=group.id)
        else:
            chat.save()
            return redirect('chat', chat_id=chat.id)
    else:
        # Получаем список пользователей
        users = User.objects.exclude(id=request.user.id)
        # Получаем список групп
        groups = request.user.group_set.all()
        return render(request, 'mainapp/create_chat.html', {'users': users, 'groups': groups})

@login_required
def send_message(request, chat_id):
    # Получаем чат по идентификатору
    chat = get_object_or_404(Chat, id=chat_id)
    # Проверяем, является ли пользователь участником чата
    if request.user not in chat.members.all():
        messages.error(request, 'Вы не участник этого чата')
        return redirect('index')
    if request.method == 'POST':
        # Получаем текст сообщения
        text = request.POST['text']
        # Создаем новое сообщение
        message = Message.objects.create(text=text, sender=request.user, chat=chat)
        return redirect('chat', chat_id=chat.id)
