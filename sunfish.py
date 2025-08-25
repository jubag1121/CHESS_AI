import streamlit as st
import chess
import chess.svg
import base64

# --- 역할 및 설명 ---
# 이 앱은 Streamlit과 'python-chess' 라이브러리를 사용하여 두 명의 플레이어가
# 로컬에서 체스 게임을 즐길 수 있도록 합니다.
# ---

# --- 페이지 설정 ---
st.set_page_config(page_title="2인용 체스 게임", page_icon="♟️")

# --- 오디오 재생을 위한 함수 ---
def play_move_sound():
    """말을 움직일 때 효과음을 재생하는 함수"""
    wav_file_base64 = "UklGRigAAABXQVZFZm1 disposizioneBAAAAABAAEARKwAAIhYAQACABAAZGF0YQQAAAAA"
    wav_bytes = base64.b64decode(wav_file_base64)
    st.audio(wav_bytes, format='audio/wav', autoplay=True)

# --- 세션 상태 초기화 ---
def initialize_game():
    """게임 상태를 관리하는 세션 변수를 초기화합니다."""
    # 'python-chess' 라이브러리의 Board 객체를 사용합니다.
    if 'board' not in st.session_state:
        st.session_state.board = chess.Board() # sunfish.Board()가 아닌 chess.Board() 사용
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False

# --- 메인 앱 로직 ---
def main():
    st.title("2인용 체스 게임 ♟️")

    initialize_game()

    turn_text = "백(WHITE)" if st.session_state.board.turn == chess.WHITE else "흑(BLACK)"
    st.subheader(f"현재 턴: {turn_text}")

    last_move = st.session_state.board.peek() if st.session_state.board.move_stack else None
    board_svg = chess.svg.board(
        board=st.session_state.board,
        lastmove=last_move
    ).encode("UTF-8")
    
    st.image(board_svg)

    if not st.session_state.game_over:
        move_uci = st.text_input("당신의 수를 입력하세요 (예: e2e4):", key="player_move").strip()

        if move_uci:
            try:
                move = chess.Move.from_uci(move_uci)
                if move in st.session_state.board.legal_moves:
                    st.session_state.board.push(move)
                    play_move_sound()
                    st.rerun()
                else:
                    st.warning("둘 수 없는 위치입니다. 다시 시도해주세요.")
            except ValueError:
                st.warning("잘못된 형식입니다. UCI 표기법(예: e2e4)으로 입력해주세요.")

    if st.session_state.board.is_game_over():
        st.session_state.game_over = True
        outcome = st.session_state.board.outcome()
        
        if outcome.winner is True:
            result = "🎉 체크메이트! 백(WHITE)이 이겼습니다!"
        elif outcome.winner is False:
            result = "🎉 체크메이트! 흑(BLACK)이 이겼습니다!"
        else:
            result = "🤝 무승부입니다!"
        
        st.success(result)

    if st.button("새 게임 시작"):
        st.session_state.board = chess.Board()
        st.session_state.game_over = False
        st.rerun()

if __name__ == "__main__":
    main()