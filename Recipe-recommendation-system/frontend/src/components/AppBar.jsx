import * as React from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import styled from 'styled-components'
import { Codechef } from '@styled-icons/simple-icons/Codechef'

// MUI components
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import AccountCircle from '@mui/icons-material/AccountCircle';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import Tooltip from '@mui/material/Tooltip';
import Divider from '@mui/material/Divider';

toast.configure();

export default function ButtonAppBar() {
  const navigate = useNavigate();
  const token = localStorage.getItem('token');
  const email = localStorage.getItem('email');
  const userId = localStorage.getItem('user_id');

  const [anchorElUser, setAnchorElUser] = React.useState(null);
  const handleOpenUserMenu = (event) => {
    setAnchorElUser(event.currentTarget);
  };
  const handleCloseUserMenu = () => {
    setAnchorElUser(null);
  };

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
        setAnchorElUser(null);
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
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="fixed" style={{ background: 'rgba(255, 255, 255, 0.6)' }}>
        <Toolbar>
          <Typography variant="h5" component="div" sx={{ flexGrow: 1 }} style={{ textTransform: 'uppercase', color: '#E16666', fontWeight: 'bold' }}>
            <RedCodechef size="50" /> Master.Chef
          </Typography>
          {token
            ? (<React.Fragment>
              <Box sx={{ flexGrow: 0 }}>
                <Tooltip title="Open settings">
                  <IconButton onClick={handleOpenUserMenu} sx={{ p: 0 }}>
                    <AccountCircle sx={{ color: 'black', fontSize: 50 }} />
                  </IconButton>
                </Tooltip>
                <Menu
                  sx={{ mt: '40px' }}
                  id="menu-appbar"
                  anchorEl={anchorElUser}
                  anchorOrigin={{
                    vertical: 'top',
                    horizontal: 'right',
                  }}
                  keepMounted
                  transformOrigin={{
                    vertical: 'top',
                    horizontal: 'right',
                  }}
                  open={Boolean(anchorElUser)}
                  onClose={handleCloseUserMenu}
                >
                  <MenuItem onClick={() => navigate(`/profile/${email}`)}>View Profile</MenuItem>
                  <MenuItem onClick={() => navigate(`/${email}/recipe/create`)}>Create Recipes</MenuItem>
                  <MenuItem onClick={() => navigate(`/profile/${email}/favorites`)}>Favorites</MenuItem>
                  <MenuItem onClick={() => window.open('/analysis')}>Analysis</MenuItem>
                  <Divider variant="fullWidth" component="li" />
                  <MenuItem onClick={handleLogout}>Logout</MenuItem>
                </Menu>
              </Box>
            </React.Fragment>)
            : (<React.Fragment>
              <Button onClick={() => navigate('/login')} style={{ fontSize: '16px', fontWeight: 'bold', color: '#557AFF' }}>Login</Button>
              <Typography variant="h6" component="div" color={{ color: 'grey' }}>
                |
              </Typography>
              <Button onClick={() => navigate('/register')} style={{ fontSize: '16px', fontWeight: 'bold', color: '#557AFF' }}>Sign up</Button>
            </React.Fragment>)}

        </Toolbar>
      </AppBar>
    </Box>
  );
}

const RedCodechef = styled(Codechef)`
  color: rgab(255, 255, 255, 1);
`
