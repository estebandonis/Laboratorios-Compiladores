import sys
import pickle
from antlr4 import *
from ConfRoomSchedulerLexer import ConfRoomSchedulerLexer
from ConfRoomSchedulerParser import ConfRoomSchedulerParser
from ConfRoomSchedulerListener import ConfRoomSchedulerListener

class ConfRoomScheduler(ConfRoomSchedulerListener):
    def __init__(self, reservations_file='reservations.pkl'):
        self.reservations_file = reservations_file
        self.reservations = self.load_reservations()

    def load_reservations(self):
        try:
            with open(self.reservations_file, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return {}

    def save_reservations(self):
        with open(self.reservations_file, 'wb') as f:
            pickle.dump(self.reservations, f)

    def enterReserveStat(self, ctx: ConfRoomSchedulerParser.ReserveStatContext):
        id = ctx.reserve().ID().getText()
        date = ctx.reserve().DATE().getText()
        start_time = ctx.reserve().TIME(0).getText()
        end_time = ctx.reserve().TIME(1).getText()
        self.reservations[(id, date, start_time, end_time)] = 'RESERVED'
        self.save_reservations()
        print(f"Reserved: {id} on {date} from {start_time} to {end_time}")

    def enterCancelStat(self, ctx: ConfRoomSchedulerParser.CancelStatContext):
        id = ctx.cancel().ID().getText()
        date = ctx.cancel().DATE().getText()
        start_time = ctx.cancel().TIME(0).getText()
        end_time = ctx.cancel().TIME(1).getText()
        if (id, date, start_time, end_time) in self.reservations:
            del self.reservations[(id, date, start_time, end_time)]
            self.save_reservations()
            print(f"Cancelled: {id} on {date} from {start_time} to {end_time}")
        else:
            print(f"No reservation found to cancel: {id} on {date} from {start_time} to {end_time}")

def main(argv):
    input_stream = FileStream(argv[1])
    lexer = ConfRoomSchedulerLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ConfRoomSchedulerParser(stream)
    tree = parser.prog()

    scheduler = ConfRoomScheduler()
    walker = ParseTreeWalker()
    walker.walk(scheduler, tree)

if __name__ == '__main__':
    main(sys.argv)
