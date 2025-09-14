import { Link } from "react-router-dom";
import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";

export default function Navbar() {
  const { user, logout } = useContext(AuthContext);

  return (
    <nav style={{ padding: "10px", backgroundColor: "#282c34", color: "white" }}>
      <Link to="/" style={{ margin: "0 10px", color: "white" }}>Inicio</Link>
      {!user && <Link to="/register" style={{ margin: "0 10px", color: "white" }}>Registro</Link>}
      {!user && <Link to="/login" style={{ margin: "0 10px", color: "white" }}>Login</Link>}
      {user && <Link to="/dashboard" style={{ margin: "0 10px", color: "white" }}>Dashboard</Link>}
      {user && (
        <button onClick={logout} style={{ marginLeft: "20px", padding: "5px 10px" }}>
          Cerrar sesión
        </button>
      )}
    </nav>
  );
}
