from .models import Post


def validate_post():
    posts = Post.objects.all()

    for post in posts:
        if "&" in post.content:
            print(post.id,"번 글에 &가 있습니다.")
            post.content = post.content.replace("&", "")
            post.save()
        if post.dt_created > post.dt_modified:
            print(post.id,"번의 글이 원글의 수정이 작성일 보다 과거입니다.")
            post.save()
