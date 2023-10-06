import React from 'react';
import styled from 'styled-components';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { useNavigate } from 'react-router-dom';

// own components
import ProfileLeftBar from '../components/ProfileLeftBar';
import backgroundImage from '../image/2.jpg';

// MUI components
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import TextField from '@mui/material/TextField';
import InputAdornment from '@mui/material/InputAdornment';
import EditIcon from '@mui/icons-material/Edit';
import SaveAsIcon from '@mui/icons-material/SaveAs';

toast.configure();

function ProfilePage() {
  const navigate = useNavigate();
  const token = localStorage.getItem('token');
  const email = localStorage.getItem('email');
  const userId = localStorage.getItem('user_id');

  const [newEmail, setNewEmail] = React.useState('');
  const [newUsername, setNewUsername] = React.useState('');
  const [allowEmailChange, setAllowEmailChange] = React.useState(false);
  const [allowUsernameChange, setAllowUsernameChange] = React.useState(false);
  const [numberOfFollowers, setNumberOfFollowers] = React.useState(0);
  const [numberOfFollowings, setNumberOfFollowings] = React.useState(0);
  const [imageFile, setImageFile] = React.useState('');

  const getUserInfoById = () => {
    const init = {
      mathod: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    }
    fetch(`http://127.0.0.1:5000/user/profile?user_id=${userId}`, init)
      .then(res => res.json())
      .then(data => {
        if (data.profile) {
          // console.log(data);
          setImageFile(data.profile.icon);
          setNumberOfFollowers(data.profile.followers.length);
          setNumberOfFollowings(data.profile.followings.length)
        } else {
          toast.error(data.error, {
            autoClose: 2000,
            position: toast.POSITION.TOP_CENTER
          })
        }
      })
  }

  React.useEffect(() => {
    getUserInfoById();
  }, [])

  const handleChangeEmail = async () => {
    if (newEmail && newEmail !== email) {
      const requestBody = {
        user_id: userId,
        token: token,
        old_email: email,
        new_email: newEmail
      }
      const init = {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      }
      const output = await fetch('http://127.0.0.1:5000/user/change/email', init);
      output.json().then(res => {
        if (res.success) {
          setAllowEmailChange(false);
          localStorage.setItem('email', newEmail);
          navigate(`/profile/${newEmail}`);
          toast('Email has changed successfully!', {
            icon: '🎉',
            position: toast.POSITION.TOP_CENTER,
            autoClose: 2000
          });
        } else {
          setAllowEmailChange(false);
          toast.error(res.error, {
            autoClose: 2000,
            position: toast.POSITION.TOP_CENTER
          })
        }
      });
    } else if (newEmail === email) {
      setAllowEmailChange(false);
      toast.error('Sorry! New email is same as original email!', {
        autoClose: 2000,
        position: toast.POSITION.TOP_CENTER
      });
    } else if (!newEmail) {
      setAllowEmailChange(false);
      toast.error('Sorry! New email can not be empty!', {
        autoClose: 2000,
        position: toast.POSITION.TOP_CENTER
      });
    }
  }

  const handleChangeUsername = async () => {
    if (newUsername) {
      const requestBody = {
        user_id: userId,
        token: token,
        new_name: newUsername
      }
      const init = {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      }
      const output = await fetch('http://127.0.0.1:5000/user/change/username', init);
      output.json().then(res => {
        if (res.success) {
          setAllowUsernameChange(false);
          toast('Username has changed successfully!', {
            icon: '🎉',
            position: toast.POSITION.TOP_CENTER,
            autoClose: 2000
          });
        } else {
          setAllowUsernameChange(false);
          toast.error(res.error, {
            autoClose: 2000,
            position: toast.POSITION.TOP_CENTER
          })
        }
      });
    } else if (!newUsername) {
      setAllowEmailChange(false);
      toast.error('Sorry! New username can not be empty!', {
        autoClose: 2000,
        position: toast.POSITION.TOP_CENTER
      });
    }
  }

  return (
    <Wrapper>
      <BarContainer>
        <ProfileLeftBar email={email} />
      </BarContainer>
      <DetailContainer>
        <InfoPart>
          <Container>
            <Blank />
            <Info>
              <FollowersInfo>{numberOfFollowers} Followers</FollowersInfo>
              <ProfileImage>
              {imageFile
                ? (<Image src={imageFile} />)
                : (<AccountCircleIcon sx={{ width: '100%', height: '100%' }} />)
              }
              </ProfileImage>
              <FollowingInfo>{numberOfFollowings} Following</FollowingInfo>
            </Info>
          </Container>
        </InfoPart>
        <EditPart>
          {allowEmailChange
            ? (<TextField
              id="Email"
              label="New Email"
              sx={{ width: '35%' }}
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <SaveAsIcon
                      aria-label="toggle email change allowed"
                      onClick={handleChangeEmail}
                      edges="end" />
                  </InputAdornment>
                ),
              }} variant="standard" onChange={e => setNewEmail(e.target.value)} />)
            : (<TextField
              id="Email"
              label="New Email"
              sx={{ width: '35%' }}
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <EditIcon
                      aria-label="toggle email change allowed"
                      onClick={() => setAllowEmailChange(true)}
                      edges="end" />
                  </InputAdornment>
                ),
                readOnly: true,
              }} variant="standard" value='' />)
          }
          {allowUsernameChange
            ? (<TextField
              id="Username"
              label="New Username"
              sx={{ width: '35%' }}
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <SaveAsIcon
                      aria-label="toggle username change allowed"
                      onClick={handleChangeUsername}
                      edges="end" />
                  </InputAdornment>
                ),
              }} variant="standard" onChange={e => setNewUsername(e.target.value)} />)
            : (<TextField
              id="Username"
              label="New Username"
              sx={{ width: '35%' }}
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <EditIcon
                      aria-label="toggle username change allowed"
                      onClick={() => setAllowUsernameChange(true)}
                      edges="end" />
                  </InputAdornment>
                ),
                readOnly: true,
              }} variant="standard" value='' />)
          }
        </EditPart>
      </DetailContainer>
    </Wrapper>
  )
}

export default ProfilePage;

const Wrapper = styled.div`
  background-size: 100% 100%;
  height: 100vh;
`;

const BarContainer = styled.div`
  position: fixed;
	left: 0;
	height: 100%;
	width: 20vw;
`;

const DetailContainer = styled.div`
  position: fixed;
	right: 0;
	height: 100%;
	width: calc(100% - 20vw);
	border-radius: 20px 20px 0 0;
`;

const InfoPart = styled.div`
  background-image: url(${backgroundImage});
	background-size: 100% 100%;
	height: 60vh;
	border-radius: 20px 20px 0 0;
`;

const EditPart = styled.div`
  display: flex;
	flex-direction: column;
	align-items: center;
	gap: 2rem;
	height: calc(100% - 60vh);
	border-radius: 0 0 20px 20px;
	justify-content: center;
`;

const Container = styled.div`
  align-items: center;
  margin: auto;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.5);
`;

const Blank = styled.div`
  height: 200px;
`;

const Info = styled.div`
  display: flex;
	flex-direction: row;
	justify-content: center;
	width: 100%;
	gap: 80px;
`;

const ProfileImage = styled.div`
  width: 250px;
  height: 250px;
  background: #FFFFFF;
  box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.50);
	border-radius: 50%;
	display: flex;
`;

const FollowersInfo = styled.div`
  font-size: 40px;
	margin-top: 160px;
	width: 200px;
	text-align: center;
`;

const FollowingInfo = styled.div`
  font-size: 40px;
	margin-top: 160px;
	width: 200px;
	text-align: center;
`;

const Image = styled.img`
  width: 100%;
  height: 100%;
`;
