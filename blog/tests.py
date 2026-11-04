from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Downvote, Post, Upvote


class BlogTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user('alice', password='pass12345!')
        self.bob = User.objects.create_user('bob', password='pass12345!')
        self.post = Post.objects.create(author=self.alice, title='Hello', text='First post')

    def test_post_list_is_public(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hello')

    def test_register_logs_user_in(self):
        response = self.client.post(reverse('register'), {
            'username': 'carol',
            'password1': 'Str0ng-pass-123',
            'password2': 'Str0ng-pass-123',
        })
        self.assertRedirects(response, reverse('post_list'))
        self.assertTrue(User.objects.filter(username='carol').exists())

    def test_new_post_requires_login(self):
        response = self.client.get(reverse('post_new'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

    def test_logged_in_user_can_create_post(self):
        self.client.login(username='bob', password='pass12345!')
        response = self.client.post(reverse('post_new'), {'title': 'Bob post', 'text': 'Hi'})
        post = Post.objects.get(title='Bob post')
        self.assertRedirects(response, reverse('post_detail', kwargs={'pk': post.pk}))
        self.assertEqual(post.author, self.bob)

    def test_only_author_can_edit(self):
        self.client.login(username='bob', password='pass12345!')
        self.client.post(reverse('post_edit', kwargs={'pk': self.post.pk}),
                         {'title': 'Hacked', 'text': 'x'})
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Hello')

    def test_only_author_can_delete(self):
        self.client.login(username='bob', password='pass12345!')
        self.client.post(reverse('post_delete', kwargs={'pk': self.post.pk}))
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())

    def test_author_can_delete(self):
        self.client.login(username='alice', password='pass12345!')
        self.client.post(reverse('post_delete', kwargs={'pk': self.post.pk}))
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_vote_requires_login(self):
        response = self.client.get(reverse('upvote_post', kwargs={'post_id': self.post.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Upvote.objects.count(), 0)

    def test_one_vote_per_user_and_switching(self):
        self.client.login(username='bob', password='pass12345!')
        up = reverse('upvote_post', kwargs={'post_id': self.post.pk})
        down = reverse('downvote_post', kwargs={'post_id': self.post.pk})
        self.client.get(up)
        self.client.get(up)  # a second upvote must not count twice
        self.assertEqual(self.post.upvotes_count, 1)
        self.client.get(down)  # switching removes the upvote
        self.assertEqual(self.post.upvotes_count, 0)
        self.assertEqual(self.post.downvotes_count, 1)
        self.assertEqual(Downvote.objects.count(), 1)

    def test_profile_page_lists_posts(self):
        response = self.client.get(reverse('profile', kwargs={'username': 'alice'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hello')
