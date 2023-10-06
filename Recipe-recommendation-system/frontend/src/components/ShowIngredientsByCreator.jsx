import * as React from 'react';
import { useNavigate } from 'react-router-dom';
import PropTypes from 'prop-types';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

// MUI Components
import { styled } from '@mui/material/styles';
// import Box from '@mui/material/Box';
import ButtonBase from '@mui/material/ButtonBase';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import AddIcon from '@mui/icons-material/Add';

toast.configure();

function ShowIngredientsByCreator({ userId }) {
  const email = localStorage.getItem('email');
  const myUserID = localStorage.getItem('user_id');

  const navigate = useNavigate();

  const [recipesList, setRecipesList] = React.useState([]);
  const getRecipesByCreatorId = () => {
    const init = {
      mathod: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    }
    fetch(`http://127.0.0.1:5000/recipe/own?user_id=${userId}`, init)
      .then(res => res.json())
      .then(data => {
        if (data.recipes) {
          setRecipesList(data.recipes);
        } else {
          toast.error(data.error, {
            autoClose: 2000,
            position: toast.POSITION.TOP_CENTER
          })
        }
      })
  }

  React.useEffect(() => {
    getRecipesByCreatorId();
  }, [])

  return (
    <Wrapper>
      {recipesList.map((recipe) => (
        <ImageButton
          focusRipple
          key={recipe._id}
          style={{
            width: '200px',
            borderRadius: '10px',
          }}
          onClick={() => window.open(`/recipe/${recipe._id}`)}
        >
          <ImageSrc style={{ backgroundImage: `url(${recipe.image})` }} />
          <ImageBackdrop className="MuiImageBackdrop-root" />
          <Image>
            <Typography
              component="span"
              variant="subtitle1"
              color="inherit"
              sx={{
                position: 'relative',
                p: 4,
                pt: 2,
                pb: (theme) => `calc(${theme.spacing(1)} + 6px)`,
              }}
            >
              {recipe.name}
              <ImageMarked className="MuiImageMarked-root" />
            </Typography>
          </Image>
        </ImageButton>
      ))}
      {myUserID === userId
        ? (<Button sx={{ width: '200px', height: '200px', border: '1px solid grey' }} aria-label="Create a new Recipe" onClick={() => navigate(`/${email}/recipe/create`)} ><AddIcon style={{ fontSize: '50', color: 'black' }} /></Button>)
        : (<div />)
      }
    </Wrapper>
  );
}

export default ShowIngredientsByCreator;

ShowIngredientsByCreator.propTypes = {
  userId: PropTypes.any,
}

const Wrapper = styled('div')({
  display: 'flex',
  flexDirection: 'row',
  alignItems: 'flex-start',
  gap: '1rem',
  margin: 'auto',
  borderRadius: '5px',
  width: '95%',
  flexWrap: 'wrap',
  justifyContent: 'flex-start',
  overflow: 'auto',
  marginTop: '2%',
});

const ImageButton = styled(ButtonBase)(({ theme }) => ({
  position: 'relative',
  height: 200,
  [theme.breakpoints.down('sm')]: {
    width: '100% !important', // Overrides inline-style
    height: 100,
  },
  '&:hover, &.Mui-focusVisible': {
    zIndex: 1,
    '& .MuiImageBackdrop-root': {
      opacity: 0.15,
    },
    '& .MuiImageMarked-root': {
      opacity: 0,
    },
    '& .MuiTypography-root': {
      border: '4px solid currentColor',
      borderRadius: '10px'
    },
  },
}));

const ImageSrc = styled('span')({
  position: 'absolute',
  left: 0,
  right: 0,
  top: 0,
  bottom: 0,
  backgroundSize: 'cover',
  backgroundPosition: 'center 40%',
});

const Image = styled('span')(({ theme }) => ({
  position: 'absolute',
  left: 0,
  right: 0,
  top: 0,
  bottom: 0,
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  color: theme.palette.common.white,
}));

const ImageBackdrop = styled('span')(({ theme }) => ({
  position: 'absolute',
  left: 0,
  right: 0,
  top: 0,
  bottom: 0,
  backgroundColor: theme.palette.common.black,
  opacity: 0.4,
  transition: theme.transitions.create('opacity'),
}));

const ImageMarked = styled('span')(({ theme }) => ({
  height: 3,
  width: 18,
  backgroundColor: theme.palette.common.white,
  position: 'absolute',
  bottom: -2,
  left: 'calc(50% - 9px)',
  transition: theme.transitions.create('opacity'),
}));
