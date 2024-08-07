# yurumikuji

[![PyPI version](https://badge.fury.io/py/yurumikuji.svg)](https://badge.fury.io/py/yurumikuji)
[![Python Versions](https://img.shields.io/pypi/pyversions/wandbox_api.svg)](https://pypi.org/project/yurumikuji/)

[kamidana][] slack additonal

## Usage

```sh
$ pip install yurumikuji
$ echo "SLACK_TOKEN=<your token>" > .env
$ kamidana --additionals=yurumikuji.yurumikuji sample/profile.j2
https://secure.gravatar.com/avatar/a7614593f3f6f46b73da348c89beba81.jpg?s=512&d=https%3A%2F%2Fa.slack-edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0023-512.png
https://secure.gravatar.com/avatar/a7614593f3f6f46b73da348c89beba81.jpg?s=512&d=https%3A%2F%2Fa.slack-edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0023-512.png
active
```

sample/profile.j2

```j2
{{ ("srz_zumix" | slack_user_id | slack_user_info).profile.image_512 }}
{{ ("srz_zumix" | slack_user_id | slack_user_profile).image_512 }}
{{ "srz_zumix" | slack_user_id | slack_user_presence }}
```

## Features

### Filter

|name|usage|detail|slack required scope|
|:--|:--|:--|:--|
|slack_user_id|\<user_name\> \| slack_user_id |user name\|real_name\|display_name\|email to user_id|users:read|
|search_slack_user_id|\[\<user_names\>\] \| slack_user_id | Find user_id from multiple search candidates (user name\|real_name\|display_name\|email)|users:read|
|slack_user_presence|\<user_id\> \| slack_user_presence |get user presence|users:read|
|slack_user_info|\<user_id\> \| slack_user_info |get user info|users:read|
|slack_user_profile|\<user_id\> \| slack_user_profile |get user profile|users.profile:read|
|slack_user_info_by_email|\<user_email\> \| slack_user_info_by_email |get user info|users:read.email|
|slack_usergroup_id|\<usergroup_name\> \| slack_usergroup_id |usergroup name to usergroup_id|usergroups:read|
|slack_usergroup_member_ids|\<usergroup_id\> \| slack_usergroup_member_ids |get usergroup member user ids|usergroups:read|
|slack_usergroup_member_infos|\<usergroup_id\> \| slack_usergroup_member_infos |get usergroup member user info|usergroups:read|
|slack_usergroup_member_infos|\<usergroup_id\> \| slack_usergroup_member_infos |get usergroup member user info|usergroups:read|
|slack_search|\<search_query\> \| slack_search | search message |search:read|
|mention|\<user_or_usergroup_id\> \| mention | get user or group mention text ||
|mention_menber|\<user_id\> \| mention | get mention text ||
|mention_group|\<usergroup_id\> \| mention | get group mention text ||
|slack_channel_members|\<channel_id\> \| slack_channel_members | get channel members |channels:read|

### Globals

|name|usage|detail|slack required scope|
|:--|:--|:--|:--|
|slack_users_name| slack_users_name | list users name |users:read|
|slack_user_groups| slack_user_groups | list user groups |usergroups:read|

[kamidana]:https://github.com/podhmo/kamidana
