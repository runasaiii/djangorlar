# Python modules
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from decimal import Decimal

# Django modules
from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Max

# Project modules
from apps.education.models import Course, Lesson
from apps.education.serializers import CourseSerializer, LessonSerializer
from apps.education.permissions import IsOwnerPermission


class CourseViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """List all non-deleted courses, with optional filtering by is_active."""
        courses = Course.objects.filter(deleted_at__isnull=True).select_related('owner').order_by('id')
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            courses = courses.filter(is_active=is_active.lower() == 'true')
        serializer = CourseSerializer(
            courses, 
            many=True,
            context={'request': request},
            )
        return Response(serializer.data)
    
    def create(self, request):
        """Create a new course."""
        serializer = CourseSerializer(
            data=request.data, 
            context={'request': request}
            )
        serializer.is_valid(raise_exception=True)
        course = serializer.save()
        return Response(
            CourseSerializer(course, context={'request': request}).data,
            status=status.HTTP_201_CREATED
            )
    
    def retrieve(self, request, pk=None):
        """Retrieve a specific course by ID."""
        course = get_object_or_404(
            Course, 
            pk=pk, 
            deleted_at__isnull=True
            )
        serializer = CourseSerializer(
            course,
            context={'request': request}
            )
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        """Update a specific course by ID."""
        course = get_object_or_404(
            Course, 
            pk=pk, 
            deleted_at__isnull=True
            )
        if course.owner.id != request.user.id:
            return Response(
                {'detail': 'Only owner can do updated'}, 
                status=status.HTTP_403_FORBIDDEN
                )
        serializer = CourseSerializer(
            course, 
            data=request.data, 
            context={'request': request}
            )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, pk=None):
        """Soft delete a specific course by ID."""
        course = get_object_or_404(
            Course, 
            pk=pk, 
            deleted_at__isnull=True
            )
        
        if course.owner.id != request.user.id:
            return Response(
                {'detail': 'Only owner can delete'}, 
                status=status.HTTP_403_FORBIDDEN
                )
        course.deleted_at = timezone.now()
        course.save(update_fields=['deleted_at'])
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate a specific course by ID."""
        course = get_object_or_404(
            Course, 
            pk=pk, 
            deleted_at__isnull=True
            )
        if course.owner.id != request.user.id:
            return Response(
                {'detail': 'Only owner can activate'}, 
                status=status.HTTP_403_FORBIDDEN
                )
        if course.is_active:
            return Response(
                {'detail': 'Course is already active.'}, 
                status=status.HTTP_400_BAD_REQUEST)
        course.is_active = True
        course.save(update_fields=['is_active'])
        return Response(CourseSerializer(course, context={'request': request}).data)
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate a specific course by ID."""
        course = get_object_or_404(
            Course, 
            pk=pk, 
            deleted_at__isnull=True
            )
        if course.owner.id != request.user.id:
            return Response(
                {'detail': 'Only owner can deactivate'}, 
                status=status.HTTP_403_FORBIDDEN
                )
        if not course.is_active:
            return Response(
                {'detail': 'Course is already inactive.'}, 
                status=status.HTTP_400_BAD_REQUEST)
        course.is_active = False
        course.save(update_fields=['is_active'])
        return Response(CourseSerializer(course, context={'request': request}).data)
    
    @action(detail=True, methods=['get'])
    def lessons(self, request, pk=None):
        """List all non-deleted lessons for a specific course."""
        course = get_object_or_404(
            Course, 
            pk=pk, 
            deleted_at__isnull=True
            )
        lessons_courses = course.lessons.filter(deleted_at__isnull=True)
        serializer = LessonSerializer(
            lessons_courses, 
            many=True,
            context={'request': request}
            )
        return Response(serializer.data)
    

class LessonViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        """Create a new lesson"""
        serializer = LessonSerializer(
            data=request.data, 
            context={'request': request}
            )
        serializer.is_valid(raise_exception=True)
        course = serializer.validated_data.get('course')
        if course.owner.id != request.user.id:
            return Response(
                {'detail': 'You must be the owner of course to add lessons'},
                status=status.HTTP_403_FORBIDDEN
                )
        lesson = serializer.save()
        return Response(
            LessonSerializer(lesson, context={'request': request}).data,
            status=status.HTTP_201_CREATED
            )
    

    def delete(self, request, pk=None):
        """Soft delete specific lesson by ID"""
        lesson = get_object_or_404(
            Lesson, 
            pk=pk, 
            deleted_at__isnull=True
            )
        if lesson.course.owner.id != request.user.id:
            return Response(
                {'detail': 'Only owner can delete lesson'}, 
                status=status.HTTP_403_FORBIDDEN
                )
        lesson.deleted_at = timezone.now()
        lesson.save(update_fields=['deleted_at'])
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['put'], url_path='move')
    def move(self, request, pk=None):
        """Move lesson to a new order within its course."""
        lesson = get_object_or_404(
            Lesson, 
            pk=pk, 
            deleted_at__isnull=True
            )
        if lesson.course.owner.id != request.user.id:
            return Response(
                {'detail': 'Only course owner can move lesson'}, 
                status=status.HTTP_403_FORBIDDEN
                )
        before_id = request.data.get('before_lesson_id', None)
        course = lesson.course
        
        if before_id is None:
            max_order = course.lessons.filter(deleted_at__isnull=True).aggregate(m=Max('order'))['m']
            if max_order is None:
                new_order = Decimal(0)
            else:
                new_order = max_order + Decimal('1')
            lesson.order = new_order
            lesson.indentation = 0
            lesson.save(update_fields=['order', 'indentation'])
            return Response({'order': str(lesson.order), 'indentation': lesson.indentation})
        else:
            try:
                target = course.lessons.get(
                    pk=before_id, 
                    deleted_at__isnull=True
                    )
            except Lesson.DoesNotExist:
                return Response(
                    {'detail': 'Target lesson does not exist in the same course.'}, 
                    status=status.HTTP_400_BAD_REQUEST
                    )
            
            prev_lesson = course.lessons.filter(
                order__lt=target.order,
                deleted_at__isnull=True).order_by('-order').first()
            if prev_lesson:
                prev_order = Decimal(prev_lesson.order)
                target_order = Decimal(target.order)

                new_order = (prev_order + target_order) / Decimal(2)
            else:
                new_order = Decimal(target.order) - Decimal('1')

            new_indentation = target.indentation
            if new_indentation > 5:
                new_indentation = 5

            lesson.order = new_order
            lesson.indentation = new_indentation
            lesson.save(update_fields=['order', 'indentation'])
            return Response({'order': str(lesson.order), 'indentation': lesson.indentation})
        
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """Publish a specific lesson by ID."""
        lesson = get_object_or_404(
            Lesson, 
            pk=pk, 
            deleted_at__isnull=True
            )
        if lesson.course.owner.id != request.user.id:
            return Response(
                {'detail': 'Only course owner can publish lesson'}, 
                status=status.HTTP_403_FORBIDDEN
                )
        lesson.is_published = True
        lesson.save(update_fields=['is_published'])
        return Response(
            LessonSerializer(lesson, context={'request': request}).data
            )
    
    @action(detail=True, methods=['post'])
    
    def unpublish(self, request, pk=None):
        """Unpublish a specific lesson by ID."""
        lesson = get_object_or_404(
            Lesson,
            pk=pk,
            deleted_at__isnull=True
        )
        if lesson.course.owner.id != request.user.id:
            return Response(
                {'detail': 'Only course owner can unpublish lesson'},
                status=status.HTTP_403_FORBIDDEN
            )
        lesson.is_published = False
        lesson.save(update_fields=['is_published'])
        return Response(LessonSerializer(lesson, context={'request': request}).data)
    
