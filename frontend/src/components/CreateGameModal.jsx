import { useState } from 'react'
import styles from './CreateGameModal.module.css'

const TIME_PRESETS = [
    { label: '3 min', base: 180, increment: 0 },
    { label: '5 min', base: 300, increment: 0 },
    { label: '10 min + 5 s', base: 600, increment: 5 },
    { label: '15 min + 10 s', base: 900, increment: 10 },
    { label: 'Custom', base: null, increment: null },
]

export default function CreateGameModal({ onClose }) {
    const [color, setColor] = useState('random')
    const [preset, setPreset] = useState(0)
    const [customMin, setCustomMin] = useState(10)
    const [customInc, setCustomInc] = useState(0)

    const isCustom = TIME_PRESETS[preset].base === null

    function handleCreate() {
        const timeControl = isCustom 
        ? { base: customMins * 60, increment: customInc }
        : { base: TIME_PRESETS[preset].base, increment: TIME_PRESETS[preset].increment}

        console.log('Tworzę lobby:', { color, timeControl })
        // TODO: POST /lobbies
        onClose()
    }

    return (
        <div className={styles.overlay} on onClick={onClose}>
            <div className={styles.modal} onClick={e => e.stopPropagation()}>
                <div className={styles.header}>
                    <h3>New game</h3>
                    <button className={styles.close} onClick={onClose}>✕</button>
                </div>

                <div className={styles.section}>
                    <label className={styles.label}>Your color</label>
                    <div className={styles.colorPicker}>
                        {
                            [{ value: 'white',  label: 'White'   },
                            { value: 'random', label: 'Random'  },
                            { value: 'red',    label: 'Red'}].map(opt => (
                                <button 
                                key={opt.value} className={`${styles.colorBtn} ${color === opt.value ? styles.colorBtnActive : ''}`}
                                onClick={() => setColor(opt.value)}>
                                    {opt.label}
                                </button>
                            ))
                        }
                    </div>
                </div>

                <div className={styles.section}>
                    <label className={styles.label}>Game tempo</label>
                    <div className={styles.presets}>
                        {TIME_PRESETS.map((p, i) => (
                            <button key={i} className={`${styles.presetBtn} ${preset === i ? styles.presetBtnActive : ''}`}
                            onClick={() => setPreset(i)}>
                                {p.label}
                            </button>
                        ))}
                    </div>

                    {isCustom && (
                        <div className={styles.custom}>
                            <div className={styles.customField}>
                                <label>Time (minutes)</label>
                                <input 
                                type='number' 
                                min='1' max='60' 
                                value={customMin} 
                                onChange={e => setCustomMin(Number(e.target.value))}
                                />
                            </div>
                            <div className={styles.customField}>
                                <label>Increment (seconds)</label>
                                <input 
                                type='number' 
                                min='0' max='60' 
                                value={customInc} 
                                onChange={e => setCustomInc(Number(e.target.value))}
                                />
                            </div>
                        </div>
                    )}
                </div>

                <button className={styles.createBtn} onClick={handleCreate}>
                    Create game
                </button>
            </div>
        </div>
    )
}

