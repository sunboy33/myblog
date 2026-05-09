from django.urls import path
from .views import *


urlpatterns = [
    path('pagination', get_article_by_pagination), # 分页查询
    path('add', add_article), # 添加文章
    path('delete/<int:id>', delete_article),
    path('<int:id>', get_article_by_id), # 根据id查询
    path('listSortAticle', get_list_sort_article),    # 获取所有文章, 按照类别分类
    path('type', get_article_by_type),  # 查询某一类的文章,
    path('listRecommend', get_recommend_articles),
    path('update/<int:id>', article_detail)

]