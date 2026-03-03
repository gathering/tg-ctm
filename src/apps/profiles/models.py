from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  wannabe_id = models.CharField(max_length=200, blank=True)

  planned_meetup = models.DateTimeField(blank=True, null=True)

  def __str__(self): return self.user.get_full_name() or self.user.username

  @property
  def crew_name(self):
    if self.crew_memberships.count() > 1: return "Multi-crew"
    if self.crew_memberships.count() == 1:
      membership = self.crew_memberships.first()
      return membership.team.__str__() if membership.team else membership.crew.__str__()
    return "N/A"


class Crew(models.Model):
  crew_id = models.IntegerField()
  name = models.CharField(max_length=200)
  sorted_weight = models.IntegerField(default=0)

  def __str__(self): return self.name
  # extra properties: members, teams

  class Meta:
    ordering = ["sorted_weight", "name"]

  @property
  def chiefs(self): return self.members.filter(is_chief=True).order_by("profile__user__first_name", "profile__user__last_name")

  @property
  def members_without_team(self): return self.members.filter(team__isnull=True)


class CrewTeam(models.Model):
  team_id = models.IntegerField()
  crew = models.ForeignKey(Crew, on_delete=models.CASCADE, related_name="teams")
  name = models.CharField(max_length=200)

  def __str__(self): return f"{self.crew.name}:{self.name}"
  # extra properties: members

  class Meta:
    ordering = ["crew", "name"]


class CrewMember(models.Model):
  profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="crew_memberships")
  crew = models.ForeignKey(Crew, on_delete=models.CASCADE, related_name="members")
  team = models.ForeignKey(CrewTeam, on_delete=models.SET_NULL, blank=True, null=True, related_name="members")

  is_chief = models.BooleanField(default=False)
  title = models.CharField(max_length=200, blank=True, null=True)

  def __str__(self):
    team_or_crew = self.team if self.team else self.crew
    user_name = self.profile.user.get_full_name() or self.profile.user.username
    title_suffix = f" ({self.title})" if self.title else ""
    return f"{team_or_crew} - {user_name}{title_suffix}"
  # extra properties: none

  class Meta:
    ordering = ["crew", "team", "is_chief", "profile__user__first_name", "profile__user__last_name"]
