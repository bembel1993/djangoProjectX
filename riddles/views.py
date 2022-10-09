# Базовый класс для обработки страниц с формами.
import form as form
import self as self
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import FormView
# Спасибо django за готовую форму регистрации.
from django.contrib.auth.forms import UserCreationForm
# Спасибо django за готовую форму аутентификации.
from django.contrib.auth.forms import AuthenticationForm
# Функция для установки сессионного ключа.
# По нему django будет определять,
# выполнил ли вход пользователь.
from django.contrib.auth import login

# базовый URL приложения, главной страницы -
# часто нужен при указании путей переадресации
from riddles.models import Riddle, Option

app_url = "/riddles/"

# главная страница со списком загадок
def index(request):
    message = None
    if "message" in request.GET:
        message = request.GET["message"]
    # создание HTML-страницы по шаблону index.html
    # с заданными параметрами latest_riddles и message
    return render(
        request,
        "index.html",
        {
            "latest_riddles":
                Riddle.objects.order_by('-pub_date')[:5],
            "message": message
        }
    )


# страница загадки со списком ответов
def detail(request, riddle_id):
    error_message = None
    if "error_message" in request.GET:
        error_message = request.GET["error_message"]
    return render(
        request,
        "answer.html",
        {
            "riddle": get_object_or_404(Riddle, pk=riddle_id),
            "error_message": error_message
        }
    )

# 
# обработчик выбранного варианта ответа -
# сам не отдает страниц, а только перенаправляет (redirect)
# на другие страницы с передачей в GET-параметре
# сообщения для отображения на этих страницах
def answer(request, riddle_id):
    riddle = get_object_or_404(Riddle, pk=riddle_id)
    try:
        option = riddle.option_set.get(pk=request.POST['option'])
    except (KeyError, Option.DoesNotExist):
        return redirect(
            '/riddles/' + str(riddle_id) +
            '?error_message=Option does not exist',
        )
    else:
        if option.correct:
            return redirect(
                "/riddles/?message=Nice! Choose another one!")
        else:
            return redirect(
                '/riddles/'+str(riddle_id)+
                '?error_message=Wrong Answer!',
            )


# наше представление для регистрации
class RegisterFormView(FormView):
# будем строить на основе
# встроенной в django формы регистрации
    form_class = UserCreationForm
# Ссылка, на которую будет перенаправляться пользователь
# в случае успешной регистрации.
# В данном случае указана ссылка на
# страницу входа для зарегистрированных пользователей.
    success_url = app_url + "login/"
# Шаблон, который будет использоваться
# при отображении представления.
    template_name = "reg/register.html"
    def form_valid(self, form):
# Создаём пользователя,
# если данные в форму были введены корректно.
        form.save()
# Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)

# наше представление для входа
class LoginFormView(FormView):
# будем строить на основе
# встроенной в django формы входа
    form_class = AuthenticationForm
# Аналогично регистрации,
# только используем шаблон аутентификации.
    template_name = "reg/login.html"
# В случае успеха перенаправим на главную.
    success_url = app_url
    def form_valid(self, form):
# Получаем объект пользователя
# на основе введённых в форму данных.
        self.user = form.get_user()
# Выполняем аутентификацию пользователя.login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)