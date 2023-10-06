import React from 'react';
import styled from 'styled-components';
import { useNavigate } from 'react-router-dom';

// outside css
import 'animate.css';

// MUI components
import Button from '@mui/material/Button';

// own components
import backgroundImage from '../image/1.png';

function HomePage() {
  const navigate = useNavigate();
  const token = localStorage.getItem('token');
  const email = localStorage.getItem('email');
  return (
    <Wrapper>
      <Container>
        <Title>Welcome</Title>
        <Label>Welcome to the recipe system...</Label>
        <ButtonField>
          {token
            ? (<ContributorButton variant="contained" color='secondary' onClick={() => navigate(`/dashboard/${email}`)}><span style={{ color: '#fff', fontSize: '25px', fontWeight: 'bold', textTransform: 'capitalize' }}>Contributor</span></ContributorButton>)
            : (<ContributorButton variant="contained" color='secondary' onClick={() => navigate('/login')}><span style={{ color: '#fff', fontSize: '25px', fontWeight: 'bold', textTransform: 'capitalize' }}>Contributor</span></ContributorButton>)
          }
          {token
            ? (<ExplorerButton variant="contained" color='last' onClick={() => navigate(`/dashboard/${email}`)}><span style={{ color: '#fff', fontSize: '25px', fontWeight: 'bold', textTransform: 'capitalize' }}>Explorer</span></ExplorerButton>)
            : (<ExplorerButton variant="contained" color='last' onClick={() => navigate('/dashboard/explorer')}><span style={{ color: '#fff', fontSize: '25px', fontWeight: 'bold', textTransform: 'capitalize' }}>Explorer</span></ExplorerButton>)
          }
        </ButtonField>
      </Container>
    </Wrapper>
  );
}

export default HomePage;

const Wrapper = styled.div`
  background-image: url(${backgroundImage});
  background-size: 100% 100%;
  height: 100vh;
`;

const Container = styled.div`
  align-items: center;
  margin: auto;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.4);
`;

const Title = styled.h1`
  font-size: 150px;
  color: #FFF;
	margin: auto;
	text-align: center;
	padding: 10rem;
	animation: heartBeat 3s infinite;
`;

const Label = styled.h2`
  font-size: 20px;
  color: #BCFFFB;
	margin: auto;
	margin-top: 9rem;
	margin-bottom: 5px;
	width: 300px;
	animation: headShake 1s 2 forwards;
`;

const ButtonField = styled.div`
	display: flex;
	flex-direction: column;
	gap: 0.5rem;
  align-items: center;
  margin: auto;
  width: 100%;
`;

const ContributorButton = styled(Button)`
  width: 250px;
	height: 50px;
`;

const ExplorerButton = styled(Button)`
  width: 250px;
	height: 50px;
`;
