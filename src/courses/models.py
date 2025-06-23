import uuid
from django.db import models
import helpers
from cloudinary.models import CloudinaryField
from django.utils import timezone
from django.utils.text import slugify

helpers.cloudinary_init()

"""
- Each course comes with:
        -  Title: Clear, searchable course name
        - Description: Brief overview of what the - - course covers
        - Thumbnail/Image: Visual identity for each course

- Access Levels:
        - Open Access : No login needed
        - Email Access : Email required to view content
        - Purchase Access : Requires one-time payment
        - Logged-In Users Only : (Optional / future scope)

- Course Status Options:
        - Published : Live and accessible to users
        - Coming Soon : Announced but not yet available
        - Draft : Still in editing phase

- Lessons (Per Course):
        - Title & Description
        - Embedded Video Content
        - Status: Published, Coming Soon, or Draft

- Email Verification Flow (For Limited-Time Access):
        - Collect Email from user
        - Send Verification Token
        - Verify Email
        - Activate Session for limited-time access

- Core Models:
        - Email : Stores user emails for access
        - EmailVerificationToken : Manages token-based verification

"""

class AccessRequirement(models.TextChoices):
    ANYONE = "any", "Anyone"
    EMAIL_REQUIRED ="email_required", "Email Required"


class PublishStatus(models.TextChoices):
    PUBLISHED = "publish", "Published"
    COMING_SOON ="soon", "Coming Soon"
    DRAFT = "draft", "Draft"

def handle_upload(instance, filename):
    return f"{filename}"

# from courses.models import Course
# Course.objects.all() -> List out all courses
# Course.objects.first() -> first row of all courses

def get_public_id_prefix(instance, *args, **kwargs):
    title = instance.title
    if title:
        slug = slugify(title)
        unique_id = str(uuid.uuid4()).replace("-", "")[:5]
        return f"courses/{slug}-{unique_id}"
    if instance.id:
        return "courses/{instance.id}"
    return "courses"

def get_display_name(instance, *args, **kwargs):
    title = instance.title
    if title:
        return title
    return "course Upload"

class Course(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    # image= models.ImageField(upload_to=handle_upload, blank=True, null=True)
    image = CloudinaryField(
        "image", 
        null=True,
        public_id_prefix=get_public_id_prefix,
        display_name=get_display_name,
        tags=["course", "thumbnail"]
    )
    access = models.CharField(
        max_length=20,
        choices=AccessRequirement.choices,
        default=AccessRequirement.EMAIL_REQUIRED
    )
    
    status = models.CharField(
        max_length=10,
        choices=PublishStatus.choices,
        default=PublishStatus.DRAFT
    )

    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    @property
    def is_published(self):
        return self.status ==PublishStatus.PUBLISHED
    
    @property
    def image_admin(self):
        if not self.image:
            return ""
        image_options = {
            "width": 200
        }
        url = self.image.build_url(**image_options)
        return url
    
  
    def get_image_thumbnail(self, as_html=False, width=500):
        if not self.image:
            return ""
        image_options = {
            "width": width
        }
        if as_html:
            return self.image.image(**image_options)
        url = self.image.build_url(**image_options)
        return url
    

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    thumbnail = CloudinaryField("image", blank=True, null=True)
    video = CloudinaryField("video", blank=True, null=True, resource_type='video')
    order = models.IntegerField(default=0)
    can_preview = models.BooleanField(default=False, help_text="If user does not have access to course, can they see this?")
    status = models.CharField(
        max_length=10,
        choices=PublishStatus.choices,
        default=PublishStatus.PUBLISHED
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-updated']