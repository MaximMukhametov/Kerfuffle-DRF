class UserFields:
    """
    Dynamically include/exclude fields to Django Rest Framework serializers
    based on properties of this class. It's handling in __init__ method of
    Serializer class
    """

    user_show_fields = (
        'name', 'id', 'unique_url_name', 'photos', 'status', 'followers', 'following')
    users_upload_field = ('name', 'id', 'unique_url_name', 'photos', 'status')
    profile_contacts_put_fields = (
        'id', 'looking_for_a_job', 'background_photo',
        'looking_for_a_job_description',
        'full_name',
        'contacts',)
    profile_contacts_get_fields = (
        'id', 'name', 'background_photo', 'looking_for_a_job',
        'looking_for_a_job_description',
        'full_name', 'posts',
        'contacts', 'photos')
    status_fields = ('status',)
    user_auth_fields = ('id', 'name', 'photos', 'background_photo')
