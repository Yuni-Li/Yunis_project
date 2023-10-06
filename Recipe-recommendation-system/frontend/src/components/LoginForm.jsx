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

function LoginForm() {
  const navigate = useNavigate();

  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');

  const submitHandler = async () => {
    if (email && password) {
      const requestBody = {
        email: email,
        password: password
      }
      const init = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      }
      const output = await fetch('http://127.0.0.1:5000/auth/login', init);
      // get token
      // console.log(output)
      output.json()
        .then(res => {
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
        });
    } else if (!email) {
      toast.error('Sorry! Email can not be empty!', {
        autoClose: 2000,
        position: toast.POSITION.TOP_CENTER
      });
    } else if (!password) {
      toast.error('Sorry! Password can not be empty!', {
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
      <Title id='loginTitle'>Login</Title>
      <InputCont>
        <TextField id="logInEmail" label="Email" variant="standard" color="info" onChange={e => setEmail(e.target.value)} />
        <TextField id="logInPassword" label="Password" type='password' variant="standard" color="info" onChange={e => setPassword(e.target.value)} />
      </InputCont>
      <Cont>
        <Submit>
          <LogInButton variant="contained" color='secondary' onClick={submitHandler} ><span style={{ color: '#fff', fontSize: '20px', fontWeight: 'bold' }}>Login</span></LogInButton>
        </Submit>
        <Link to='/register'>
          <Text>Don‘t have an account? Sign up</Text>
        </Link>
      </Cont>
    </Wrapper>
  );
}

export default LoginForm;

const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  background: rgba(255, 255, 255, 0.8);
  box-shadow: rgba(0, 0, 0, 0.50) 1.95px 1.95px 2.6px;
  margin: auto;
  width: 30vw;
  height: 55vh;
  min-width: 350px;
  min-height: 300px;
  border-radius: 5px;
`;

const Title = styled.h1`
  margin: auto;
  margin-top: 5rem;
  height: 30px;
`;

const InputCont = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem;
  width: 80%;
  margin: auto;
  margin-top: 4rem;
  flex-grow: 2;
`;

const Submit = styled.div`
  display: flex;
  margin: auto;
  margin-top: 2rem;
`;

const LogInButton = styled(Button)`
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
