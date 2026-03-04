import time

from utils import generate_click_datastream

if __name__ == "__main__":
    n = 10000
    while n > 0:
        n -= 1
        generate_click_datastream()
        time.sleep(1)
        print(f"Generated {n} events")
        if n == 0:
            time.sleep(10)  # Sleep for 10 seconds before generating more data
            n = 10000
