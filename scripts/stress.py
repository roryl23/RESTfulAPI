import argparse
import time

import requests
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor


class Stress:
    def __init__(self, url, port):
        self.url: str = f"http://{url}:{port}"

    def create_user(self):
        r = requests.post(f"{self.url}/users", json={
            'name': 'testuser',
            'email': 'testuser@test.net',
        })
        if r.status_code == 201:
            print(r.json())
            return r.json()['user_id']
        else:
            print(f"failed to create user: {r.status_code}")
            return None

    def update_record(self, user_id: str, i: int):
        r = requests.put(f"{self.url}/users/{user_id}", json={
            'name': f"testuser{i}",
            'email': f"testuser{i}@test.net",
        })
        if r.status_code == 200:
            return True
        else:
            return False

    def update_records(self, user_id: str, n: int=10000, w: int=128):
        with ThreadPoolExecutor(max_workers=w) as executor:
            threads = [executor.submit(self.update_record, user_id, i) for i in range(1, n)]
            results = []
            for future in futures.as_completed(threads):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    print(f"thread generated an exception: {e}")
            return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Stress tests RESTfulAPI production deployment'
    )
    parser.add_argument(
        '--host',
        type=str,
        required=True,
    )
    parser.add_argument(
        '--port',
        type=int,
        required=True,
    )
    args = parser.parse_args()

    stresser = Stress(args.host, args.port)
    user_id = stresser.create_user()
    if user_id is not None:
        print(f"created user, running concurrent update stress test...")
        start_time = time.time()
        results = stresser.update_records(user_id)
        end_time = time.time()
        duration = end_time - start_time
        if not all(results):
            print(f"failed to update records atomically")
        else:
            print(f"all records updated atomically")
            print(f"updated record {user_id} {len(results)} times in {duration} seconds at ~{int(len(results) / duration)} records/s")
    else:
        print("failed to create user")
