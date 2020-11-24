import requests
import os
import json
import time

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'


def auth():
    return os.environ.get("BEARER_TOKEN")


def create_url(names_list):
    # Specify the usernames that you want to lookup below
    # You can enter up to 100 comma-separated values.
    usernames = "usernames=%s" % names_list
    user_fields = "user.fields=created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
    # User fields are adjustable, options include:
    # created_at, description, entities, id, location, name,
    # pinned_tweet_id, profile_image_url, protected,
    # public_metrics, url, username, verified, and withheld
    url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, user_fields)
    return url


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main():
    bearer_token = auth()
    fout = open('users_info.txt', 'a')
    start = time.time()
    with open('users_list.txt', 'r') as f:
        lno = 0
        names_list = []
        for line in f:
            name = str(line.rstrip())
            names_list.append(name)
            lno += 1
            if lno % 100 == 0 or lno == 968345:
                # get names_list by 100 batches
                url = create_url(','.join(names_list))
                headers = create_headers(bearer_token)
                json_response = connect_to_endpoint(url, headers)
                fout.write(json.dumps(json_response))
                fout.write('\n')
                fout.flush()
                names_list = []
                elapsed = time.time() - start
                sleep_time = 3.-elapsed
                if sleep_time > 0:
                    time.sleep(sleep_time)
                start = time.time()
    fout.close()

if __name__ == "__main__":
    main()
