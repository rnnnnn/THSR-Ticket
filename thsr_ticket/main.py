import sys
import time
sys.path.append("./")

from input_validation import input_profile
from thsr_ticket.controller.booking_flow import BookingFlow

def main():
    profile = input_profile()
    Booking_flag = True
    try:
        while Booking_flag:
            flow = BookingFlow()
            _, Booking_flag = flow.run(profile, Booking_flag)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting...")

if __name__ == "__main__":
    main()