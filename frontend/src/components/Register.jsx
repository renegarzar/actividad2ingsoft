import React, { useState } from 'react'
import axios from 'axios'

export default function Register() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  const handleRegister = async () => {
    try {
      await axios.post('/register', { username, password })
      alert('Usuario registrado con éxito')
    } catch (err) {
      alert('Error al registrar usuario')
    }
  }

  return (
    <div>
      <h2>Registro</h2>
      <input type="text" placeholder="Usuario" onChange={e => setUsername(e.target.value)} />
      <input type="password" placeholder="Contraseña" onChange={e => setPassword(e.target.value)} />
      <button onClick={handleRegister}>Registrarse</button>
    </div>
  )
}
