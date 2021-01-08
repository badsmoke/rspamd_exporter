# rspamd_exporter
prometheus exporter for rspamd spam filter

inspired by [thannaske](https://github.com/thannaske/rspamd-influxdb) but for prometheus


if other architectures are desired, like arm or arm64, just let us know

MAINTAINER badsmoke <dockerhub@badcloud.eu>

### Environment Variables

ENV_URL = e.g https://mail.server.de/rspamd/ <br>
ENV_PASSWORD = e.g "secret_raspmd_passord"


### Docker- Compose

```
version: '2'
services:
  rspamd-exporter:
    restart: always
    image: badsmoke/rspamd-exporter:1.0.3
    ports:
        - 9500:5000
    environment:
        - "ENV_URL=https://mail.server.de/rspamd/"
        - "ENV_PASSWORD=secret_rspamd_password"

```

### docker run 

```
docker run -e "ENV_URL=http://mail.server.de/rspamd/" -e "ENV_PASSWORD=secret_rspamd_password" -p 9500:5000 badsmoke/rspamd-exporter:1.0.3
```



### Dockerfile
```
FROM python:3-slim-buster

MAINTAINER badsmoke <dockerhub@badcloud.eu>


WORKDIR /usr/src/app



COPY server.py ./server.py
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python","-u","/usr/src/app/server.py" ]

```

### original rspamd metrics

```json

{
  "read_only": false,
  "scanned": 46490,
  "learned": 35,
  "actions": {
    "reject": 27,
    "soft reject": 0,
    "rewrite subject": 0,
    "add header": 57,
    "greylist": 264,
    "no action": 46142
  },
  "spam_count": 84,
  "ham_count": 46406,
  "connections": 233,
  "control_connections": 33154,
  "pools_allocated": 63594,
  "pools_freed": 63554,
  "bytes_allocated": 31461256,
  "chunks_allocated": 320,
  "shared_chunks_allocated": 85,
  "chunks_freed": 0,
  "chunks_oversized": 235,
  "fragmented": 0,
  "total_learns": 35,
  "statfiles": [
    {
      "revision": 4,
      "used": 0,
      "total": 0,
      "size": 0,
      "symbol": "BAYES_SPAM",
      "type": "redis",
      "languages": 0,
      "users": 1
    },
    {
      "revision": 31,
      "used": 0,
      "total": 0,
      "size": 0,
      "symbol": "BAYES_HAM",
      "type": "redis",
      "languages": 0,
      "users": 1
    }
  ],
  "fuzzy_hashes": {
    "local": 15,
    "rspamd.com": 1075751952,
    "mailcow": 11951
  }
}

```

prometheus values
```
rspamd_actions_reject 27
rspamd_actions_soft_reject 0
rspamd_actions_rewrite_subject 0
rspamd_actions_add_header 57
rspamd_actions_greylist 264
rspamd_actions_no_action 46142
rspamd_stats_scanned 46490
rspamd_stats_learned 35
rspamd_stats_spam_count 84
rspamd_stats_ham_count 46406
rspamd_stats_connections 233
rspamd_stats_control_connections 33191
rspamd_stats_pools_allocated 63662
rspamd_stats_pools_freed 63622
rspamd_stats_bytes_allocated 31463624
rspamd_stats_chunks_allocated 320
rspamd_stats_chunks_freed 0
rspamd_stats_chunks_oversized 235
rspamd_stats_fragmented 0
rspamd_stats_total_learns 35
rspamd_stats_fuzzy 1075756039


```