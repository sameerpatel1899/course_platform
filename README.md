# What We're Building: A Full-Featured Online Course Platform

# 3Courses Module

- Each course comes with:
        -  Title: Clear, searchable course name
        - Description: Brief overview of what the - - course covers
        - Thumbnail/Image: Visual identity for each course

- Access Levels:
        - Open Access – No login needed
        - Email Access – Email required to view content
        - Purchase Access – Requires one-time payment
        - Logged-In Users Only – (Optional / future scope)

- Course Status Options:
        - Published – Live and accessible to users
        - Coming Soon – Announced but not yet available
        - Draft – Still in editing phase

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
        - Email – Stores user emails for access
        - EmailVerificationToken – Manages token-based verification