#
# yurumikuji.py
#
# MIT License
#
# Copyright (c) 2021 srz_zumix
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.http_retry import all_builtin_retry_handlers
from kamidana import (
  as_filter,
  as_global,
  as_globals_generator,
  as_test,
)

def load_dotenv():
  f = dotenv.find_dotenv(usecwd=True)
  return dotenv.load_dotenv(f)

load_dotenv()

retry_handlers = all_builtin_retry_handlers()
client = WebClient(token=os.environ['SLACK_TOKEN'], retry_handlers=retry_handlers)

slack_users_list = []

def on_error(e):
  if os.getenv('SLACK_API_ERROR_RAISE', 'false').lower() == 'true':
    raise e
  return e


@as_filter
def search_slack_user_id(v):
  def check(arr, key, v):
    return (key in arr) and (arr[key] in v)
  if not isinstance(v, list):
    v = [str(v)]
  for user in slack_users():
    if check(user, 'name', v):
      return user['id']
    if check(user, 'real_name', v):
      return user['id']
    if 'profile' in user:
      profile = user['profile']
      if check(profile, 'real_name', v):
        return user['id']
      if check(profile, 'display_name', v):
        return user['id']
      if check(profile, 'email', v):
        return user['id']
      if check(profile, 'real_name_normalized', v):
        return user['id']
      if check(profile, 'display_name_normalized', v):
        return user['id']
  return None


@as_filter
def slack_user_id(v):
  return search_slack_user_id([str(v)])


@as_filter
def slack_user_presence(v):
  try:
    result = client.users_getPresence(user=v)
    return result['presence']
  except SlackApiError as e:
    return on_error(e)


@as_filter
def slack_user_info(v):
  try:
    result = client.users_info(user=v)
    return result['user']
  except SlackApiError as e:
    return on_error(e)


@as_filter
def slack_user_info_by_email(v):
  try:
    result = client.users_lookupByEmail(email=v)
    return result['user']
  except SlackApiError as e:
    return on_error(e)


@as_filter
def slack_user_profile(v):
  try:
    result = client.users_profile_get(user=v)
    return result['profile']
  except SlackApiError as e:
    return on_error(e)


@as_filter
def slack_usergroup_id(v):
  try:
    result = client.usergroups_list()
    groups = result['usergroups']
    for group in groups:
      if group['name'] == v:
        return group['id']
  except SlackApiError as e:
    return on_error(e)


@as_filter
def slack_usergroup_member_ids(v):
  try:
    result = client.usergroups_users_list(usergroup=v)
    return result['users']
  except SlackApiError as e:
    return on_error(e)


@as_filter
def slack_usergroup_member_infos(v):
  try:
    result = client.usergroups_users_list(usergroup=v)
    infos = []
    for user in result['users']:
      info = client.users_info(user=user)
      infos.append(info['user'])
    return infos
  except SlackApiError as e:
    return on_error(e)


@as_filter
def slack_search(v):
  try:
    result = client.search_messages(query=v)
    return result['messages']
  except SlackApiError as e:
    return on_error(e)


@as_filter
def mention(v):
  if v in slack_user_groups():
    return mention_group(v)
  return mention_member(v)


@as_filter
def mention_member(v):
  return '<@{}>'.format(v) if v else ''


@as_filter
def mention_group(v):
  return '<!subteam^{}>'.format(v) if v else ''


@as_global
def slack_users():
  if len(slack_users_list) != 0:
    return slack_users_list
  try:
    cursor = None
    while True:
      result = client.users_list(cursor=cursor)
      slack_users_list.extend(result["members"])
      cursor = result.get('response_metadata', {}).get('next_cursor')
      if not cursor:
        break
    return slack_users_list
  except SlackApiError as e:
      return on_error(e)


@as_global
def slack_users_name():
  names = []
  for user in slack_users():
    names.append(user['name'])
  return names


@as_global
def slack_user_groups():
  try:
    result = client.usergroups_list()
    return result['usergroups']
  except SlackApiError as e:
    return on_error(e)


@as_filter
def slack_channel_members(v):
  try:
    result = client.conversations_members(channel=v)
    return result['members']
  except SlackApiError as e:
    return on_error(e)
