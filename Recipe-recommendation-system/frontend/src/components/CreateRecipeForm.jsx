import React from 'react';
import styled from 'styled-components';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

// MUI components
import Fab from '@mui/material/Fab';
import HomeOutlinedIcon from '@mui/icons-material/HomeOutlined';
import IconButton from '@mui/material/IconButton';
import PhotoCamera from '@mui/icons-material/PhotoCamera';
import TextField from '@mui/material/TextField';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Button from '@mui/material/Button';
import RemoveIcon from '@mui/icons-material/Remove';
import AddIcon from '@mui/icons-material/Add';

toast.configure();

const Input = styled('input')({
  display: 'none',
});

const convertBase64 = (file) => {
  return new Promise((resolve, reject) => {
    const fileReader = new FileReader();
    fileReader.readAsDataURL(file);

    fileReader.onload = () => {
      resolve(fileReader.result);
    };

    fileReader.onerror = (error) => {
      reject(error);
    };
  });
};

function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

function CreateRecipeForm() {
  const navigate = useNavigate();
  const token = localStorage.getItem('token');
  const email = localStorage.getItem('email');
  const userId = localStorage.getItem('user_id');

  const [imageFile, setImageFile] = React.useState('');
  const [imageShow, setImageShow] = React.useState(false);
  const [mealType, setMealType] = React.useState('');
  const [recipeName, setRecipeName] = React.useState('');
  const [ingredientsList, setIngredientsList] = React.useState([]);
  const [ingredientsDescription, setIngredientsDescription] = React.useState('');

  const uploadImage = async (event) => {
    const file = event.target.files[0];
    const base64 = await convertBase64(file);
    setImageFile(base64);
    setImageShow(true);
  };

  const handleAddIngredient = () => {
    const temp = {
      IngredientName: '',
      IngredientCategory: ''
    }
    setIngredientsList([...ingredientsList, temp])
  };

  const checkIngredients = () => {
    let hasUnknown = false;
    ingredientsList.map(ingredient =>
      ingredient.IngredientCategory === 'Unknown' ? (hasUnknown = true) : (hasUnknown)
    );
    return hasUnknown;
  }

  const createHandler = async () => {
    console.log('creating recipe');
    if (!imageFile) {
      toast.error('Sorry! Please upload image about your recipe!', {
        autoClose: 2000,
        position: toast.POSITION.TOP_CENTER
      });
    } else if (!mealType) {
      toast.error('Sorry! Please select the type of your recipe!', {
        autoClose: 2000,
        position: toast.POSITION.TOP_CENTER
      });
    } else if (!recipeName) {
      toast.error('Sorry! Please input the name of your recipe!', {
        autoClose: 2000,
        position: toast.POSITION.TOP_CENTER
      });
    } else if (ingredientsList.length === 0) {
      toast.error('Sorry! Please input ingredients that your recipe needed!', {
        autoClose: 2000,
        position: toast.POSITION.TOP_CENTER
      });
    } else if (!ingredientsDescription) {
      toast.error('Sorry! Please input the description of your recipe!', {
        autoClose: 2000,
        position: toast.POSITION.TOP_CENTER
      });
    } else if (checkIngredients()) {
      toast.error('Do not find matched ingredient', {
        autoClose: 2000,
        position: toast.POSITION.TOP_CENTER
      });
    } else {
      const requestBody = {
        user_id: userId,
        token: token,
        name: recipeName,
        image: imageFile,
        ingredients: ingredientsList,
        description: ingredientsDescription,
        category: mealType
      }
      const init = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      }
      const output = await fetch('http://127.0.0.1:5000/recipe/create', init);
      output.json().then(res => {
        if (res.recipe_id) {
          navigate(`/profile/${email}/own-recipes`);
          toast('Recipe created successfully!', {
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
  }

  return (
    <Wrapper>
      <Fab
        color="default"
        aria-label="add"
        sx={{ position: 'fixed', top: '2rem', left: '2rem' }}
        onClick={() => navigate(`/dashboard/${email}`)}>
        <HomeOutlinedIcon />
      </Fab>
      <br />
      <h1 style={{ color: 'red' }}>Create Recipe</h1>
      <br />
      <ImageUpload style={{ backgroundImage: imageShow ? `url(${imageFile})` : 'none', backgroundSize: '100% 100%' }} >
        <ImageCanvas>
          <label htmlFor="icon-button-file">
            <Input accept="image/*" id="icon-button-file" type="file" single onChange={e => uploadImage(e)} />
            <IconButton color="primary" aria-label="upload picture" component="span">
              <PhotoCamera sx={{ fontSize: '30pt' }} />
            </IconButton>
          </label>
        </ImageCanvas>
      </ImageUpload>
      <RecipeName>
        <TextField id="recipe-name" label="Recipe Name" variant="outlined" color="info" sx={{ width: '60%', borderRadius: '10px', background: '#ffffff' }} value={recipeName} onChange={e => setRecipeName(capitalizeFirstLetter(e.target.value))} />
        <FormControl required sx={{ width: '35%', borderRadius: '10px', background: '#ffffff' }}>
          <InputLabel id="recipe-type">Meal Type</InputLabel>
          <Select
            labelId="recipe-type"
            id="recipe-type"
            value={mealType}
            label="Meal Type"
            onChange={e => setMealType(e.target.value)}
          >
            <MenuItem value=''><em>Unknown</em></MenuItem>
            <MenuItem value='breakfast'>Breakfast</MenuItem>
            <MenuItem value='lunch'>Lunch</MenuItem>
            <MenuItem value='dinner'>Dinner</MenuItem>
            <MenuItem value='entree'>Entree</MenuItem>
            <MenuItem value='main'>Main</MenuItem>
            <MenuItem value='dessert'>Dessert</MenuItem>
            <MenuItem value='other'>Other</MenuItem>
          </Select>
        </FormControl>
      </RecipeName>
      <IngredientsInput>
        <br />
        <h3>Ingredients requirement</h3>
        <IngredientsField>
          {ingredientsList.length > 0 && ingredientsList.map((ingredient, index) => {
            const changeContentHandler = (e) => {
              const init = {
                method: 'GET',
                headers: {
                  'Content-Type': 'application/json'
                }
              }
              fetch(`http://127.0.0.1:5000/ingredient/select?name=${capitalizeFirstLetter(e.target.value)}`, init)
                .then(res => res.json()).then(data => {
                  // console.log(data);
                  if (data.name) {
                    setIngredientsList(() => ingredientsList.map(item => (
                      item === ingredient
                        ? ({ ...item, IngredientName: capitalizeFirstLetter(e.target.value), IngredientCategory: data.category })
                        : (item)
                    )));
                  } else {
                    setIngredientsList(() => ingredientsList.map(item => (
                      item === ingredient
                        ? ({ ...item, IngredientName: capitalizeFirstLetter(e.target.value), IngredientCategory: 'Unknown' })
                        : (item)
                    )))
                  }
                });
            }

            return (
              <Ingredients key={index}>
                <TextField id="ingredient" label="Ingredient Name" variant="outlined" color="info" sx={{ width: '60%', borderRadius: '10px', background: '#ffffff' }} onChange={e => changeContentHandler(e)} />
                <TextField id="ingredient" label="Ingredient Category" value={ingredient.IngredientCategory} variant="outlined" color="info" InputProps={{ readOnly: true, }} sx={{ width: '30%', borderRadius: '10px', background: '#ffffff' }} />
                <RemoveIngredient variant='contained' color='secondary' aria-label="Remove this ingredient" onClick={() => setIngredientsList(() => ingredientsList.filter(item => item !== ingredient))}><RemoveIcon /></RemoveIngredient>
              </Ingredients>
            );
          })}
        </IngredientsField>
        <AddIngredient variant='contained' color='last' aria-label="Add more one ingredient" onClick={handleAddIngredient}><AddIcon /></AddIngredient>
      </IngredientsInput>
      <DescriptionField>
        <br />
        <h3>Details Description</h3>
        <TextField
          id="details-description"
          label="Please input description, such as cook steps, the amount of each ingredient."
          multiline
          rows={10}
          sx={{ width: '100%', borderRadius: '10px', background: '#ffffff' }}
          color="info"
          value={ingredientsDescription}
          onChange={e => setIngredientsDescription(e.target.value)}
        />
      </DescriptionField>
      <br />
      <CreateButton variant='contained' color='secondary' aria-label="Create Recipe" onClick={createHandler}><span style={{ color: '#fff', fontSize: '20px', fontWeight: 'bold' }}>Create</span></CreateButton>
      <br />
      <br />
    </Wrapper>
  );
}

export default CreateRecipeForm;

const Wrapper = styled.div`
  position: fixed;
  top: 5vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  background: rgba(255, 255, 255, 0.8);
  box-shadow: rgba(0, 0, 0, 0.50) 1.95px 1.95px 2.6px;
  margin: auto;
  width: 70vw;
  height: 90vh;
  border-radius: 10px;
  overflow: auto;
`;

const ImageUpload = styled.div`
  width: 70%;
  height: 500px;
  border: 0.5px solid lightGrey;
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin: auto;
  align-items: center;
  border-radius: 10px;
`;

const ImageCanvas = styled.div`
  width: 100%;
  height: 500px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin: auto;
  align-items: center;
  background: rgba(255, 255, 255, 0.4);
  border-radius: 10px;
`;

const RecipeName = styled.div`
  width: 80%;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  margin: auto;
  align-items: center;
  border-radius: 10px;
`;

const IngredientsInput = styled.div`
  width: 80%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin: auto;
  align-items: center;
  border-radius: 10px;
  gap: 1rem;
`;

const RemoveIngredient = styled(Button)`
  width: 5%;
`;

const IngredientsField = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin: auto;
  align-items: center;
  border-radius: 10px;
  gap: 1rem;
`;

const Ingredients = styled.div`
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  margin: auto;
  align-items: center;
  border-radius: 10px;
  gap: 1rem;
`;

const AddIngredient = styled(Button)`
  width: 100%;
`;

const DescriptionField = styled.div`
  width: 80%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin: auto;
  align-items: center;
  border-radius: 10px;
  gap: 1rem;
`;

const CreateButton = styled(Button)`
  width: 50%;
`;
