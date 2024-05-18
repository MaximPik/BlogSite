from posts.models import Post, Comment, Group, User, Follow
from rest_framework import serializers 

class PostSerializer(serializers.ModelSerializer):
    # Поле сериализатора, которое представляет связб с другой моделью (User)
    # slug_field='username', вместо id будем использовать username
    # read_only=True, нельзя изменять
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    class Meta:
        model = Post
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    # аналогично PostSerializer
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['post']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'title', 'description', 'slug']
        extra_kwargs = {
            'slug': {'write_only': True}
        }
    
class UserSerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'posts_count']

    def get_posts_count(self, obj):
        return obj.posts.count()  # Метод для подсчета постов

class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    author = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all()
    )
    class Meta:
        model = Follow
        fields = ['user', 'author']

    def validate(self, data):
        if self.context['request'].user == data['author']:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        return data

class FollowListSerializer(serializers.Serializer):
    following = FollowSerializer(many=True)
    followers = FollowSerializer(many=True)
