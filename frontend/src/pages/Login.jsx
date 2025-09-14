import { useState, useContext } from "react";
import { login } from "../api";
import { AuthContext } from "../context/AuthContext";

export default function Login() {
  const { login: loginContext } = useContext(AuthContext);
  const [formData, setFormData] = useState({ username: "", password: "" });
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await login(formData);
      loginContext(res.data); // Guardar tokens en el contexto
      alert("Inicio de sesión exitoso");
    } catch (err) {
      setError("Usuario o contraseña incorrectos");
    }
  };

  return (
    <div>
      <h2>Iniciar Sesión</h2>
      {error && <p>{error}</p>}
      <form onSubmit={handleSubmit}>
        <input type="text" name="username" placeholder="Usuario" onChange={handleChange} required />
        <input type="password" name="password" placeholder="Contraseña" onChange={handleChange} required />
        <button type="submit">Entrar</button>
      </form>
    </div>
  );
}
