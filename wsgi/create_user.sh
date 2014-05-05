#!/bin/bash
for i in {1..10}
do
curl -i -H "Content-Type: application/json" -X POST -d '{"twitter_user": "user-'"$i"'", "twitter_id": "0000'"$i"'", "time_zone": "Rome", "utc_offset": "7200", "profile_image_url": ""}' http://localhost:9090/api/post_login

done