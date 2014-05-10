ZombieTweet's API
=================

API Version
-----------

Curren version is *v0.1*; release date May, 10 2014.


Get Status
----------

Used to test if app is online. ::

    /api/status

Returns: ::

    { "response": "Service online" }

Authentication *required*.
Note: datetime must be exchanged in UTC format.


Post-login with Twitter
-----------------------

Used as callback URL after successul Twitter login. ::

    /api/post_login

Returns: ::

    HTTP/1.1 200 OK
    Date: Sat, 10 May 2014 10:29:30 GMT
    Server: Apache/2.2.15 (Red Hat)
    Content-Length: 4
    Content-Type: text/html; charset=utf-8
    Vary: Accept-Encoding

    myToken

Where ``myToken`` is the user logged token. This value must be used in the next queries.

Example: ::

    curl -i -H "Content-Type: application/json" -X POST -d '{"twitter_user": "twitter_username", "twitter_id": "twitter_uid", "time_zone": "Rome", "utc_offset": "7200", "profile_image_url": ""}' http://<host>/api/post_login


Get my schedules
----------------

Used to fetch user's schedules list from server. ::

    /api/get_schedules

Returns: ::

    [
      {
        "_cls": "Schedule",
        "_id": {
          "$oid": "5363f10584fda5d98eb402b8"
        },
        "created_at": {
          "$date": 1399058625459
        },
        "end_date": {
          "$date": 1399063800000
        },
        "hashtag": "Crozza",
        "start_date": {
          "$date": 1399058634000
        },
        "subject": "Crozza 2 maggio",
        "uid": "acarmisc"
      }
    ]

Authentication *required*.
Note: datetime must be exchanged in UTC format.


Get Zombies
-----------

Fetch zombies for the given schedule. ::

    /api/get_zombies/{schedule_id}

Returns: ::

    [
        {
            "oid": "462320872335106048",
            "screen_name": "john",
            "author": "John Doe",
            "text": "Tweet text",
            "created_at": {"$date": 1399060860000},
            "hashtags": ["crozzanelpaesedellemeraviglie"],
            "avatar": "https://pbs.twimg.com/profile_images/123456/aaaaa_normal.jpeg",
            "_id": {"$oid": "5363f9a184fda585d3df798b"},
            "_cls": "Zombie"
        },
    ]

Authentication *required*.
Note: datetime must be exchanged in UTC format.


Create schedule
---------------

Create a new schedule. ::

    /api/create_schedule

You have to pass data in a POST like ::

    {
        "end_date": "2014-05-02 20:04:06",
        "hashtag": "#dolorSit",
        "start_date": "2014-05-02 19:04:06",
        "subject": "Lorem ipsum"
    }

Follow the next example to insert new schedule. ::

    curl -u username:password -i -H "Content-Type: application/json" -X POST -d '{"subject": "Lorem ipsum", "hashtag": "#dolorSit", "start_date": "2014-05-02 19:04:06", "end_date": "2014-05-02 20:04:06"}' http:///api/create_schedule

Authentication *required*.
Note: datetime must be exchanged in UTC format.
