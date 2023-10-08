
In auth_login function, we should check whether the email is valid before checking whether it has been registered.

In auth_login function, we should check whether the password is valid before checking whether the password is correct.

In auth_login function, we should check whether the password is correct before we talk about the condition which the email does not belong to a user.

In auth_logout function, we should set the token to 0 after logout to make it invalid.

In auth_register function, we should check whether the email is valid before checking whether it has been registered.

In auth_register function, the length of valid password should longer than 6.

In auth_register function, fist name and last name shold between 1 and 50 characters and should not contains symbols and numbers.

In auth_register function, set token as a concatentation of a lowercase-only first name and last name. If the concatenation is longer than 20 characters, it is cutoff at 20 characters. If the handle is already taken, move all the characters to the left to make it unique for every user.

In auth_register function, if email, password, first name, last name and token are all valid, add the new user to 'data' dictionary.

In this part, it is assumed that token is the same as u_id.

In channel_invite and channel_join function, if the invited user is in the channel, then the user cannot be invited. (Considered as InputError) Also, global owner will be the owner of the channel once invited or joined.

In channel_details function, if the user is not a member in the group, then the detail must be invisible.

In channel_messages function, if the user is not a member in the group, then the messages should not be visible.

In channel_leave function, if the user is not a member in the group, then the function will not execute. Also, the owner of the channel cannot be removed. (Both situation will be considered as an AccessError)

In channel_addowner function, if the added user is the owner, then the function will not execute.

In channel_removeowner function, if the added user is not the owner, then the function will not execute.
