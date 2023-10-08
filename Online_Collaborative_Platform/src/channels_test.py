import pytest
from channels import channels_list, channels_listall, channels_create
from channel_data import data
from error import InputError
from other import clear


def test_channels_create():
    # test user 0 create a channel
    clear()
    data['users'].append({
        'u_id': 0,
        'name_first': 'SUPER',
        'name_last': 'USER',
        'global_owner': True,
        'token': '0',
    })
    channels_create('0', 'create1', True)
    assert data['channels'][0]['channel_id'] == 0

    with pytest.raises(InputError):
        assert channels_create('0', 'longlonglonglonglonglonglonglong', True)


        
def test_channels_list():
    clear()
    data['users'].append({
        'u_id': 0,
        'name_first': 'SUPER',
        'name_last': 'USER',
        'global_owner': True,
        'token': '0',
    })
    data['users'].append({
        'u_id': 1,
        'name_first': 'Hayden',
        'name_last': 'Jacobs',
        'token': '1',
    })
    data['channels'].append({
        'channel_id': 1,
        'is_public': False,
        'name' : 'channel1',
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
        ],
    })
    data['channels'].append({
        'channel_id': 2,
        'is_public': True,
        'name' : 'channel2',
        'owner_members': [
            {
                'u_id': 0,
                'name_first': 'SUPER',
                'name_last': 'USER',
            },
        ],
        'all_members': [
            {
                'u_id': 0,
                'name_first': 'SUPER',
                'name_last': 'USER',
            },
        ],
    })
    data['channels'].append({
        'channel_id': 3,
        'is_public': True,
        'name' : 'channel3',
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
        ],
    })
    assert channels_list('1') == {
        'channels': [ 
            {
                'channel_id': 1,
                'name': 'channel1'
            },
            {
                'channel_id': 3,
                'name': 'channel3'     
            },
        ]
    }

def test_channels_listall():
    assert channels_listall('0') == {
        'channels': [ 
            {
                'channel_id': 1,
                'name': 'channel1'
            },
            {
                'channel_id': 2,
                'name': 'channel2'     
            },
            {
                'channel_id': 3,
                'name': 'channel3'
            }
        ]
    }
