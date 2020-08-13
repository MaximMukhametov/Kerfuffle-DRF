"""
Dynamically include/exclude fields to Django Rest Framework serializers
based on properties of this class. It's handling in __init__ method of
Serializer class
"""

user_show_fields = (
    'name', 'id', 'unique_url_name', 'photos', 'status', 'following')
users_upload_field = ('name', 'id', 'unique_url_name', 'photos', 'status')
profile_fields = (
    'id', 'name', 'background_photo', 'looking_for_a_job',
    'looking_for_a_job_description',
    'full_name', 'posts',
    'contacts', 'photos')
user_auth_fields = ('id', 'name', 'photos', 'background_photo')
like_users_fields = ('id', 'name', 'photos')
