from django.http import Http404, HttpResponseNotFound
from django.shortcuts import render, redirect
from MainApp.models import Snippet, Comment, Tarif, Account, Elektro
from MainApp.forms import SnippetForm, UserForm, CommentForm, TarifForm, AccountForm, ElektroForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def get_base_context(request, pagename):
    return {
        'pagename': pagename
    }

def index_page(request):
    context = get_base_context(request, 'СНТ САДОВОД СЧАСТЛИВОЕ БАРЫБИНО')
    return render(request, 'pages/index.html', context)


def add_snippet_page_old(request):
    context = get_base_context(request, 'Добавление новой заметки')
    return render(request, 'pages/add_snippet.html', context)


def snippets_page(request):
    context = get_base_context(request, 'Просмотр заметок')
    snippets_all=Snippet.objects.all()
    paginator=Paginator(snippets_all,5)
    page = request.GET.get('page')
    try:
        snippets=paginator.page(page)
    except PageNotAnInteger:
        snippets=paginator.page(1)
    except EmptyPage:
        snippets=paginator.page(paginator.num_pages)
    context.update({"snippets": snippets})
    context.update({"count": snippets_all.count()})
    return render(request, 'pages/view_snippets.html', context)


def snippets_page_privat(request):
    context = get_base_context(request, 'Просмотр заметок')
    snippets=Snippet.objects.filter(visible=True)
    context.update({"snippets": snippets})
    return render(request, 'pages/view_snippets.html', context)


@login_required()
def snippets_page_my (request):
    context = get_base_context(request, 'Просмотр  Моих заметок')
    snippets=Snippet.objects.filter(user=request.user)
    context.update({"snippets": snippets})
    return render(request, 'pages/view_snippets.html', context)


@login_required()
def add_snippet_page(request):
    if request.method=='POST':
        form=SnippetForm(request.POST)
        if form.is_valid():
            snippet=form.save(commit=False)
            snippet.user=request.user
            snippet.save()
            return redirect ('list_snippet')
        context = get_base_context(request, 'Добавление новой заметки')
        context['form'] = form
        return render(request, 'pages/add_snippet.html', context)
    elif request.method=='GET':
        context = get_base_context(request, 'Добавление новой заметки')
        form=SnippetForm()
        context['form']=form
        return render(request, 'pages/add_snippet.html', context)


def account_add(request):
    if request.method=='POST':
        account_form=AccountForm(request.POST)
        #print (request.POST)
        #print(request.user)
        user = request.POST['user']
        if account_form.is_valid :
            account=account_form.save(commit=False)
            account.user=User.objects.get(id=user)
            account.save()
            return redirect('view_account',user)
        context['account_form'] = account_form
        context['account'] = account
        context['user'] = account.user
        return render(request, 'pages/account_create', context)
    elif request.method =='GET':
        account_form=AccountForm ()
        context['account_form']=account_form
        #context['account'] = account
        context['user'] = request.user
        #context['button']='EDIT'
        return render(request,'pages/account_create.html',context)
    raise Http404


def new_tarif (request):
    form= TarifForm()
    return render( request, 'pages/add_newtarif.html', {'form' : form })


@user_passes_test (lambda u: u.is_superuser )
def add_new_tarif (request):
    if request.method == 'POST':
        form = TarifForm(request.POST)
        if form.is_valid():
            tarif = form.save(commit=False)
            tarif.save()
            return redirect('view_tarif')
        context = get_base_context(request, 'Ввод нового тарифв')
        context['form'] = form
        return render(request, 'pages/add_newtarif.html', context)
    elif request.method == 'GET':
        context = get_base_context(request, 'Ввод нового тарифв')
        form = TarifForm()
        context['form'] = form
        return render(request, 'pages/add_newtarif.html', context)


def tarif_page(request):
    context = get_base_context(request, 'Просмотр тарифов')
    tarif_all=Tarif.objects.all()
    tarif_act=Tarif.objects.last()
    paginator=Paginator(tarif_all,5)
    page = request.GET.get('page')
    try:
        tarifs=paginator.page(page)
    except PageNotAnInteger:
        tarifs=paginator.page(1)
    except EmptyPage:
        tarifs=paginator.page(paginator.num_pages)
    context.update({"tarifs": tarifs})
    context.update({"count": tarif_all.count()})
    context.update({"tarif_act": tarif_act})
    return render(request, 'pages/view_tarifs.html', context)


@login_required()
def add_elektro_page(request):
    el_old = Elektro.objects.filter(user=request.user).last()
    if el_old == None:
        el_old = Elektro(user=request.user, el_acc=0, account= None, comment='Initial value')
    if request.method=='POST':
        form=ElektroForm(request.POST)
        if form.is_valid():
            elektro=form.save(commit=False)
            if elektro.el_acc >= el_old.el_acc:
                elektro.user=request.user
                tarif=Tarif.objects.last()
                account=Account(user=request.user,amount= -int((elektro.el_acc - el_old.el_acc)*tarif.tarif),comment=(f'Ввод показаний счетчика {elektro.creation_date}'))
                account.save()
                elektro.account=account
                elektro.save()
                return redirect ('view_account',request.user.id)
        context = get_base_context(request, 'Добавлены новые показания')
        context['form'] = form
        context['user'] = request.user
        context['el_old'] = el_old.el_acc
        return render(request, 'pages/add_elektro.html', context)
    elif request.method=='GET':
        context = get_base_context(request, 'Ввод показаний счетчика')
        form=ElektroForm()
        context['form']=form
        context['el_old'] = el_old.el_acc
        context['user'] = request.user
        return render(request, 'pages/add_elektro.html', context)


def snippet_create (request):
    form= SnippetForm()
    return render( request, 'pages/add_snippet.html', {'form': form})


def comments_view_all (request):
    comments_all=Comment.objects.all()
    context = get_base_context(request, 'Просмотр списка комментариев к заметкам')
    context['count'] = comments_all.count()
    paginator = Paginator (comments_all,7)
    page=request.GET.get ('page')
    try:
        comments=paginator.page(page)
    except PageNotAnInteger:
        comments=paginator.page(1)
    except EmptyPage:
        comments=paginator.page(paginator.num_pages)
    context['comments']=comments
    return render(request,'pages/view_comments.html', context)


def snippet_view (request,id=0):
    #print ('method', request.method)
    #print (request.POST)
    #return None
    context = get_base_context(request, 'Просмотр выбранной заметки')
    if id== 0:
        id=request.POST['id']

    try:
        snippet = Snippet.objects.get(id=id)
        comments= Comment.objects.filter(snippet=snippet)
        context.update({"snippet": snippet})
        context.update({"comments": comments})
        comment_form=CommentForm()
        context.update({"comment_form": comment_form})
    #redirect ('view_one_snippet')
        return render(request, 'pages/view_one_snippet.html', context)
    except Snippet.DoesNotExist :
        return HttpResponseNotFound ('<h2> ЗАМЕТКА не найдена! </h2>')


def test_page (request):
    users=User.objects.all()
    context=get_base_context(request, 'test_page test')
    context.update({"users": users})
    return render (request, 'pages/test_page.html', context)


@login_required()
def snippet_delete (request,id):
    try:
        #id=request.POST['id']
        snippet=Snippet.objects.get(id=id)
    except Snippet.DoesNotExist:
        return HttpResponseNotFound('<h3> ЗАМЕТКА не найдена! </h3>')
    snippet.delete ()
    context = get_base_context(request, 'Просмотр заметок')
    snippets = Snippet.objects.all()
    context.update({"snippets": snippets})
    return render(request, 'pages/view_snippets.html', context)


def comment_delete (request,id):
    try:
        #id=request.POST['id']
        comment=Comment.objects.get(id=id)
    except Comment.DoesNotExist:
        return HttpResponseNotFound('<h3> Комментарий не найден </h3>')
    comment.delete ()
    return redirect('view_comments')


@login_required()
def snippet_edit (request, id):
    context={'pagename': 'Редактирование заметки'}
    try:
        snippet=Snippet.objects.get(id=id)
    except Snippet.DoesNotExist:
        return HttpResponseNotFound('<h3> Заметка не найдена! </h3>')
    if request.method =='GET':
        form=SnippetForm(instance=snippet)
        context['form']=form
        context['button']='EDIT'
        return render(request,'pages/add_snippet.html',context)
    elif request.method == 'POST':
        snippet = Snippet.objects.get(id=id)
        form=SnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            form.save()
            return redirect('list_snippet')
        context['form'] = form
        return render(request, 'pages/add_snippet.html', context)


def account_edit (request, id):
    context={'pagename': 'Редактирование платежа'}
    try:
        account=Account.objects.get(id=id)
    except Account.DoesNotExist:
        return HttpResponseNotFound('<h3> Платеж не найден! </h3>')
    user = account.user
    if request.method =='GET':
        account_form=AccountForm (instance=account)
        context['account_form']=account_form
        context['account'] = account
        context['user'] = account.user
        context['button']='EDIT'
        return render(request,'pages/account_create.html',context)
    elif request.method == 'POST':
        #account = Account.objects.get(id=id)
        account_form=AccountForm(request.POST, instance=account) #form=SnippetForm(request.POST, instance=snippet)
        if account_form.is_valid():
            account_form.save()
            return redirect('view_account', user.id)
        context['account_form'] = account_form
        context['account'] = account
        context['user'] = account.user
        return render(request, 'pages/account_create.html', context)


def login_page(request):
   if request.method == 'POST':
       username = request.POST.get("username")
       password = request.POST.get("password")
       user = auth.authenticate(request, username=username, password=password)
       if user is not None:
           auth.login(request, user)
       else:
           # Return error message
           pass
   return redirect('home')


def logout_page (request):
    auth.logout(request)
    return redirect('home')


def create_user (request):
    if request.method == 'GET':
        form=UserForm()
        context=get_base_context(request,'Создание пользователя садовода')
        context['form']=form
        return render(request,'pages/add_user.html',context)
    elif request.method == 'POST':
        form=UserForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active=True
            user.set_password(user.password)
            user.save()
            return redirect('home')
        context['form']=form
        return render(request, 'pages/add_user.html', context)


def comment_add(request):
    if request.method=='POST':
        comment_form=CommentForm(request.POST)
        #print (request.POST)
        #print(request.user)
        id = request.POST['snippet']
        if comment_form.is_valid:
            comment=comment_form.save(commit=False)
            comment.author=request.user
            comment.snippet=Snippet.objects.get(id=id)
            #print(comment.author, '  ', comment.snippet, ' ', comment.text, '!!')
            comment.save()
        return redirect('list_snippet')
    raise Http404


def account_view (request,id=0):
    #print ('method', request.method)
    #print (request.POST)
    #return None
    context = get_base_context(request, 'Просмотр лицевого счета садовода')
    if id== 0:
        id=request.POST['id']

    try:

        user=User.objects.get(id=id)
        account = Account.objects.filter(user=user)
        ballance=sum(account.values_list('amount',flat=True))
        #for items in account:
        #    ballance+=items.amount
        last_pay=account.last()
        paginator = Paginator(account, 8)
        page = request.GET.get('page')
        try:
            accounts = paginator.page(page)
        except PageNotAnInteger:
            accounts = paginator.page(1)
        except EmptyPage:
            accounts = paginator.page(paginator.num_pages)
        context.update({"account": accounts})
        context.update({"ballance": ballance})
        account_form=AccountForm()
        context.update({"last_pay": last_pay})
        context.update({"account_form": account_form})
        context.update({"user": user})
    #redirect ('view_one_snippet')
        return render(request, 'pages/view_account.html', context)
    except Account.DoesNotExist :
        return HttpResponseNotFound ('<h2> Счет не найден! </h2>')


def users_view_all (request):
    users_all=User.objects.all()
    context = get_base_context(request, 'Просмотр списка садоводов')
    paginator = Paginator (users_all,7)
    page=request.GET.get ('page')
    try:
        users=paginator.page(page)
    except PageNotAnInteger:
        users=paginator.page(1)
    except EmptyPage:
        users=paginator.page(paginator.num_pages)
    context['users']=users
    return render(request,'pages/view_users.html', context)


def elektro_view_all (request):
    elektro_all=Elektro.objects.all()
    count=elektro_all.count()
    context = get_base_context(request, 'Просмотр показаний счетчиков')
    paginator = Paginator (elektro_all,7)
    page=request.GET.get ('page')
    try:
        elektro=paginator.page(page)
    except PageNotAnInteger:
        elektro=paginator.page(1)
    except EmptyPage:
        elektro=paginator.page(paginator.num_pages)
    context['elektro']=elektro
    context['count']=count
    return render(request,'pages/view_elektro.html', context)


def elektro_delete (request,id):
    try:
        #id=request.POST['id']
        elektro=Elektro.objects.get(id=id)
    except Elektro.DoesNotExist:
        return HttpResponseNotFound('<h3> Операция не найдена </h3>')
    elektro.delete()
    try:
        account = Account.objects.get(id=elektro.account.id)
    except Account.DoesNotExist:
        return HttpResponseNotFound('<h3> Операция не найдена </h3>')
    except elektro.account == None:
        return HttpResponseNotFound('<h3> Операция не найдена </h3>')
    account.delete ()
    return redirect('elektro_view_all')


def account_add_cred(request):
    if request.method=='POST':
        account_form=AccountForm(request.POST)
        #print (request.POST)
        #print(request.user)
        user = request.POST['user']
        if account_form.is_valid :
            account=account_form.save(commit=False)
            account.user=User.objects.get(id=user)
            if account.amount>0:
                account.amount=-account.amount
            #print(comment.author, '  ', comment.snippet, ' ', comment.text, '!!')
            account.save()
        return redirect('view_account',user)
    raise Http404


def account_add_deb(request):
    if request.method=='POST':
        account_form=AccountForm(request.POST)
        #print (request.POST)
        #print(request.user)
        user = request.POST['user']
        if account_form.is_valid :
            account=account_form.save(commit=False)
            account.user=User.objects.get(id=user)
            if account.amount<0:
                account.amount=-account.amount
            account.save()
        return redirect('view_account',user)
    raise Http404


def account_delete (request,id):
    try:
        #id=request.POST['id']
        account=Account.objects.get(id=id)
        user=account.user
    except Account.DoesNotExist:
        return HttpResponseNotFound('<h3> Операция не найдена </h3>')
    account.delete ()
    return redirect('view_account',user.id)

def view_one_account (request,id=0):
    context = get_base_context(request, 'Просмотр конкретной операции')
    if id== 0:
        id=request.POST['id']

    try:
        account=Account.objects.get(id=id)
        user=account.user
        context.update({"account": account})
        context.update({"user": user})
        #account_form=AccountForm()
        #context.update({"account_form": account_form})
    #redirect ('view_one_snippet')
        return render(request, 'pages/view_one_account.html', context)
    except Account.DoesNotExist :
        return HttpResponseNotFound ('<h2> Счет не найден! </h2>')


def account_view_personal (request):
    #print ('method', request.method)
    #print (request.POST)
    #return None
    context = get_base_context(request, 'Просмотр лицевого счета садовода')
    user=request.user
    account = Account.objects.filter(user=user)
    ballance=sum(account.values_list('amount',flat=True))
    #for items in account:
       #ballance+=items.amount
    paginator = Paginator(account, 8)
    page = request.GET.get('page')
    try:
        accounts = paginator.page(page)
    except PageNotAnInteger:
        accounts = paginator.page(1)
    except EmptyPage:
        accounts = paginator.page(paginator.num_pages)
    last_pay=account.last()
    context.update({"account": accounts})
    context.update({"ballance": ballance})
    account_form=AccountForm()
    context.update({"last_pay": last_pay})
    context.update({"account_form": account_form})
    context.update({"user": user})
    #redirect ('view_one_snippet')
    return render(request, 'pages/view_account.html', context)


def add_total_account(request):
    users = User.objects.all()
    count = users.count()
    if request.method=='POST':
        form=AccountForm(request.POST)
        if form.is_valid():
            total_acc=form.save(commit=False)
            if total_acc.amount !=0:
                payment=round(total_acc.amount/count,0)
                for user in users:
                    account=Account(user=user,amount = -payment, comment=total_acc.comment)
                    account.save()
                return redirect ('users_view_all')
        context = get_base_context(request, 'Рапределение общего начисления на всех садоводов')
        context['form'] = form
        return render(request, 'pages/add_total_payment.html', context)
    elif request.method=='GET':
        context = get_base_context(request, 'Рапределение общего начисления на всех садоводов')
        form=AccountForm()
        context['form']=form
        return render(request, 'pages/add_total_payment.html' , context)

def ballance_view (request):
    users=User.objects.all()
    context = get_base_context(request, 'Просмотр баланса по СНТ')
    users_acc=[]
    for user in users:
        account_user=Account.objects.filter(user=user)
        acc_sum=sum(account_user.values_list('amount',flat=True))
        users_acc.append((user,acc_sum))
    paginator = Paginator (users_acc,7)
    page=request.GET.get ('page')
    try:
        users_info=paginator.page(page)
    except PageNotAnInteger:
        users_info=paginator.page(1)
    except EmptyPage:
        users_info=paginator.page(paginator.num_pages)
    context['users']=users_info
    accounts=Account.objects.all()
    sum_total=sum(accounts.values_list('amount',flat=True))
    #for account in accounts:
    #    sum_total+=account.amount
    if sum_total > 0:
        context['comment'] = 'переплата'
    elif sum_total < 0:
        context['comment'] = 'задолженность'
    else:
        context['comment'] = 'задолженности и переплат нет'
    context['sum']=abs(sum_total)
    return render(request,'pages/ballance_view.html', context)