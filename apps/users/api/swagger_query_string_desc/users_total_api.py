from drf_yasg import openapi

user_param = openapi.Parameter('user', openapi.IN_QUERY,
                               description="get particular user by id",
                               type=openapi.TYPE_INTEGER)
name_param = openapi.Parameter('name', openapi.IN_QUERY,
                               description="get user by name",
                               type=openapi.TYPE_STRING)
following_param = openapi.Parameter('following', openapi.IN_QUERY,
                                    description="get all followed users",
                                    type=openapi.TYPE_BOOLEAN)
followers_param = openapi.Parameter('followers', openapi.IN_QUERY,
                                    description="get all followers",
                                    type=openapi.TYPE_BOOLEAN)
post_id_param = openapi.Parameter('post_id', openapi.IN_QUERY,
                                  description="get all users who likes "
                                              "particular post by id",
                                  type=openapi.TYPE_INTEGER)
