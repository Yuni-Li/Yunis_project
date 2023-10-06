import React from 'react';
import styled from 'styled-components';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
// import { useNavigate } from 'react-router-dom';

// outside css
import 'animate.css';

// MUI components
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Modal from '@mui/material/Modal';
import Stepper from '@mui/material/Stepper';
import Step from '@mui/material/Step';
import StepLabel from '@mui/material/StepLabel';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import Paper from '@mui/material/Paper';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import Stack from '@mui/material/Stack';
import SearchIcon from '@mui/icons-material/Search';
import Chip from '@mui/material/Chip';
import Autocomplete from '@mui/material/Autocomplete';
import InputBase from '@mui/material/InputBase';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import { useTheme } from '@mui/material/styles';
import MobileStepper from '@mui/material/MobileStepper';
import KeyboardArrowLeft from '@mui/icons-material/KeyboardArrowLeft';
import KeyboardArrowRight from '@mui/icons-material/KeyboardArrowRight';

// own components
import backgroundImage from '../image/1.png';
import AppBar from '../components/AppBar';

const style = {
  display: 'flex',
  flexDirection: 'column',
  gap: '2rem',
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: '90%',
  bgcolor: 'background.paper',
  boxShadow: 'rgba(0, 0, 0, 0.80) 1.95px 1.95px 2.6px',
  borderRadius: '10px',
  p: 4,
};

toast.configure();

const steps = ['Add new ingredient', 'Choose category', 'Confirm'];

function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

function DashboardPage() {
  // const navigate = useNavigate();

  const [ingredientName, setIngredientName] = React.useState('');
  const [ingredientCategory, setIngredientCategory] = React.useState('');
  const [allIngredientsName, setAllIngredientsName] = React.useState([]);
  const [ingredientsList, setIngredientsList] = React.useState([]);
  const [recipesList, setRecipesList] = React.useState([]);
  const [popup, setPopup] = React.useState(false);
  const [ingredientInputValue, setIngredientInputValue] = React.useState([]);
  const [recipeInputValue, setRecipeInputValue] = React.useState('');
  const [searchResults, setSearchResults] = React.useState([]);
  const [mealType, setMealType] = React.useState('');
  const [sortBy, setSortBy] = React.useState('');
  const [nextIngredientSuggestion, setNextIngredientSuggestion] = React.useState([]);

  const theme = useTheme();
  const [activePage, setActivePage] = React.useState(0);
  let maxPages = searchResults.length === 0 ? (parseInt(searchResults.length / 10) + 1) : (Math.ceil(searchResults.length / 10));
  const handleNextPage = () => {
    setActivePage((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBackPage = () => {
    setActivePage((prevActiveStep) => prevActiveStep - 1);
  };

  const handleOpenPopup = () => setPopup(true);
  const handleClosePopup = () => {
    setPopup(false);
    setActiveStep(0);
    setIngredientName('');
    setIngredientCategory('');
    getAllDetail();
  }

  const [activeStep, setActiveStep] = React.useState(0);
  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };
  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      event.preventDefault();
      console.log('hello')
    }
  }

  const createHandler = async () => {
    const requestBody = {
      name: ingredientName,
      category: ingredientCategory
    }
    const init = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestBody)
    }
    const output = await fetch('http://127.0.0.1:5000/ingredient/populate', init);
    output.json().then(res => {
      if (res.success) {
        handleNext();
      } else {
        toast.error(res.error, {
          autoClose: 2000,
          position: toast.POSITION.TOP_CENTER
        });
      }
    });
  }

  const getAllDetail = () => {
    const init = {
      mathod: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    }
    fetch('http://127.0.0.1:5000/ingredient/show', init)
      .then(res => res.json())
      .then(data => {
        console.log(data.ingredients)
        setIngredientsList(data.ingredients);
        // console.log(ingredientsList);
        const ingredientNamesList = data.ingredients.map(function(obj) {
          const namesList = obj.matched_ingredients.map(function(item) {
            const ingredient = {};
            ingredient.name = item.name
            return ingredient;
          })
          return namesList;
        })
        const newIngredientNamesList = [].concat.apply([], ingredientNamesList);
        // console.log(newIngredientNamesList);
        setAllIngredientsName(newIngredientNamesList)
      });
    fetch('http://127.0.0.1:5000/recipe/show', init)
      .then(res => res.json())
      .then(data => {
        // console.log(data.recipes);
        setRecipesList(data.recipes);
      });
  }

  React.useEffect(() => {
    getAllDetail();
  }, [])

  const getResults = async () => {
    if (recipeInputValue && ingredientInputValue.length > 0) {
      setNextIngredientSuggestion([]);
      const requestBody = {
        recipe_name: recipeInputValue,
        meal_type: !mealType ? null : mealType,
        sort_by: !sortBy ? null : sortBy,
      }
      // console.log(requestBody);
      const init = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      }
      const output = await fetch('http://127.0.0.1:5000/recipe/search/name', init);
      output.json().then(res => {
        // console.log(res);
        if (res.recipes) {
          setSearchResults(res.recipes);
        } else {
          toast.error(res.error, {
            autoClose: 2000,
            position: toast.POSITION.TOP_CENTER
          });
        }
      });
    } else if (recipeInputValue && ingredientInputValue.length === 0) {
      setNextIngredientSuggestion([]);
      const requestBody = {
        recipe_name: recipeInputValue,
        meal_type: !mealType ? null : mealType,
        sort_by: !sortBy ? null : sortBy,
      }
      // console.log(requestBody);
      const init = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      }
      const output = await fetch('http://127.0.0.1:5000/recipe/search/name', init);
      output.json().then(res => {
        // console.log(res);
        if (res.recipes) {
          setSearchResults(res.recipes);
        } else {
          toast.error(res.error, {
            autoClose: 2000,
            position: toast.POSITION.TOP_CENTER
          });
        }
      });
    } else if (!recipeInputValue && ingredientInputValue.length > 0) {
      const newIngredientInputValue = ingredientInputValue.map((item) => item.name);
      // console.log(newIngredientInputValue);
      const requestBody = {
        ingredients: newIngredientInputValue,
        meal_type: !mealType ? null : mealType,
        sort_by: !sortBy ? null : sortBy,
      }
      // console.log(requestBody);
      const init = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      }
      const output = await fetch('http://127.0.0.1:5000/recipe/search/ingredients', init);
      output.json().then(res => {
        // console.log(res)
        if (res.matched_recipes) {
          setSearchResults(res.matched_recipes);
          setNextIngredientSuggestion(res.missing_ingredients);
        } else {
          toast.error(res.error, {
            autoClose: 2000,
            position: toast.POSITION.TOP_CENTER
          });
        }
      });
    } else if (!recipeInputValue && ingredientInputValue.length === 0 && (mealType || sortBy)) {
      setMealType('');
      setSortBy('');
    } else if (!recipeInputValue && ingredientInputValue.length === 0 && !mealType && !sortBy) {
      setSearchResults([]);
      setNextIngredientSuggestion([]);
      maxPages = searchResults.length === 0 ? (parseInt(searchResults.length / 10) + 1) : (Math.ceil(searchResults.length / 10));
      setActivePage(0);
    }
  }

  React.useEffect(() => {
    getResults();
  }, [recipeInputValue, ingredientInputValue, mealType, sortBy])

  // console.log(allIngredientsName);
  // console.log(recipeInputValue);
  // console.log(mealType);
  // console.log(ingredientInputValue);
  // console.log(searchResults);
  // console.log(nextIngredientSuggestion);

  return (
    <Wrapper>
      <Container>
        <AppBar />
        <DashboardLeftField>
          <Paper
            component="form"
            sx={{ p: '2px 4px', display: 'flex', alignItems: 'center', width: '90%', marginTop: '20px' }}
          >
            <Autocomplete
              freeSolo
              options={recipesList}
              getOptionLabel={(option) => option.name ? option.name : ''}
              value={recipeInputValue.name}
              renderInput={(params) => {
                const { InputLabelProps, InputProps, ...rest } = params;
                return (
                  <InputBase
                  {...params.InputProps} {...rest}
                  placeholder="Search Recipes By Input Name..."
                  onKeyDown={handleKeyDown}
                  />
                )
              }}
              sx={{ ml: 1, flex: 1 }}
              onChange={(event, value) => { value === null ? setRecipeInputValue('') : setRecipeInputValue(value.name) }}
            />
            <Divider sx={{ height: 28, m: 0.5 }} orientation="vertical" />
            <IconButton sx={{ p: '10px' }} aria-label="search">
              <SearchIcon />
            </IconButton>
          </Paper>
          <RecipeShowField>
            <Box sx={{ width: '100%', height: '81.5vh', bgcolor: 'background.paper', overflow: 'auto' }}>
              <Box sx={{ m: 2, height: '11.5vh', overflow: 'auto' }}>
                {(recipeInputValue || ingredientInputValue.length !== 0)
                  ? (
                    <Typography gutterBottom variant="body1" sx={{ fontSize: '30pt', fontWeight: 'bold' }} >
                      Get {searchResults.length} Results
                    </Typography>
                    )
                  : (
                    <Typography gutterBottom variant="body1" sx={{ fontSize: '23pt', fontWeight: 'bold' }} >
                      Please Input Recipe Name Or Your Owned Ingredients To Fit the Search!
                    </Typography>
                    )
                }
                {nextIngredientSuggestion.length > 0
                  ? (
                    <Stack direction="row" sx={{ flexWrap: 'wrap', alignItems: 'center', justifyContent: 'flex-start', gap: '0.3rem' }}>
                      Ingredients Input Suggestion:
                      {nextIngredientSuggestion.map((item, index) => (
                        <Chip label={item} key={index} />
                      ))}
                    </Stack>
                    )
                  : (
                    <div></div>
                    )
                }
                <br />
              </Box>
              <Divider variant="fullWidth" />
              <FormControl sx={{ width: '11%', borderRadius: '10px', background: '#ffffff', top: 1, left: '76%' }}>
                <InputLabel id="recipe-type">Meal Type</InputLabel>
                <Select
                  labelId="recipe-type"
                  id="recipe-type"
                  value={mealType}
                  label="Meal Type"
                  onChange={e => setMealType(e.target.value)}
                >
                  <MenuItem value=''>No Select</MenuItem>
                  <MenuItem value='breakfast'>Breakfast</MenuItem>
                  <MenuItem value='lunch'>Lunch</MenuItem>
                  <MenuItem value='dinner'>Dinner</MenuItem>
                  <MenuItem value='entree'>Entree</MenuItem>
                  <MenuItem value='main'>Main</MenuItem>
                  <MenuItem value='dessert'>Dessert</MenuItem>
                  <MenuItem value='other'>Other</MenuItem>
                </Select>
              </FormControl>
              <FormControl sx={{ width: '11%', borderRadius: '10px', background: '#ffffff', top: 1, left: '77%' }}>
                <InputLabel id="sort">Sort By</InputLabel>
                <Select
                  labelId="sort"
                  id="sort"
                  value={sortBy}
                  label="Sort By"
                  onChange={e => setSortBy(e.target.value)}
                >
                  <MenuItem value=''>No Sort</MenuItem>
                  <MenuItem value='ratings'>Rating</MenuItem>
                  <MenuItem value='likes'>Likes</MenuItem>
                </Select>
              </FormControl>
              <Box sx={{ height: '60vh', flexGrow: 1 }}>
                <Box sx={{ m: 2, height: '51vh', overflow: 'auto', flexWrap: 'wrap', display: 'flex', flexDirection: 'row', gap: '1rem', alignItems: 'flex-start', justifyContent: 'flex-start', boxShadow: 5 }}>
                  {searchResults.slice(activePage * 10, (activePage + 1) * 10).map((recipe, index) => (
                    <Card sx={{ width: 'calc(50% - 1.7rem)', boxShadow: 10, m: 1, display: 'flex', flexDirection: 'row' }} key={index} >
                      <CardMedia
                        component="img"
                        image={recipe.image}
                        alt="recipe image"
                        sx={{ m: 'auto', marginLeft: 1, width: '230px', height: '180px' }}
                      />
                      <div style={{ display: 'flex', flexDirection: 'column', width: '400px' }}>
                        <CardContent>
                          <Typography gutterBottom variant="h5" component="div" sx={{ height: '80px', overflow: 'auto' }}>
                            {recipe.name}
                          </Typography>
                          <Typography variant="body2" color="text.secondary" sx={{ height: '60px', overflow: 'auto' }}>
                            Required Ingredinets: {recipe.ingredients.map((item) => item.IngredientName + ', ')}
                          </Typography>
                          <br />
                          {recipe.missing_ingredients && recipe.missing_ingredients.length > 0
                            ? (
                              <Typography variant="body2" color="secondary" sx={{ height: '30px', overflow: 'auto' }}>
                                Missing Ingredinets: {recipe.missing_ingredients.map((item) => item + ', ')}
                              </Typography>
                              )
                            : (
                              <div style={{ height: '30px' }}></div>
                              )
                          }
                        </CardContent>
                        <CardActions>
                          <Button size="small" onClick={() => window.open(`/recipe/${recipe._id}`)} >See More Details</Button>
                        </CardActions>
                      </div>
                    </Card>
                  ))}
                </Box>
                <MobileStepper
                  variant="text"
                  steps={maxPages}
                  position="static"
                  activeStep={activePage}
                  nextButton={
                    <Button
                      size="small"
                      onClick={handleNextPage}
                      disabled={activePage === maxPages - 1}
                    >
                      Next
                      {theme.direction === 'rtl'
                        ? (
                          <KeyboardArrowLeft />
                          )
                        : (
                          <KeyboardArrowRight />
                          )}
                    </Button>
                  }
                  backButton={
                    <Button size="small" onClick={handleBackPage} disabled={activePage === 0}>
                      {theme.direction === 'rtl'
                        ? (
                          <KeyboardArrowRight />
                          )
                        : (
                          <KeyboardArrowLeft />
                          )}
                      Back
                    </Button>
                  }
                />
              </Box>
            </Box>
          </RecipeShowField>
        </DashboardLeftField>
        <DashboardRightBar>
          <Paper
            component="form"
            sx={{ p: '2px 4px', display: 'flex', alignItems: 'center', width: '90%', marginTop: '20px' }}
          >
            <Autocomplete
              multiple
              freeSolo
              options={allIngredientsName}
              getOptionLabel={(option) => option.name}
              value={ingredientInputValue.map((item) => item)}
              renderInput={(params) => {
                const { InputLabelProps, InputProps, ...rest } = params;
                return (
                  <InputBase
                  {...params.InputProps} {...rest}
                  placeholder="Search Recipes By Input Ingredients..."
                  onKeyDown={handleKeyDown}
                  />
                )
              }}
              sx={{ ml: 1, flex: 1 }}
              onChange={(event, value) => setIngredientInputValue(value)}
            />
            <Divider sx={{ height: 28, m: 0.5 }} orientation="vertical" />
            <IconButton sx={{ p: '10px' }} aria-label="search">
              <SearchIcon />
            </IconButton>
          </Paper>
          <Box sx={{ width: '100%', height: '81.5vh', bgcolor: 'background.paper', overflow: 'auto' }}>
            {ingredientsList.map((item) => (
              <React.Fragment key={item.category}>
                <Box sx={{ m: 2, height: '15vh' }}>
                  <Typography gutterBottom variant="body1">
                    {item.category}
                  </Typography>
                  <Stack direction="row" sx={{ flexWrap: 'wrap', alignItems: 'flex-start', justifyContent: 'flex-start', gap: '0.3rem', height: '10vh', overflow: 'auto' }}>
                    {item.matched_ingredients.map((ingredient, index) => (
                      (ingredientInputValue.some(item => item.name === ingredient.name)
                        ? <Chip label={ingredient.name} key={index} color="info" onClick={() => setIngredientInputValue(() => ingredientInputValue.filter(item => item.name !== ingredient.name))} />
                        : <Chip label={ingredient.name} key={index} onClick={() => setIngredientInputValue([...ingredientInputValue, ingredient])} />
                      )
                    ))}
                  </Stack>
                  <br />
                </Box>
                <Divider variant="fullWidth" />
              </React.Fragment>
            ))}
            <Box sx={{ m: 2, textAlign: 'center' }}>
              <SuggestIngredientButton variant="contained" style={{ marginBottom: '20px', borderRadius: '5px' }} color='paper' onClick={handleOpenPopup} ><span style={{ color: '#002e9b', fontSize: '20px', textTransform: 'capitalize' }}>Suggest Ingredient</span></SuggestIngredientButton>
              <Modal
                open={popup}
                onClose={handleClosePopup}
                aria-labelledby="modal-modal-title"
                aria-describedby="modal-modal-description"
              >
                <Box sx={style}>
                  <Stepper activeStep={activeStep}>
                    {steps.map((label) => {
                      const stepProps = {};
                      const labelProps = {};
                      return (
                        <Step key={label} {...stepProps}>
                          <StepLabel {...labelProps}>{label}</StepLabel>
                        </Step>
                      );
                    })}
                  </Stepper>
                  {activeStep === steps.length
                    ? (
                      <React.Fragment>
                        <Typography sx={{ textAlign: 'center', fontSize: '20px' }}>
                          <span style={{ color: 'green', fontWeight: 'bold' }} >Fine! New ingredient has created successfully!</span>
                        </Typography>
                        <Box sx={{ display: 'flex', flexDirection: 'row', pt: 2 }}>
                          <Box sx={{ flex: '1 1 auto' }} />
                          <Button variant='contained' color='last' onClick={handleClosePopup}>Done</Button>
                        </Box>
                      </React.Fragment>
                      )
                    : (activeStep === 0
                        ? (
                        <React.Fragment>
                          <TextField label="Ingredient Name" variant="outlined" color="info" value={ingredientName} onChange={(e) => setIngredientName(capitalizeFirstLetter(e.target.value))} />
                          <Box sx={{ display: 'flex', flexDirection: 'row', pt: 2 }}>
                            <Box sx={{ flex: '1 1 auto' }} />
                            <Button
                            variant='contained'
                            color='last'
                            onClick={
                              () => {
                                if (ingredientName) {
                                  handleNext();
                                } else {
                                  toast.error('Sorry! Please input Ingredient Name!', {
                                    autoClose: 2000,
                                    position: toast.POSITION.TOP_CENTER
                                  });
                                }
                              }
                            }>
                              {activeStep === steps.length - 1 ? 'Create' : 'Next'}
                            </Button>
                          </Box>
                        </React.Fragment>
                          )
                        : (activeStep === 1
                            ? (
                            <React.Fragment>
                              <TextField label="Ingredient Category" variant="outlined" color="info" value={ingredientCategory} onChange={(e) => setIngredientCategory(capitalizeFirstLetter(e.target.value))} />
                              <Box sx={{ display: 'flex', flexDirection: 'row', pt: 2 }}>
                                <Button
                                  color="secondary"
                                  variant='contained'
                                  disabled={activeStep === 0}
                                  onClick={handleBack}
                                  sx={{ mr: 1 }}
                                >
                                  Back
                                </Button>
                              <Box sx={{ flex: '1 1 auto' }} />
                              <Button
                              variant='contained'
                              color='last'
                              onClick={
                                () => {
                                  if (ingredientCategory) {
                                    handleNext();
                                  } else {
                                    toast.error('Sorry! Please input Ingredient Category!', {
                                      autoClose: 2000,
                                      position: toast.POSITION.TOP_CENTER
                                    });
                                  }
                                }
                              }>
                                {activeStep === steps.length - 1 ? 'Create' : 'Next'}
                              </Button>
                            </Box>
                          </React.Fragment>
                              )
                            : (
                          <React.Fragment>
                            <Typography sx={{ textAlign: 'center', fontSize: '20px' }}>Ingredient Name: <span style={{ color: 'red', fontWeight: 'bold' }} >{ingredientName}</span></Typography>
                            <Typography sx={{ textAlign: 'center', fontSize: '20px' }}>Ingredient Category: <span style={{ color: 'red', fontWeight: 'bold' }} >{ingredientCategory}</span></Typography>
                            <Box sx={{ display: 'flex', flexDirection: 'row', pt: 2 }}>
                              <Button
                                color="secondary"
                                variant='contained'
                                disabled={activeStep === 0}
                                onClick={handleBack}
                                sx={{ mr: 1 }}
                              >
                                Back
                              </Button>
                              <Box sx={{ flex: '1 1 auto' }} />
                              <Button variant='contained' color='last' onClick={createHandler}>
                                Create
                              </Button>
                            </Box>
                          </React.Fragment>
                              )
                          )
                      )
                  }
                </Box>
              </Modal>
            </Box>
          </Box>
        </DashboardRightBar>
      </Container>
    </Wrapper>
  );
}

export default DashboardPage;

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

const DashboardLeftField = styled.div`
  position: fixed;
  left: 1vw;
  height: 90vh;
  width: 71.5vw;
  top: 8.5vh;
  background: rgba(255, 119, 15, 0.8);
  border-radius: 10px;
  overflow: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: auto;
  gap: 1rem;
`;

const RecipeShowField = styled.div`
  height: 81.5vh;
  width: 100%;
  background: rgba(255, 255, 255);
  border-radius: 10px;
  overflow: auto;
  margin: auto;
  gap: 1rem;
`;

const DashboardRightBar = styled.div`
  position: fixed;
  right: 1vw;
  height: 90vh;
  width: 26vw;
  top: 8.5vh;
  background: rgba(255, 119, 15, 0.8);
  border-radius: 10px;
  overflow: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  margin: auto;
`;

const SuggestIngredientButton = styled(Button)`
  width: 300px;
  height: 30px;
`;
