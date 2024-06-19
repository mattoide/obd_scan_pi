import time
import random
import curses
import obd

obd_port = None
connection = None
supported_commands = None
supported_commands_names = []
watch_values = {}



# Definizione di una classe per gestire ogni quadrato
class Square:
    def __init__(self, label):
        self.label = label
        self.current_value = 0
        self.min_value = float('inf')  # Inizializza il minimo a un valore molto grande
        self.max_value = float('-inf') # Inizializza il massimo a un valore molto piccolo

    def update_value(self, new_value):
        # print(type(new_value))
        # print(new_value)
        # time.sleep(1)
        self.current_value = new_value
        if new_value < self.min_value:
            self.min_value = new_value
        if new_value > self.max_value:
            self.max_value = new_value

    def get_current_value(self):
        return self.current_value

    def get_min_value(self):
        return self.min_value

    def get_max_value(self):
        return self.max_value

def unwatch_all():
    with connection.paused() as was_running:
        connection.unwatch_all()

    if was_running:
        connection.start()

def unwatch_pid(pid):
    global watch_values
    if pid == 'BOOST':
        with connection.paused() as was_running:
            connection.unwatch(obd.commands.INTAKE_PRESSURE) 
            connection.unwatch(obd.commands.BAROMETRIC_PRESSURE) 
            del watch_values[pid]
            time.sleep(0.1)
    else:  
        with connection.paused() as was_running:
            connection.unwatch(obd.commands[pid])
            del watch_values[pid]
            time.sleep(0.1)
        if was_running:
            connection.start()

def read_pid(pid):
    with connection.paused() as was_running:
        if pid != 'BOOST':
            cmd = obd.commands[pid] 
            response = connection.query(cmd)
            connection.start()
            if response.is_null():
                return 'N/A'
            else:
                return float(str(response.value).split(" ")[0])
        else:
            read_turbo()

def watch_pid(pid):
    if pid == 'BOOST':
        read_turbo()
    else:
        with connection.paused() as was_running:
            connection.watch(obd.commands[pid], callback=update_watch)

        connection.start()

def update_watch(response):
    global watch_values
    # print(response)

# print(type(response.value))
    if '[obd.obd]' in str(response.value).split(" ")[0]:
        watch_values[response.command.name] = float(0)

    val = float(str(response.value).split(" ")[0])
    watch_values[response.command.name] = val

def update_watch_custom(a):
    global watch_values
    cmd = obd.commands.INTAKE_PRESSURE
    INTAKE_PRESSURE = connection.query(cmd)
    cmd = obd.commands.BAROMETRIC_PRESSURE
    BAROMETRIC_PRESSURE = connection.query(cmd)
    time.sleep(.01)
    if INTAKE_PRESSURE.value is not None and BAROMETRIC_PRESSURE.value is not None:
        turbo_pressure = INTAKE_PRESSURE.value.to('bar') - BAROMETRIC_PRESSURE.value.to('bar')
        # print('INTAKE_PRESSURE:'   )
        # print(INTAKE_PRESSURE.value.to('bar'))
        # print('BAROMETRIC_PRESSURE:')
        # print(BAROMETRIC_PRESSURE.value.to('bar'))
        # print('turbo_pressure:')
        # print( turbo_pressure)
        watch_values['BOOST'] = round(float(str(turbo_pressure.to('bar')).split(' ')[0]), 2)

def read_turbo():
    with connection.paused() as was_running:
        connection.watch(obd.commands.INTAKE_PRESSURE)
        connection.watch(obd.commands.BAROMETRIC_PRESSURE, callback=update_watch_custom)
        connection.start()
        time.sleep(1)

def connect(port):
    global obd_port
    global connection
    obd_port = port
    # connection = obd.OBD()
    connection = obd.Async(port)

# Funzione per generare un valore casuale
def generate_random_value(pid):
    # return random.randint(1, 100)
    if pid in watch_values:
        res = watch_values[pid]
    else:
        res = float(0)

    return res

# Funzione per disegnare un quadrato con valori aggiuntivi
def draw_square(stdscr, x, y, width, height, square):
    label = square.label
    current_value = square.get_current_value()
    min_value = square.get_min_value()
    max_value = square.get_max_value()

    # Disegna i bordi del quadrato
    for i in range(width):
        stdscr.addstr(y, x + i, '─')
        stdscr.addstr(y + height - 1, x + i, '─')

    for i in range(height):
        stdscr.addstr(y + i, x, '│')
        stdscr.addstr(y + i, x + width - 1, '│')

    # Angoli del quadrato
    stdscr.addstr(y, x, '┌')
    stdscr.addstr(y, x + width - 1, '┐')
    stdscr.addstr(y + height - 1, x, '└')
    stdscr.addstr(y + height - 1, x + width - 1, '┘')

    # Inserisci l'etichetta sopra il valore
    stdscr.addstr(y + 1, x + (width // 2) - (len(label) // 2), label)
    
    # Inserisci la label "min" in rosso sotto la base sinistra del quadrato
    min_label = "min"
    stdscr.addstr(y + height - 3, x + 1, min_label, curses.color_pair(1))

    # Inserisci il valore minimo sotto la label "min" (bianco)
    min_value_str = f"{min_value}"
    stdscr.addstr(y + height - 2, x + 1, min_value_str, curses.color_pair(0))  # Color Pair 0 per il bianco

    # Inserisci la label "max" in verde sotto la base destra del quadrato
    max_label = "max"
    stdscr.addstr(y + height - 3, x + width - len(max_label) - 2, max_label, curses.color_pair(2))

    # Inserisci il valore massimo sotto la label "max" (bianco)
    max_value_str = f"{max_value}"
    stdscr.addstr(y + height - 2, x + width - len(max_value_str) - 2, max_value_str, curses.color_pair(0))  # Color Pair 0 per il bianco

    # Inserisci il valore corrente al centro del quadrato (bianco)
    stdscr.addstr(y + height // 2 + 1, x + (width // 2) - 3, str(current_value).center(6), curses.color_pair(0))

def main(stdscr):

    connect('/dev/pts/11')
    

    # Inizializza i colori
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)    # Colore rosso per "min"
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Colore verde per "max"

    # Inizializza i quadrati
    squares = [
        Square("RPM"),
        Square("Water Temp"),
        Square("Turbo Pressure"),
        Square("Air Temp"),
        Square("Air Flow"),
        Square("Oil Temp")
    ]

    pids = [
        "RPM",
        "COOLANT_TEMP",
        "BOOST",
        "INTAKE_TEMP",
        "MAF",
        "OIL_TEMP"
    ]


    for pid in pids:
                watch_pid(pid)
                time.sleep(0.1)

    while True:
        # stdscr.clear()
        
        # Ottieni le dimensioni del terminale
        term_height, term_width = stdscr.getmaxyx()

        # Calcola le dimensioni di ciascun quadrato con un fattore di scala
        scale_factor = 0.9  # Fattore di scala per aumentare la dimensione dei quadrati
        square_width = int((term_width // 3) * scale_factor)
        square_height = int((term_height // 2) * scale_factor)

        # Spazio tra i quadrati per centrarli
        horizontal_padding = (term_width - (square_width * 3)) // 4
        vertical_padding = (term_height - (square_height * 2)) // 3

        # Genera e disegna i 6 quadrati con valori casuali, etichette e valori aggiuntivi
        for i, square in enumerate(squares):
            x = horizontal_padding + (i % 3) * (square_width + horizontal_padding)
            y = vertical_padding + (i // 3) * (square_height + vertical_padding)

            new_value = generate_random_value(pids[i])
            # print(new_value)
            square.update_value(new_value)
            draw_square(stdscr, x, y, square_width, square_height, square)

        stdscr.refresh()
        time.sleep(0.1)

if __name__ == '__main__':
    curses.wrapper(main)

