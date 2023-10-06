import React from 'react';
import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

// MUI components
import { createTheme, ThemeProvider } from '@mui/material/styles';

// Own components
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import ProfilePage from './pages/ProfilePage';
import PasswordChangePage from './pages/PasswordChangePage';
import OwnRecipePage from './pages/OwnRecipePage';
import FavoritesPage from './pages/FavoritesPage';
import CreateRecipePage from './pages/CreateRecipePage';
import RecipeDetailPage from './pages/RecipeDetailPage';
import PersonalDetailPage from './pages/PersonalDetailPage';
import AnalysisPage from './pages/AnalysisPage';

const theme = createTheme({
  palette: {
    primary: {
      main: '#0739EA'
    },
    secondary: {
      main: '#E16666',
      contrastText: '#ffffff'
    },
    last: {
      main: '#6AE3B8',
      dark: '#326D58',
      contrastText: '#ffffff'
    },
    paper: {
      main: '#c1c1c1',
      contrastText: '#d7000f'
    },
  }
});

function App () {
  return (
    <ThemeProvider theme={theme}>
      <BrowserRouter>
        <Routes>
          <Route path='/' element={<HomePage />} />
          <Route path='/login' element={<LoginPage />} />
          <Route path='/register' element={<RegisterPage />} />
          <Route path='/dashboard/:email' element={<DashboardPage />} />
          <Route path='/profile/:email' element={<ProfilePage />} />
          <Route path='/profile/:email/change-password' element={<PasswordChangePage />} />
          <Route path='/profile/:email/own-recipes' element={<OwnRecipePage />} />
          <Route path='/profile/:email/favorites' element={<FavoritesPage />} />
          <Route path='/:email/recipe/create' element={<CreateRecipePage />} />
          <Route path='/recipe/:recipeId' element={<RecipeDetailPage />} />
          <Route path='/personal-detail/:userID' element={<PersonalDetailPage />} />
          <Route path='/analysis' element={<AnalysisPage />} />
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;
