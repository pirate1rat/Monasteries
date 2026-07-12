import { useEffect, useState } from 'react'

function App() {
    const [message, setMessage] = useState('Loading')

    useEffect(() => {
        fetch('http://127.0.0.1:5000/')
        .then(res => res.json())
        .then(data => setMessage(data.message))
        .catch(err => {
            console.error('Error while fetching data', err)
            setMessage("Couldn't connect with beckend")
        })
    }, [])

    return (
        <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
            <h1>Flask + React</h1>
            <p>Reply from backend: <strong>{message}</strong></p>
        </div>
    )
}

export default App