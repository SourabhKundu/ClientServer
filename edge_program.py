import time
import json
import pandas as pd
import requests

# loading csv file
df = pd.read_csv("dataset.csv")
df = list(df.to_dict("index").items())

# current successful and bounce file
state_file_name = "current_state.json"

# initalizing variables
bounced_request = []
successful_count = 0
bounced_count = 0


# save latest value of successful and bounce to file
def save_state(successful_count, bounced_count):
    data = json.dumps({"successful_count": successful_count,
                      "bounced_count": bounced_count})
    json.dump(data, open(state_file_name, "w"))


# iterates over csv and call the server
for row in df:

    # Bounecd in Current Iteration
    current_bounce = []
    payload = json.dumps(row)
    wait = 10

    try:
        # Calling the server
        res = requests.post('http://127.0.0.1:5000/', data=payload).json()
        print(payload)
        

        # if Failed update the value of successful and bounceand add to current_bounce list
        if res["status"] != "successful":
            current_bounce.append(payload)
            bounced_count += 1
            print("Unsuccessful -",payload)
            save_state(successful_count, bounced_count)

        # If successful update the value of successful and bounce
        else:
            successful_count += 1
            print("Successful -",payload)
            save_state(successful_count, bounced_count)

    except Exception as e:
        # if Error occured update the value of successful and bounceand add to current_bounce list
        print("Exception : ", str(e))
        current_bounce.append(payload)
        bounced_count += 1
        save_state(successful_count, bounced_count)

    # iterating over Bounce List
    if bounced_request:
        for bounce in list(bounced_request):
            try:
                # Calling the server
                res = requests.post(
                    'http://127.0.0.1:5000/', data=bounce).json()

                # if Failed update the value of successful and bounceand add to current_bounce list
                if res["status"] != "successful":
                    current_bounce.append(bounce)
                    
                    save_state(successful_count, bounced_count)

                # If successful update the value of successful and bounce
                else:
                    successful_count += 1
                    bounced_count -= 1
                    print("Successful -",bounce)
                    save_state(successful_count, bounced_count)

            except Exception as e:
                # if Error occured update the value of successful and bounceand add to current_bounce list
                print("Exception : ", str(e))
                current_bounce.append(bounce)
                
                save_state(successful_count, bounced_count)

            # reduceing the total wait time by five seconds and checking if we want to continue or call the main call
            wait -= 1
            if not wait:
                break

            # bouned_request
            bounced_request.pop(0)
            time.sleep(1)

    # Updating the Bounce List
    bounced_request.extend(current_bounce)
    print("current_state: ", (successful_count, bounced_count))
    time.sleep(wait)
