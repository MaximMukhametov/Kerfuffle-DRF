# SECURITY WARNING: keep the secret key used in production secret!
import os
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY',
                            'cg#p$g+j9tax!#a3cup@1$8obt2_+&k3q+pmu)5%asj6yjpkag')
ALLOWED_HOSTS = ['social-network-spa.herokuapp.com','*']