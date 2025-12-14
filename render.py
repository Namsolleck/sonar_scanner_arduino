import serial
import time
import numpy as np
import matplotlib.pyplot as plt

PORT = 'COM3'
BAUD_RATE = 9600
ROWS = 46
COLS = 31


def wizualizuj_odleglosci(tablica_odleglosci):
    try:
        dane = np.array(tablica_odleglosci)

        if dane.ndim != 2:
            print("Błąd: Wprowadzona tablica musi być dwuwymiarowa.")
            return

        print(f"Dane gotowe do wizualizacji. Rozmiar: {dane.shape[0]}x{dane.shape[1]}")

        plt.figure(figsize=(10, 8))

        obraz = plt.imshow(dane, cmap='Spectral_r', origin='upper')

        plt.colorbar(obraz, label='Odległość (cm)')

        plt.title("Mapa Skanowania Sonarem (Y-Axis vs X-Axis)")
        plt.xlabel(f"Kąt X (Kolumna, co {int((120 - 60) / (COLS - 1))} stopnie)")
        plt.ylabel(f"Kąt Y (Wiersz, co {int((135 - 45) / (ROWS - 1))} stopnie)")

        plt.show()

    except Exception as e:
        print(f"Wystąpił błąd podczas wizualizacji: {e}")


def read_data_from_arduino():
    data_matrix = []

    try:
        ser = serial.Serial(PORT, BAUD_RATE, timeout=5)
        print(f"Pomyślnie połączono z {PORT} (Baud: {BAUD_RATE}).")

        time.sleep(2)
        ser.flushInput()

        print("Oczekiwanie na nagłówek danych '--- MAPA WYNIKÓW ---'...")
        while True:
            try:
                line = ser.readline().decode('utf-8').strip()
            except UnicodeDecodeError:
                continue

            if "--- MAPA WYNIKÓW ---" in line:
                print("Znaleziono nagłówek. Rozpoczynam odczyt wierszy.")
                break

            time.sleep(0.01)

        rows_read = 0
        while rows_read < ROWS:
            line = ser.readline().decode('utf-8').strip()

            if "--- Koniec ---" in line:
                print("Osiągnięto znacznik końca.")
                break

            if line:
                try:
                    row = [int(val) for val in line.split('\t') if val.strip().isdigit()]

                    if len(row) == COLS:
                        data_matrix.append(row)
                        rows_read += 1
                        print(f"Odczytano wiersz {rows_read}/{ROWS}")

                except ValueError as e:
                    print(f"Błąd konwersji danych: {e}. Linia: '{line}'")

        ser.close()
        print(f"Odczyt zakończony. Zebrano {len(data_matrix)} wierszy.")

    except serial.SerialException as e:
        print(f"Błąd połączenia szeregowego: {e}")
        print(
            f"Upewnij się, że port '{PORT}' jest poprawny, Arduino jest podłączone i nie jest używane przez Monitor Szeregowy Arduino IDE.")
        return None
    except Exception as e:
        print(f"Wystąpił nieoczekiwany błąd: {e}")
        return None

    return data_matrix


if __name__ == '__main__':
    sonar_data = read_data_from_arduino()

    if sonar_data and len(sonar_data) == ROWS:
        wizualizuj_odleglosci(sonar_data)
    else:
        print("Nie udało się pobrać pełnej macierzy danych do wizualizacji.")
