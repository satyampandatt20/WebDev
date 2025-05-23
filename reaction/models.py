from django.db import models
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from post.models import Post
from notification.models import Notification

# Create your models here.

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')

    def like_notification(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user
        notify = Notification(post=post, sender=sender, receiver=post.user, type='Like')
        notify.save()

    def unlike_notification(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user
        notify = Notification.objects.filter(post=post, sender=sender, type='Like')
        notify.delete()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    body = models.TextField()
    commented_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    def comment_notification(sender, instance, *args, **kwargs):
        comment = instance
        post = comment.post
        sender = comment.user
        comment_body = comment.body
        notify = Notification(post=post, sender=sender, receiver=post.user, type='Comment', comment_body=comment_body)
        notify.save()

    def uncomment_notification(sender, instance, *args, **kwargs):
        comment = instance
        post = comment.post
        sender = comment.user
        notify = Notification.objects.filter(post=post, sender=sender, type='Comment')
        notify.delete()


post_save.connect(Like.like_notification, sender=Like)
post_delete.connect(Like.unlike_notification, sender=Like)

post_save.connect(Comment.comment_notification, sender=Comment)
post_delete.connect(Comment.uncomment_notification, sender=Comment)
