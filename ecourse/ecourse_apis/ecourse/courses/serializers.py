from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Category, Course, Lesson, Tag, User, Comment, Action, Rating


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CourseSerializer(ModelSerializer):
    image = SerializerMethodField()

    def get_image(self, course):
        request = self.context['request']
        name = course.image.name
        if name.startswith("static/"):
            path = '/%s' % name
        else:
            path = '/static/%s' % name
        return request.build_absolute_uri(path)

    class Meta:
        model = Course
        fields = ['id', 'subject', 'image', 'created_date', 'category']

class LessonSerializer(ModelSerializer):
    # image = SerializerMethodField()
    #
    # def get_image(self, course):
    #     request = self.context['request']
    #     name = course.image.name
    #     if name.startswith("static/"):
    #         path = '/%s' % name
    #     else:
    #         path = '/static/%s' % name
    #     return request.build_absolute_uri(path)

    class Meta:
        model = Lesson
        fields = ['id', 'subject', 'image', 'created_date', 'updated_date', 'course']

class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class LessonDetailSerializer(LessonSerializer):
    tag = TagSerializer(many=True)
    image = SerializerMethodField()
    rate = SerializerMethodField()

    def get_image(self, lesson):
        request = self.context['request']
        name = lesson.image.name
        if name.startswith("static/"):
            path = '/%s' % name
        else:
            path = '/static/%s' % name
        return request.build_absolute_uri(path)

    def get_rate(self,lesson):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            r = lesson.rating_set.filter(creator=request.user).first()
            if r:
                return r.rate

        return -1
    class Meta:
        model = LessonSerializer.Meta.model
        fields = LessonSerializer.Meta.fields + ['content', 'tag', 'rate']

class UserSerializer(ModelSerializer):
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'email', "date_joined"]
        extra_kwargs = {
            'password': {'write_only': 'true'}
        }

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'creator', 'created_date', 'updated_date']

class ActionSerializer(ModelSerializer):
    class Meta:
        model = Action
        fields = ['id', 'type', 'created_date']

class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'rate', 'created_date']