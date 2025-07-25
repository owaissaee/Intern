import tempfile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from resume_builder.models import (
    ResumeTemplate, Resume, ResumeSection, WorkExperience,
    TechnicalSkill, Education, Technology, Project,
    Certification, Award, Language
)

User = get_user_model()


def create_user():
    return User.objects.create_user(email='test@example.com', password='testpass123')


class ResumeTemplateTests(APITestCase):
    def setUp(self):
        self.user = create_user()
        self.client.force_authenticate(self.user)
        self.url = reverse('resumetemplate-list')
        self.data = {
            'name': 'Classic',
            'format_type': 'CLASSIC',
            'description': 'A classic template',
            'version': 1,
        }

    def test_create_resume_template(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_resume_templates(self):
        ResumeTemplate.objects.create(**self.data)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_resume_template(self):
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.template.refresh_from_db()
        self.assertEqual(self.template.name, 'Updated Template')

    def test_delete_resume_template(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ResumeTemplate.objects.filter(id=self.template.id).exists())


class TechnologyTests(APITestCase):
    def setUp(self):
        self.user = create_user()
        self.client.force_authenticate(self.user)
        self.url = reverse('technology-list')
        self.data = {'name': 'Python', 'category': 'LANG'}

    def test_create_technology(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_technologies(self):
        Technology.objects.create(**self.data)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_technology(self):
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.technology.refresh_from_db()
        self.assertEqual(self.technology.name, 'Updated Technology')

    def test_delete_technology(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Technology.objects.filter(id=self.technology.id).exists())


class ResumeTests(APITestCase):
    def setUp(self):
        self.user = create_user()
        self.client.force_authenticate(self.user)
        self.template = ResumeTemplate.objects.create(name='Modern', format_type='MODERN')
        self.url = reverse('resume-list')
        self.data = {
            'user': self.user.id,
            'title': 'My Resume',
            'slug': 'my-resume',
            'template': self.template.id,
            'language': 'en',
            'visibility': 'PRIVATE',
        }

    def test_create_resume(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_resumes(self):
        Resume.objects.create(user=self.user, title='Test', slug='test', template=self.template)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_resume(self):
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.resume.refresh_from_db()
        self.assertEqual(self.resume.title, 'Updated Resume')

    def test_delete_resume(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Resume.objects.filter(id=self.resume.id).exists())


class ResumeSectionTests(APITestCase):
    def setUp(self):
        self.user = create_user()
        self.client.force_authenticate(self.user)
        self.template = ResumeTemplate.objects.create(name='Modern', format_type='MODERN')
        self.resume = Resume.objects.create(user=self.user, title='Test', slug='test', template=self.template)
        self.url = reverse('resumesection-list')
        self.data = {
            'resume': self.resume.id,
            'section_type': 'SUMMARY',
            'title': 'Summary',
            'content': {},
        }

    def test_create_resume_section(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_resume_sections(self):
        ResumeSection.objects.create(resume=self.resume, section_type='SUMMARY', title='Summary')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WorkExperienceTests(APITestCase):
    def setUp(self):
        self.user = create_user()
        self.client.force_authenticate(self.user)
        self.template = ResumeTemplate.objects.create(name='Modern', format_type='MODERN')
        self.resume = Resume.objects.create(user=self.user, title='Test', slug='test', template=self.template)
        self.url = reverse('workexperience-list')
        self.data = {
            'resume': self.resume.id,
            'job_title': 'Developer',
            'company': 'Company',
            'start_date': '2020-01-01',
        }

    def test_create_work_experience(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_work_experiences(self):
        WorkExperience.objects.create(resume=self.resume, job_title='Dev', company='Co', start_date='2020-01-01')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TechnicalSkillTests(APITestCase):
    def setUp(self):
        self.user = create_user()
        self.client.force_authenticate(self.user)
        self.template = ResumeTemplate.objects.create(name='Modern', format_type='MODERN')
        self.resume = Resume.objects.create(user=self.user, title='Test', slug='test', template=self.template)
        self.technology = Technology.objects.create(name='Python', category='LANG')
        self.url = reverse('technicalskill-list')
        self.data = {
            'resume': self.resume.id,
            'technology': self.technology.id,
            'proficiency': 100,
        }

    def test_create_technical_skill(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_technical_skills(self):
        TechnicalSkill.objects.create(resume=self.resume, technology=self.technology, proficiency=100)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class EducationTests(APITestCase):
    def setUp(self):
        self.user = create_user()
        self.client.force_authenticate(self.user)
        self.template = ResumeTemplate.objects.create(name='Modern', format_type='MODERN')
        self.resume = Resume.objects.create(user=self.user, title='Test', slug='test', template=self.template)
        self.url = reverse('education-list')
        self.data = {
            'resume': self.resume.id,
            'degree': 'BSc',
            'institution': 'Uni',
            'start_date': '2018-01-01',
            'end_date': '2022-01-01',
        }

    def test_create_education(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_educations(self):
        Education.objects.create(resume=self.resume, degree='BSc', institution='Uni', start_date='2018-01-01',
                                 end_date='2022-01-01')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProjectTests(APITestCase):
    def setUp(self):
        self.user = create_user()
        self.client.force_authenticate(self.user)
        self.template = ResumeTemplate.objects.create(name='Modern', format_type='MODERN')
        self.resume = Resume.objects.create(user=self.user, title='Test', slug='test', template=self.template)
        self.url = reverse('project-list')
        self.data = {
            'resume': self.resume.id,
            'title': 'Project',
            'role': 'Lead',
            'start_date': '2021-01-01',
            'description': 'Desc',
        }

    def test_create_project(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_projects(self):
        Project.objects.create(resume=self.resume, title='Project', role='Lead', start_date='2021-01-01',
                               description='Desc')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CertificationTests(APITestCase):
    def setUp(self):
        self.user = create_user()
        self.client.force_authenticate(self.user)
        self.template = ResumeTemplate.objects.create(name='Modern', format_type='MODERN')
        self.resume = Resume.objects.create(user=self.user, title='Test', slug='test', template=self.template)
        self.url = reverse('certification-list')
        self.data = {
            'resume': self.resume.id,
            'name': 'Cert',
            'issuer': 'Org',
            'issue_date': '2022-01-01',
        }

    def test_create_certification(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_certifications(self):
        Certification.objects.create(resume=self.resume, name='Cert', issuer='Org', issue_date='2022-01-01')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AwardTests(APITestCase):
    def setUp(self):
        self.user = create_user()
        self.client.force_authenticate(self.user)
        self.template = ResumeTemplate.objects.create(name='Modern', format_type='MODERN')
        self.resume = Resume.objects.create(user=self.user, title='Test', slug='test', template=self.template)
        self.url = reverse('award-list')
        self.data = {
            'resume': self.resume.id,
            'title': 'Award',
            'issuer': 'Org',
            'issue_date': '2022-01-01',
            'category': 'professional',
        }

    def test_create_award(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_awards(self):
        Award.objects.create(resume=self.resume, title='Award', issuer='Org', issue_date='2022-01-01',
                             category='professional')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LanguageTests(APITestCase):
    def setUp(self):
        self.user = create_user()
        self.client.force_authenticate(self.user)
        self.template = ResumeTemplate.objects.create(name='Modern', format_type='MODERN')
        self.resume = Resume.objects.create(user=self.user, title='Test', slug='test', template=self.template)
        self.url = reverse('language-list')
        self.data = {
            'resume': self.resume.id,
            'name': 'English',
            'proficiency': 'native',
        }

    def test_create_language(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_languages(self):
        Language.objects.create(resume=self.resume, name='English', proficiency='native')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

