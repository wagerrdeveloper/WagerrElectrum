import sys

BTX_HEX_PREFIX = "42"
PB_OP_STRLEN = 16

class PeerlessBet:
    def __init__(self, eventId, outcomeType):
        if eventId is None:
            raise Exception('Empty Event Id')
        self.eventId = eventId
        if outcomeType is None:
            raise Exception('Empty Outcome Type')
        self.outcomeType = outcomeType

    @staticmethod
    #def ToOpCode(pb, opCode: str) -> bool :
    def ToOpCode(pb):
        eventId = hex(pb.eventId).lstrip("0x").zfill(8)
        print('Event Id hex : ', eventId)
        outcomeType = hex(pb.outcomeType).lstrip("0x").zfill(2)
        print('outcome hex: ',outcomeType)
        opCode = BTX_HEX_PREFIX + "0103" + eventId + outcomeType
        print('opCode: ',opCode)
        print('opCode len: ',len(opCode))
        #Ensure peerless bet OpCode string is the correct length.
        if len(opCode) != PB_OP_STRLEN :
            return False,opCode
        return True,opCode

    @staticmethod
    def FromOpCode(opCode: str, pb) -> bool :
        raise Exception('Not implemented')