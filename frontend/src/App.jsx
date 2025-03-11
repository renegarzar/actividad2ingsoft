import { useState } from 'react';
import Login from './components/Login';
import Register from './components/Register';
import Books from './components/Books';

export default function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
  };

  return (
    <div>
      <nav>
        {!token ? (
          <>
            <a href="/">Login</a> | <a href="/">Registro</a>
          </>
        ) : (
          <button onClick={handleLogout}>Cerrar sesión</button>
        )}
      </nav>

      {!token ? (
        <>
          <Login setToken={setToken} />
          <Register />
        </>
      ) : (
        <Books token={token} />
      )}
    </div>
  );
};
