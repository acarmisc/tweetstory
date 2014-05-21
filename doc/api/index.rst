ZombieTweet's API
=================

API Version
-----------

Curren version is *v0.2*; release date May, 20 2014.


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

    { "response": "UsErT0k3n" }

Where ``response`` contains the user logged token. This value must be used in the next queries.

Example: ::

    curl -i -H "Content-Type: application/json" -X POST -d '{"twitter_user": "twitter_username", "twitter_id": "twitter_uid", "time_zone": "Rome", "utc_offset": "7200", "profile_image_url": ""}' http://<host>/api/post_login


Get my schedules
----------------

Used to fetch user's schedules list from server. ::

    /api/get_schedules

Returns: ::

    {
      "schedules": [
        {
          "created_at": "2014-36-10 17:05:48",
          "end_date": "2014-57-10 17:05:01",
          "hashtag": "selfie",
          "id": "536e63c77a1d345acc9e2333",
          "start_date": "2014-37-10 17:05:01",
          "subject": "selfie",
          "uid": "acarmisc"
        },
        {
          "created_at": "2014-21-02 19:07:06",
          "end_date": "2014-19-02 20:08:32",
          "hashtag": "Crozza",
          "id": "5363f0307a1d344b54d982ee",
          "start_date": "2014-19-02 19:07:32",
          "subject": "Crozza",
          "uid": "acarmisc"
        }
      ]
    }

Authentication *required*.
Note: datetime must be exchanged in UTC format.


Get Zombies
-----------

Fetch zombies for the given schedule. ::

    /api/get_zombies/{schedule_id}

Returns: ::

    {
        "zombies": [
            {
              "author": "FutureOLLG_2",
              "avatar": "https://pbs.twimg.com/profile_images/464709234173558784/u_HPsCDm_normal.png",
              "created_at": "2014-37-10 17:05:38",
              "id": "536e63f17a1d345ad07873d8",
              "oid": "465183894372110336",
              "screen_name": "FutureOLLG_2",
              "text": "lorem ipsum dolor sit amet"
            },
            {
              "author": "LuFernandezSily",
              "avatar": "https://pbs.twimg.com/profile_images/440398976467353600/SUT-wxKI_normal.jpeg",
              "created_at": "2014-37-10 17:05:37",
              "id": "536e63f17a1d345ad07873dc",
              "oid": "465183891331244033",
              "screen_name": "LuFernandezSily",
              "text": "lorem ipsum dolor sit amet"
            },
        ]
    }

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
