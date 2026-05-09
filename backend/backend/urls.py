from django.urls import path, include


urlpatterns = [
    path("api/article/", include("article.urls")),
    path("api/sort/", include("categorie.urls")),
    path("api/media/", include("media.urls")),
    path("api/comment/", include("comment.urls")),
    path("api/authority/", include("authority.urls")),
    path("api/user/", include("user.urls"))

]