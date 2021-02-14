from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .services import UserService
from .serializers import UserLoginRequestSerializer

from .services import UserService


class UserViewSet(GenericViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get", "post"]
    serializers_dict = {
        'login': UserLoginRequestSerializer
    }

    def get_serializer_class(self):
        """
        """
        try:
            return self.serializers_dict[self.action]
        except KeyError as e:
            raise Exception('Unable', errors=e)

    @action(
        methods=["post"], detail=False, authentication_classes=[], permission_classes=[]
    )
    def login(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = UserService.get_user(email=username)
        if not user:
            return Response({
                'status':400, 'message':'User does not exists'
            })
        if user.check_password(password):
            return Response({"token": UserService.access_token(user)})
        return Response({
                'status':400, 'message':'User does not exists'
            })

    @action(
        methods=["post"], detail=False, authentication_classes=[], permission_classes=[]
    )
    def signup(self, request):
        data = request.data
        response = UserService.create_signup(data)
        return Response(response)

    @action(
        methods=["post"], detail=False,
    )
    def follow_user(self, request):
        follower = request.user.id
        followee = request.data.get('followee_id')
        is_follow = request.data.get('is_follow')
        response = UserService.create_follow(follower, followee, is_follow)
        return Response(response)

    @action(
        methods=["post"], detail=False,
    )
    def post_tweet(self, request):
        user_id = request.user.id
        type = request.data.get('type')
        content = request.data.get('content')
        response = UserService.post_tweet(user_id, type, content)
        return Response(response)

    @action(
        methods=["get"], detail=False,
    )
    def get_tweets(self, request):
        user_id = request.user.id
        response = UserService.get_tweets(user_id)
        return Response(response)

    @action(
        methods=["post"], detail=False,
    )
    def like_tweets(self, request):
        user_id = request.user.id
        post_id = request.data.get('post_id')
        is_like = request.data.get('is_like',True)
        response = UserService.like_tweet(user_id, post_id, is_like)
        return Response(response)

    @action(
        methods=["get"], detail=False,
    )
    def like_tweet_by(self, request):
        post_id = request.GET.get('post_id')
        response = UserService.like_tweet_by(post_id)
        return Response(response)

    @action(
        methods=["get"], detail=False,
    )
    def followed_by(self, request):
        followee_id = request.user.id
        response = UserService.followed_by(followee_id)
        return Response(response)
