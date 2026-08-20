from main import extract
import time


text = """
Customer: John Smith
Order ID: ORD-100
Date: January 10, 2026

The customer received a damaged product.
The customer wants a replacement.
"""


success = 0
recovered = 0
failed = 0
crashes = 0


for i in range(50):

    print(f"Run {i + 1}/50")

    try:
        result, status = extract(text)

        if status == "success":
            success += 1
            print("  SUCCESS")

        elif status == "recovered":
            recovered += 1
            print("  RECOVERED")

        elif status == "failed":
            failed += 1
            print("  FAILED CLEANLY:", result)

    except Exception as error:
        crashes += 1
        print("  CRASH:", error)

    time.sleep(4)


print("\n==============================")
print("50 RUN RESULTS")
print("==============================")
print("Successful first attempt :", success)
print("Recovered after retry    :", recovered)
print("Failed cleanly           :", failed)
print("Crashes                  :", crashes)
print("Total                    :", success + recovered + failed + crashes)