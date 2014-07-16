SCHEDULES
=========


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

Schedules are provided in descending order by ``created_at`` field.

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

This methods return the ID of the last inserted schedule.

Authentication *required*.

.. NOTE::
  datetime must be exchanged in UTC format.


Delete schedule
---------------

Delete a schedule by ID. ::

    /api/delete_schedule/<id>

You have to pass data in the URL like ::

    http://localhost/api/delete_schedule/53a1f7154459d92264f3369e

In order to delete a schedule you have to use ``DELETE`` method.

Follow the next example to delete a schedule. ::

    curl -u username:password -i -H "Accept: application/json" -X DELETE http://localhost:9090/api/delete_schedule/53a1f7154459d92264f3369e

.. WARNING::
   no confirm or alert provided, you have to implement them on your own!

