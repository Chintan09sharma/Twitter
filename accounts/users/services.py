from rest_framework.authtoken.models import Token
from .models import User, Followers_Data, Posts, Likes

class UserService(object):
    """
    """
    @staticmethod
    def get_user(**kwargs):
        try:
            user = User.objects.get(**kwargs)
            return user
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_post(**kwargs):
        try:
            post = Posts.objects.get(**kwargs)
            return post
        except Posts.DoesNotExist:
            return None

    @staticmethod
    def create_user(**kwargs):
        user = User.objects.create(**kwargs)
        if kwargs.get("password"):
            user.set_password(kwargs["password"])
            user.save()
        return user

    @staticmethod
    def create_signup(data):
        user_email = data.get("email")
        if UserService.get_user(email=user_email):
            return {"status": 500,
                    "message": "User Already Exists."}
        user = UserService.create_user(**data)
        return {"token": UserService.access_token(user)}

    @staticmethod
    def access_token(user):
        token, _ = Token.objects.get_or_create(user=user)
        return token.key

    @staticmethod
    def create_follow(follower, followee, is_follow):
        data = {'status': 200, 'message': 'Success'}
        if is_follow is False:
            Followers_Data.objects.get(follower_id=follower, followee_id= followee).delete()
            return data
        else:
            Followers_Data.objects.create(follower_id=follower, followee_id=followee)
            return data

    @staticmethod
    def post_tweet(user_id, type, content):
        user = UserService.get_user(id=user_id)
        post = Posts.objects.create(user = user, type=type, content=content)
        return {"post_id": post.id}

    @staticmethod
    def get_tweets(user_id):
        user = UserService.get_user(id=user_id)
        posts = Posts.objects.filter(user =user)
        data = []
        for post in posts:
            post_data = {}
            post_data['id'] = post.id
            post_data['content'] = post.content
            post_data['type'] = post.type
            data.append(post_data)
        return data

    @staticmethod
    def like_tweet(user_id,post_id,is_like):
        res = {'status':200,'message':'Success'}
        user = UserService.get_user(id=user_id)
        post = UserService.get_post(id=post_id)
        if is_like:
            if user and post:
                like_object = Likes.objects.get_or_create(user=user,post=post)
                return res
        else:
            if user and post:
                like_object = Likes.objects.get(user=user, post=post)
                like_object.delete()
                return res

    @staticmethod
    def like_tweet_by(post_id):
        post = UserService.get_post(id=post_id)
        likes = Likes.objects.filter(post=post)
        data = []
        for like in likes:
            post_data = {}
            user = like.user
            post_data['user_id'] = user.id
            post_data['first_name'] = user.first_name
            post_data['last_name'] = user.last_name
            data.append(post_data)
        return data

    @staticmethod
    def followed_by(followee_id):
        follow_ids = Followers_Data.objects.filter(followee_id=followee_id).values_list('follower_id',flat=True)
        users = User.objects.filter(id__in=follow_ids)
        data = []
        for user in users:
            post_data = {}
            post_data['user_id'] = user.id
            post_data['first_name'] = user.first_name
            post_data['last_name'] = user.last_name
            data.append(post_data)
        return data
