import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { Home } from './pages/Home/Home';
import { GetRequest } from './pages/GetRequest/GetRequest';
import { RepairRequest } from './pages/RepairRequest/RepairRequest';
import { Login } from './pages/Login/Login';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Home />,
  },
  {
    path: '/login',
    element: <Login />,
  },
  {
    path: '/get/:id',
    element: <GetRequest />,
  },
  {
    path: '/repair/:id',
    element: <RepairRequest />,
  },
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
