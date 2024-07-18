import sys
import pickle
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from ConfRoomSchedulerLexer import ConfRoomSchedulerLexer
from ConfRoomSchedulerParser import ConfRoomSchedulerParser
from ConfRoomSchedulerListener import ConfRoomSchedulerListener

class ConfRoomSchedulerErrorListener(ErrorListener):
    def __init__(self):
        super(ConfRoomSchedulerErrorListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise Exception(f"Syntax error at line {line}, column {column}: {msg}")

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
        id = ctx.reserve().ID(0).getText()
        date = ctx.reserve().DATE().getText()
        start_time = ctx.reserve().TIME(0).getText()
        end_time = ctx.reserve().TIME(1).getText()
        requester = ctx.reserve().ID(1).getText()
        if self.is_valid_time(start_time, end_time):
            if not self.is_overlapping(id, date, start_time, end_time):
                self.reservations[(id, date, start_time, end_time)] = requester
                self.save_reservations()
                print(f"Reserved: {id} on {date} from {start_time} to {end_time} by {requester}")
            else:
                print(f"Error: Reservation overlaps with an existing reservation for {id} on {date} from {start_time} to {end_time}")
        else:
            print(f"Error: Invalid time range '{start_time} to {end_time}' for reservation on {date} by {requester}")

    def enterCancelStat(self, ctx: ConfRoomSchedulerParser.CancelStatContext):
        id = ctx.cancel().ID(0).getText()
        date = ctx.cancel().DATE().getText()
        start_time = ctx.cancel().TIME(0).getText()
        end_time = ctx.cancel().TIME(1).getText()
        requester = ctx.cancel().ID(1).getText()
        if (id, date, start_time, end_time) in self.reservations:
            del self.reservations[(id, date, start_time, end_time)]
            self.save_reservations()
            print(f"Cancelled: {id} on {date} from {start_time} to {end_time} by {requester}")
        else:
            print(f"No reservation found to cancel: {id} on {date} from {start_time} to {end_time}")

    def is_valid_time(self, start_time, end_time):
        try:
            start_hour, start_minute = map(int, start_time.split(':'))
            end_hour, end_minute = map(int, end_time.split(':'))
            if start_hour < 0 or start_hour > 23 or end_hour < 0 or end_hour > 23:
                return False
            if start_minute < 0 or start_minute > 59 or end_minute < 0 or end_minute > 59:
                return False
            if (end_hour < start_hour) or (end_hour == start_hour and end_minute <= start_minute):
                return False
            return True
        except ValueError:
            return False

    def is_overlapping(self, id, date, start_time, end_time):
        for (res_id, res_date, res_start, res_end) in self.reservations:
            if id == res_id and date == res_date:
                if not (end_time <= res_start or start_time >= res_end):
                    return True
        return False

def main(argv):
    if len(argv) < 2:
        print("Usage: python3 DriverConfroom.py <input_file>")
        return

    input_file = argv[1]

    try:
        input_stream = FileStream(input_file)
    except IOError as e:
        print(f"Error opening file {input_file}: {e}")
        return

    lexer = ConfRoomSchedulerLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ConfRoomSchedulerParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(ConfRoomSchedulerErrorListener())

    tree = parser.prog()

    scheduler = ConfRoomScheduler()
    walker = ParseTreeWalker()
    walker.walk(scheduler, tree)

if __name__ == '__main__':
    main(sys.argv)
