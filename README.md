# RedTeam Blog (Django)

A multi-user blog built with Python and Django, with user accounts, posts and voting.

Originally built as a team project for **SDEV 265 (Ivy Tech Community College, Summer 2024)**. Later repaired and tested: resolved merge conflicts, fixed broken routes and templates, added permission checks and an automated test suite.

<!-- Add 2-3 screenshots here: the post list, a post page and the login page.
![Post list](screenshots/post_list.png) -->

## Features

- User registration, login and logout (Django authentication)
- Create, edit and delete posts. Only the author can edit or delete a post.
- Upvote and downvote posts, with **one vote per user per post** (voting the other way switches your vote)
- Public profile pages that list each user's posts
- Login required for writing and voting. Browsing is public.

## Tech stack

Python, Django 4.2, SQLite, HTML/CSS (Bootstrap 4)

## Run it locally

```bash
# 1. Clone the repo and enter the folder
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create the database
python manage.py migrate

# 5. Start the server
python manage.py runserver
```

Open http://127.0.0.1:8000/ and register an account. To use the admin site, run `python manage.py createsuperuser` and visit `/admin/`.

## Run the tests

```bash
python manage.py test
```

The suite has 10 tests covering registration, login-required pages, author-only editing and deleting, one-vote-per-user logic, and public pages.

## Data model

- **Post**: author, title, text, created and published dates
- **Upvote / Downvote**: link a user to a post, with a uniqueness constraint so a user can vote once per post
- **Profile**: one-to-one with User (stores a profile image)

## Configuration

The secret key and debug mode are read from environment variables. The defaults are for local development only:

| Variable | Purpose | Default |
|---|---|---|
| `DJANGO_SECRET_KEY` | Django secret key | development-only key |
| `DJANGO_DEBUG` | Debug mode (`True` / `False`) | `True` |

Set both before deploying anywhere public.

## Known limitations

- Profile images exist in the model but cannot be uploaded from the site yet.
- Votes use plain links (GET requests). Using POST requests with CSRF protection would be safer.
- No comments or pagination yet.
- Pinned to Django 4.2 (LTS). Logout via link relies on behavior removed in Django 5.

## My contributions

[Add what you personally built, for example: "Implemented the voting system and author-only permissions" or "Repaired the project and wrote the test suite".]
