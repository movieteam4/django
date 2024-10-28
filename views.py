from myapp.models import Dreamreal,createAccount,verifiedAccount,Favorite,massage,user_liked
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.templatetags.static import static
from django import forms
from .models import Dreamreal
from myapp.forms import LoginForm
import re
from django.urls import reverse
from django.middleware import csrf
import pandas as pd
import datetime
import base64
import mysql.connector
from django.core.cache import cache
# from myapp.call_dataframe import call_dataframe
from myapp.html_show import html_show
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg
from django.db import IntegrityError
'123111121233'
show_data='暫無資料'
db_config = {
    'host': 'u3r5w4ayhxzdrw87.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',         # 資料庫伺服器地址 (可以是 IP 或域名)
    'user': 'dhv81sqnky35oozt',     # 資料庫使用者名稱
    'password': 'rrdv8ehsrp8pdzqn', # 資料庫密碼
    'database': 'xltc236odfo1enc9',  # 要使用的資料庫名稱
}
# if 'logged_in' in request.session:
#     mail=request.session['logged_in']
#     account=verifiedAccount.objects.get(mail=mail)
def search(request):
    m=request.POST.get('searchKeyword')
    return redirect(f'https://taiwan-movies-36c4c3ac2ec6.herokuapp.com/Taiwan_movies_all/more_detail/?m={m}')
def user_more(request):
    if request.method =='POST':
        df = cache.get('address')
        if df is None:
            print('沒有暫存')
            from myapp.call_dataframe import address
            df=address()
            cache.set('address',df)
        else:
            print('找到了暫存')
        dict_road = {}
        dict_town = {}
        same_list=[]
        list_city = list(df["縣市名稱"].unique())
        # 讀取所有縣市
        for city_name in list_city:
            dict_town[city_name] = list(df[(df["縣市名稱"] == city_name)]["鄉鎮市區"].unique())
            for n,town_name in enumerate(dict_town[city_name]):
                if town_name in same_list:
                    town_name=city_name[:-1]+town_name
                    dict_town[city_name][n]=town_name
                    dict_road[town_name] = list(df[(df["縣市名稱"] == city_name) & (df["鄉鎮市區"] == town_name[2:])]["街路聚落名稱"].unique())
                else:
                    dict_road[town_name] = list(df[(df["縣市名稱"] == city_name) & (df["鄉鎮市區"] == town_name)]["街路聚落名稱"].unique())
                same_list.append(town_name)
        mail=request.POST.get('email_address')
        account = verifiedAccount.objects.get(mail=mail)
        account.name=request.POST.get('name')
        if request.POST.get('date_of_birth'):
            try:
                account.date_of_birth=request.POST.get('date_of_birth')
            except:
                account.date_of_birth=datetime.strptime(request.POST.get('date_of_birth'),'%Y-%m-%d')
        account.mobile_phone=request.POST.get('mobile_phone')
        account.national_id=request.POST.get('national_id')
        account.occupation=request.POST.get('occupation')
        account.favorite_cinema=request.POST.get('favorite_cinema')
        account.marital_status=request.POST.get('marital_status')
        account.household_income=request.POST.get('household_income')
        account.gender=request.POST.get('sex')
        account.education=request.POST.get('education')
        account.favorite_genres=request.POST.getlist('f_genres')
        account.preferences=request.POST.getlist('seat')
        try:
            account.address=request.POST.get('city')+request.POST.get('district')+request.POST.get('road')+request.POST.get('address')
        except:
            pass
        detail='資料輸入完成'
        account.save()
        mail=request.session['logged_in']
        account=verifiedAccount.objects.get(mail=mail)
        name=account.name
        date_of_birth=str(account.date_of_birth)
        mobile_phone=account.mobile_phone
        national_id=account.national_id
        address=account.address
        occupation=account.occupation
        favorite_cinema=account.favorite_cinema
        marital_status=account.marital_status
        household_income=account.household_income
        sex=account.gender
        education=account.education
        favorite_genres=account.favorite_genres
        print(favorite_genres)
        seat=account.preferences
        print(seat)
        return render(request,'user_more.html',locals())

    if 'logged_in' in request.session:
        df = cache.get('address')
        if df is None:
            print('沒有暫存')
            from myapp.call_dataframe import address
            df=address()
            cache.set('address',df)
        else:
            print('找到了暫存')
        dict_road = {}
        dict_town = {}
        same_list=[]
        list_city = list(df["縣市名稱"].unique())
        # 讀取所有縣市
        for city_name in list_city:
            dict_town[city_name] = list(df[(df["縣市名稱"] == city_name)]["鄉鎮市區"].unique())
            for n,town_name in enumerate(dict_town[city_name]):
                if town_name in same_list:
                    town_name=city_name[:-1]+town_name
                    dict_town[city_name][n]=town_name
                    dict_road[town_name] = list(df[(df["縣市名稱"] == city_name) & (df["鄉鎮市區"] == town_name[2:])]["街路聚落名稱"].unique())
                else:
                    dict_road[town_name] = list(df[(df["縣市名稱"] == city_name) & (df["鄉鎮市區"] == town_name)]["街路聚落名稱"].unique())
                same_list.append(town_name)
        mail=request.session['logged_in']
        account=verifiedAccount.objects.get(mail=mail)
        name=account.name
        date_of_birth=str(account.date_of_birth)
        mobile_phone=account.mobile_phone
        national_id=account.national_id
        address=account.address
        occupation=account.occupation
        favorite_cinema=account.favorite_cinema
        marital_status=account.marital_status
        household_income=account.household_income
        sex=account.gender
        favorite_genres=account.favorite_genres
        seat=account.preferences
        education=account.education
        return render(request,'user_more.html',locals())
    else:
        return redirect('https://taiwan-movies-36c4c3ac2ec6.herokuapp.com/Taiwan_movies_all/?detail=請先登入會員')
def Line(request):
    return render(request,'Line.html',locals())
def initialise(request):
    from myapp.call_dataframe import call_dataframe ,week_ranking
    final_data=week_ranking(call_dataframe())
    cache.set('dataframe',final_data)
    print('暫存已設置')
    res='暫存已設置'
    return render(request,'initialise.html', {'res': res})
def contact(request):
    return render(request,'contact.html')
def product_details(request):
    return render(request,'product_details.html')
def shop(request):
    Favorite_movies_list=[]
    mail=False
    favorite=request.GET.get('favorite','')
    status = request.GET.get('status','')
    detail = request.GET.get('detail','')
    if status=='Sign_out':
        if 'logged_in' in request.session:
            del request.session['logged_in']
            return redirect('/Taiwan_movies_all/shop/?detail=已登出')
    if 'logged_in' in request.session:
        mail=request.session.get('logged_in')
        account=verifiedAccount.objects.filter(mail=mail).first()
        name=account.name
        Favorite_movies=Favorite.objects.filter(mail=mail)
        for movie in Favorite_movies:
                Favorite_movies_list.append(movie.which_movie)
        account=verifiedAccount.objects.filter(mail=mail).first()
        name=account.name
        if name=='' or name is None:
            name='無名的遊盪者'
        status='signed_in'
    else:
         status='signed_out'
    csrf_token = csrf.get_token(request)
    form_action_url = reverse('Taiwan_movies_all')
    final_data = cache.get('dataframe')
    if final_data is None:
        from myapp.call_dataframe import call_dataframe ,week_ranking
        final_data=week_ranking(call_dataframe())
        cache.set('dataframe',final_data)  #暫存
    from myapp.show_more_filter import filter_show
    res=filter_show(final_data,Favorite_movies_list,mail)
    return render(request,'shop.html',locals())
def Taiwan_movies_all(request):
    mail=False
    global show_data , db_config
    Favorite_movies_list=[]
    if request.method !='POST':
        status = request.GET.get('status','''<li><a href="/signin">Sign in</a></li>''' )
        detail = request.GET.get('detail','')
        create_e_mail = request.GET.get('create_e_mail','')
        if create_e_mail!='':
            request.session['logged_in']=create_e_mail
            user = createAccount.objects.filter(mail=create_e_mail).first()
            create_password=user.password
            name=user.name
            verifiedAccount(mail=create_e_mail,password=create_password,name=name).save()
        detail = request.GET.get('detail','' )
        if status=='sign_out':
            if 'logged_in' in request.session:
                del request.session['logged_in']
            return redirect('/Taiwan_movies_all/?detail=已登出')
        elif 'logged_in' in request.session:
            mail=request.session.get('logged_in')
            account=verifiedAccount.objects.filter(mail=mail).first()
            name=account.name
            Favorite_movies=Favorite.objects.filter(mail=mail)
            for movie in Favorite_movies:
                 Favorite_movies_list.append(movie.which_movie)
            if name=='' or name is None:
                name='無名的遊盪者'
            status=f''' <li><a href="https://taiwan-movies-36c4c3ac2ec6.herokuapp.com/Taiwan_movies_all/user_more"><i class="fas fa-user"></i>{name}</a></li>
                        <li><a href="/Taiwan_movies_all?status=sign_out">Sign out</a></li>
                        '''
        csrf_token = csrf.get_token(request)
        form_action_url = reverse('Taiwan_movies_all')

        final_data = cache.get('dataframe')
        if final_data is not None:
            print('找到了暫存')
            res=html_show(final_data,Favorite_movies_list,mail)
            number_1=final_data['宣傳照'].iloc[0]
            description=final_data['簡介'].iloc[0]
            number_1_name=final_data['中文片名'].iloc[0]
            number_1_name_eng=final_data['英文片名'].iloc[0]
            description=description[:len(description)//3]+'...'
            cache.set('dataframe',final_data)
            return render(request,'Taiwan_movie_all.html', locals())
        print('沒有暫存,要重新加載資料庫')
        from myapp.call_dataframe import call_dataframe ,week_ranking
        final_data=week_ranking(call_dataframe())
        cache.set('dataframe',final_data)
        res=html_show(final_data,Favorite_movies_list,mail)
        number_1=final_data['宣傳照'].iloc[0]
        description=final_data['簡介'].iloc[0]
        number_1_name=final_data['中文片名'].iloc[0]
        number_1_name_eng=final_data['英文片名'].iloc[0]
        description=description[:len(description)//3]+'...'
        # number_1_name=re.sub(r'[^0-9a-zA-Z\u4e00-\u9fa5]', '', number_1_name)
        return render(request,'Taiwan_movie_all.html', locals())
    else:
        status='''<li><a href="/signin">Sign in</a></li>'''
        if request.session.get('logged_in') =='logged_in':
            status='''<li><a href="/Taiwan_movies_all">Sign out</a></li>'''
        csrf_token = csrf.get_token(request)
        form_action_url = reverse('Taiwan_movies_all')
        final_data = cache.get('dataframe')
        if final_data is not None:
            print('找到了暫存')
            res=html_show(final_data,Favorite_movies_list,mail)
            number_1=final_data['宣傳照'].iloc[0]
            description=final_data['簡介'].iloc[0]
            number_1_name=final_data['中文片名'].iloc[0]
            number_1_name_eng=final_data['英文片名'].iloc[0]
            description=description[:len(description)//3]+'...'
            cache.set('dataframe',final_data)
            # number_1_name=re.sub(r'[^0-9a-zA-Z\u4e00-\u9fa5]', '', number_1_name)
            return render(request,'Taiwan_movie_all.html', locals())
        print('沒有暫存,要重新加載資料庫')
        from myapp.call_dataframe import call_dataframe ,week_ranking
        final_data=week_ranking(call_dataframe())
        cache.set('dataframe',final_data)
        res=html_show(final_data)
        number_1=final_data['宣傳照'].iloc[0]
        description=final_data['簡介'].iloc[0]
        number_1_name=final_data['中文片名'].iloc[0]
        number_1_name_eng=final_data['英文片名'].iloc[0]
        description=description[:len(description)//3]+'...'
        return render(request,'Taiwan_movie_all.html', locals())
def hello(request):
    if request.method=='POST':
        where_from=request.POST.get('where_from')
        if where_from=='create_account':
            return render(request,'create_account.html')
        elif where_from=='from_create':
            create_e_mail = request.POST.get('create_e_mail')
            name=request.POST.get('create_name')
            create_password_1 = request.POST.get('create_password_1')
            create_password_2 = request.POST.get('create_password_2')
            pattern=re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
            if not re.match(pattern,create_e_mail):
                detail='信箱不正確'
                return render(request,'create_account.html',locals())
            pattern=re.compile(r'^(?=.*[A-Z])[A-Za-z0-9]{8,}$')
            if createAccount.objects.filter(mail=create_e_mail).exists()==False:
                if create_password_2 !=create_password_1 :
                    detail='密碼不一樣'
                    return render(request,'create_account.html',locals())
                elif not re.match(pattern,create_password_1):
                    detail='密碼強度不夠'
                    return render(request,'create_account.html',locals())
                createAccount(mail=create_e_mail,password=create_password_2,name=name).save()
                res = send_mail("驗證信", "comment tu vas?", "ian27368885@gmail.com", [create_e_mail], html_message=f'<a href="https://taiwan-movies-36c4c3ac2ec6.herokuapp.com/Taiwan_movies_all/?detail=帳號驗證完成&create_e_mail={create_e_mail}" class="button">點我驗證帳號</a>')
                detail='驗證信已寄出,請查收'
                return render(request,'hello.html',locals())
            else:
                 detail='信箱已註冊'
                 return render(request,'create_account.html',locals())
        elif where_from=='from_log_in':
            e_mail = request.POST.get('e_mail')
            password=request.POST.get('password')
            user=verifiedAccount.objects.filter(mail=e_mail)
            for i in user:
                if i.password==password:
                    request.session['logged_in']=i.mail
                    response=redirect('/Taiwan_movies_all')
                    response.set_cookie('e_mail',e_mail)
                    return response
                else:
                     detail='密碼錯誤'
                     return render(request,'hello.html',locals())
            user=createAccount.objects.filter(mail=e_mail)
            for i in user:
                res = send_mail("驗證信", "comment tu vas?", "ian27368885@gmail.com", [e_mail], html_message=f'<a href="https://taiwan-movies-36c4c3ac2ec6.herokuapp.com/Taiwan_movies_all/?detail=帳號驗證完成&create_e_mail={e_mail}" class="button">點我驗證帳號</a>')
                detail='驗證信已寄出,請查收'
                return render(request,'hello.html',locals())
            detail='無此帳號'
            return render(request,'hello.html',locals())
        elif where_from=='from_log_out':
            e_mail=request.COOKIES.get('e_mail')
            for i in verifiedAccount.objects.filter(mail=e_mail):
                password=i.password
            detail='已登出'
            del request.session['logged_in']
            return render(request,'hello.html',locals())
    else:
        if request.session.get('logged_in') =='logged_in':
            return redirect('/Taiwan_movies_all')
        detail=request.GET.get('detail')
        create_e_mail=request.GET.get('create_e_mail')
        if detail==None:
            return render(request,'hello.html')
        users = createAccount.objects.filter(mail=create_e_mail)
        for user in users:
            create_password=user.password
            name=user.name
        verifiedAccount(mail=create_e_mail,password=create_password,name=name).save()
        return render(request,'hello.html',locals())
    return render(request,'hello.html')
def check_email(request):
    email = request.GET.get('#id_email', None)
    email_exists = False   # 初始化檢查結果
    # 檢查信箱是否已存在
    if email:
        email_exists = createAccount.objects.filter(email_address=email).exists()
    # 返回 JSON 給前端
    return JsonResponse({'email_exists': email_exists})
def handle(request):
    if request.method =='POST':
        if 'logged_in' in request.session:
            liked = request.POST.get('liked')  # 取得是否勾選 (True or False)
            movie_title = request.POST.get('movie_title')  # 取得電影名稱
            mail=request.session['logged_in']
        else:
            detail='請先登入'
            return JsonResponse({
            'detail':detail
        })
        if liked =='true':
             Favorite(mail=mail,which_movie= movie_title).save()
             print('資料已新增')
        else:
            favorite = Favorite.objects.get(mail=mail,which_movie= movie_title)
            favorite.delete()
            print('資料已刪除')
        movie_title = request.POST.get('movie_title')  # 取得電影名稱
        print(movie_title)
        return JsonResponse({
            'status': 'success',
            'liked': liked,
            'movie_title': movie_title,
        })
def favorite_page(request):
    if 'logged_in' in request.session:
        return redirect('https://taiwan-movies-36c4c3ac2ec6.herokuapp.com/Taiwan_movies_all/shop/?favorite=favorite')
    else:
        return redirect('https://taiwan-movies-36c4c3ac2ec6.herokuapp.com/Taiwan_movies_all/?detail=請先登入')
def about_us(request):
    return render(request,'about_us.html')
def more_detail(request):
    status = request.GET.get('status','')
    movie_name=request.GET.get('m','')
    check=''
    mail=''
    if status=='Sign_out':
        if 'logged_in' in request.session:
            del request.session['logged_in']
            return redirect('/Taiwan_movies_all/shop/?detail=已登出')
    if 'logged_in' in request.session:
        mail=request.session.get('logged_in')
        account=verifiedAccount.objects.filter(mail=mail).first()
        name=account.name
        favorite=Favorite.objects.filter(mail=mail,which_movie= movie_name ).first()
        if favorite:
            check='checked'
        if name=='' or name is None:
            name='無名的遊盪者'
        status='signed_in'
    else:
         status='signed_out'
    csrf_token = csrf.get_token(request)
    final_data = cache.get('more_detail')
    if final_data is None:
        from myapp.call_dataframe import call_dataframe
        final_data=call_dataframe()
        cache.set('more_detail',final_data)  #暫存
    # cinema_list = final_data[final_data['中文片名']==movie_name].groupby('電影院名稱').count().index
    img=final_data[final_data['中文片名']==movie_name]['宣傳照'].iloc[0]
    actors=final_data[final_data['中文片名']==movie_name]['演員'].iloc[0]
    if pd.isna(actors) or actors =='':
        actors = "沒有演員"
    director=final_data[final_data['中文片名']==movie_name]['導演'].iloc[0]
    if pd.isna(director) or director=='':
        director = "沒有導演"
    eng_name=final_data[final_data['中文片名']==movie_name]['英文片名'].iloc[0]
    release_date=final_data[final_data['中文片名']==movie_name]['上映日'].iloc[0]
    release_date=re.sub(r'\D', '', release_date)
    release_date=release_date[:4]+'-'+release_date[4:6]+'-'+release_date[6:]
    cinema_group=final_data[final_data['中文片名']==movie_name].groupby('影城').count().index
    description=final_data[final_data['中文片名']==movie_name]['簡介'].iloc[0]
    youtube=final_data[final_data['中文片名']==movie_name]['youtube'].iloc[0]
    mass_obj = massage.objects.filter(which_movie=movie_name).exclude(what_manage="team4_star_rating").order_by('creat_at')
    liked = user_liked.objects.filter(mail=mail)
    liked_list=[]
    for i in liked:
        liked_list.append(int(i.which_id))
        print(type(i.which_id))
    print(liked_list)
    average_rating = massage.objects.filter(what_manage="team4_star_rating",which_movie=movie_name).aggregate(Avg('rating'))
    try:
        personal_rating=massage.objects.get(what_manage="team4_star_rating",which_movie=movie_name,mail=mail)
        personal_rating=personal_rating.rating
    except ObjectDoesNotExist:
        personal_rating=''
    if average_rating['rating__avg'] is not None:
        average_rating=f'{average_rating["rating__avg"]:.1f}'
    else:
        average_rating=''
    # movie_name=re.sub(r'[^\u4e00-\u9fa5]', '', movie_name)
    if movie_name =="辣手警探2":
        release_date='2024-10-18'
        actors='黃晸珉、吳達洙、張允柱、吳代煥、金時厚、丁海寅'
        director='柳承完'

    return render(request,"more_detail.html",locals())

def get_cinemas(request):
    final_data = cache.get('more_detail')
    if final_data is None:
        from myapp.call_dataframe import call_dataframe
        final_data=call_dataframe()
        cache.set('more_detail',final_data)  #暫存
    movie_name = request.GET.get('back_movie')
    cinema_group = request.GET.get('back_cinema_group')
    print(len(final_data))
    print(cinema_group)
    # group_key=''
    # if '威秀' in cinema_group:
    #     group_key='威秀'
    #     cinemas = final_data[(final_data['中文片名'] == movie_name) & (final_data['電影院名稱'].str.contains(group_key,case=False))]['電影院名稱'].unique().tolist()+['MUVIE CINEMAS']
    #     return JsonResponse({'cinemas': cinemas})
    # elif '秀泰' in cinema_group:
    #     group_key='秀泰'
    #     final_data=final_data[final_data['電影院名稱'].str.contains(group_key,case=False)]
    #     print(len(final_data))
    # elif '國賓' in cinema_group:
    #     group_key='國賓'
    # elif '美麗華' in cinema_group:
    #     group_key='美麗華'
    # elif '美麗新' in cinema_group:
    #     group_key='美麗新'
    # elif '新光' in cinema_group:
    #     group_key='新光'
    # print(group_key)
    cinemas = final_data[(final_data['中文片名'] == movie_name) & (final_data['影城']==cinema_group)]['電影院名稱'].unique().tolist()
    print(cinemas)
    return JsonResponse({'cinemas': cinemas})
def get_dates(request):
    final_data = cache.get('more_detail')
    if final_data is None:
        from myapp.call_dataframe import call_dataframe
        final_data=call_dataframe()
        cache.set('more_detail',final_data)  #暫存
    movie_name = request.GET.get('back_movie')
    cinema_name = request.GET.get('back_cinema')
    dates = final_data[(final_data['中文片名'] == movie_name) & (final_data['電影院名稱'] == cinema_name)]['日期'].unique().tolist()
    return JsonResponse({'dates': dates})

def get_times(request):
    final_data = cache.get('more_detail')
    if final_data is None:
        from myapp.call_dataframe import call_dataframe
        final_data=call_dataframe()
        cache.set('more_detail',final_data)  #暫存
    movie_name = request.GET.get('back_movie')
    cinema_name = request.GET.get('back_cinema')
    print(cinema_name)
    date = request.GET.get('back_date')
    times = final_data[(final_data['中文片名'] == movie_name) & (final_data['電影院名稱'] == cinema_name) & (final_data['日期'] == date)]['時刻表'].tolist()
    print(type(times))
    print(times)
    types = final_data[(final_data['中文片名'] == movie_name) & (final_data['電影院名稱'] == cinema_name) & (final_data['日期'] == date)]['廳位'].tolist()
    if '新光' in cinema_name:
        types=[cinema_name]*len(times)
    links=final_data[(final_data['中文片名'] == movie_name) & (final_data['電影院名稱'] == cinema_name)]['time_link'].tolist()
    return JsonResponse({'times': times,'types':types,'links':links})
def massage123(request):
        #登錄才有session
        if request.session.has_key('logged_in'):
        #抓session確定是哪個用戶
            mail = request.session.get('logged_in')
            user = verifiedAccount.objects.get(mail=mail)
            name=user.name
            #對哪部電影評論  抓Movie.id?!
            movie=request.POST.get('movieName')
            print(movie)
            #chinses=final_data[final_data["英文片名"]==movie].iloc[:,0]
            #評論內容
            mass=request.POST.get('massage','')
            print(mass)
            #開始時間
            today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            #計算兩個時間字串之間的時間差
            today_end = today_start + timedelta(days=1)
            #今日沒留言過+1分
            if not massage.objects.filter(mail=mail,creat_at__range=(today_start,today_end)).exists():
                user.score+=1
                user.save()

            #留言存資料庫
            new_mass =massage.objects.create(
                mail=mail,
                which_movie=movie,
                what_manage=mass,
                creat_at=timezone.now(),
                name=name
                )
            new_mass.save()
            print(new_mass.id)
            return JsonResponse({
                'success': True,
                'author': user.name,
                'massage': new_mass.what_manage,
                'created_at': '剛剛',
                'id':new_mass.id,
                'init_like':0
            })
def forum(request):
    status = request.GET.get('status','')
    detail = request.GET.get('detail','')
    check=''
    if status=='Sign_out':
        if 'logged_in' in request.session:
            del request.session['logged_in']
            return redirect('/Taiwan_movies_all/shop/?detail=已登出')
    if 'logged_in' in request.session:
        mail=request.session.get('logged_in')
        account=verifiedAccount.objects.filter(mail=mail).first()
        name=account.name
        if name=='' or name is None:
            name='無名的遊盪者'
        status='signed_in'
    else:
         status='signed_out'
    posts = massage.objects.filter(which_movie='team4_forum')
    return render(request,"forum.html",locals())
def create_post(request):
    status = request.GET.get('status','')
    detail = request.GET.get('detail','')
    check=''
    if status=='Sign_out':
        if 'logged_in' in request.session:
            del request.session['logged_in']
            return redirect('/Taiwan_movies_all/shop/?detail=已登出')
    if 'logged_in' in request.session:
        mail=request.session.get('logged_in')
        account=verifiedAccount.objects.filter(mail=mail).first()
        name=account.name
        if name=='' or name is None:
            name='無名的遊盪者'
        status='signed_in'
    else:
         status='signed_out'
         return redirect('https://taiwan-movies-36c4c3ac2ec6.herokuapp.com/Taiwan_movies_all/?detail=請先登入')
    if request.method =='POST':
        img=request.FILES.get('image')
        if img:
            import requests

            # Imgur API 客戶端ID
            CLIENT_ID = '10ba5360e0c6073'

            # 上傳圖片的路徑
            image_path = img  # 比如 'image.jpg'


            headers = {
                'Authorization': f'Client-ID {CLIENT_ID}',
                'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
            }
            url = 'https://api.imgur.com/3/upload'

            files = {'image': img}
            response = requests.post(url, headers=headers, files=files)

            # 確保上傳成功
            if response.status_code == 200:
                data = response.json()
                link = data['data']['link']  # 獲得圖片的 URL
            else:
                return redirect('https://taiwan-movies-36c4c3ac2ec6.herokuapp.com/Taiwan_movies_all/forum?detail=發布失敗')
        else:
            link=''
        create_post=massage.objects.create(
        mail=mail,
        which_movie='team4_forum',
        title=request.POST.get('title'),
        comment=request.POST.get('post'),
        img=link,
        creat_at=timezone.now(),
        name=name)
        create_post.save()
        return redirect('https://taiwan-movies-36c4c3ac2ec6.herokuapp.com/Taiwan_movies_all/forum?detail=發布成功')
    else:
        return render(request,"create_post.html",locals())
def post(request):
    status = request.GET.get('status','')
    detail = request.GET.get('detail','')
    check=''
    if status=='Sign_out':
        if 'logged_in' in request.session:
            del request.session['logged_in']
            return redirect('/Taiwan_movies_all/shop/?detail=已登出')
    if 'logged_in' in request.session:
        mail=request.session.get('logged_in')
        account=verifiedAccount.objects.filter(mail=mail).first()
        name=account.name
        if name=='' or name is None:
            name='無名的遊盪者'
        status='signed_in'
    else:
         status='signed_out'
    id=request.GET.get('post','')
    post=massage.objects.get(id=id)
    try:
        comments = massage.objects.filter(which_movie=f'post_id_{id}')
    except massage.DoesNotExist:
        pass
    if post.img:
        print(post.img)
        img=post.img.split('/')[-1]
        print(img)
        img=f"https://i.imgur.com/{img}"
    return render(request,"post.html",locals())
def delete_comment(request, comment_id):
    try:
        # 获取指定 ID 的评论
        comment = massage.objects.get(id=comment_id)
        comment.delete()  # 删除评论
        return JsonResponse({'success': True})
    except massage.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Comment not found'})
def edit_comment(request):
    comment_id = request.POST.get('comment_id')
    print(comment_id)
    new_text=request.POST.get('new_text')
    print(new_text)
    mass=massage.objects.get(id=comment_id)
    mass.what_manage=new_text
    mass.save()
    res=f'''<div id="comment_{mass.id}">
              <strong>{mass.name}:</strong>
              <p>{mass.what_manage} </p>
              <em style="font-size: 10px; opacity: 0.7;">{mass.creat_at}</em>
              <button onclick="deleteComment({mass.id})">刪除留言</button>
              <button onclick="editComment({mass.id})">編輯</button>'''
    return JsonResponse({'success': True,'res':res})
def edit_post(request):
    status = request.GET.get('status','')
    detail = request.GET.get('detail','')
    check=''
    if status=='Sign_out':
        if 'logged_in' in request.session:
            del request.session['logged_in']
            return redirect('/Taiwan_movies_all/shop/?detail=已登出')
    if 'logged_in' in request.session:
        mail=request.session.get('logged_in')
        account=verifiedAccount.objects.filter(mail=mail).first()
        name=account.name
        if name=='' or name is None:
            name='無名的遊盪者'
        status='signed_in'
    else:
         status='signed_out'
    if request.method =='POST':
        # img=request.FILES.get('image')
        # if img:
        #     import requests

        #     # Imgur API 客戶端ID
        #     CLIENT_ID = '10ba5360e0c6073'

        #     # 上傳圖片的路徑
        #     image_path = img  # 比如 'image.jpg'


        #     headers = {
        #         'Authorization': f'Client-ID {CLIENT_ID}',
        #         'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
        #     }
        #     url = 'https://api.imgur.com/3/upload'

        #     files = {'image': img}
        #     response = requests.post(url, headers=headers, files=files)

        #     # 確保上傳成功
        #     if response.status_code == 200:
        #         data = response.json()
        #         link = data['data']['link']  # 獲得圖片的 URL
        #     else:
        #         return redirect('https://taiwan-movies-36c4c3ac2ec6.herokuapp.com/Taiwan_movies_all/forum?detail=發布失敗')
        # else:
        #     link=''
        edited_post=massage.objects.get(id=request.POST.get('post_id'))
        edited_post.comment=request.POST.get('post')
        edited_post.title=request.POST.get('title')
        edited_post.save()
        return redirect('https://taiwan-movies-36c4c3ac2ec6.herokuapp.com/Taiwan_movies_all/forum?detail=編輯成功')
    else:
        movie_id=request.GET.get('movie_id','')
        post=massage.objects.get(id=movie_id)
        return render(request,'edit_post.html',locals())
def star(request):
    if request.session.has_key('logged_in'):
        mail = request.session.get('logged_in')
    else:
        return redirect('https://taiwan-movies-36c4c3ac2ec6.herokuapp.com/Taiwan_movies_all/?detail=請先登入會員')
    try:
        user_star = massage.objects.get(mail=mail,what_manage="team4_star_rating",which_movie=request.POST.get('movie'))
        user_star.rating=request.POST.get('rating')
        user_star.save()
    except ObjectDoesNotExist:
        new_star=massage.objects.create(
            what_manage="team4_star_rating",
            mail=mail,
            rating=request.POST.get('rating'),
            which_movie=request.POST.get('movie'),
            creat_at=timezone.now()
        )
        new_star.save()
    average_rating = massage.objects.filter(what_manage="team4_star_rating",which_movie=request.POST.get('movie')).aggregate(Avg('rating'))
    print(average_rating['rating__avg'])
    return JsonResponse({
            'success': True,
            'average_rating':f"{average_rating['rating__avg']:.1f}"
        })
def tomato(request):
    from myapp.tomato import get_tomatos,simplify_release_date
    release_date=simplify_release_date(request.POST.get('release_date'))[:4]
    print(release_date)
    eng_movie=request.POST.get('eng_movie')
    print(eng_movie)
    score=f"🍅 爛番茄指數為{get_tomatos(eng_movie,release_date)}"
    if get_tomatos(eng_movie,release_date)=='%' or get_tomatos(eng_movie,release_date)=='':
         score='🍅 尚未有爛番茄指數'
    return JsonResponse({
            'success': True,
            'score': score
        })

def massage_like(request):
    if request.method =='POST':
        try:
            #登錄才有session
            if request.session.has_key('logged_in'):
                #抓session確定是哪個用戶
                e_mail=request.session.get('logged_in')
                user=verifiedAccount.objects.get(mail=e_mail)
                comment_id = request.POST.get('commentId')
                isLiked = request.POST.get('isLiked')
                mail=request.POST.get('mail')
                print(comment_id)
                if isLiked =='true':
                    comment = massage.objects.get(id=comment_id)
                    comment.like_count+=1
                    comment.save()
                    try:
                        liked=user_liked.objects.create(mail=mail,which_id=comment_id)
                    except IntegrityError:
                        print("This entry already exists.")

                else:
                    comment = massage.objects.get(id=comment_id)
                    comment.like_count-=1
                    comment.save()
                    try:
                        liked = user_liked.objects.get(mail=mail, which_id=comment_id)
                        liked.delete()
                    except ObjectDoesNotExist:
                        print("This entry does not exist.")

                # 返回新的點讚數量
                print(comment.like_count)
                return JsonResponse({'success': True, 'new_like_count': comment.like_count})

            else:
                return HttpResponse('用戶未登錄')
        except massage.DoesNotExist:
            return JsonResponse({'error': '找不到該評論'}, status=404)
        except verifiedAccount.DoesNotExist:
            return JsonResponse({'error': '找不到用戶'}, status=404)