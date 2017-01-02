from field import Field
import copy

def rotate_clockwise(shape):
    return [ [ shape[y][x]
            for y in xrange(len(shape)) ]
        for x in xrange(len(shape[0]) - 1, -1, -1) ]


class Ai:

    @staticmethod
    def best(field, workingPieces, workingPieceIndex, weights, level):
        bestRotation = None
        bestOffset = None
        bestScore = None
        workingPieceIndex = copy.deepcopy(workingPieceIndex)
        workingPiece = workingPieces[workingPieceIndex]
        shapes_rotation = { 4 : 4, 8 : 2, 12 : 2, 16 : 4, 20 : 4, 24 : 2, 28 : 1 }
        flat_piece = [val for sublist in workingPiece for val in sublist]
        hashedPiece = sum(flat_piece)

        for rotation in range(0, shapes_rotation[hashedPiece]):
            for offset in range(0, field.width):
                result = field.projectPieceDown(workingPiece, offset, level)
                if not result is None:
                    score = None
                    if workingPieceIndex == len(workingPieces)-1 :
                        heuristics = field.heuristics()
                        score = sum([a*b for a,b in zip(heuristics, weights)])
                    else:
                        _, _, score = Ai.best(field, workingPieces, workingPieceIndex + 1, weights, 2)

                    if score > bestScore or bestScore is None:
                        bestScore = score
                        bestOffset = offset
                        bestRotation = rotation
                field.undo(level)
            workingPiece = rotate_clockwise(workingPiece)

        return bestOffset, bestRotation, bestScore

    #def choose(initialField, piece, next_piece, offsetX, weights):
    @staticmethod
    def choose(initialField, piece, next_piece, offsetX, weights, parent):
        field = Field(len(initialField[0]), len(initialField))
        field.updateField(copy.deepcopy(initialField))

        offset, rotation, _ = Ai.best(field, [piece, next_piece], 0, weights, 1)
        moves = []

        offset = offset - offsetX
        for _ in range(0, rotation):
            moves.append("UP")
        for _ in range(0, abs(offset)):
            if offset > 0:
                moves.append("RIGHT")
            else:
                moves.append("LEFT")
        moves.append('RETURN')
        parent.executes_moves(moves)
        #return moves

    #
    #
    # @staticmethod
    # def choose2(field, piece, next_piece, offsetX, weights):
    #     bestScore = -float("inf")
    #     offset = 0
    #     rotation = 0
    #     scores = []
    #     fieldObj = Field(len(field[0]), len(field))
    #     initialField = field
    #
    #     for i in range(0, 4):
    #         for x in range(0, fieldObj.width):
    #             fieldObj.updateField(initialField)
    #             field = fieldObj.projectPieceDown(piece, x)
    #             if not field is None:
    #                 fieldObj.updateField(field)
    #                 heuritics = fieldObj.heuristics()
    #                 result = sum([a*b for a,b in zip(heuritics, weights)])
    #                 scores.append(result)
    #                 #print(result)
    #                 if result > bestScore:
    #                     bestScore = result
    #                     offset = x
    #                     rotation = i
    #         piece = rotate_clockwise(piece)
    #
    #     moves = []
    #     offset = offset - offsetX
    #     for _ in range(0, rotation):
    #         moves.append("UP")
    #     for _ in range(0, abs(offset)):
    #         if offset > 0:
    #             moves.append("RIGHT")
    #         else:
    #             moves.append("LEFT")
    #     moves.append('RETURN')
    #
    #     # print("")
    #     # print("")
    #     # for line in initialField:
    #     #     print(line)
    #     # print("")
    #     # print(scores)
    #
    #     return moves
    #
    # @staticmethod
    # def hashList(field):
    #     result = ""
    #     for line in field:
    #         result += "".join([str(el) for el in line])
    #     return result
    #
    # @staticmethod
    # def generateFields(field, piece):
    #     piece = copy.deepcopy(piece)
    #     result = {}
    #     initialField = copy.deepcopy(field.field)
    #     fieldObj = Field(len(field.field[0]), len(field.field))
    #     flat_piece = [val for sublist in piece for val in sublist]
    #     shapes_rotation = { 4 : 4, 8 : 2, 12 : 2, 16 : 4, 20 : 4, 24 : 2, 28 : 1 }
    #     hashedField = Ai.hashList(initialField)
    #     hashedPiece = sum(flat_piece)
    #
    #     # fields = Ai.cache.get(hashedField + str(hashedPiece), None)
    #     # if not fields is None:
    #     #     return fields
    #
    #     for rotation in range(0,shapes_rotation[hashedPiece]):
    #         for offset in range(0, fieldObj.width):
    #             fieldObj.updateField(initialField)
    #             field = fieldObj.projectPieceDown(piece, offset)
    #             if not field is None:
    #                 fieldObj.updateField(field)
    #                 result[(rotation, offset)] = copy.deepcopy(fieldObj)
    #         piece = rotate_clockwise(piece)
    #     #
    #     # Ai.cache[hashedField + str(hashedPiece)] = result
    #     return result
    #
    # @staticmethod
    # def choose3(fieldOrigin, piece, next_piece, offsetX, weights):
    #     fieldObj = Field(len(fieldOrigin[0]), len(fieldOrigin))
    #     fieldObj.updateField(fieldOrigin)
    #     bestScore = -float("inf")
    #     offset = 0
    #     rotation = 0
    #     fields = Ai.generateFields(fieldObj, piece)
    #     for key, field in fields.iteritems():
    #         subfields = Ai.generateFields(field, next_piece)
    #         for _, subfield in subfields.iteritems():
    #             heuristics = field.heuristics()
    #             result = sum([a*b for a,b in zip(heuristics, weights)])
    #             if result > bestScore:
    #                 bestScore = result
    #                 rotation = key[0]
    #                 offset = key[1]
    #
    #     moves = []
    #     #print(scores)
    #     offset = offset - offsetX
    #     for _ in range(0, rotation):
    #         moves.append("UP")
    #     for _ in range(0, abs(offset)):
    #         if offset > 0:
    #             moves.append("RIGHT")
    #         else:
    #             moves.append("LEFT")
    #     moves.append('RETURN')
    #     #print(moves)
    #     # print("")
    #     # print("")
    #     # for line in initialField:
    #     #     print(line)
    #     # print("")
    #     # print(scores)
    #
    #     return moves
    #
    # # @staticmethod
    # # def choose(field, piece, next_piece, offsetX, weights):
    # #     shapes_rotation = { 4 : 4, 8 : 2, 12 : 2, 16 : 4, 20 : 4, 24 : 2, 28 : 1 }
    # #     bestScore = -float("inf")
    # #     offset = 0
    # #     rotation = 0
    # #     scores = []
    # #     fieldObj = Field(len(field[0]), len(field))
    # #     initialField = field
    # #     flat_piece = [val for sublist in piece for val in sublist]
    # #     flat_next_piece = [val for sublist in next_piece for val in sublist]
    # #     counter = 0
    # #     for i1 in range(0, shapes_rotation[sum(flat_piece)]):
    # #         for x1 in range(0, fieldObj.width):
    # #             fieldObj.updateField(initialField)
    # #             field = fieldObj.projectPieceDown(piece, x1)
    # #             if not field is None:
    # #                 fieldObj.updateField(field)
    # #                 for i2 in range(0, shapes_rotation[sum(flat_next_piece)]):
    # #                     for x2 in range(0, fieldObj.width):
    # #                         field = fieldObj.projectPieceDown(next_piece, x2)
    # #                         if not field is None:
    # #                             fieldObj.updateField(field)
    # #                             heuritics = fieldObj.heuristics()
    # #                             #heuritics = [1,1,1,1,1,1,1,1]
    # #                             result = sum([a*b for a,b in zip(heuritics, weights)])
    # #                             scores.append(result)
    # #                             if result > bestScore:
    # #                                 bestScore = result
    # #                                 offset = x1
    # #                                 rotation = i1
    # #                     next_piece = rotate_clockwise(next_piece)
    # #         piece = rotate_clockwise(piece)
    # #     moves = []
    # #     #print(scores)
    # #     offset = offset - offsetX
    # #     #print "rotation => ", rotation, " | offset => ", offset
    # #     for _ in range(0, rotation):
    # #         moves.append("UP")
    # #     for _ in range(0, abs(offset)):
    # #         if offset > 0:
    # #             moves.append("RIGHT")
    # #         else:
    # #             moves.append("LEFT")
    # #     moves.append('RETURN')
    # #     #print(moves)
    # #     # print("")
    # #     # print("")
    # #     # for line in initialField:
    # #     #     print(line)
    # #     # print("")
    # #     # print(scores)
    # #
    # #     return moves
