import React from 'react';
import styled from 'styled-components';
import PropTypes from 'prop-types';
// import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

// MUI Components
import IconButton from '@mui/material/IconButton';
import ThumbUpOffAltIcon from '@mui/icons-material/ThumbUpOffAlt';
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import BookmarkBorderIcon from '@mui/icons-material/BookmarkBorder';
import BookmarkIcon from '@mui/icons-material/Bookmark';
import Rating from '@mui/material/Rating';
import Typography from '@mui/material/Typography';
import Chip from '@mui/material/Chip';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

toast.configure();

function RecipeDetailForm({ recipeId }) {
  const myUserId = localStorage.getItem('user_id');
  const myEmail = localStorage.getItem('email');
  const myToken = localStorage.getItem('token');

  const [recipeName, setRecipeName] = React.useState('');
  const [recipeImage, setRecipeImage] = React.useState('');
  const [creatorId, setCreatorId] = React.useState('');
  const [creatorName, setCreatorName] = React.useState('');
  const [amountOfLikes, setAmountOfLikes] = React.useState(0);
  const [amountOfCollect, setAmountOfCollect] = React.useState(0);
  const [recipeRating, setRecipeRating] = React.useState(0);
  const [ingredientRequired, setIngredientRequired] = React.useState([]);
  const [recipeDescription, setRecipeDescription] = React.useState('');
  const [recipeComments, setRecipeComments] = React.useState([]);

  const [likesClick, setLikesClick] = React.useState(false);
  const [collectClick, setCollectClick] = React.useState(false);
  const [newComment, setNewComment] = React.useState('');
  const textInput = React.useRef(null);
  // const navigate = useNavigate();

  const getRecipeInfoById = () => {
    const init = {
      mathod: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    }
    fetch(`http://127.0.0.1:5000/recipe/detail?recipe_id=${recipeId}`, init)
      .then(res => res.json())
      .then(recipe => {
        if (recipe._id) {
          // console.log(recipe);
          setRecipeName(recipe.name);
          setCreatorId(recipe.created_by);
          setRecipeImage(recipe.image);
          setAmountOfLikes(recipe.liked_by.length);
          setAmountOfCollect(recipe.collected_by.length);
          setRecipeRating(recipe.rating);
          setIngredientRequired(recipe.ingredients);
          setRecipeDescription(recipe.description);
          setRecipeComments(recipe.comments);
          if (recipe.liked_by.includes(myUserId)) {
            setLikesClick(true);
          } else {
            setLikesClick(false);
          }
          if (recipe.collected_by.includes(myUserId)) {
            setCollectClick(true);
          } else {
            setCollectClick(false);
          }
          fetch(`http://127.0.0.1:5000/user/profile?user_id=${recipe.created_by}`, init)
            .then(res => res.json())
            .then(data => {
              if (data.profile) {
                setCreatorName(data.profile.username);
              } else {
                toast.error(data.error, {
                  autoClose: 2000,
                  position: toast.POSITION.TOP_CENTER
                })
              }
            })
        } else {
          toast.error(recipe.error, {
            autoClose: 2000,
            position: toast.POSITION.TOP_CENTER
          })
        }
      })
  };

  React.useEffect(() => {
    getRecipeInfoById();
  }, []);

  const RatingHandler = async (newValue) => {
    if (newValue === null) {
      newValue = recipeRating;
    }
    // console.log(newValue);
    if (creatorId === myUserId) {
      toast.error('You cannot add rating to your own recipe!!!', {
        autoClose: 2000,
        position: toast.POSITION.TOP_CENTER
      })
    } else if (!myToken) {
      toast.error('Please Login!!!', {
        autoClose: 2000,
        position: toast.POSITION.TOP_CENTER
      })
    } else {
      // console.log(myToken)
      const requestBody = {
        user_id: myUserId,
        token: myToken,
        recipe_id: recipeId,
        rating: newValue,
      }
      const init = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      }
      const output = await fetch('http://127.0.0.1:5000/recipe/rating', init);
      // get token
      // console.log(output)
      output.json()
        .then(res => {
          if (res.success) {
            fetch(`http://127.0.0.1:5000/recipe/detail?recipe_id=${recipeId}`, {
              mathod: 'GET',
              headers: {
                'Content-Type': 'application/json'
              }
            }).then(data => data.json()).then(recipe => {
              if (recipe._id) {
                // console.log(recipe);
                setRecipeRating(recipe.rating)
              } else {
                toast.error(recipe.error, {
                  autoClose: 2000,
                  position: toast.POSITION.TOP_CENTER
                })
              }
            })
          } else {
            toast.error(res.error, {
              autoClose: 2000,
              position: toast.POSITION.TOP_CENTER
            })
          }
        });
    }
  }

  const LikeHandler = async () => {
    if (creatorId === myUserId) {
      toast.error('You cannot add likes your own recipe!!!', {
        autoClose: 2000,
        position: toast.POSITION.TOP_CENTER
      })
    } else if (!myToken) {
      toast.error('Please Login!!!', {
        autoClose: 2000,
        position: toast.POSITION.TOP_CENTER
      })
    } else {
      const requestBody = {
        user_id: myUserId,
        token: myToken,
        recipe_id: recipeId,
      }
      const init = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      }
      const output = await fetch('http://127.0.0.1:5000/recipe/like', init);
      output.json()
        .then(res => {
          if (res.success) {
            setLikesClick(true);
            fetch(`http://127.0.0.1:5000/recipe/detail?recipe_id=${recipeId}`, {
              mathod: 'GET',
              headers: {
                'Content-Type': 'application/json'
              }
            }).then(data => data.json()).then(recipe => {
              if (recipe._id) {
                // console.log(recipe);
                setAmountOfLikes(recipe.liked_by.length);
              } else {
                toast.error(recipe.error, {
                  autoClose: 2000,
                  position: toast.POSITION.TOP_CENTER
                })
              }
            })
          } else {
            toast.error(res.error, {
              autoClose: 2000,
              position: toast.POSITION.TOP_CENTER
            })
          }
        });
    }
  }

  const UnlikeHandler = async () => {
    if (creatorId === myUserId) {
      toast.error('You cannot remove likes from your own recipe!!!', {
        autoClose: 2000,
        position: toast.POSITION.TOP_CENTER
      })
    } else if (!myToken) {
      toast.error('Please Login!!!', {
        autoClose: 2000,
        position: toast.POSITION.TOP_CENTER
      })
    } else {
      const requestBody = {
        user_id: myUserId,
        token: myToken,
        recipe_id: recipeId,
      }
      const init = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      }
      const output = await fetch('http://127.0.0.1:5000/recipe/unlike', init);
      output.json()
        .then(res => {
          if (res.success) {
            setLikesClick(false);
            fetch(`http://127.0.0.1:5000/recipe/detail?recipe_id=${recipeId}`, {
              mathod: 'GET',
              headers: {
                'Content-Type': 'application/json'
              }
            }).then(data => data.json()).then(recipe => {
              if (recipe._id) {
                // console.log(recipe);
                setAmountOfLikes(recipe.liked_by.length);
              } else {
                toast.error(recipe.error, {
                  autoClose: 2000,
                  position: toast.POSITION.TOP_CENTER
                })
              }
            })
          } else {
            toast.error(res.error, {
              autoClose: 2000,
              position: toast.POSITION.TOP_CENTER
            })
          }
        });
    }
  }

  const CollectHandler = async () => {
    if (creatorId === myUserId) {
      toast.error('You cannot bookmark your own recipe!!!', {
        autoClose: 2000,
        position: toast.POSITION.TOP_CENTER
      })
    } else if (!myToken) {
      toast.error('Please Login!!!', {
        autoClose: 2000,
        position: toast.POSITION.TOP_CENTER
      })
    } else {
      const requestBody = {
        user_id: myUserId,
        token: myToken,
        recipe_id: recipeId,
      }
      const init = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      }
      const output = await fetch('http://127.0.0.1:5000/recipe/collect', init);
      output.json()
        .then(res => {
          if (res.success) {
            setCollectClick(true);
            fetch(`http://127.0.0.1:5000/recipe/detail?recipe_id=${recipeId}`, {
              mathod: 'GET',
              headers: {
                'Content-Type': 'application/json'
              }
            }).then(data => data.json()).then(recipe => {
              if (recipe._id) {
                // console.log(recipe);
                setAmountOfCollect(recipe.collected_by.length);
              } else {
                toast.error(recipe.error, {
                  autoClose: 2000,
                  position: toast.POSITION.TOP_CENTER
                })
              }
            })
          } else {
            toast.error(res.error, {
              autoClose: 2000,
              position: toast.POSITION.TOP_CENTER
            })
          }
        });
    }
  }

  const UncollectHandler = async () => {
    if (creatorId === myUserId) {
      toast.error('You cannot remove your own recipe from bookmark!!!', {
        autoClose: 2000,
        position: toast.POSITION.TOP_CENTER
      })
    } else if (!myToken) {
      toast.error('Please Login!!!', {
        autoClose: 2000,
        position: toast.POSITION.TOP_CENTER
      })
    } else {
      const requestBody = {
        user_id: myUserId,
        token: myToken,
        recipe_id: recipeId,
      }
      const init = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      }
      const output = await fetch('http://127.0.0.1:5000/recipe/uncollect', init);
      output.json()
        .then(res => {
          if (res.success) {
            setCollectClick(false);
            fetch(`http://127.0.0.1:5000/recipe/detail?recipe_id=${recipeId}`, {
              mathod: 'GET',
              headers: {
                'Content-Type': 'application/json'
              }
            }).then(data => data.json()).then(recipe => {
              if (recipe._id) {
                // console.log(recipe);
                setAmountOfCollect(recipe.collected_by.length);
              } else {
                toast.error(recipe.error, {
                  autoClose: 2000,
                  position: toast.POSITION.TOP_CENTER
                })
              }
            })
          } else {
            toast.error(res.error, {
              autoClose: 2000,
              position: toast.POSITION.TOP_CENTER
            })
          }
        });
    }
  }

  const CommentPosttHandler = async () => {
    if (creatorId === myUserId) {
      toast.error('You cannot post comments to your own recipe!!!', {
        autoClose: 2000,
        position: toast.POSITION.TOP_CENTER
      })
    } else if (!myToken) {
      toast.error('Please Login!!!', {
        autoClose: 2000,
        position: toast.POSITION.TOP_CENTER
      })
    } else {
      const requestBody = {
        user_id: myUserId,
        token: myToken,
        recipe_id: recipeId,
        comment: newComment,
      }
      const init = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      }
      const output = await fetch('http://127.0.0.1:5000/recipe/comment', init);
      output.json()
        .then(res => {
          if (res.success) {
            fetch(`http://127.0.0.1:5000/recipe/detail?recipe_id=${recipeId}`, {
              mathod: 'GET',
              headers: {
                'Content-Type': 'application/json'
              }
            }).then(data => data.json()).then(recipe => {
              if (recipe._id) {
                // console.log(recipe);
                setRecipeComments(recipe.comments);
                textInput.current.value = '';
              } else {
                toast.error(recipe.error, {
                  autoClose: 2000,
                  position: toast.POSITION.TOP_CENTER
                })
              }
            })
          } else {
            toast.error(res.error, {
              autoClose: 2000,
              position: toast.POSITION.TOP_CENTER
            })
          }
        })
    }
  }

  const RecipeDelete = () => {
    const requestBody = {
      user_id: myUserId,
      token: myToken,
      recipe_id: recipeId,
    }
    const init = {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestBody)
    }
    fetch('http://127.0.0.1:5000/recipe/delete', init)
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          window.close();
          // navigate()
        } else {
          toast.error(data.error, {
            autoClose: 2000,
            position: toast.POSITION.TOP_CENTER
          })
        }
      })
  }

  return (
    <Wrapper>
      <h1 style={{ fontSize: '50pt', textAlign: 'center' }}>{recipeName}</h1>
      <TopContainer>
        <SubContainerLeft>
          <ImageField>
            <Image src={recipeImage} alt='Recipe Image' />
          </ImageField>
          {myUserId === creatorId
            ? (<CreatorLink>Recipe Created by: <a onClick={() => window.open(`/profile/${myEmail}`)} style={{ textDecoration: 'underline', color: 'blue' }} >{creatorName}</a></CreatorLink>)
            : (<CreatorLink>Recipe Created by: <a onClick={() => window.open(`/personal-detail/${creatorId}`)} style={{ textDecoration: 'underline', color: 'blue' }} >{creatorName}</a></CreatorLink>)
          }
        </SubContainerLeft>
        <SubContainerRight>
          <IngredientField>
            <h1 style={{ marginLeft: '1%', marginRight: '1%', color: 'green' }}>Required Ingredients:</h1>
            {ingredientRequired.length > 0 && ingredientRequired.map((ingredient, index) => {
              return (
                <Chip key={index} color="primary" label={ingredient.IngredientName} variant="outlined" sx={{ fontSize: '20px', marginLeft: '1%', marginBottom: '1%' }} />
              );
            })}
          </IngredientField>
          <ClickInteraction>
            {likesClick
              ? (
                <IconButton aria-label="like" size="large" onClick={UnlikeHandler}>
                  <ThumbUpIcon fontSize="inherit" />
                  {amountOfLikes}
                </IconButton>
                )
              : (
                <IconButton aria-label="unlike" size="large" onClick={LikeHandler}>
                  <ThumbUpOffAltIcon fontSize="inherit" />
                  {amountOfLikes}
                </IconButton>
                )
            }
            {collectClick
              ? (
                <IconButton aria-label="collect" size="large" onClick={UncollectHandler}>
                  <BookmarkIcon fontSize="inherit" />
                  {amountOfCollect}
                </IconButton>
                )
              : (
                <IconButton aria-label="uncollect" size="large" onClick={CollectHandler}>
                  <BookmarkBorderIcon fontSize="inherit" />
                  {amountOfCollect}
                </IconButton>
                )
            }
            <RatingBox>
              {recipeRating > 0
                ? (<Typography component="legend">Average Rating: {recipeRating}</Typography>)
                : (<Typography component="legend">No Rating Given</Typography>)
              }
              <Rating
                name="no-value"
                value={recipeRating}
                precision={0.5}
                onChange={(event, newValue) => {
                  RatingHandler(newValue);
                }}
              />
            </RatingBox>
          </ClickInteraction>
        </SubContainerRight>
      </TopContainer>
      <DescriptionContainer>
        <h2 style={{ marginLeft: '1%', marginRight: '1%', color: 'green' }}>Cooking Steps:</h2>
        <p style={{ marginLeft: '1%', marginRight: '1%', marginBottom: '1%', fontSize: '15pt', lineHeight: '30px' }}>{recipeDescription}</p>
      </DescriptionContainer>
      <CommentsContainer>
        <h2 style={{ marginLeft: '1%', marginRight: '1%', color: 'green' }}>5 Newest Comments:</h2>
        {recipeComments.map((comment, index) => {
          return (
            <p key={index} style={{ marginLeft: '1%', marginRight: '1%', marginBottom: '1%', fontSize: '15pt', lineHeight: '30px' }}>{index + 1}: {comment}</p>
          );
        })}
      </CommentsContainer>
      <CommentsAddField>
        <TextField id="newComments" placeholder='Please input your commnets here and then click right button to post it!!!' label="Post Your Comments" variant="outlined" color="info" sx={{ width: '90%', borderRadius: '10px', background: '#ffffff', marginTop: '0.4rem' }} multiline rows={1} inputRef={textInput} onChange={(e) => setNewComment(e.target.value)} />
        <Post>
          <PostButton variant="contained" color='last' ><span style={{ color: '#fff', fontSize: '20px', fontWeight: 'bold' }} onClick={CommentPosttHandler} >Post</span></PostButton>
        </Post>
      </CommentsAddField>
      {creatorId === myUserId
        ? (
          <Delete>
            <DeleteButton variant="contained" color='secondary' onClick={RecipeDelete} ><span style={{ color: '#fff', fontSize: '15pt', fontWeight: 'bold', textTransform: 'capitalize' }}>Delete This Recipe</span></DeleteButton>
          </Delete>
          )
        : (
            <div></div>
          )
      }
    </Wrapper>
  );
}

export default RecipeDetailForm;

RecipeDetailForm.propTypes = {
  recipeId: PropTypes.any,
}

const Wrapper = styled.div`
  position: fixed;
  top: 5vh;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.8);
  box-shadow: rgba(0, 0, 0, 0.50) 1.95px 1.95px 2.6px;
  margin: auto;
  width: 70vw;
  height: 90vh;
  border-radius: 10px;
  overflow: auto;
`;

const TopContainer = styled.div`
  width: 95%;
  height: 300px;
  border-radius: 10px;
  display: flex;
  flex-direction: row;
  gap: 0.5rem;
  margin: auto;
  margin-bottom: 0.5rem;
`;

const DescriptionContainer = styled.div`
  width: 95%;
  height:300px;
  border-radius: 10px;
  overflow: auto;
  background: #ffffff;
  margin: auto;
  margin-bottom: 0.5rem;
`;

const CommentsContainer = styled.div`
  width: 95%;
  height:300px;
  border-radius: 10px;
  overflow: auto;
  background: #ffffff;
  display: flex;
  flex-direction: column;
  margin: auto;
  margin-bottom: 0.5rem;
  gap: 0.5rem;
`;

const CommentsAddField = styled.div`
  width: 95%;
  border-radius: 10px;
  overflow: auto;
  margin: auto;
  margin-bottom: 50px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
`;

const SubContainerLeft = styled.div`
  width: 40%;
  height: 100%;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
`;

const SubContainerRight = styled.div`
  width: 60%;
  height: 100%;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
`;

const ImageField = styled.div`
  height: 90%;
  width: 100%;
  border-radius: 10px;
`;

const CreatorLink = styled.div`
  height: 10%;
  width: 100%;
  border-radius: 10px;
  text-align: center;
  justify-content: center;
  align-item: center;
  color: #4F4D4D;
`;

const ClickInteraction = styled.div`
  height: 20%;
  width: 100%;
  border-radius: 10px;
  display: flex;
  flex-direction: row;
  gap: 0.5rem;
  align-items: center;
  justify-content: space-around;
`;

const IngredientField = styled.div`
  height: 80%;
  width: 100%;
  border-radius: 10px;
  overflow: auto;
  background: #ffffff;
`;

const Image = styled.img`
  width: 100%;
  height: 100%;
  border-radius: 10px;
`;

const RatingBox = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
  align-items: center;
  justify-content: center;
`;

const Post = styled.div`
  display: flex;
  margin: auto;
  margin-top: 0.4rem;
  width: 9%;
  height: 55px;
`;

const PostButton = styled(Button)`
  width: 100%;
`;

const Delete = styled.div`
  width: 95%; 
  display: flex;
  flex-direction: column;
  margin: auto;
  margin-top: 2rem;
  align-items: center;
  margin-bottom: 50px;
`;

const DeleteButton = styled(Button)`
  width: 250px;
`;
