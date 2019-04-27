# Some References

- [How do I Locust](https://github.com/pglass/how-do-i-locust)
- [Locust Web API Code](https://github.com/locustio/locust/blob/master/locust/web.py)
- [Locust Github](https://github.com/locustio/locust)

# Initialization

Install the locust library:

```
pip install locust
```

# Starting the server

This will use the `locustfile.py` or we can specify the file name using -f option.

```
locust --host=http://wg2.nmahmoudi.ir:31112/function/pyfibo
```

# Changing the number of users

Send a POST request to the endpoint `localhost:8089/swarm` with the following arguments:

```
locust_count: 10
hatch_rate: 3
```

The response is of the form:

```
{
    "message": "Swarming started",
    "success": true
}
```

# Getting the latest stats

These stats are usually updated at around once every 2 seconds. To get them, send a GET request
to `localhost:8089/stats/requests`. The result is of the following format:

```
{
    "current_response_time_percentile_50": 570,
    "current_response_time_percentile_95": 1300,
    "errors": [],
    "fail_ratio": 0,
    "state": "running",
    "stats": [
        {
            "avg_content_length": 4,
            "avg_response_time": 407.4528589435168,
            "current_rps": 131.2,
            "max_response_time": 10368.172645568848,
            "median_response_time": 350,
            "method": "GET",
            "min_response_time": 24.10292625427246,
            "name": "/function/pyfibo/",
            "num_failures": 0,
            "num_requests": 50212
        },
        {
            "avg_content_length": 4,
            "avg_response_time": 407.4528589435168,
            "current_rps": 131.2,
            "max_response_time": 10368.172645568848,
            "median_response_time": 350,
            "method": null,
            "min_response_time": 24.10292625427246,
            "name": "Total",
            "num_failures": 0,
            "num_requests": 50212
        }
    ],
    "total_rps": 131.2,
    "user_count": 1000
}
```
