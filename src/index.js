import React from 'react';
import ReactDOM from 'react-dom/client';
import {
  createBrowserRouter,
  RouterProvider,
} from 'react-router-dom';
import './index.css';
import Leaderboard from './components/leaderboard';
import TopChart from './components/top-chart';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Leaderboard />,
  },
  {
    path: '/region/:region/top/:playerCount/',
    element: <Leaderboard />,
  },
  {
    path: '/region/:region/top/:playerCount/chart/',
    element: <TopChart />,
  }
]);

const root = ReactDOM.createRoot(document.getElementById('root'))
root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
