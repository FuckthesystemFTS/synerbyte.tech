import React from 'react'
import { createRoot } from 'react-dom/client'
import App from './pages/App'
import Expired from './pages/Expired'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'

const router = createBrowserRouter([
  { path: '/', element: <App /> },
  { path: '/expired', element: <Expired /> }
])

const container = document.getElementById('root')!
createRoot(container).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
)