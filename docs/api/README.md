# API Documentation

## Authentication
- POST /api/auth/register - User Registration
- POST /api/auth/login - User Login
- GET /api/auth/me - Get Current User Info
- PUT /api/auth/profile - Update User Profile

## User Profile
- GET /api/profile/skills - Get Skill Assessment
- GET /api/profile/achievements - Get User Achievements
- GET /api/profile/learning-path - Get Learning Path

## Course Management
- GET /api/courses - Get Course List
- GET /api/courses/{id} - Get Course Details
- POST /api/courses - Create Course
- PUT /api/courses/{id} - Update Course
- DELETE /api/courses/{id} - Delete Course

## Lab Environment
- GET /api/labs - Get Lab List
- POST /api/labs/start - Start Lab Environment
- POST /api/labs/stop - Stop Lab Environment
- GET /api/labs/status - Get Environment Status

## Learning Records
- GET /api/learning/progress - Get Learning Progress
- POST /api/learning/record - Record Learning Activity
- GET /api/learning/statistics - Get Learning Statistics

## Achievement System
- GET /api/achievements - Get Achievement List
- GET /api/achievements/user - Get User Achievements
- POST /api/achievements/verify - Verify Achievement Completion
