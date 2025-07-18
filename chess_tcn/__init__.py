import io
import chess
import chess.pgn

ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!?{~}(^)[_]@#$,./&-*++="
PROMO_PIECES = "qnrbkp"
PIECE_MAP = {
    chess.QUEEN: "q",
    chess.ROOK: "r",
    chess.BISHOP: "b",
    chess.KNIGHT: "n",
    chess.KING: "k",
    chess.PAWN: "p"
}


def square_to_index(square: str) -> int:
    """
    Convert a board square (e.g. "e4") into a 0-63 index.
    """
    file = ord(square[0]) - ord("a")    # 0-7
    rank = int(square[1]) - 1           # 0-7
    return file + rank * 8


def index_to_square(idx: int) -> str:
    """
    Convert a 0-63 index into a board square (e.g. "e4").
    """
    file = idx % 8
    rank = idx // 8 + 1
    file_char = ALPHABET[file]
    return f"{file_char}{rank}"


def decode_tcn(tcn: str) -> list[dict]:
    """
    Decode a TCN-encoded string into a list of move dicts.
    Each move dict may have keys: 'from', 'to', 'promotion', 'drop'.
    """
    moves = []
    for i in range(0, len(tcn), 2):
        code1 = ALPHABET.index(tcn[i])
        code2 = ALPHABET.index(tcn[i + 1])
        mv: dict = {}

        # promotions
        if code2 > 63:
            promo_index = (code2 - 64) // 3
            mv["promotion"] = PROMO_PIECES[promo_index]
            offset = ((code2 - 1) % 3) - 1
            direction = -8 if code1 < 16 else 8
            code2 = code1 + direction + offset

        # drops vs normal from-square
        if code1 > 75:
            drop_index = code1 - 79
            mv["drop"] = PROMO_PIECES[drop_index]
        else:
            mv["from"] = index_to_square(code1)

        # to-square always
        mv["to"] = index_to_square(code2)
        moves.append(mv)

    return moves


def encode_tcn(moves: list[dict] | dict) -> str:
    """
    Encode one or more move dicts into a TCN string.
    A move dict may have 'from', 'to', 'promotion', 'drop'.
    """
    if isinstance(moves, dict):
        moves = [moves]

    result = []
    for mv in moves:
        # from-index (drops start at 79)
        if mv.get("drop"):
            from_idx = 79 + PROMO_PIECES.index(mv["drop"])
        else:
            from_idx = square_to_index(mv["from"])

        # to-index
        to_idx = square_to_index(mv["to"])

        # promotion adjust
        if mv.get("promotion"):
            p_idx = PROMO_PIECES.index(mv["promotion"])
            if to_idx < from_idx:
                diff = 9 + to_idx - from_idx
            else:
                diff = to_idx - from_idx - 7
            to_idx = 3 * p_idx + 64 + diff

        result.append(ALPHABET[from_idx])
        result.append(ALPHABET[to_idx])

    return "".join(result)


def tcn_to_pgn(tcn: str) -> str:
    """
    Convert a full TCN string into a PGN move-text string.
    Raises ValueError if a decoded move is illegal or a drop occurs.
    """
    board = chess.Board()
    game = chess.pgn.Game()
    node = game

    for mv in decode_tcn(tcn):
        if mv.get("drop"):
            raise ValueError("Drop moves are not supported by python-chess")

        # build a UCI string, include promotion if present
        uci = mv["from"] + mv["to"] + (mv.get("promotion") or "")
        move = chess.Move.from_uci(uci)
        if move not in board.legal_moves:
            raise ValueError(f"Illegal move: {uci}")

        board.push(move)
        node = node.add_variation(move)

    exporter = chess.pgn.StringExporter(headers=False, variations=False, comments=False)
    return game.accept(exporter)


def pgn_to_tcn(pgn: str) -> str:
    """
    Convert a PGN move-text string into a TCN-encoded string.
    Raises ValueError if the PGN is invalid.
    """
    game = chess.pgn.read_game(io.StringIO(pgn))
    if game is None:
        raise ValueError("Failed to parse PGN")

    board = game.board()
    moves = []
    for move in game.mainline_moves():
        # record file/rank strings
        from_sq = index_to_square(move.from_square)
        to_sq = index_to_square(move.to_square)

        mv: dict = { "from": from_sq, "to": to_sq }
        if move.promotion:
            mv["promotion"] = PIECE_MAP[move.promotion]

        board.push(move)
        moves.append(mv)

    return encode_tcn(moves)
