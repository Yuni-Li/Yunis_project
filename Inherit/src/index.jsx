import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import {
  createBrowserRouter,
  RouterProvider,
} from 'react-router-dom';

import HomePage from './pages/homePage';
import Events from './pages/events';
import Project from './pages/project';
import Relate from './pages/relate';
import User from './pages/user';

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      {
        path: 'home',
        element: <HomePage />,
      },
      {
        path: 'project',
        element: <Project />,
      },
      {
        path: 'user',
        element: <User />,
      },
      {
        path: 'events',
        element: <Events />,
      },
      {
        path: 'relate',
        element: <Relate />,
      },
    ]
  },
]);

ReactDOM.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
  document.getElementById('root'),
);
