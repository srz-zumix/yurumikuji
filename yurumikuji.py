from dotenv import load_dotenv
load_dotenv()

import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from kamidana import (
    as_filter,
    as_global,
    as_globals_generator,
    as_test,
)

client = WebClient(token=os.environ['SLACK_TOKEN'])


@as_filter
def slack_user_id(v):
    try:
        result = client.users_list()
        users = result["members"]
        for user in users:
            if user['name'] == v:
                return user['id']
            profile = user['profile']
            if profile['real_name'] == v:
                return user['id']
            if profile['display_name'] == v:
                return user['id']
    except SlackApiError as e:
        return e


@as_filter
def slack_user_presence(v):
    try:
        result = client.users_getPresence(user=v)
        return result['presence']
    except SlackApiError as e:
        return e


@as_filter
def slack_user_info(v):
    try:
        result = client.users_info(user=v)
        return result['user']
    except SlackApiError as e:
        return e


@as_filter
def slack_user_info_by_email(v):
    try:
        result = client.users_lookupByEmail(email=v)
        return result['user']
    except SlackApiError as e:
        return e


@as_filter
def slack_user_profile(v):
    try:
        result = client.users_profile_get(user=v)
        return result['profile']
    except SlackApiError as e:
        return e


@as_filter
def slack_usergroup_id(v):
    try:
        result = client.usergroups_list()
        groups = result['usergroups']
        for group in groups:
            if group['name'] == v:
                return group['id']
    except SlackApiError as e:
        return e


@as_filter
def slack_usergroup_member_ids(v):
    try:
        result = client.usergroups_users_list(usergroup=v)
        return result['users']
    except SlackApiError as e:
        return e


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
        return e


@as_filter
def slack_search(v):
    try:
        result = client.search_messages(query=v)
        return result['messages']
    except SlackApiError as e:
        return e


@as_global
def slack_users_name():
    try:
        names = []
        result = client.users_list()
        users = result["members"]
        for user in users:
            names.append(user['name'])
        return names
    except SlackApiError as e:
        return e


@as_global
def slack_user_groups():
    try:
        result = client.usergroups_list()
        return result['usergroups']
    except SlackApiError as e:
        return e
