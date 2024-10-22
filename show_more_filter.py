def filter_show(final_data,Favorite_movies_list=[],mail=False):
    from django.templatetags.static import static
    from django.urls import reverse
    import pandas as pd
    genre_list=['all','horror','story_rich','animation','action','documentary','musical','romance','my_favorite']
    res=''
    form_action_url = reverse('product_details')
    alert=''
    if mail==False:
        alert='''onclick="alert('請先登入！'); return false"'''
    for n,i in enumerate([final_data]):
        che=[]
        eng_che=[]
        for N,i2 in enumerate(range(len(i))):
            img=i['宣傳照'].iloc[i2]
            ch_name=i['中文片名'].iloc[i2]
            check=''
            if ch_name in Favorite_movies_list:
                check='checked'
            if ch_name in che:
                continue
            che.append(ch_name)
            try:
                eng_name=i['英文片名'].iloc[i2].lower()
            except:
                eng_name=i['英文片名'].iloc[i2]
            if eng_name in eng_che:
                continue
            eng_che.append(eng_name)
            genre=str(i['類型'].iloc[i2])
            all_genre=' all'
            if '恐'in genre:
                all_genre+=' horror'
            if '劇情'in genre:
                all_genre+=' story_rich'
            if '動畫'in genre or '卡通' in genre:
                all_genre+=' animation'
            if '動作'in genre:
                all_genre+=' action'
            if '紀錄'in genre:
                all_genre+=' documentary'
            if '音樂'in genre:
                all_genre+=' musical'
            if '愛'in genre:
                all_genre+=' romance'
            if '喜劇'in genre:
                all_genre+=' comedy'
            if '冒險'in genre:
                all_genre+=' adventure'
            if '藝術'in genre:
                all_genre+=' art'
            if '犯罪'in genre:
                all_genre+=' crime'
            if '家'in genre:
                all_genre+=' family'
            if '兒童'in genre:
                all_genre+=' child'
            if '功夫'in genre:
                all_genre+=' kongfu'
            if '科幻'in genre:
                all_genre+=' scifi'
            if '驚悚'in genre or '懸疑' in genre:
                all_genre+=' thriller'
            if ch_name in Favorite_movies_list:
                all_genre+=' my_favorite'


            if pd.isna(img) or img == '':
                img='https://raw.githubusercontent.com/movieteam4/img/refs/heads/main/dog.jpg'
            res+=f'''<div class="col-lg-3 col-md-6 align-self-center mb-30 trending-items col-md-6 {all_genre}">
          <div class="item">
            <div class="thumb">
              <a href="/Taiwan_movies_all/more_detail/?m={ch_name}"><img src="{img}" alt="" width='261px' height='392px' ></a>
            </div>
            <div class="down-content">
              <span class="category">{genre}</span>
              <h4>{ch_name}</h4>
              <h6>{eng_name}</h6>
              <a href="/Taiwan_movies_all/more_detail/?m={ch_name}"><i class="fas fa-arrow-right"></i></a>
              <div class="heart-checkbox {ch_name}">
                <input type="checkbox" id="heart-checkbox{ch_name}" data-movie-title="{ch_name}" {check} />
                <label for="heart-checkbox{ch_name}" {alert} >
                  <i class="far fa-heart" id="img_heart"></i>  <!-- 空心愛心 -->
                  <i class="fas fa-heart"></i>  <!-- 實心愛心 -->
                </label>
              </div>
            </div>

          </div>
        </div>
        '''
    return res