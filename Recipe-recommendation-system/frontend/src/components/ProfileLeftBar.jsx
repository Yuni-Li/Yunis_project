import React from 'react';
import styled from 'styled-components';
import { useNavigate } from 'react-router-dom';
import PropTypes from 'prop-types';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

// MUI components
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import Avatar from '@mui/material/Avatar';
import ManageAccountsIcon from '@mui/icons-material/ManageAccounts';
import PasswordIcon from '@mui/icons-material/Password';
import DescriptionIcon from '@mui/icons-material/Description';
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import LogoutIcon from '@mui/icons-material/Logout';
import Divider from '@mui/material/Divider';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';

function ProfileLeftBar({ email }) {
  const navigate = useNavigate();
  const token = localStorage.getItem('token');
  const userId = localStorage.getItem('user_id');

  const handleLogout = async () => {
    const requestBody = {
      user_id: userId,
      token: token
    }
    const init = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestBody)
    }
    const output = await fetch('http://127.0.0.1:5000/auth/logout', init);
    output.json().then(res => {
      if (res.success) {
        localStorage.clear();
        navigate('/');
        toast('Thank you for using, Goodbye!', {
          icon: '🎉',
          position: toast.POSITION.TOP_CENTER,
          autoClose: 2000
        });
      } else {
        toast.error(res.error, {
          autoClose: 2000,
          position: toast.POSITION.TOP_CENTER
        })
      }
    });
  }

  return (
    <Wrapper>
      <List
        sx={{
          width: '90%',
          bgcolor: 'background.paper',
        }}
        component="nav"
        aria-label="mailbox folders"
      >
        <br />
        <ListItem button onClick={() => navigate(`/dashboard/${email}`)}>
          <ListItemAvatar>
            <Avatar>
              <ArrowBackIcon />
            </Avatar>
          </ListItemAvatar>
          <ListItemText primary="Back to Dashboard" />
        </ListItem>
        <Divider variant="fullWidth" component="li" />
        <br />
        <br />
        <br />
        <ListItem button onClick={() => navigate(`/profile/${email}`)}>
          <ListItemAvatar>
            <Avatar>
              <ManageAccountsIcon />
            </Avatar>
          </ListItemAvatar>
          <ListItemText primary="My Profile" />
        </ListItem>
        <Divider variant="inset" component="li" />
        <ListItem button onClick={() => navigate(`/profile/${email}/change-password`)}>
          <ListItemAvatar>
            <Avatar>
              <PasswordIcon />
            </Avatar>
          </ListItemAvatar>
          <ListItemText primary="Change Password" />
        </ListItem>
        <Divider variant="inset" component="li" />
        <ListItem button onClick={() => navigate(`/profile/${email}/own-recipes`)}>
          <ListItemAvatar>
            <Avatar>
              <DescriptionIcon />
            </Avatar>
          </ListItemAvatar>
          <ListItemText primary="Own Recipes" />
        </ListItem>
        <Divider variant="inset" component="li" />
        <ListItem button onClick={() => navigate(`/profile/${email}/favorites`)}>
          <ListItemAvatar>
            <Avatar>
              <FavoriteBorderIcon />
            </Avatar>
          </ListItemAvatar>
          <ListItemText primary="Favorites" />
        </ListItem>
        <Divider variant="inset" component="li" />
      </List>
      <List
        sx={{
          width: '90%',
          bgcolor: 'background.paper',
        }}
        component="nav"
        aria-label="mailbox folders"
      >
        <Divider variant="fullWidth" component="li" />
        <ListItem button onClick={handleLogout}>
          <ListItemAvatar>
            <Avatar>
              <LogoutIcon />
            </Avatar>
          </ListItemAvatar>
          <ListItemText primary="Logout" />
        </ListItem>
        <br />
        <br />
      </List>
    </Wrapper>
  );
}

ProfileLeftBar.propTypes = {
  email: PropTypes.any,
}

export default ProfileLeftBar;

const Wrapper = styled.div`
  display: flex;
	flex-direction: column;
  width: 20vw;
  height: 100%;
  box-shadow: rgba(0, 0, 0, 0.50) 1.95px 1.95px 2.6px;
  align-items: center;
	justify-content: space-between;
  border-radius: 0 0 15px 15px;
`;
