import React from 'react';
import styled from 'styled-components';
import PropTypes from 'prop-types';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

// MUI components
import AccountBoxIcon from '@mui/icons-material/AccountBox';
import StarBorderIcon from '@mui/icons-material/StarBorder';
import StarIcon from '@mui/icons-material/Star';
import Button from '@mui/material/Button';

// own components
import ShowIngredientsByCreator from './ShowIngredientsByCreator';

toast.configure();

function PersonalDetailForm({ userID }) {
  const [imageFile, setImageFile] = React.useState('');
  const [userEmail, setUserEmail] = React.useState('');
  const [username, setUsername] = React.useState('');
  const [numberOfFollowers, setNumberOfFollowers] = React.useState(0);
  const [isStar, setIsStar] = React.useState(false);

  const myUserID = localStorage.getItem('user_id');
  const myToken = localStorage.getItem('token');
  const getUserInfoById = () => {
    const init = {
      mathod: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    }
    fetch(`http://127.0.0.1:5000/user/profile?user_id=${userID}`, init)
      .then(res => res.json())
      .then(data => {
        if (data.profile) {
          // console.log(data);
          setImageFile(data.profile.icon);
          setUserEmail(data.profile.email);
          setUsername(data.profile.username);
          setNumberOfFollowers(data.profile.followers.length);
          if (data.profile.followers.includes(myUserID)) {
            setIsStar(true);
          } else {
            setIsStar(false);
          }
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
  }, [isStar])

  const handleFllow = async () => {
    if (myUserID !== userID) {
      const requestBody = {
        curr_user_id: myUserID,
        token: myToken,
        target_user_id: userID,
      }
      const init = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      }
      const output = await fetch('http://127.0.0.1:5000/user/follow', init);
      // console.log(output);
      output.json()
        .then(res => {
          if (res.success) {
            setIsStar(true);
          } else {
            toast.error(res.error, {
              autoClose: 2000,
              position: toast.POSITION.TOP_CENTER
            })
          }
        })
    } else if (!myToken) {
      toast.error('Please Login!!!', {
        autoClose: 2000,
        position: toast.POSITION.TOP_CENTER
      })
    } else {
      toast.error('Sorry! Your cannot follow yourself!', {
        autoClose: 2000,
        position: toast.POSITION.TOP_CENTER
      });
    }
  }

  const handleUnfllow = async () => {
    if (myUserID !== userID) {
      const requestBody = {
        curr_user_id: myUserID,
        token: myToken,
        target_user_id: userID
      }
      const init = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      }
      const output = await fetch('http://127.0.0.1:5000/user/unfollow', init);
      // console.log(output);
      output.json()
        .then(res => {
          // console.log(res);
          if (res.success) {
            setIsStar(false);
          } else {
            toast.error(res.error, {
              autoClose: 2000,
              position: toast.POSITION.TOP_CENTER
            })
          }
        })
    } else if (!myToken) {
      toast.error('Please Login!!!', {
        autoClose: 2000,
        position: toast.POSITION.TOP_CENTER
      })
    } else {
      toast.error('Sorry! Your cannot follow yourself!', {
        autoClose: 2000,
        position: toast.POSITION.TOP_CENTER
      });
    }
  }

  //   const navigate = useNavigate();
  return (
    <Wrapper>
      <UserInfo>
        <UserIcon>
          {imageFile
            ? (<Image src={imageFile} />)
            : (<AccountBoxIcon sx={{ width: '100%', height: '100%', borderRadius: '10px' }} />)
          }
        </UserIcon>
        <UserDetail>
          <Email><Detail>Email: {userEmail}</Detail></Email>
          <Username><Detail>Username: {username}</Detail></Username>
          <NumberOfFollowers><Detail>Amount of Followers: {numberOfFollowers}</Detail></NumberOfFollowers>
        </UserDetail>
        <InteractionField>
          <ButtonField>
            <br />
            {isStar
              ? (<React.Fragment>
                <FollowButton variant="contained" sx={{ backgroundColor: 'white' }} onClick={handleUnfllow}>
                  <StarIcon sx={{ width: '100%', height: '100%', borderRadius: '10px', color: '#F6DF07' }} />
                </FollowButton>
              </React.Fragment>)
              : (<React.Fragment>
                <FollowButton variant="contained" sx={{ backgroundColor: 'white' }} onClick={handleFllow}>
                  <StarBorderIcon sx={{ width: '100%', height: '100%', borderRadius: '10px', color: '#F6DF07' }} />
                </FollowButton>
              </React.Fragment>)
            }
          </ButtonField>
        </InteractionField>
      </UserInfo>
      <RecipeInfo>
        <h2 style={{ marginLeft: '2%', color: 'green' }}>Recipes Owned:</h2>
        <ShowIngredientsByCreator userId={userID} />
      </RecipeInfo>
    </Wrapper>
  );
}

export default PersonalDetailForm;

PersonalDetailForm.propTypes = {
  userID: PropTypes.any,
}

const Wrapper = styled.div`
  position: fixed;
  top: 5vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.8);
  box-shadow: rgba(0, 0, 0, 0.50) 1.95px 1.95px 2.6px;
  margin: auto;
  width: 70vw;
  height: 90vh;
  border-radius: 10px;
  overflow: auto;
`;

const UserInfo = styled.div`
  width: 80%;
  height: 35%;
  display: flex;
  gap: 0.1rem;
  flex-direction: row;
  border-radius: 10px;
`;

const RecipeInfo = styled.div`
  width: 90%;
  height: 60%;
  background: rgba(255, 255, 255, 1);
  border-radius: 10px;
  overflow: 'auto';
`;

const UserIcon = styled.div`
  width: 30%;
  height: 100%;
  border-radius: 10px;
  background-color: #ffffff;
`;

const UserDetail = styled.div`
  width: 64%;
  height: 100%;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-around;
`;

const InteractionField = styled.div`
  width: 5%;
  height: 100%;
  border-radius: 10px;
`;

const Email = styled.div`
  width: 95%;
  border-radius: 10px;
  align-items: center;
  justify-content: flex-start;
`;

const Username = styled.div`
  width: 95%;
  border-radius: 10px;
`;

const NumberOfFollowers = styled.div`
  width: 95%;
  border-radius: 10px;
`;

const Detail = styled.h1`
  margin-left: 10px;
`;

const Image = styled.img`
  width: 100%;
  height: 100%;
  border-radius: 10px;
`;

const ButtonField = styled.div`
  width: 100%;
  text-align: center;
`;

const FollowButton = styled(Button)`
  width: 100%;
  height: 100%;
  border: 1px solid black;
`;
