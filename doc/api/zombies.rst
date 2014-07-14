ZOMBIES
=======


Get Zombies
-----------

Fetch zombies for the given schedule. ::

    /api/get_zombies/{schedule_id}/{page_n}

Where:
  - {schedule_id}: contains the ID of the desired schedule
  - {page_n}: is the number for pagination. The number of elements foreach page is set on the server side.

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
