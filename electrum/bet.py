import sys


BTX_HEX_PREFIX = "42"
PB_OP_STRLEN = 16  
plBetTxType="\x03"
BTX_FORMAT_VERSION="\x01" 

class PeerlessBet:
    def __init__(self, eventId, outcomeType):
        if eventId is None:
            raise Exception('Empty Event Id')
        self.eventId = eventId
        if outcomeType is None:
            raise Exception('Empty Outcome Type')
        self.outcomeType = outcomeType

    @staticmethod
    def ToOpCode(pb):
        eventId = hex(pb.eventId).lstrip("0x").zfill(8)
        outcomeType = hex(pb.outcomeType).lstrip("0x").zfill(2)
        opCode = BTX_HEX_PREFIX + "0103" + eventId + outcomeType
        #Ensure peerless bet OpCode string is the correct length.
        if len(opCode) != PB_OP_STRLEN :
            return False,opCode
        return True,opCode

    @staticmethod
    def FromOpCode(opCode) :
        #Ensure peerless bet OpCode string is the correct length.
        pb=PeerlessBet(0,0)
    #print(opCode)
        #print(len(opCode))
        if (len(opCode) != PB_OP_STRLEN / 2):
            # TODO - add proper error handling
            print("length mismatch")
       
            return False,pb
    

        if (opCode[2] != plBetTxType):
            # TODO - add proper error handling
            # print (opCode[2])
            # print(plBetTxType)
            print("type not matching")
            return False,pb
    

         #Ensure the peerless bet OpCode has the correct BTX format version number.
        if (PeerlessBet.ReadBTXFormatVersion(opCode) != BTX_FORMAT_VERSION):
            print("version not matching")
            
            return False,pb
            
    

        #eventId = FromChars(opCode[3], opCode[4], opCode[5], opCode[6])
        pb.eventId=int.from_bytes((opCode[3]+opCode[4]+opCode[5]+opCode[6]).encode('utf-8'), byteorder='big', signed=False)
        pb.outcomeType = int.from_bytes(opCode[7].encode('utf-8'), "big")
        #pb=PeerlessBet(eventId,outcomeType)

        # print("peventid:",pb.eventId)
        # print("outcometype:",pb.outcomeType)
        return True,pb

   
    def ReadBTXFormatVersion(opCode):

   #Check the first three bytes match the "BTX" format specification.
        if (opCode[0] != 'B'):
            return -1
        #print("opcode[1]:",opCode[1])
    #bb=bytes(opCode[1],'utf-8')
    #bb = opCode[1].encode('utf-8')
    #print("bb:",bb)
        bb=opCode[1]

        v = int.from_bytes(opCode[1].encode('utf-8'), "big") 
    #v = opCode[1]
        #print("v:",v)
    # Versions outside the range [1, 254] are not supported.
    

        if v<1 or v>254:
            return -1
        else:
            return opCode[1]

# x=bytes.fromhex('42010300000c1d01').decode('utf-8')
# #x1= '42010300000c1d01'   
# #x2 = x1.decode("hex")

# print ("x: ",x)
# FromOpCode(x)
    

   
   