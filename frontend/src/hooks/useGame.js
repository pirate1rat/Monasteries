import { useState, useEffect, useRef, useCallback } from 'react'
import { PIECE_CATALOG } from '../data/pieceCatalog'
import { getSocket } from '../services/socket'

const socket = getSocket()

function buildPieceList(piecesFromServer) {
    if(!piecesFromServer) return []

    return Object.entries(piecesFromServer)
        .filter(([, qty]) => qty > 0)
        .map(([id, qty]) => ({
            piece_id: Number(id),
            quantity: qty,
            ...(PIECE_CATALOG[Number(id)] ?? { name: '?', cells: [[0, 0]], color: 'neutral'})
        }))
}

function buildBoard(boardFromServer){
    if(!boardFromServer) return Array(100).fill(null)
    return boardFromServer.grid.flat()
}

export function useGame(gameId) {
    //game state
    const [board, setBoard] = useState(Array(100).fill(null))
    const [playerPieces, setPlayerPieces] = useState([])
    const [oppPieces, setOppPieces] = useState([])
    const [playerColor, setPlayerColor] = useState(null)   // 'white'/'red'
    const [currentTurn, setCurrentTurn] = useState(null)
    const [playerTime, setPlayerTime] = useState(null)
    const [oppTime, setOppTime] = useState(null)
    const [history, setHistory] = useState([])
    const [status, setStatus] = useState('in_progress')
    const [result, setResult] = useState(null)
    const [drawOffered, setDrawOffered] = useState(false)
    const [oppDisconnected, setOppDisconnected] = useState(false)
    const [reconnectTimer, setReconnectTimer] = useState(null)
    const [error, setError] = useState(null)
    const [connected, setConnected] = useState(false)

    //piece and rotation
    const [selectedPiece, setSelectedPiece] = useState(null)
    const [selectedRotation, setSelectedRotation] = useState(0)

    const gameIdRef = useRef(gameId)
    const playerColorRef = useRef(null)

    function updatePieces(whitePieces, redPieces, color) {
        const myColor = color ?? playerColorRef.current
        if (myColor === 'white') {
            setPlayerPieces(buildPieceList(whitePieces))
            setOppPieces(buildPieceList(redPieces))
        } else {
            setPlayerPieces(buildPieceList(redPieces))
            setOppPieces(buildPieceList(whitePieces))
        }
    }

    useEffect(() => {
        socket.emit('join_game', { game_id: gameId })

        socket.on('connect', () => setConnected(true))
        socket.on('disconnect', () => setConnected(false))

        socket.on('game_state', (data) => {
            console.log(data)
            setBoard(buildBoard(data.board))
            setPlayerColor(data.player_color)
            playerColorRef.current = data.player_color
            setCurrentTurn(data.current_turn)
            setPlayerTime(data.player_time)
            setOppTime(data.opponent_time)
            setStatus(data.status)
            setResult(data.result)
            updatePieces(data.white_pieces, data.red_pieces, data.player_color)
            if (data.draw_offered_by != null 
                && data.draw_offered_by !== playerColorRef.current) {
                setDrawOffered(true)
            } else {
                setDrawOffered(false)
            }
        })

        socket.on('move_made', (data) => {
            setBoard(buildBoard(data.board))
            setCurrentTurn(data.current_turn)
            
            const myColor = playerColorRef.current
            setPlayerTime(myColor === 'white' ? data.white_time : data.red_time)
            setOppTime(myColor === 'white' ? data.red_time : data.white_time)
            
            updatePieces(data.white_pieces, data.red_pieces, null)

            setHistory(prev => [...prev, {
                move: prev.length + 1,
                player: data.move_player,
                action: data.move_notation
            }])
            setSelectedPiece(null)
            setSelectedRotation(0)
        })

        socket.on('game_over', (data) => {
            setStatus('finished')
            setResult(data.result)
        })

        socket.on('draw_proposed', (data) => {
            if (data.by !== playerColorRef.current) {
                setDrawOffered(true)
            }
        })
        socket.on('draw_rejected', () => setDrawOffered(false))

        socket.on('opponent_disconnected', (data) => {
            setOppDisconnected(true)
            setReconnectTimer(data.reconnect_time_left)
        })

        socket.on('opponent_reconnected', () => {
            setOppDisconnected(false)
            setReconnectTimer(null)
        })

        socket.on('error', (data) => setError(data.message))
        //console.log("pieces of players: ", playerPieces, oppPieces)
        return () => {
            socket.off('game_state')
            socket.off('move_made')
            socket.off('game_over')
            socket.off('draw_proposed')
            socket.off('draw_rejected')
            socket.off('opponent_disconnected')
            socket.off('opponent_reconnected')
            socket.off('error')
        }
    }, [gameId])

    const makeMove = useCallback((pieceId, anchor, rotation) => {
        socket.emit('make_move', {
            game_id: gameIdRef.current,
            piece_id: pieceId,
            anchor,
            rotation
        })
    }, [])

    const resign = useCallback(() => {
        socket.emit('resign', {game_id : gameIdRef.current})
    }, [])

    const proposeDraw = useCallback(() => {
        socket.emit('propose_draw', { game_id: gameIdRef.current })
    }, [])

    const acceptDraw = useCallback(() => {
        socket.emit('accept_draw', { game_id: gameIdRef.current })
        setDrawOffered(false)
    }, [])

    const rejectDraw = useCallback(() => {
        socket.emit('reject_draw', { game_id: gameIdRef.current })
        setDrawOffered(false)
    }, [])
    
    //piece selection
    const selectPiece = useCallback((pieceId) => {
        setSelectedPiece(prev => prev === pieceId ? null : pieceId)
        setSelectedRotation(0)
    }, [])

    const selectRotation = useCallback(() => {
        setSelectedRotation(prev => (prev + 1) % 4)
    }, [])

    const isPlayerTurn = playerColor === currentTurn && status === 'in_progress'

    return {
        // board state
        board,
        playerPieces,
        oppPieces,
        playerColor,
        currentTurn,
        isPlayerTurn,

        // timers
        playerTime,
        oppTime,

        // history and status
        history,
        status,
        result,

        // interactions
        drawOffered,
        oppDisconnected,
        reconnectTimer,

        //
        connected,
        error,

        // piece selection (UI)
        selectedPiece,
        selectedRotation,
        selectPiece,
        selectRotation,

        // actions
        makeMove,
        resign,
        proposeDraw,
        acceptDraw,
        rejectDraw,
    }
}