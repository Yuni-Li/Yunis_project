import message
from channel_data import data
from other import clear
from error import InputError, AccessError
import pytest

def test_message_send():
    # test send
    clear()
    data['users'].append({
        'u_id': 0,
        'name_first': 'SUPER',
        'name_last': 'USER',
        'token': '0',
        'permission_id': 1,
    })
    data['users'].append({
        'u_id': 1,
        'name_first': 'Hayden',
        'name_last': 'Jacobs',
        'token': '1',
        'permission_id': 2,
    })
    data['users'].append({
        'u_id': 2,
        'name_first': 'Kusuo',
        'name_last': 'Saiki',
        'token': '2',
        'permission_id': 2,
    })
    data['users'].append({
        'u_id': 3,
        'name_first': 'Kokomi',
        'name_last': 'Teruhashi',
        'token': '3',
        'permission_id': 2,
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
        ],
        'messages':[],
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
        'messages':[],
    })

    assert message.message_send('1', 1, 'Hellooooo') == {'message_id': 1}
    assert message.message_send('2', 2, 'AAAAAAAAA') == {'message_id': 2}
    assert message.message_send('3', 2, 'BBBBBBBBB') == {'message_id': 3}

    # more than 1000 characters
    with pytest.raises(InputError):
        assert message.message_send('1', 1, 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')

    # post message to the not joined channel
    with pytest.raises(AccessError):
        assert message.message_send('1', 2, 'Invalid')

def test_message_remove():
    message.message_remove('1', 1)
    # message no longer exist
    with pytest.raises(InputError):
        assert message.message_remove('1', 1)

    # Message with message_id was not sent by the authorised user making this request
    with pytest.raises(AccessError):
        assert message.message_remove('3', 2)

    message.message_remove('2', 3)
    message.message_remove('0', 2)

    assert data['channels'][1]['messages'] == []

def test_message_edit():
    message.message_send('1', 1, 'Hellooooo')
    message.message_send('2', 2, 'AAAAAAAAA')
    message.message_send('3', 2, 'BBBBBBBBB')

    message.message_edit('1', 4, 'H')
    assert data['channels'][0]['messages'][0]['message'] == 'H'

    message.message_edit('1', 4, '')
    assert data['channels'][0]['messages'] == []

    # Message with message_id was not sent by the authorised user making this request
    with pytest.raises(AccessError):
        assert message.message_edit('3', 5, 'AA')

    message.message_edit('2', 6, 'H')
    assert data['channels'][1]['messages'][1]['message'] == 'H'

    message.message_edit('0', 5, 'H')
    assert data['channels'][1]['messages'][0]['message'] == 'H'