import { useState, useEffect } from "react";
import ReactMarkdown from 'react-markdown'
import styles from './TutorialPage.module.css'
import { NavBar } from "../components/NavBar";

export default function TutorialPage() {
    const [content, setContent] = useState('')
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        fetch('/rules.md')
        .then(res => res.text())
        .then(text => {
            setContent(text)
            setLoading(false)
        })
    }, [])

    return (
        <>
            <NavBar/>
            <div className={styles.page}>
                <div className={styles.card}>
                    {loading ? 
                    <p className={styles.loading}>Loading...</p> : 
                    <ReactMarkdown className={styles.markdown}> 
                        {content} 
                    </ReactMarkdown>}
                </div>
            </div>
        </>
    )
}