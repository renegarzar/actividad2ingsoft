import React, { useState, useEffect } from 'react'
import axios from 'axios'

export default function Books({ token }) {
  const [books, setBooks] = useState([])
  const [title, setTitle] = useState('')
  const [author, setAuthor] = useState('')

  useEffect(() => {
    fetchBooks()
  }, [])

  const fetchBooks = async () => {
    const res = await axios.get('http://localhost:5000/books', {
      headers: { 'x-access-token': token }
    })
    setBooks(res.data.books)
  }

  const addBook = async () => {
    await axios.post('http://localhost:5000/books', { title, author }, {
      headers: { 'x-access-token': token }
    })
    fetchBooks()
  }

  return (
    <div>
      <h2>Mis libros</h2>
      <ul>
        {books.map((book, idx) => (
          <li key={idx}>{book.title} por {book.author}</li>
        ))}
      </ul>
      <input placeholder="Título" onChange={e => setTitle(e.target.value)} />
      <input placeholder="Autor" onChange={e => setAuthor(e.target.value)} />
      <button onClick={addBook}>Agregar Libro</button>
    </div>
  )
}
