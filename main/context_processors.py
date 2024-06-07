from django.http import HttpRequest

from . import models


def chapters(request: HttpRequest):
    if request.user.is_authenticated:
        return {
            "root_chapters": models.Chapter.objects.filter(
                parent=None, roles=request.user.role, is_active=True
            ),
            "root_chapter_groups": models.ChapterGroup.objects.filter(
                parent=None, roles=request.user.role, is_active=True
            ),
        }
    return {
        "root_chapters": models.Chapter.objects.filter(
            parent=None, is_default=True, is_active=True
        ),
        "root_chapter_groups": models.ChapterGroup.objects.filter(
            parent=None, is_default=True, is_active=True
        ),
    }
