ZombieTweet
===========

http://www.zombietweet.com

Run
---

Environment variables must be set like next: ::
    export t_api_key=<yourdata>
    export t_api_secret=<yourdata>
    export t_acc_token=<yourdata>
    export t_acc_secret=<yourdata>

Exec ``uwsgi --http :9090 --wsgi-file wsgi_test.py --honour-stdin`` to emulate the OpenShift behaviour locally.
