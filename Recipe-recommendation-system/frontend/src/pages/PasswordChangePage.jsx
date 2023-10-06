import React from 'react';
import styled from 'styled-components';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

// own components
import ProfileLeftBar from '../components/ProfileLeftBar';
import backgroundImage from '../image/2.jpg';

// MUI components
import LockOpenIcon from '@mui/icons-material/LockOpen';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

toast.configure();

function PasswordChangePage() {
  const [originalPassword, setOriginalPassword] = React.useState('');
  const [newPassword, setNewPassword] = React.useState('');
  const [confirmedNewPassword, setConfirmedNewPassword] = React.useState('');

  const token = localStorage.getItem('token');
  const email = localStorage.getItem('email');
  const userId = localStorage.getItem('user_id');

  const handleChangePassword = async () => {
    if (originalPassword && newPassword && confirmedNewPassword && newPassword === confirmedNewPassword && newPassword !== originalPassword) {
      const requestBody = {
        user_id: userId,
        token: token,
        old_password: originalPassword,
        new_password: newPassword
      }
      const init = {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      }

      const output = await fetch('http://127.0.0.1:5000/user/change/password', init);
      output.json().then(res => {
        if (res.success) {
          setOriginalPassword('');
          setNewPassword('');
          setConfirmedNewPassword('');
          toast('Password has changed successfully!', {
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
    } else if (!originalPassword) {
      toast.error('Sorry! Original Password can not be empty!', {
        autoClose: 2000,
        position: toast.POSITION.TOP_CENTER
      });
    } else if (!newPassword) {
      toast.error('Sorry! New Password can not be empty!', {
        autoClose: 2000,
        position: toast.POSITION.TOP_CENTER
      });
    } else if (!confirmedNewPassword) {
      toast.error('Sorry! Please input and confirm your new password correctly!', {
        autoClose: 2000,
        position: toast.POSITION.TOP_CENTER
      });
    } else if (originalPassword && newPassword && confirmedNewPassword && newPassword !== confirmedNewPassword) {
      toast.error('Sorry! Please confirm your new password again!', {
        autoClose: 2000,
        position: toast.POSITION.TOP_CENTER
      });
    } else if (newPassword && originalPassword && confirmedNewPassword && newPassword === originalPassword) {
      toast.error('Sorry! Your new password is same as your orignial password!', {
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
              <ProfileImage>
                <LockOpenIcon sx={{ width: '100%', height: '100%' }} />
              </ProfileImage>
            </Info>
          </Container>
        </InfoPart>
        <EditPart>
          <TextField id="originalPassword" label="Original Password" type='password' variant="standard" color="info" sx={{ width: '35%' }} value={originalPassword} onChange={e => setOriginalPassword(e.target.value)} />
          <TextField id="newPassword" label="New Password" type='password' variant="standard" color="info" sx={{ width: '35%' }} value={newPassword} onChange={e => setNewPassword(e.target.value)} />
          <TextField id="ConfirmedNewPassword" label="New Password Confirmed" type='password' variant="standard" color="info" sx={{ width: '35%' }} value={confirmedNewPassword} onChange={e => setConfirmedNewPassword(e.target.value)} />
          <SaveButton variant="contained" sx={{ marginTop: '2rem' }} color='secondary' onClick={handleChangePassword}><span style={{ color: '#fff', fontSize: '20px', fontWeight: 'bold' }}>Save</span></SaveButton>
        </EditPart>
      </DetailContainer>
    </Wrapper>
  )
}

export default PasswordChangePage;

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
	height: 50vh;
	border-radius: 20px 20px 0 0;
`;

const EditPart = styled.div`
  display: flex;
	flex-direction: column;
	align-items: center;
	gap: 1.5rem;
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
  height: 150px;
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

const SaveButton = styled(Button)`
  width: 250px;
`;
