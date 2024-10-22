from django.templatetags.static import static
import pandas as pd
from myapp.models import Favorite
def html_show(final_data,Favorite_movies_list=[],mail=False):
    # 初始化HTML表格
    movie_list = final_data.groupby('中文片名').count().index
    res = '<table style="vertical-align: top;">'
    opt_btn=['<h4>Free Storage</h4>','<h4>User More</h4>','<h4>Reply Ready</h4>','<h4>Easy Layout</h4>']
    alert=''
    if mail==False:
        alert='''onclick="alert('請先登入！'); return false"'''
    # 遍歷每部電影
    for n, movie in enumerate(movie_list[1:5]):
        check=''
        ch_name = final_data["中文片名"].iloc[n+1]
        if ch_name in Favorite_movies_list:
             check='checked'
        eng_name = final_data["英文片名"].iloc[n+1]
        genre=final_data["類型"].iloc[n+1]

        # 初始化圖片顯示標誌
        img_displayed = False

        # 遍歷電影中的每一筆資料
        cinema_list = final_data.groupby('電影院名稱').count().index
        img_url = final_data['宣傳照'].iloc[n+1]  # 取得宣傳照的URL
        if pd.isna(img_url):
            img_url =static('dog.jpg')
            show_more=static('show_more.png')

        res += f'''<div class="col-lg-3 col-md-6">
            <div class="item">
              <div class="thumb">
                <a href="/Taiwan_movies_all/more_detail/?m={ch_name}"><img src="{img_url}" alt="" width='260px' height='400px'></a>
                <span class="ranking">&nbsp;當周第{n+2}名</span>
              </div>

              <div class="down-content">
                <span class="category">{genre}</span>
                <h4>{ch_name}</h4>
                <a href="/Taiwan_movies_all/more_detail/?m={ch_name}">
                  <i class="fas fa-arrow-right"></i>
                </a>
              <div class="heart-checkbox">
                <input type="checkbox" id="heart-checkbox{n}" data-movie-title="{ch_name}" {check}/>
                <label for="heart-checkbox{n}" {alert} >
                  <i class="far fa-heart"></i>  <!-- 空心愛心 -->
                  <i class="fas fa-heart"></i>  <!-- 實心愛心 -->
                </label>
              </div>
              </div>
            </div>
          </div>'''

        # 顯示電影院名稱
    #     res += '<div style="text-align: left;">'
    #     for cinema in cinema_list:
    #         res += cinema
    #         date_list=final_data_movie[final_data_movie['電影院名稱']==cinema].groupby('日期').count().index
    #         for date in date_list:
    #             res+=f'<br><span style="font-size: 12px;">{date}</span><br>'
    #             time_list=final_data_movie[(final_data_movie['電影院名稱']==cinema) & (final_data_movie['日期']==date)].groupby('時刻表').count().index
    #             for time in time_list:
    #                 res+=f'<span style="border: 2px solid #333; padding: 5px 10px; margin: 3px; display: inline-block; font-size: 10px;">{time}</span>'
    #             res+='<br>'
    #     # 關閉<td>和<tr>標籤
    #     res += '</div></td></tr></table>'

    # # 結束表格
    # res += '</table>'

    return res  # 返回生成的HTML

