import React, { useState } from 'react'
import axios from 'axios'

export default function Login({ setToken }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  const handleLogin = async () => {
    try {
      const res = await axios.post('http://localhost:5000/login', {
        username,
        password
      })
      localStorage.setItem('token', res.data.token)
      setToken(res.data.token)
    } catch (err) {
      alert("Error en inicio de sesión")
    }
  }

  return (
    <div>
      <h2>Iniciar Sesión</h2>
      <input placeholder="Usuario" onChange={(e) => setUsername(e.target.value)} />
      <input type="password" placeholder="Contraseña" onChange={(e) => setPassword(e.target.value)} />
      <button onClick={handleLogin}>Ingresar</button>
    </div>
  )
}
