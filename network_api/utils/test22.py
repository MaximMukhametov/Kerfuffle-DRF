from network_api.models import User

user = User.objects.get(id=1765)
User.objects.filter(followed__id=1765)
User.objects.filter(followed__followed__id=1765)
user.followed.all()

user.followers.all()

