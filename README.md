<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./tgctm/static/ctm-white.png">
  <img alt="ctm logo" src="./tgctm/static/ctm.png" height="100">
</picture>

# TG-CTM

The Gatherings Common Task Management

# Setup

The best way to go about this is to use Docker. Pull this repo, then run:

```
docker-compose up -d --build
docker-compose exec app python3 manage.py migrate
```

After this, you might want to create a user for logging in:

```
docker-compose exec app python3 manage.py createsuperuser
```

This user can be used to login in the admin panel, here: `/admin`
