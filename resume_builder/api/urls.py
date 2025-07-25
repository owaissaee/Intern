from django.urls import path, include
from rest_framework.routers import DefaultRouter

from resume_builder.api.api import (
    ResumeTemplateViewSet, ResumeViewSet, ResumeSectionViewSet,
    WorkExperienceViewSet, TechnicalSkillViewSet, EducationViewSet,
    TechnologyViewSet, ProjectViewSet, CertificationViewSet,
    AwardViewSet, LanguageViewSet
)

router = DefaultRouter()
router.register(r'resume-templates', ResumeTemplateViewSet)
router.register(r'resumes', ResumeViewSet)
router.register(r'resume-sections', ResumeSectionViewSet)
router.register(r'work-experiences', WorkExperienceViewSet)
router.register(r'technical-skills', TechnicalSkillViewSet)
router.register(r'educations', EducationViewSet)
router.register(r'technologies', TechnologyViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'certifications', CertificationViewSet)
router.register(r'awards', AwardViewSet)
router.register(r'languages', LanguageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]