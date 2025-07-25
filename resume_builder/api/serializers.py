from rest_framework import serializers

from resume_builder.models import (
    ResumeTemplate, Resume, ResumeSection, WorkExperience,
    TechnicalSkill, Education, Technology, Project,
    Certification, Award, Language
)



class ResumeTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeTemplate
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class ResumeSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeSection
        exclude = ['resume']


class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        exclude = ['resume']


class TechnicalSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalSkill
        exclude = ['resume']


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        exclude = ['resume']


class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = ['id', 'name', 'category', 'icon']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        exclude = ['resume']


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        exclude = ['resume']


class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        exclude = ['resume']


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        exclude = ['resume']


class ResumeSerializer(serializers.ModelSerializer):
    sections = ResumeSectionSerializer(many=True, read_only=True)
    work_experiences = WorkExperienceSerializer(many=True, read_only=True)
    technical_skills = TechnicalSkillSerializer(many=True, read_only=True)
    educations = EducationSerializer(many=True, read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)
    certifications = CertificationSerializer(many=True, read_only=True)
    awards = AwardSerializer(many=True, read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)

    class Meta:
        model = Resume
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at', 'last_modified']
