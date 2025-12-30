import time
from datetime import datetime

class ParkingLotDFA:
    def __init__(self, capacity=5, timer_delay=2):
        # DFA states
        self.states = {"IDLE", "CHECK_TOKEN", "OPEN_GATE", "CLOSE_GATE", "ACCEPT", "REJECT"}
        # DFA input alphabet
        self.alphabet = {"CarArrives", "ValidToken", "InvalidToken", "CarEnters", "Timer", "CarExits"}
        # Start and accepting states
        self.start_state = "IDLE"
        self.accept_states = {"ACCEPT"}
        # Current DFA state
        self.current_state = self.start_state
        # Transition function
        self.transition_function = {
            ("IDLE", "CarArrives"): "CHECK_TOKEN",
            ("CHECK_TOKEN", "ValidToken"): "OPEN_GATE",
            ("CHECK_TOKEN", "InvalidToken"): "REJECT",
            ("OPEN_GATE", "CarEnters"): "CLOSE_GATE",
            ("CLOSE_GATE", "Timer"): "ACCEPT"
        }
        # Parking lot properties
        self.capacity = capacity
        self.cars_inside_list = []  # Track specific car IDs
        self.timer_delay = timer_delay
        # Statistics and logs
        self.total_accepted = 0
        self.total_rejected = 0
        self.log = []

    # ---------------- DFA Operations ----------------
    def reset(self):
        self.current_state = self.start_state

    def transition(self, symbol, car_id=None):
        # Exit a car
        if symbol == "CarExits" and car_id:
            if car_id in self.cars_inside_list:
                self.cars_inside_list.remove(car_id)
                print(f"Car {car_id} exited. Cars inside: {len(self.cars_inside_list)}/{self.capacity}")
            else:
                print(f"Car {car_id} not found in the lot!")
            self.log_attempt(symbol, car_id)
            return

        # Car arrives – check capacity
        if symbol == "CarArrives":
            if len(self.cars_inside_list) >= self.capacity:
                self.current_state = "REJECT"
                self.log_attempt(symbol, car_id)
                print("Parking full! Entry rejected.")
                self.total_rejected += 1
                return

        # Invalid input
        if symbol not in self.alphabet:
            self.current_state = "REJECT"
            self.log_attempt(symbol, car_id)
            self.total_rejected += 1
            return

        key = (self.current_state, symbol)
        if key in self.transition_function:
            self.current_state = self.transition_function[key]

            # If car entry completes successfully
            if self.current_state == "ACCEPT" and car_id:
                self.cars_inside_list.append(car_id)
                self.total_accepted += 1
        else:
            self.current_state = "REJECT"
            self.total_rejected += 1

        self.log_attempt(symbol, car_id)

    # ---------------- Parking Operations ----------------
    def add_car(self):
        """Manually add a car with ID and token status"""
        print("\n--- Adding a Car ---")
        if len(self.cars_inside_list) >= self.capacity:
            print("Parking lot full! Cannot add car.")
            self.total_rejected += 1
            return

        car_id = input("Enter car ID or license plate: ").strip()
        if car_id in self.cars_inside_list:
            print("This car is already inside the lot!")
            return

        token_status = input("Enter token status (ValidToken / InvalidToken): ").strip()
        if token_status not in ["ValidToken", "InvalidToken"]:
            print("Invalid token input. Rejecting entry.")
            token_status = "InvalidToken"

        # Run DFA for this car
        self.reset()
        self.transition("CarArrives", car_id)
        print(f"Token scanned for {car_id}: {token_status}")
        self.transition(token_status, car_id)

        if self.current_state == "REJECT":
            print(f"Car {car_id} entry rejected due to invalid token.")
            return

        print(f"Car {car_id} entering gate...")
        self.transition("CarEnters", car_id)
        print("Waiting for gate to close...")
        time.sleep(self.timer_delay)
        self.transition("Timer", car_id)

        if self.current_state in self.accept_states:
            print(f"Car {car_id} entered successfully. Cars inside: {len(self.cars_inside_list)}/{self.capacity}")
        else:
            print(f"Car {car_id} entry failed.")

    def remove_car(self):
        """Manually remove a specific car"""
        print("\n--- Removing a Car ---")
        if not self.cars_inside_list:
            print("Parking lot is empty!")
            return
        print("Cars currently inside:", ", ".join(self.cars_inside_list))
        car_id = input("Enter the car ID to remove: ").strip()
        self.transition("CarExits", car_id)

    # ---------------- Logging & Stats ----------------
    def log_attempt(self, symbol, car_id=None):
        self.log.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "car_id": car_id if car_id else "N/A",
            "symbol": symbol,
            "state": self.current_state,
            "cars_inside": len(self.cars_inside_list)
        })

    def show_log(self):
        print("\n--- Parking Log ---")
        for entry in self.log:
            print(f"{entry['timestamp']} | Car ID: {entry['car_id']:<10} | "
                  f"Input: {entry['symbol']:<12} | State: {entry['state']:<10} | "
                  f"Cars inside: {entry['cars_inside']}")

    def show_stats(self):
        print("\n--- Parking Lot Statistics ---")
        print(f"Capacity: {self.capacity}")
        print(f"Cars inside ({len(self.cars_inside_list)}): {', '.join(self.cars_inside_list) if self.cars_inside_list else 'None'}")
        print(f"Spaces left: {self.capacity - len(self.cars_inside_list)}")
        print(f"Total Accepted Entries: {self.total_accepted}")
        print(f"Total Rejected Entries: {self.total_rejected}")

    # ---------------- Display Functions ----------------
    def show_transition_table(self):
        print("\nTransition Table:")
        print(f"{'Current State':<15} {'Input Symbol':<15} {'Next State':<15}")
        print("-" * 45)
        for (state, symbol), next_state in self.transition_function.items():
            print(f"{state:<15} {symbol:<15} {next_state:<15}")

    def show_states(self):
        print("\nStates (Q):", self.states)

    def show_alphabet(self):
        print("\nInput Alphabet (Σ):", self.alphabet)


# ---------------- Main Program ----------------
def main():
    capacity = int(input("Enter parking lot capacity: "))
    dfa = ParkingLotDFA(capacity=capacity, timer_delay=2)

    while True:
        print("\n========== Parking Lot DFA ==========")
        print("1. Show DFA States")
        print("2. Show Input Alphabet")
        print("3. Show Transition Table")
        print("4. Add a Car (Entry)")
        print("5. Remove a Car (Exit)")
        print("6. Show Log")
        print("7. Show Statistics")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            dfa.show_states()
        elif choice == "2":
            dfa.show_alphabet()
        elif choice == "3":
            dfa.show_transition_table()
        elif choice == "4":
            dfa.add_car()
        elif choice == "5":
            dfa.remove_car()
        elif choice == "6":
            dfa.show_log()
        elif choice == "7":
            dfa.show_stats()
        elif choice == "8":
            print("\nExiting Program...")
            break
        else:
            print("\nInvalid choice. Try again.")


if __name__ == "__main__":
    main()
