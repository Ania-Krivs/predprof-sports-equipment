import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { Home } from "./pages/Home/Home";
import { GetRequest } from "./pages/GetRequest/GetRequest";
import { RepairRequest } from "./pages/RepairRequest/RepairRequest";
import { Login } from "./pages/Login/Login";
import { Admin } from "./pages/Admin/Admin";
import { CreateInventory } from './pages/CreateInventory/CreateInventory';
import { EditInventory } from './pages/EditInventory/EditInventory';

const router = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
  },
  {
    path: "/login",
    element: <Login />,
  },
  {
    path: "/get/:id",
    element: <GetRequest />,
  },
  {
    path: "/repair/:id",
    element: <RepairRequest />,
  },
  {
    path: "/admin",
    element: <Admin />,
  },
  {
    path: "/admin/create",
    element: <CreateInventory />,
  },
  {
    path: "/admin/edit/:id",
    element: <EditInventory />,
  },
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
