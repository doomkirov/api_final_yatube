from rest_framework import serializers


from posts.models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Post


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.CharField(
        read_only=True
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )

    def validate_following(self, value):
        if Follow.objects.filter(
            user=self.context['request'].user, following=value
        ):
            raise serializers.ValidationError(
                'Нельзя подписаться на одного пользователя дважды!'
            )
        elif self.context['request'].user == value:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )
        return value

    class Meta:
        model = Follow
        fields = ('user', 'following')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('post',)
