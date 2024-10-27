from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Seller, Comment, Reply
from .forms import CommentCreateForm, ReplyCreateForm

User = get_user_model()

class CommentReplyCRUDTests(TestCase):
    
    def setUp(self):
        # Create a user and seller for testing
        self.user = User.objects.create_user(username='testuser', password='password')
        self.seller = Seller.objects.create(company_name='Test Company', user=self.user)
        self.client.login(username='testuser', password='password')

        # Create a comment for testing
        self.comment = Comment.objects.create(
            seller=self.seller,
            name='Test Commenter',
            body='This is a test comment.',
            star=5,
            author=self.user
        )

        # Create a reply for the comment
        self.reply = Reply.objects.create(
            parent_comment=self.comment,
            name='Test Reply',
            body='This is a test reply.'
        )

    def test_create_comment(self):
        response = self.client.post(reverse('diskusi:review_section', args=[self.seller.pk]), {
            'body': 'New comment body',
            'star': 4
        })
        self.assertEqual(response.status_code, 302)  # Check for redirect after post
        self.assertEqual(Comment.objects.count(), 2)  # Ensure comment count increased

    def test_read_comment(self):
        response = self.client.get(reverse('diskusi:review_section', args=[self.seller.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.comment.body)  # Check if comment is displayed

    def test_update_comment(self):
        response = self.client.post(reverse('diskusi:edit_comment', args=[self.comment.pk]), {
            'body': 'Updated comment body',
            'star': 5
        })
        self.assertEqual(response.status_code, 200)  # Check for success response
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.body, 'Updated comment body')  # Check if comment was updated

    def test_delete_comment(self):
        response = self.client.post(reverse('diskusi:delete_comment', args=[self.comment.pk]))
        self.assertEqual(response.status_code, 200)  # Check for success response
        self.assertEqual(Comment.objects.count(), 0)  # Ensure comment count is now 0

    def test_create_reply(self):
        response = self.client.post(reverse('diskusi:reply', args=[self.comment.pk]), {
            'body': 'New reply body'
        })
        self.assertEqual(response.status_code, 200)  # Check for success response
        self.assertEqual(Reply.objects.count(), 2)  # Ensure reply count increased

    def test_update_reply(self):
        response = self.client.post(reverse('diskusi:edit_reply', args=[self.reply.pk]), {
            'body': 'Updated reply body'
        })
        self.assertEqual(response.status_code, 200)  # Check for success response
        self.reply.refresh_from_db()
        self.assertEqual(self.reply.body, 'Updated reply body')  # Check if reply was updated

    def test_delete_reply(self):
        response = self.client.post(reverse('diskusi:delete_reply', args=[self.reply.pk]))
        self.assertEqual(response.status_code, 200)  # Check for success response
        self.assertEqual(Reply.objects.count(), 0)  # Ensure reply count is now 0

    def tearDown(self):
        self.comment.delete()
        self.reply.delete()
        self.seller.delete()
        self.user.delete()
