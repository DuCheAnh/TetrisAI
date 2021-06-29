from model import Field
import copy


def rotate_clockwise(shape):
    return [[shape[y][x] for y in range(len(shape))] for x in range(len(shape[0]) - 1, -1, -1)]


class Ai:
    @staticmethod
    def best(field, workingPieces, workingPieceIndex, weights, undo_level):
        bestRotation = bestOffset = bestScore = None
        workingPieceIndex = copy.deepcopy(workingPieceIndex)
        workingPiece = workingPieces[workingPieceIndex]
        shapes_rotation = {4: 4, 8: 2, 12: 2, 16: 4, 20: 4, 24: 2, 28: 1}
        flattended_piece = [val for sublist in workingPiece for val in sublist]
        hashedPiece = sum(flattended_piece)

        for rotation in range(0, shapes_rotation[hashedPiece]):
            for offset in range(0, field.width):
                result = field.projectPieceDown(workingPiece, offset, undo_level)
                if not result is None:
                    score = None
                    if workingPieceIndex == len(workingPieces) - 1:
                        heuristics = field.heuristics()
                        score = sum([a * b for a, b in zip(heuristics, weights)])
                    else:
                        _, _, score = Ai.best(field, workingPieces, workingPieceIndex + 1, weights, 2)
                    if bestScore is None or score > bestScore:
                        bestScore = score
                        bestOffset = offset
                        bestRotation = rotation
                field.undo(undo_level)
            workingPiece = rotate_clockwise(workingPiece)
        return bestOffset, bestRotation, bestScore

    @staticmethod
    def choose(initialField, piece, next_piece, offsetX, weights, parent, do_forseen):
        field = Field(len(initialField[0]), len(initialField))
        field.updateField(copy.deepcopy(initialField))

        if do_forseen:
            pieces_set = [piece, next_piece]
        else:
            pieces_set = [piece]
        offset, rotation, _ = Ai.best(field, pieces_set, 0, weights, 1)
        moves = []

        offset = offset - offsetX
        for _ in range(0, rotation):
            moves.append("UP")
        for _ in range(0, abs(offset)):
            if offset > 0:
                moves.append("RIGHT")
            else:
                moves.append("LEFT")
        # moves.append('RETURN')
        parent.executes_moves(moves)
        # return moves
