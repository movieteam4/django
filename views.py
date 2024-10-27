from myapp.models import Dreamreal,createAccount,verifiedAccount,Favorite,massage
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
        from myapp.call_dataframe import address # 從 call_dataframe 中匯入 address 方法以取得地址資訊
        df=address() # 呼叫 address 方法並將其回傳結果存入 df
        dict_road = {} # 初始化一個空字典以存儲每個鄉鎮的街路聚落名稱
        dict_town = {} # 初始化一個空字典以存儲縣市中的鄉鎮市區名稱
        same_list=[] # 初始化一個空清單以避免重複的鄉鎮名稱
        list_city = ['選擇縣市']+list(df["縣市名稱"].unique()) # 取得所有縣市的名稱並加上 '選擇縣市' 選項
        # 讀取所有縣市並分組存入 dict_town 和 dict_road
        for city_name in list_city:
            dict_town[city_name] = list(df[(df["縣市名稱"] == city_name)]["鄉鎮市區"].unique()) # 根據縣市名稱取得所有鄉鎮市區名稱並存入 dict_town
            for n,town_name in enumerate(dict_town[city_name]):
                if town_name in same_list: # 若鄉鎮名稱已在 same_list 中，避免重複
                    town_name=city_name[:-1]+town_name # 以縣市名稱的部分字母拼接區分鄉鎮名稱
                    dict_town[city_name][n]=town_name # 更新 dict_town 的鄉鎮名稱
                    dict_road[town_name] = list(df[(df["縣市名稱"] == city_name) & (df["鄉鎮市區"] == town_name[2:])]["街路聚落名稱"].unique()) # 存入街路聚落名稱
                else:
                    dict_road[town_name] = list(df[(df["縣市名稱"] == city_name) & (df["鄉鎮市區"] == town_name)]["街路聚落名稱"].unique()) # 直接存入街路聚落名稱
                same_list.append(town_name) # 加入同名鄉鎮至 same_list 避免重複
        # 從 POST 請求中取得使用者資料
        mail=request.POST.get('email_address') # 取得使用者的電子郵件地址
        account = verifiedAccount.objects.get(mail=mail) # 根據郵件地址從 verifiedAccount 資料表中查找使用者
        account.name=request.POST.get('name') # 更新使用者名稱
        # 取得使用者生日，並處理日期格式
        if request.POST.get('date_of_birth'):
            try:
                account.date_of_birth=request.POST.get('date_of_birth') # 直接設定生日
            except:
                account.date_of_birth=datetime.strptime(request.POST.get('date_of_birth'),'%Y-%m-%d') # 若出現錯誤，將日期格式轉換
        # 取得其他使用者資料
        account.mobile_phone=request.POST.get('mobile_phone') # 取得手機號碼
        account.national_id=request.POST.get('national_id') # 取得身分證字號
        account.occupation=request.POST.get('occupation') # 取得職業
        account.favorite_cinema=request.POST.get('favorite_cinema') # 取得最常去的影城
        account.marital_status=request.POST.get('marital_status') # 取得婚姻狀況
        account.household_income=request.POST.get('household_income') # 取得年收入
        account.gender=request.POST.get('sex') # 取得性別
        account.education=request.POST.get('education') # 取得教育程度
        account.favorite_genres=request.POST.getlist('f_genres') # 取得使用者喜愛的電影類型
        account.preferences=request.POST.getlist('seat') # 取得使用者座位偏好
        # 設定使用者的完整地址
        try:
            account.address=request.POST.get('city')+request.POST.get('district')+request.POST.get('road')+request.POST.get('address')
        except:
            pass
        # 保存資料並確認
        detail='資料輸入完成'
        account.save() # 儲存使用者資料
        mail=request.session['logged_in'] # 取得使用者登入的 session 資料
        account=verifiedAccount.objects.get(mail=mail) # 根據登入的 session 查找帳戶
        # 將帳戶資料傳遞給模板
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
        print(favorite_genres) # 輸出喜愛的電影類型
        seat=account.preferences
        print(seat) # 輸出座位偏好
        return render(request,'user_more.html',locals()) # 渲染並返回模板 'user_more.html'
    # 若使用者已登入
    if 'logged_in' in request.session:
        df = cache.get('address') # 從快取中取得地址資料
        if df is None:
            print('沒有暫存')
            from myapp.call_dataframe import address
            df=address() # 呼叫 address 方法取得地址資料
            cache.set('address',df) # 將地址資料存入快取
        else:
            print('找到了暫存')
        # 讀取並組織縣市、鄉鎮、市區資料
        dict_road = {}
        dict_town = {}
        same_list=[]
        list_city = ['選擇縣市']+list(df["縣市名稱"].unique())
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
        # 查找使用者並將資料傳遞給模板
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
        return render(request,'user_more.html',locals()) # 渲染並返回模板 'user_more.html'
    else:
        return redirect('https://taiwan-movies-36c4c3ac2ec6.herokuapp.com/Taiwan_movies_all/?detail=請先登入會員') # 若未登入，重定向到登入頁面
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
    status = request.GET.get('status','') #設定status值，沒有則設空值
    movie_name=request.GET.get('m','') #設定電影名稱值，沒有則設空值
    check='' #設定是否為收藏電影
    if status=='Sign_out': #檢查status是否正在執行登出
        if 'logged_in' in request.session: #檢查session是否為登入狀態
            del request.session['logged_in'] #刪除session中的logged_in項目使帳號呈現登出
            return redirect('/Taiwan_movies_all/shop/?detail=已登出') #跳至登出頁面
    if 'logged_in' in request.session: #檢查session是否為登入狀態
        mail=request.session.get('logged_in') #檢查session中的logged_in儲存到變數mail中
        account=verifiedAccount.objects.filter(mail=mail).first() #將身分資料庫中對應mail變數的值取出存入account變數中
        name=account.name #取出account中的name值存入name變數中
        favorite=Favorite.objects.filter(mail=mail,which_movie= movie_name ).first() #查詢本會員在最愛資料庫中是否儲存本電影
        if favorite: #若favorite內有本電影
            check='checked' #將check從''改為'checked'，表示已收藏
        if name=='' or name is None: #假如變數name為空值或是none
            name='無名的遊盪者' #將name變數改成'無名的遊盪者'
        status='signed_in' #使用者為登入狀態
    else:
         status='signed_out' #使用者為登出狀態
    csrf_token = csrf.get_token(request) #獲取 CSRF token，防止跨站請求偽造攻擊
    final_data = cache.get('more_detail') #從快取中獲取'more_detail'的資料，如果有的話直接使用，避免重複查詢。
    if final_data is None: #若final_data未從快取中獲得
        from myapp.call_dataframe import call_dataframe #從call_dataframe中獲得電影資訊final_data
        final_data=call_dataframe() #將call_dataframe中的final_data存入變數final_data中
        cache.set('more_detail',final_data) #將final_data的值暫存入more_detail中
        # cinema_list = final_data[final_data['中文片名']==movie_name].groupby('電影院名稱').count().index  #取得宣傳照網址
        img=final_data[final_data['中文片名']==movie_name]['宣傳照'].iloc[0] #取得宣傳照網址
        actors=final_data[final_data['中文片名']==movie_name]['演員'].iloc[0] #取得演員
        if pd.isna(actors) or actors =='': #假如演員為空值
        actors = "沒有演員" #顯示'沒有演員'
    director=final_data[final_data['中文片名']==movie_name]['導演'].iloc[0] #取得導演
    if pd.isna(director) or director=='': #假如導演為空值
        director = "沒有導演" #顯示'沒有導演'
    eng_name=final_data[final_data['中文片名']==movie_name]['英文片名'].iloc[0] #取得英文片名
    release_date=final_data[final_data['中文片名']==movie_name]['上映日'].iloc[0] #取得上映日
    cinema_group=final_data[final_data['中文片名']==movie_name].groupby('影城').count().index #將資料按「影城」進行分組，獲取該電影放映的影城列表。
    description=final_data[final_data['中文片名']==movie_name]['簡介'].iloc[0] #取得電影簡介
    youtube=final_data[final_data['中文片名']==movie_name]['youtube'].iloc[0] #取得youtube預告片連結
    mass_obj = massage.objects.filter(which_movie=movie_name).exclude(what_manage="team4_star_rating").order_by('creat_at') #從massage資料庫中查詢與該電影相關的留言，並按創建時間排序。
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
    return render(request,"more_detail.html",locals()) #將所有變數傳遞給模板more_detail.html進行渲染。
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
                'id':new_mass.id
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
