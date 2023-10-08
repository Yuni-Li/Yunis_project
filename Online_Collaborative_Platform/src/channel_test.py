import channel
import pytest
from error import InputError
from error import AccessError
from other import clear
from channel_data import data

def test_channel_invite():
    data['users'].append({
        'u_id': 0,
        'name_first': 'SUPER',
        'name_last': 'USER',
        'permission_id': 1,
        'token': '0',
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
        'messages':[
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
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
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    })

    # invalid channel
    with pytest.raises(InputError):
        assert channel.channel_invite("1", 3, 3)

    # invalid_user
    with pytest.raises(InputError):
        assert channel.channel_invite("1", 1, 4)

    # not_member
    with pytest.raises(AccessError):
        assert channel.channel_invite("4", 1, 3)

    # already_member
    with pytest.raises(InputError):
        assert channel.channel_invite("1", 1, 1)

def test_channel_details():
    clear()
    data['users'].append({
        'u_id': 0,
        'name_first': 'SUPER',
        'name_last': 'USER',
        'permission_id': 1,
        'token': '0',
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
        'messages':[
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
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
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    })
    channel.channel_invite("1", 1, 2)
    assert channel.channel_details("1", 1) == {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
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
    }
    
    # invalid_ch
    with pytest.raises(InputError):
        assert channel.channel_details("1", 3)

    # not_member
    with pytest.raises(AccessError):
        assert channel.channel_details("4", 1)

    # not channel member
    with pytest.raises(InputError):                       # Both InputError & AccessError
        assert channel.channel_details("4", 3)            # Consider it as InputError

def test_channel_messages():
    clear()
    data['users'].append({
        'u_id': 0,
        'name_first': 'SUPER',
        'name_last': 'USER',
        'permission_id': 1,
        'token': '0',
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
        'messages':[
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
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
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    })
    assert channel.channel_messages("3", 2, 0) == {
        'messages': [
            {
                'message_id': 1,
                'u_id': 2,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': -1,
    }

    # invalid channel
    with pytest.raises(InputError):
        assert channel.channel_messages("1", 3, 0)
    
    # invalid start
    with pytest.raises(InputError):
        assert channel.channel_messages("1", 1, 49)
    
    # invalid user
    with pytest.raises(AccessError):
        assert channel.channel_messages("3", 1, 0)

    for i in range(2, 52):
        dic = {
            'message_id': i,
            'u_id': 2,
            'message': 'TEST TEXT',
            'time_created': 1582426789 + i
        }

        data['channels'][1]['messages'].append(dic)

    assert channel.channel_messages('3', 2, 0) == {
        'messages': [
            {'message_id': 50, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426839}, {'message_id': 49, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426838}, {'message_id': 48, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426837}, {'message_id': 47, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426836}, {'message_id': 46, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426835}, {'message_id': 45, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426834}, {'message_id': 44, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426833}, {'message_id': 43, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426832}, {'message_id': 42, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426831}, {'message_id': 41, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426830}, {'message_id': 40, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426829}, {'message_id': 39, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426828}, {'message_id': 38, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426827}, {'message_id': 37, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426826}, {'message_id': 36, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426825}, {'message_id': 35, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426824}, {'message_id': 34, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426823}, {'message_id': 33, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426822}, {'message_id': 32, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426821}, {'message_id': 31, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426820}, {'message_id': 30, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426819}, {'message_id': 29, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426818}, {'message_id': 28, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426817}, {'message_id': 27, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426816}, {'message_id': 26, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426815}, {'message_id': 25, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426814}, {'message_id': 24, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426813}, {'message_id': 23, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426812}, {'message_id': 22, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426811}, {'message_id': 21, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426810}, {'message_id': 20, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426809}, {'message_id': 19, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426808}, {'message_id': 18, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426807}, {'message_id': 17, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426806}, {'message_id': 16, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426805}, {'message_id': 15, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426804}, {'message_id': 14, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426803}, {'message_id': 13, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426802}, {'message_id': 12, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426801}, {'message_id': 11, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426800}, {'message_id': 10, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426799}, {'message_id': 9, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426798}, {'message_id': 8, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426797}, {'message_id': 7, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426796}, {'message_id': 6, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426795}, {'message_id': 5, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426794}, {'message_id': 4, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426793}, {'message_id': 3, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426792}, {'message_id': 2, 'u_id': 2, 'message': 'TEST TEXT', 'time_created': 1582426791}, {'message_id': 1, 'u_id': 2, 'message': 'Hello world', 'time_created': 1582426789}
        ],
        'start': 0,
        'end': 50,
    }


def test_channel_leave():
    clear()
    data['users'].append({
        'u_id': 0,
        'name_first': 'SUPER',
        'name_last': 'USER',
        'permission_id': 1,
        'token': '0',
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
        'messages':[
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
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
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    })
    channel.channel_invite("1", 1, 2)
    channel.channel_leave("2",1)
    assert channel.channel_details("1", 1) == {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            },
        ],
    }
    
    # invalid channel
    with pytest.raises(InputError):
        assert channel.channel_leave("1", 3)
    
    # invalid user
    with pytest.raises(AccessError):
        assert channel.channel_leave("2", 1)
    
    # remove an owner
    with pytest.raises(AccessError):
        assert channel.channel_leave("1", 1)


def test_channel_join():
    clear()
    data['users'].append({
        'u_id': 0,
        'name_first': 'SUPER',
        'name_last': 'USER',
        'permission_id': 1,
        'token': '0',
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
        'messages':[
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
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
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    })
    channel.channel_join("1", 2)
    assert channel.channel_details("1", 2) == {
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
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            },
        ],
    }

    channel.channel_join("0", 1)
    assert channel.channel_details("0", 1) == {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            },
            {
                'u_id': 0,
                'name_first': 'SUPER',
                'name_last': 'USER',
            },
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            },
            {
                'u_id': 0,
                'name_first': 'SUPER',
                'name_last': 'USER',
            },
        ],
    }

    # invalid channel
    with pytest.raises(InputError):
        assert channel.channel_join("1", 3)

    # private channel
    with pytest.raises(AccessError):
        assert channel.channel_join("3", 1)

    # already member
    with pytest.raises(InputError):
        assert channel.channel_join('2', 2)

def test_channel_addowner():
    clear()
    data['users'].append({
        'u_id': 0,
        'name_first': 'SUPER',
        'name_last': 'USER',
        'permission_id': 1,
        'token': '0',
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
        'messages':[
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
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
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    })
    # invalid channel
    with pytest.raises(InputError):
        assert channel.channel_addowner("1", 3, 2)

    channel.channel_addowner("1", 1, 0)

    # user is already an owner in the channel
    with pytest.raises(InputError):
        assert channel.channel_addowner("1", 1, 0)
    
    # invalid auth
    with pytest.raises(AccessError):
        assert channel.channel_addowner("3", 2, 1)

    channel.channel_addowner("0", 2, 1)
    assert channel.channel_details("1", 2) == {
        'name' : 'channel2',
        'owner_members': [
            {
                'u_id': 2,
                'name_first': 'Kusuo',
                'name_last': 'Saiki',
            },
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
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
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            },
        ],
    }
    

def test_channel_removeowner():
    clear()
    data['users'].append({
        'u_id': 0,
        'name_first': 'SUPER',
        'name_last': 'USER',
        'permission_id': 1,
        'token': '0',
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
        'messages':[
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
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
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    })
    channel.channel_addowner("2", 2, 3)
    channel.channel_removeowner("0", 2, 3)
    assert channel.channel_details("3", 2) == {
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
    }

    # invalid channel
    with pytest.raises(InputError):
        assert channel.channel_removeowner("1", 3, 2)
    
    # invalid user
    with pytest.raises(InputError):
        assert channel.channel_removeowner("2", 2, 3)

    # invalid user
    with pytest.raises(AccessError):
        assert channel.channel_removeowner("3", 2, 2)
