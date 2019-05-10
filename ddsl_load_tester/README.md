# Some References

- [DDSL Locust](https://github.com/nimamahmoudi/ddsl_locust)
- [How do I Locust](https://github.com/pglass/how-do-i-locust)
- [Locust Web API Code](https://github.com/locustio/locust/blob/master/locust/web.py)
- [Locust Github](https://github.com/locustio/locust)

# Initialization

Uninstall locust library:
```bash
pip uninstall locust locustio
# Check successful uninstall
pip freeze | grep locust
```

Install the DDSL locust library:

```bash
pip install ddsl-locustio
```

# Starting the server

This will use the `locustfile.py` or we can specify the file name using -f option.

```
ddsl_locust --host=THE_TEST_URL -f locustfile.py
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
    "current_max_response_time": 760,
    "current_min_response_time": 420,
    "current_response_time_average": 438,
    "current_response_time_percentile_50": 450,
    "current_response_time_percentile_95": 760,
    "errors": [],
    "fail_ratio": 0,
    "state": "running",
    "stats": [
        {
            "avg_content_length": 100.2,
            "avg_response_time": 522.722864151001,
            "current_rps": 0.5,
            "max_response_time": 762.3703479766846,
            "median_response_time": 450,
            "method": "GET",
            "min_response_time": 421.9634532928467,
            "name": "/",
            "num_failures": 0,
            "num_requests": 5
        },
        {
            "avg_content_length": 100.2,
            "avg_response_time": 522.722864151001,
            "current_rps": 0.5,
            "max_response_time": 762.3703479766846,
            "median_response_time": 450,
            "method": null,
            "min_response_time": 421.9634532928467,
            "name": "Total",
            "num_failures": 0,
            "num_requests": 5
        }
    ],
    "total_average_response_time": 522.722864151001,
    "total_rps": 0.5,
    "user_count": 1
}
```
