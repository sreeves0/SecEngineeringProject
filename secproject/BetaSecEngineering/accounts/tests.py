from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import LabAccount


class AuthenticationFlowTests(TestCase):
    def test_home_redirects_to_login_for_anonymous_user(self):
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('login'))

    def test_account_requires_login(self):
        response = self.client.get(reverse('account'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('account')}")

    def test_login_links_to_read_only_transport_guide(self):
        response = self.client.get(reverse('login'))

        self.assertContains(response, reverse('transport-guide'))
        self.assertContains(response, 'Read the manual server setup guide')
        self.assertContains(response, '>HTTP Lab<')
        self.assertNotContains(response, 'Authentication lab')
        self.assertNotContains(response, 'class="brand"')
        self.assertNotContains(response, 'signal-map')

    def test_transport_guide_is_public_and_informational(self):
        response = self.client.get(reverse('transport-guide'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This page cannot enable or disable HTTPS.')
        self.assertContains(response, 'betasecengineering/settings.py')
        self.assertContains(response, 'X-Forwarded-Proto: https')
        self.assertNotContains(response, '<form')

    def test_signup_hashes_password_and_opens_account_page(self):
        response = self.client.post(
            reverse('signup'),
            {
                'username': 'student',
                'password1': 'A-strong-local-passphrase-42',
                'password2': 'A-strong-local-passphrase-42',
            },
            follow=True,
        )

        self.assertContains(response, 'Session active')
        user = User.objects.get(username='student')
        self.assertNotEqual(user.password, 'A-strong-local-passphrase-42')
        self.assertTrue(user.check_password('A-strong-local-passphrase-42'))

    def test_logout_requires_post_and_clears_authentication(self):
        user = User.objects.create_user(username='student', password='local-pass-42')
        self.client.force_login(user)

        get_response = self.client.get(reverse('logout'))
        self.assertEqual(get_response.status_code, 405)

        post_response = self.client.post(reverse('logout'))
        self.assertRedirects(post_response, reverse('login'))
        self.assertNotIn('_auth_user_id', self.client.session)


class SqlInjectionLabTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        LabAccount.objects.get_or_create(
            username='analyst',
            defaults={
                'lab_password': 'secengy124!',
                'display_name': 'Demo Analyst',
            },
        )

    def test_vulnerable_login_accepts_valid_dummy_credentials(self):
        response = self.client.post(
            reverse('lab-vulnerable-login'),
            {'username': 'analyst', 'password': 'secengy124!'},
        )
        self.assertRedirects(response, reverse('lab-result'))

    def test_lab_pages_show_mode_specific_demo_guidance(self):
        vulnerable_response = self.client.get(reverse('lab-vulnerable-login'))
        secure_response = self.client.get(reverse('lab-secure-login'))

        self.assertContains(vulnerable_response, 'Bypass test value')
        self.assertContains(vulnerable_response, 'Unsafe string-built SQL')
        self.assertContains(vulnerable_response, 'Dummy Account')
        self.assertNotContains(vulnerable_response, 'seeded')
        self.assertNotContains(vulnerable_response, '<code>POST</code>')
        self.assertNotContains(vulnerable_response, 'scope-note')
        self.assertContains(secure_response, 'Bypass test value')
        self.assertContains(secure_response, 'Django ORM filtering')
        self.assertNotContains(secure_response, '<h1>Secure comparison</h1>')

    def test_vulnerable_login_can_be_bypassed_by_injection(self):
        response = self.client.post(
            reverse('lab-vulnerable-login'),
            {'username': "' OR 1=1 --", 'password': 'incorrect'},
        )
        self.assertRedirects(response, reverse('lab-result'))
        self.assertEqual(self.client.session['lab_mode'], 'vulnerable')

    def test_secure_login_rejects_same_injection_input(self):
        response = self.client.post(
            reverse('lab-secure-login'),
            {'username': "' OR 1=1 --", 'password': 'incorrect'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid lab username or password.')
        self.assertNotIn('lab_account', self.client.session)

    @override_settings(ENABLE_SECURITY_LABS=False)
    def test_lab_can_be_disabled(self):
        response = self.client.get(reverse('lab-vulnerable-login'))
        self.assertEqual(response.status_code, 404)
