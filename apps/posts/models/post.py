from django.db import models


class Post(models.Model):
    """User posts"""
    text = models.TextField()
    owner = models.ForeignKey('users.User', null=True, blank=True,
                              verbose_name='Post owner',
                              on_delete=models.CASCADE,
                              related_name='my_posts')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Created time')
    like = models.ManyToManyField('users.User', verbose_name='Users who like the post',
                                  related_name='my_likes',
                                  related_query_name='my_like')

    class Meta:
        ordering = ['-created_at']

    @property
    def likes_count(self):
        """Number of likes for this post"""
        likes = self.like.count()
        return likes


