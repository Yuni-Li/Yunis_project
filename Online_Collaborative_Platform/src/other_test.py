from other import clear, users_all, admin_userpermission_change, search
from channel_data import data
import pytest
from error import InputError, AccessError

def test_clear():
    data['users'].append({'u_id': 1})
    data['users'].append({'u_id': 2})
    clear()
    assert data == {
        'users': [],
        'channels': [],
    }

def test_users_all():
    clear()
    data['users'].append({
        'u_id': 1,
        'email': 'cs1531@cse.unsw.edu.au',
        'name_first': 'Hayden',
        'name_last': 'Jacobs',
        'handle_str': 'hjacobs',
        'token': '1',
    })
    data['users'].append({
        'u_id': 2,
        'email': 'cs1532@cse.unsw.edu.au',
        'name_first': 'Rei',
        'name_last': 'Ayanami',
        'handle_str': 'rayanami',
        'token': '2',
    })

    assert users_all('1') == {
        'users': [
            {
                'u_id': 1,
                'email': 'cs1531@cse.unsw.edu.au',
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
                'handle_str': 'hjacobs',
            },
            {
                'u_id': 2,
                'email': 'cs1532@cse.unsw.edu.au',
                'name_first': 'Rei',
                'name_last': 'Ayanami',
                'handle_str': 'rayanami',
            },
        ]
    }

def test_admin_userpermission_change():
    clear()
    data['users'].append({
        'u_id': 1,
        'permission_id': 1,
        'global_owner': True,
        'email': 'cs1531@cse.unsw.edu.au',
        'name_first': 'Hayden',
        'name_last': 'Jacobs',
        'handle_str': 'hjacobs',
        'token': '1',
    })
    data['users'].append({
        'u_id': 2,
        'permission_id': 2,
        'email': 'cs1532@cse.unsw.edu.au',
        'name_first': 'Rei',
        'name_last': 'Ayanami',
        'handle_str': 'rayanami',
        'token': '2',
    })

    # invalid user id
    with pytest.raises(InputError):
        assert admin_userpermission_change('1', 3, 1)
    
    # not a global_owner
    with pytest.raises(AccessError):
        assert admin_userpermission_change('2', 1, 1)

    admin_userpermission_change('1', 2, 1)

    assert data['users'][1]['permission_id'] == 1

def test_search():
    clear()
    data['users'].append({
        'u_id': 1,
        'name_first': 'Hayden',
        'name_last': 'Jacobs',
        'token':'1',
    })
    data['users'].append({
        'u_id': 2,
        'name_first': 'Kusuo',
        'name_last': 'Saiki',
        'token': '2',
    })
    data['users'].append({
        'u_id': 3,
        'name_first': 'Kokomi',
        'name_last': 'Teruhashi',
        'token': '3',
    })

    data['channels'].append({
        'channel_id': 1,
        'is_public': False,
        'name' : 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            },
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            },
            {
                'u_id': 2,
                'name_first': 'Kusuo',
                'name_last': 'Saiki',
            },
        ],
        'messages':[
            {
                'message_id': 1,
                'u_id': 2,
                'message': 'Hello world',
                'time_created': 1582426789,
            },
        ],
    })
    data['channels'].append({
        'channel_id': 2,
        'is_public': True,
        'name' : 'channel2',
        'owner_members': [
            {
                'u_id': 2,
                'name_first': 'Kusuo',
                'name_last': 'Saiki',
            },
        ],
        'all_members': [
            {
                'u_id': 2,
                'name_first': 'Kusuo',
                'name_last': 'Saiki',
            },
            {
                'u_id': 3,
                'name_first': 'Kokomi',
                'name_last': 'Teruhashi',
            },
        ],
        'messages':[
            {
                'message_id': 1,
                'u_id': 2,
                'message': 'Hello',
                'time_created': 1582426789,
            },
        ],
    })
    
    assert search('1', 'Hello') == {
        'messages': []
    }

    assert search('2', 'Hello') == {
        'messages': [
            {
                'message_id': 1,
                'u_id': 2,
                'message': 'Hello world',
                'time_created': 1582426789,
            },
            {
                'message_id': 1,
                'u_id': 2,
                'message': 'Hello',
                'time_created': 1582426789,
            }
        ]   
    }