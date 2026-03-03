from django.contrib.auth import get_user_model
from ..models import *
from .formatting import remove_emojis
from ..idam import TGBT

chief_ids = {18, 19}

def sync():
  tgbt = TGBT()

  User = get_user_model()
  num_new_users = 0
  num_updated_users = 0
  num_new_crews = 0
  num_updated_crews = 0
  current_syced_wannabe_users = User.objects.filter(profile__wannabe_id__isnull=False)

  for crew in tgbt.get_all_crews_with_crew_members():
    is_new_crew = False
    is_updated_crew = False

    if not Crew.objects.filter(crew_id=crew['id']).exists():
      new_crew = Crew.objects.create(
        crew_id=crew['id'],
        name=crew['name'],
        sorted_weight=crew['sorted_weight']
      )
      is_new_crew = True
    else:
      new_crew = Crew.objects.get(crew_id=crew['id'])
      if new_crew.name != crew['name'] or new_crew.sorted_weight != crew['sorted_weight']:
        new_crew.name = crew['name']
        new_crew.sorted_weight = crew['sorted_weight']
        new_crew.save()
        is_updated_crew = True

    for user in crew['users']:
      is_new_user = False
      is_updated_user = False

      full_name = remove_emojis(user['profile']['name'])
      first_name, last_name = str(full_name).rsplit(' ', 1)

      if not User.objects.filter(email=user['profile']['email']).exists():
        new_user = User.objects.create(
          username=user['profile']['email'],
          email=user['profile']['email'],
          first_name=first_name,
          last_name=last_name
        )
        new_user.profile.wannabe_id = user['user_id']
        new_user.profile.save()
        is_new_user = True
      else:
        if Profile.objects.filter(wannabe_id=user['user_id']).exists():
          new_user = User.objects.get(profile__wannabe_id=user['user_id'])
        else:
          new_user = User.objects.get(email=user['profile']['email'])

        email = user['profile']['email']
        wannabe_id = user['user_id']
        if (new_user.username, new_user.email, new_user.first_name, new_user.last_name, new_user.profile.wannabe_id) != (email, email, first_name, last_name, wannabe_id):
          new_user.username = email
          new_user.email = email
          new_user.first_name = first_name
          new_user.last_name = last_name
          new_user.save()
          new_user.profile.wannabe_id = wannabe_id
          new_user.profile.save()
          is_updated_user = True
      current_syced_wannabe_users = current_syced_wannabe_users.exclude(id=new_user.id)

      team_id = user['team']['id'] if user['team'] else None
      if team_id:
        if not CrewTeam.objects.filter(team_id=team_id, crew=new_crew).exists():
          new_team = CrewTeam.objects.create(
            team_id=team_id,
            crew=new_crew,
            name=user['team']['name']
          )
          if not is_new_crew: is_updated_crew = True
        else:
          new_team = CrewTeam.objects.get(team_id=team_id, crew=new_crew)
          if new_team.name != user['team']['name']:
            new_team.name = user['team']['name']
            new_team.save()
            if not is_new_crew: is_updated_crew = True

      if not CrewMember.objects.filter(profile=new_user.profile, crew=new_crew).exists():
        new_crew_member = CrewMember.objects.create(
          profile=new_user.profile,
          crew=new_crew,
          team=new_team if team_id else None,
          is_chief=True if user['role']['id'] in chief_ids else False,
          title=user['custom_title'] or user['role']['title']
        )
        if not is_new_user: is_updated_user = True
      else:
        new_crew_member = CrewMember.objects.get(profile=new_user.profile, crew=new_crew)
        if (new_crew_member.team, new_crew_member.is_chief, new_crew_member.title) != (new_team if team_id else None, True if user['role']['id'] in chief_ids else False, user['custom_title'] or user['role']['title']):
          new_crew_member.team = new_team if team_id else None
          new_crew_member.is_chief = True if user['role']['id'] in chief_ids else False
          new_crew_member.title = user['custom_title'] or user['role']['title']
          new_crew_member.save()
          if not is_new_user: is_updated_user = True

    if is_new_user: num_new_users += 1
    elif is_updated_user: num_updated_users += 1
  if is_new_crew: num_new_crews += 1
  elif is_updated_crew: num_updated_crews += 1

  deleted_users = 0
  for olduser in current_syced_wannabe_users:
    if not olduser.is_superuser:
      olduser.delete()
      deleted_users += 1

  return {
    "new_users": num_new_users,
    "updated_users": num_updated_users,
    "new_crews": num_new_crews,
    "updated_crews": num_updated_crews,
    "deleted_users": deleted_users
  }
