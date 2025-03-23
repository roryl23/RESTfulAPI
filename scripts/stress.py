import argparse
import requests


def parse_args():
    parser = argparse.ArgumentParser(
        description='Stress test RESTfulAPI'
    )
    parser.add_argument(
        '--host',
        type=str,
        default='localhost',
        help='Host address or hostname to connect to'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8080,
        help='Port to connect to'
    )
    return parser.parse_args()


class Stress:
    def __init__(self, url, port):
        self.url: str = f"http://{url}:{port}"

    def create_user(self):
        r = requests.post(f"{self.url}/users", json={
            'name': 'test',
            'email': 'testuser@test.net',
        })
        if r.status_code == 201:
            print(r.json())
            return r.json()['user_id']
        else:
            print(f"failed to create user: {r.status_code}")
            return None

    def update_records(self, user_id: str, num: int=100):
        for i in range(num):
            r = requests.put(f"{self.url}/users/{user_id}", json={
                'name': f"test{i}",
                'email': f"testuser{i}@test.net",
            })
            if r.status_code != 200:
                print(f"failed to update record: {r.status_code}")


if __name__ == '__main__':
    args = parse_args()

    stresser = Stress(args.host, args.port)
    user_id = stresser.create_user()
    if user_id is not None:
        stresser.update_records(user_id)
    else:
        print("failed to create user")
