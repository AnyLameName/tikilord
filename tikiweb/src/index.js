import React from 'react';
import ReactDOM from 'react-dom/client';
import {
  createBrowserRouter,
  RouterProvider,
} from 'react-router-dom';
import './index.css';
import Leaderboard from './components/leaderboard';
import TopChart from './components/top-chart';
import Root from './components/root';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Root />,
    children: [
      {
        path: '/table/',
        element: <Leaderboard />,
      },
      {
        path: '/chart/',
        element: <TopChart />,
      },
    ],
  },
]);

const root = ReactDOM.createRoot(document.getElementById('root'))
root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
