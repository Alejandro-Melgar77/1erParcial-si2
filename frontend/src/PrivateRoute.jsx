import { useContext } from "react";
import { Navigate } from "react-router-dom";
import { AuthContext } from "./context/AuthContext";

export default function PrivateRoute({ children, allowedRoles }) {
  const { user } = useContext(AuthContext);

  // No logueado → redirige a login
  if (!user) {
    return <Navigate to="/login" />;
  }

  // Si hay roles permitidos y el rol del usuario no está incluido → redirige
  if (allowedRoles && user.role && !allowedRoles.includes(user.role)) {
    return <Navigate to="/dashboard" />;
  }

  return children;
}
// Si está logueado y tiene permiso → renderiza el componente
// Si está logueado pero no tiene permiso → redirige al dashboard normal
// Si no está logueado → redirige a login