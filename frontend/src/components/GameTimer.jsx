import { useState, useEffect, useRef } from 'react'
import styles from './GameTimer.module.css'

function formatTime(seconds) {
    if (seconds === null) return '--:--'
    const s = Math.max(0, Math.floor(seconds))
    const m = Math.floor(s/60)
    const ss = s % 60
    return `${m}:${ss.toString().padStart(2, '0')}`
}

export function GameTimer({ serverTime, label, active }) {
    const [display, setDisplay] = useState(serverTime)
    const intervalRef = useRef(null)
    const lastTickRef = useRef(null)

    useEffect(() => {
        setDisplay(serverTime)
    }, [serverTime])

    useEffect(() => {
        if (!active) {
            clearInterval(intervalRef.current)
            return
        }

        lastTickRef.current = Date.now()
        intervalRef.current = setInterval(() => {
            const now = Date.now()
            const elapsed = (now - lastTickRef.current) / 1000
            lastTickRef.current = now
            setDisplay(prev => (prev == null ? prev : Math.max(0, prev - elapsed)))
        }, 100)

        return () => clearInterval(intervalRef.current)
    }, [active])

    const seconds = display != null ? Math.floor(display) : null
    const isLow = seconds != null && seconds <= 30
    const isCritical = seconds != null && seconds <= 10

    return (
        <div className={`${styles.timer} ${active ? styles.timerActive : ''} ${isLow ? styles.timerLow : ''} ${isCritical ? styles.timerCritical : ''}`}>
            <span className={styles.timerLabel}>{label}</span>
            <span className={styles.timerValue}>{formatTime(display)}</span>
        </div>
    )
}
