import React from 'react';
import styled from 'styled-components';
import { Link, useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

// MUI components
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Fab from '@mui/material/Fab';
import HomeOutlinedIcon from '@mui/icons-material/HomeOutlined';

toast.configure();

function RegisterForm() {
  const navigate = useNavigate();

  const [email, setEmail] = React.useState('');
  const [username, setUsername] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [confirmedPassword, setConfirmedPassword] = React.useState('');

  const clickHandler = async () => {
    password !== confirmedPassword && (
      toast.error('Sorry! Two Passwords are different! Please check again', {
        autoClose: 2000,
        position: toast.POSITION.TOP_CENTER
      }))
    if (email && username && password && confirmedPassword && password === confirmedPassword) {
      const requestBody = {
        email: email,
        password: password,
        confirmed_password: confirmedPassword,
        username: username
      }
      const init = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      }

      const output = await fetch('http://127.0.0.1:5000/auth/register', init);
      output.json().then(res => {
        if (res.token) {
          localStorage.setItem('token', res.token);
          localStorage.setItem('user_id', res.user_id);
          localStorage.setItem('email', email);
          navigate(`/dashboard/${email}`);
          toast('Welcome!', {
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
      })
    } else if (!email) {
      toast.error('Sorry! Email can not be empty!', {
        autoClose: 2000,
        position: toast.POSITION.TOP_CENTER
      });
    } else if (!username) {
      toast.error('Sorry! Username can not be empty!', {
        autoClose: 2000,
        position: toast.POSITION.TOP_CENTER
      });
    } else if (!password) {
      toast.error('Sorry! Password can not be empty!', {
        autoClose: 2000,
        position: toast.POSITION.TOP_CENTER
      });
    } else if (!confirmedPassword) {
      toast.error('Sorry! Confirm Password can not be empty!', {
        autoClose: 2000,
        position: toast.POSITION.TOP_CENTER
      });
    }
  }

  return (
    <Wrapper>
      <Fab
        color="default"
        aria-label="add"
        sx={{ position: 'fixed', top: '2rem', left: '2rem' }}
        onClick={() => navigate('/dashboard/explorer')}>
        <HomeOutlinedIcon />
      </Fab>
      <Title id='registerTitle'>Sign up</Title>
      <InputCont>
        <TextField id="registerEmail" label="Email" variant="standard" color="info" onChange={e => setEmail(e.target.value)} />
        <TextField id="registerUsername" label="Username" variant="standard" onChange={e => setUsername(e.target.value)} />
        <TextField id="registerPassword" label="Password" type='password' variant="standard" color="info" onChange={e => setPassword(e.target.value)} />
        <TextField id="registerPasswordConfirmed" label="Password Confirmed" type='password' variant="standard" onChange={e => setConfirmedPassword(e.target.value)} />
      </InputCont>
      <Cont>
        <Submit>
          <RegisterButton variant="contained" color='secondary' onClick={clickHandler} ><span style={{ color: '#fff', fontSize: '20px', fontWeight: 'bold' }}>Sign up</span></RegisterButton>
        </Submit>
        <Link to='/login'>
          <Text>Already have an account? Login</Text>
        </Link>
      </Cont>
    </Wrapper>
  );
}

export default RegisterForm;

const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  background: rgba(255, 255, 255, 0.8);
  box-shadow: rgba(0, 0, 0, 0.50) 1.95px 1.95px 2.6px;
  margin: auto;
  width: 30vw;
  height: 65vh;
  min-width: 350px;
  min-height: 300px;
  border-radius: 5px;
`;

const Title = styled.h1`
  margin: auto;
  margin-top: 4rem;
  height: 30px;
`;

const InputCont = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem;
  width: 80%;
  margin: auto;
  margin-top: 2rem;
  flex-grow: 2;
`;

const Submit = styled.div`
  display: flex;
  margin: auto;
  margin-top: 2rem;
`;

const RegisterButton = styled(Button)`
  width: 250px;
`;

const Cont = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: center;
`;

const Text = styled.p`
  color: #46BA51;
  text-decoration: underline;
  margin: auto;
  margin-bottom: 3rem;
`;
