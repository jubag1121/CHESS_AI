import streamlit as st
import chess
import sunfish # Sunfish 라이브러리 임포트

# Streamlit 앱 제목 설정
st.title("AI와 체스를 즐겨보세요 (Sunfish 엔진)")

# --- 세션 상태를 이용해 게임 상태 관리 ---
if "board" not in st.session_state:
    st.session_state.board = chess.Board()
    st.session_state.selected_square = None
    st.session_state.engine_board = sunfish.Board() # Sunfish용 보드 생성

# --- 체스판 그리기 및 클릭 이벤트 처리 ---
def draw_board(board):
    st.markdown("<style> .piece-button { background: none; border: none; padding: 0; margin: 0; font-size: 3em; cursor: pointer; } </style>", unsafe_allow_html=True)
    for rank in range(7, -1, -1):
        cols = st.columns(8)
        for file in range(8):
            square = chess.square(file, rank)
            piece = board.piece_at(square)
            piece_symbol = piece.unicode_symbol() if piece else ""
            with cols[file]:
                if st.button(piece_symbol, key=f"sq_{square}"):
                    handle_square_click(square)
                    st.rerun()

def handle_square_click(square):
    if st.session_state.selected_square is None:
        if st.session_state.board.piece_at(square) is not None:
            st.session_state.selected_square = square
    else:
        start_square = st.session_state.selected_square
        end_square = square
        try:
            move = chess.Move(start_square, end_square)
            if move in st.session_state.board.legal_moves:
                st.session_state.board.push(move)
                # Sunfish 보드에도 수 적용
                st.session_state.engine_board.push(move)
            else:
                st.error("유효하지 않은 수입니다.")
        except:
            st.error("잘못된 수입니다.")
        st.session_state.selected_square = None

# --- 메인 게임 루프 ---
draw_board(st.session_state.board)

# --- AI 플레이어의 차례 ---
if st.session_state.board.turn == chess.BLACK and not st.session_state.board.is_game_over():
    st.info("AI가 수를 두는 중입니다...")
    
    # Sunfish가 최적의 수를 찾는 과정
    move_uci, _ = sunfish.search(st.session_state.engine_board, 3) # 탐색 깊이를 조절할 수 있습니다
    
    # AI의 수를 체스보드에 적용
    ai_move = chess.Move.from_uci(move_uci)
    st.session_state.board.push(ai_move)
    st.session_state.engine_board.push(ai_move)
    
    st.success(f"AI가 {ai_move.uci()} 수를 두었습니다.")
    st.rerun()

# --- 게임 상태 메시지 ---
if st.session_state.board.is_game_over():
    st.write("게임 종료")
    st.write(st.session_state.board.result())