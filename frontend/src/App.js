import React, { useState, useEffect } from 'react'

function App() {

  const [data, setData] = useState([{}])

  useEffect(() => {
    fetch("/api/hello").then(
      res => res.json()
    ).then(
      data => {
        setData(data)
        console.log(data)
      }
    )
  }, [])

  return (
    <div>

      {(typeof data.name === 'undefined') ? (
        <p>Loading...</p>
      ): (
        <><p>{data.name}</p><p>{data.response}</p></>
      )}

    </div>
  )
}

export default App