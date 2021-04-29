import random

from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import authentication, permissions

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from youtube.models import *


class CreateAccount(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        data = request.data

        if User.objects.filter(username=data['username']).exists():
            return Response({'usernameTaken': 'Username is already taken'}, status=400)

        user = User.objects.create_user(username=data['username'], password=data['password'])
        return Response({'success': True}, status=200)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        # Custom data you want to include
        data.update({'username': self.user.username})
        data.update({'id': self.user.id})
        # and everything else you want to send in the response
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


def get_video_object(request, video, video_file=False, thumbnail_file=True):
    object = {
        'id'        : video.id,
        'uploaderId': video.uploader.id,
        'title'     : video.title,
        'views'     : video.views,
        'complex'   : video.complex_id,
        'slug': video.slug,
        'thumbnail' : None,
        'videoFile' : None,
        'uploaderName': video.uploader.username,
        'tags'      : [tag.name for tag in video.tags.all()],
        'tag_ids'   : [tag.id for tag in video.tags.all()],
        'date'      : video.date.strftime("%d %b %Y"),
        'likes'     : video.likes.all().count(),
        'dislikes'  : video.dislikes.all().count()
    }
    if thumbnail_file:
        object['thumbnail'] = request.build_absolute_uri(video.thumbnail.url)

    if video_file:
        object['videoFile'] = request.build_absolute_uri(video.video.url)
    
    return object


class UploadVideo(APIView):
    parser_classes     = [MultiPartParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id, format=None):
        data = request.data        
        tags = data['tags'].split(",")

        video = Video.objects.create(
            uploader_id=id, title=data['title'], description=data['description'],
            video=data['videoFile'], thumbnail=data['thumbnail']
        )
        for _tag in tags:
            tag = Tag.objects.create(name=_tag)
            video.tags.add(tag)

        response = get_video_object(request, video)
        return Response({'video': response}, status=200)


class AllUserVideos(APIView):
    permission_classes = [ permissions.IsAuthenticated ]

    def get(self, request, user_id, format=None):
        videos = Video.objects.filter(uploader_id=user_id).order_by('-id')
        video_objects = [get_video_object(request, video) for video in videos]
        return Response({'videos': video_objects}, status=200)


class VideoDetail(APIView):
    permission_classes = [ permissions.AllowAny ]

    def get(self, request, video_id, format=None):
        if not Video.objects.filter(id=video_id).exists():
            return Response({'error': True}, status=400)

        video = get_video_object(request, Video.objects.get(id=video_id), 
                                 video_file=True, thumbnail_file=False)
        return Response({'video': video}, status=200)


class CheckIfUserLikedOrDislikedVideo(APIView):
    permission_classes = [ permissions.IsAuthenticated ]

    def get(self, request, video_id, user_id, format=None):
        video = Video.objects.get(id=video_id)
        user  = User.objects.get(id=user_id)

        if user in video.likes.all():
            return Response({'liked': True}, status=200)
        elif user in video.dislikes.all():
            return Response({'disliked': True}, status=200)

        return Response({'None': True}, status=200)


class LikeVideo(APIView):
    like     = True
    liked    = True
    dislike  = False
    disliked = False
    permission_classes = [ permissions.IsAuthenticated ]

    def post(self, request, video_id, user_id, format=None):
        video = Video.objects.get(id=video_id)
        user  = User.objects.get(id=user_id)

        if self.like:
            if user in video.likes.all():
                video.likes.remove(user)
                self.liked = False
            elif user in video.dislikes.all():
                video.dislikes.remove(user)
                video.likes.add(user)
            else:
                video.likes.add(user)
        elif self.dislike:
            if user in video.dislikes.all():
                video.dislikes.remove(user)
                self.disliked = False
            elif user in video.likes.all():
                video.likes.remove(user)
                video.dislikes.add(user)
            else:
                video.dislikes.add(user)
        video.save()

        total_likes    = video.likes.all().count()
        total_dislikes = video.dislikes.all().count()
        return Response({'likes': total_likes, 'liked': self.liked, 
                         'dislikes': total_dislikes, 'disliked': self.disliked}, status=200)


class DislikeVideo(LikeVideo):
    like     = False
    liked    = False
    dislike  = True
    disliked = True


# 100 random video for unauthenticated users
class GetRandomVideos(APIView):
    permission_classes = [ permissions.AllowAny ]

    def get(self, request, format=None):
        videos = Video.objects.all()

        video_objects = [get_video_object(request, video) for video in videos]

        random_counts = videos.count() if videos.count() <= 100 else 100
        random_videos = random.sample(video_objects, random_counts) 

        return Response({'videos': random_videos}, status=200)


# user viewed video's tags
class AddUserViewedVideo(APIView):
    permission_classes = [ permissions.IsAuthenticated ]

    def post(self, request, user_id, format=None):
        data = request.data
        user_viewd_tags = None
        tag_ids = data['tag_ids']

        if not UserVideoViewTags.objects.filter(user__id=user_id).exists():
            user_viewd_tags = UserVideoViewTags.objects.create(user_id=user_id)

        user_viewd_tags = UserVideoViewTags.objects.get(user__id=user_id)
        
        for _id in tag_ids:
            user_viewd_tags.tags.add(_id)

        return Response({'success': True}, status=200)


# user viewed videos
class AddUserViewedVideos(APIView):
    permission_classes = [ permissions.IsAuthenticated ]

    def post(self, request, user_id, video_id, format=None):
        video = Video.objects.get(id=video_id)

        if not UserViewedVideo.objects.filter(user__id=user_id).exists():
            viewed_videos = UserViewedVideo.objects.create(user_id=user_id)
        else:
            viewed_videos = UserViewedVideo.objects.get(user__id=user_id)
        viewed_videos.videos.add(video)

        return Response({'success': True}, status=200)
        

class GetRandomVideosBaseOnUserViewed(APIView):
    permission_classes = [ permissions.IsAuthenticated ]

    def get(self, request, user_id, format=None):
        video_object_ids = []
        video_objects    = []
        count_for_all    = 80

        if UserVideoViewTags.objects.filter(user__id=user_id).exists():            
            count_for_all    = 20
            user_viewed_tags = UserVideoViewTags.objects.get(user__id=user_id)

            # loop through all user's viewed video tags
            for _tag in user_viewed_tags.tags.all():
                videos = Video.objects.filter(tags__id=_tag.id)
                for video in videos:
                    if len(video_objects) > 60:
                        break
                    elif video.id not in video_object_ids:
                        video_object_ids.append(video.id)
                        video_objects.insert(0, get_video_object(request, video))

        all_video_objects = []
        all_videos = Video.objects.all().order_by('-id')
        for video in all_videos:
            if len(all_video_objects) > count_for_all:
                break 
            elif video.id not in video_object_ids:
                video_object_ids.append(video.id)
                all_video_objects.append(get_video_object(request, video))

        videos = video_objects + all_video_objects

        random_counts = len(videos) if len(videos) <= 80 else 80
        random_videos = random.sample(videos, random_counts)
        
        return Response({'videos': random_videos}, status=200)


class VideoViewCount(APIView):
    permission_classes = [ permissions.AllowAny ]

    def post(self, request, video_id, format=None):
        video = Video.objects.get(id=video_id)
        video.views_increment()
        return Response({'views': video.views}, status=200)


# get 40 related videos
class GetRelatedVideos(APIView):
    permission_classes = [ permissions.AllowAny ]

    def get(self, request, video_id, format=None):
        video = Video.objects.get(id=video_id)

        if video.tags.all().count() < 15:
            tags = video.tags.all().order_by('-id')[:video.tags.all().count()]
        else:
            tags = video.tags.all().order_by('id')[:15]

        related_video_objects    = []
        related_video_object_ids = []

        for tag in tags:
            # get only 1 video for 1 tag
            related_video = Video.objects.filter(Q(tags__name__icontains=tag.name)).order_by('-id')[0]
            
            if (related_video.id not in related_video_object_ids) and (related_video.id != video_id):
                related_video_object_ids.append(related_video.id)
                related_video_objects.append(get_video_object(request, related_video))
        
        similar_video_objects    = []
        similar_video_object_ids = []

        if len(related_video_objects) < 40:
            for _split_title in video.title.split(" "):
                similar_videos = Video.objects.filter(Q(title__icontains=_split_title)).order_by('-id')
                
                for similar_video in similar_videos:
                    if len(similar_video_objects) > (40 - int(len(related_video_objects))):
                        break
                    elif (similar_video.id not in similar_video_object_ids) and \
                         (similar_video.id not in related_video_object_ids):
                        similar_video_object_ids.append(similar_video.id)
                        similar_video_objects.append(get_video_object(request, similar_video))

        all_videos = related_video_objects + similar_video_objects
        all_videos = random.sample(all_videos, len(all_videos))

        return Response({'relatedVideos': all_videos}, status=200)


def get_comment_object(comment, user_id=None, check_like=False):
    object = {
        'id': comment.id,
        'username': comment.user.username,
        'userId'  : comment.user.id,
        'content' : comment.content,
        'date'    : comment.date.strftime("%d %b %Y"),
        'likes'   : comment.likes.all().count(),
    }
    if check_like:
        user = User.objects.get(id=user_id)
        object['liked'] = True if user in comment.likes.all() else False
    return object


class GetVideoCommentsForAuthenticated(APIView):
    permission_classes = [ permissions.AllowAny ]

    def get(self, request, video_id, user_id=None, format=None):
        comments = Comment.objects.filter(video__id=video_id).order_by('-id') 
        comment_objects = []

        for comment in comments:
            comment_objects.append(get_comment_object(comment, user_id=user_id, check_like=True))

        return Response({'comments': comment_objects}, status=200)


class GetVideoCommentsForUnauthenticated(GetVideoCommentsForAuthenticated):
    def get(self, request, video_id, format=None):
        comments = Comment.objects.filter(video__id=video_id).order_by('-id') 
        comment_objects = [get_comment_object(comment) for comment in comments]
        return Response({'comments': comment_objects}, status=200)


class SendVideoComment(APIView):
    permission_classes = [ permissions.IsAuthenticated ]

    def post(self, request, video_id, user_id, format=None):
        data    = request.data
        comment = Comment.objects.create(user_id=user_id, video_id=video_id, content=data['content']) 
        return Response({'comment': get_comment_object(comment, user_id, True)}, status=200)


class LikeComment(APIView):
    permission_classes = [ permissions.IsAuthenticated ]

    def post(self, request, comment_id, user_id, format=None):
        liked   = False
        comment = Comment.objects.get(id=comment_id)
        user    = User.objects.get(id=user_id)

        if user in comment.likes.all():
            comment.likes.remove(user)
        else:
            comment.likes.add(user)
            liked = True
        return Response({'likes': comment.likes.all().count(), 'liked': liked}, status=200)


class DeleteVideo(APIView):
    permission_classes = [ permissions.IsAuthenticated ]

    def post(self, request, video_id, user_id, format=None):
        video = Video.objects.get(id=video_id)
        if video.uploader.id != user_id:
            return Response({'permissionError': True}, status=400)

        video.delete()
        return Response({'success': True}, status=200)


class DeleteComment(APIView):
    permission_classes = [ permissions.IsAuthenticated ]

    def action(self, request, comment):
        comment.delete()
        return {'success': True}

    def post(self, request, comment_id, user_id, format=None):
        comment = Comment.objects.get(id=comment_id)
        if comment.user.id != user_id:
            return Response({'permissionError': True}, status=400)
        
        return Response(self.action(request, comment), status=200)


class EditComment(DeleteComment):
    def action(self, request, comment):
        comment.content = request.data['content'] 
        comment.save()
        return {'content': comment.content}


class SearchAutoCompleteEngine(APIView):
    permission_classes = [ permissions.AllowAny ]

    def get(self, request, format=None):
        # if user types nothing response nothing
        if request.GET['searchText'] == '':
            return Response({'results': ['']}, status=200)
        
        videos = Video.objects.filter(title__startswith=request.GET['searchText'])
        response_titles = [video.title for video in videos]

        if videos.all().count() > 20:
            random_response = random.sample(response_titles, 20)
        else:
            random_response = random.sample(response_titles, videos.all().count())            
        return Response({'results': random_response}, status=200)


class GetSearchResult(SearchAutoCompleteEngine):
    def get(self, request, format=None):
        videos = Video.objects.filter(Q(title__icontains=request.GET['search'])).order_by('-id')
        responses = [get_video_object(request, video) for video in videos]
        return Response({'videos': responses}, status=200)


class GetNotification(APIView):
    permission_classes = [ permissions.IsAuthenticated ]

    def get(self, request, user_id, format=None):
        notifications = Notification.objects.filter(user__id=user_id).order_by('-id')[:20]
        notification_objects = [{
            'id'      : notification.id,
            'user_id' : notification.user_id,
            'content' : notification.content,
            'url'     : notification.url
        } for notification in notifications]

        return Response({'notifications': notification_objects}, status=200)
