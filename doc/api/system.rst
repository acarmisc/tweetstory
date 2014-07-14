SYSTEM AND SECURITY
===================


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
