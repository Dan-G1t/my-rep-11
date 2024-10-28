from celery import shared_task
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from news_portal.models import Post, Category


@shared_task
def notify_subscribers_task(post_id):
    instance = Post.objects.get(id=post_id)
    categories = instance.category.all()
    for category in categories:
        subscribers = category.subscribers.all()
        for subscriber in subscribers:
            html_content = render_to_string('email_notification.html', {
                'title': instance.title,
                'text': instance.text,
                'username': subscriber.username,
                'id': instance.id
            })
            msg = EmailMultiAlternatives(
                subject=instance.title,
                body=f'Здравствуй, {subscriber.username}. Новая статья в твоём любимом разделе!',
                from_email='gdaprog@yandex.ru',
                to=[subscriber.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

@shared_task
def weekly_newsletter_task():
    now = timezone.now()
    last_week = now - timezone.timedelta(days=7)
    new_posts = Post.objects.filter(creation_date__gt=last_week)

    categories = Category.objects.prefetch_related('subscribers')
    subscribers_posts = {}

    for category in categories:
        subscribers = category.subscribers.all()
        category_posts = new_posts.filter(category=category)
        
        if category_posts.exists():
            for subscriber in subscribers:
                if subscriber not in subscribers_posts:
                    subscribers_posts[subscriber] = []
                subscribers_posts[subscriber].extend(category_posts)

    for subscriber, posts in subscribers_posts.items():
        unique_posts = {post.id: post for post in posts}.values()
        html_content = render_to_string('email_notification_week.html', {
            'username': subscriber.username,
            'posts': unique_posts,
        })

        msg = EmailMultiAlternatives(
            subject='Новые статьи за неделю',
            body=f'Здравствуй, {subscriber.username}! Собрали подборку статей за неделю из твоих любимых разделов!',
            from_email='gdaprog@yandex.ru',
            to=[subscriber.email],
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()