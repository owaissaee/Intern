from rest_framework import viewsets

from resume_builder.models import (
    ResumeTemplate, Resume, ResumeSection, WorkExperience,
    TechnicalSkill, Education, Technology, Project,
    Certification, Award, Language
)
from resume_builder.api.serializers import (
    ResumeTemplateSerializer, ResumeSerializer, ResumeSectionSerializer,
    WorkExperienceSerializer, TechnicalSkillSerializer, EducationSerializer,
    TechnologySerializer, ProjectSerializer, CertificationSerializer,
    AwardSerializer, LanguageSerializer
)


class ResumeTemplateViewSet(viewsets.ModelViewSet):
    queryset = ResumeTemplate.objects.all()
    serializer_class = ResumeTemplateSerializer


class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer


class ResumeSectionViewSet(viewsets.ModelViewSet):
    queryset = ResumeSection.objects.all()
    serializer_class = ResumeSectionSerializer


class WorkExperienceViewSet(viewsets.ModelViewSet):
    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer


class TechnicalSkillViewSet(viewsets.ModelViewSet):
    queryset = TechnicalSkill.objects.all()
    serializer_class = TechnicalSkillSerializer


class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer


class TechnologyViewSet(viewsets.ModelViewSet):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class CertificationViewSet(viewsets.ModelViewSet):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer


class AwardViewSet(viewsets.ModelViewSet):
    queryset = Award.objects.all()
    serializer_class = AwardSerializer


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer