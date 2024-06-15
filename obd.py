import time
import random
from blessed import Terminal

# Definizione di una classe per gestire ogni quadrato
class Square:
    def __init__(self, label):
        self.label = label
        self.current_value = 0
        self.min_value = float('inf')  # Inizializza il minimo a un valore molto grande
        self.max_value = float('-inf') # Inizializza il massimo a un valore molto piccolo

    def update_value(self, new_value):
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

# Funzione per generare un valore casuale
def generate_random_value():
    return random.randint(1, 100)

# Funzione per disegnare un quadrato con valori aggiuntivi
def draw_square(term, x, y, width, height, square):
    label = square.label
    current_value = square.get_current_value()
    min_value = square.get_min_value()
    max_value = square.get_max_value()

    # Disegna i bordi del quadrato
    for i in range(width):
        print(term.move_xy(x + i, y) + '─')
        print(term.move_xy(x + i, y + height - 1) + '─')

    for i in range(height):
        print(term.move_xy(x, y + i) + '│')
        print(term.move_xy(x + width - 1, y + i) + '│')

    # Angoli del quadrato
    print(term.move_xy(x, y) + '┌')
    print(term.move_xy(x + width - 1, y) + '┐')
    print(term.move_xy(x, y + height - 1) + '└')
    print(term.move_xy(x + width - 1, y + height - 1) + '┘')

    # Inserisci l'etichetta sopra il valore
    print(term.move_xy(x + (width // 2) - (len(label) // 2), y + 1) + label)
    
    # Inserisci la label "min" sotto la base sinistra del quadrato
    min_label = "min"
    print(term.move_xy(x + 1, y + height - 3) + min_label)

    # Inserisci il valore minimo sotto la label "min"
    min_value_str = f"{min_value}"
    print(term.move_xy(x + 1, y + height - 2) + min_value_str)

    # Inserisci la label "max" sotto la base destra del quadrato
    max_label = "max"
    print(term.move_xy(x + width - len(max_label) - 1, y + height - 3) + max_label)

    # Inserisci il valore massimo sotto la label "max"
    max_value_str = f"{max_value}"
    print(term.move_xy(x + width - len(max_value_str) - 1, y + height - 2) + max_value_str)

    # Inserisci il valore corrente al centro del quadrato
    print(term.move_xy(x + (width // 2) - 3, y + height // 2 + 1) + str(current_value).center(6))

def main():
    term = Terminal()

    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        try:
            # Inizializza i quadrati
            squares = [
                Square("Quadrato 1"),
                Square("Quadrato 2"),
                Square("Quadrato 3"),
                Square("Quadrato 4"),
                Square("Quadrato 5"),
                Square("Quadrato 6")
            ]

            while True:
                print(term.clear())
                
                # Ottieni le dimensioni del terminale
                term_width = term.width
                term_height = term.height

                # Calcola le dimensioni di ciascun quadrato con un fattore di scala
                scale_factor = 0.8  # Fattore di scala per aumentare la dimensione dei quadrati
                square_width = int((term_width // 3) * scale_factor)
                square_height = int((term_height // 2) * scale_factor)

                # Spazio tra i quadrati per centrarli
                horizontal_padding = (term_width - (square_width * 3)) // 4
                vertical_padding = (term_height - (square_height * 2)) // 3

                # Genera e disegna i 6 quadrati con valori casuali, etichette e valori aggiuntivi
                for i, square in enumerate(squares):
                    x = horizontal_padding + (i % 3) * (square_width + horizontal_padding)
                    y = vertical_padding + (i // 3) * (square_height + vertical_padding)
                    
                    new_value = generate_random_value()
                    square.update_value(new_value)
                    draw_square(term, x, y, square_width, square_height, square)
                
                time.sleep(1)
        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    main()
