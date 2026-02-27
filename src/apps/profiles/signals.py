from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import Group
from .idam import TGBT
import jwt


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
  if created:
    Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
  instance.profile.save()

@receiver(user_logged_in)
def add_wb_id_to_profile(sender, user, request, **kwargs):
  public_key = settings.SOCIAL_AUTH_KEYCLOAK_PUBLIC_KEY
  if public_key is None: return
  key = '-----BEGIN PUBLIC KEY-----\n' + public_key + '\n-----END PUBLIC KEY-----'
  key_binary = key.encode('ascii')
  aud = settings.SOCIAL_AUTH_KEYCLOAK_KEY
  try:
    wannabe_user_id = jwt.decode(user.social_auth.get(provider='keycloak').extra_data['access_token'], key_binary, audience=aud, verify=False, algorithms=["RS256"])['sub'] # We do not bother to decode the JWT token since the token should already be verified.
    user.profile.wannabe_id = wannabe_user_id
    user.profile.save()
  except jwt.exceptions.InvalidTokenError as e:
    print("Failed to decode JWT. Error: " + str(e))
  except Exception as e:
    print("A general error occured. Error: " + str(e)) #ohwell

  if user.profile.wannabe_id != None:
    tgbt = TGBT()
    if tgbt.in_use is False: return

    crew_name = tgbt.get_user_from_wb_user_id(user.profile.wannabe_id)['crew']['name']
    if Group.objects.filter(name=crew_name).count() == 0:
      group = Group.objects.create(name=crew_name)
    else:
      group = Group.objects.filter(name=crew_name).first()

    group.user_set.add(user)
