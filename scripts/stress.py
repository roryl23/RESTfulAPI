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

    # Parse arguments and return
    args = parser.parse_args()
    return args


class Stress:
    def __init__(self, url, port):
        self.url: str = f"http://{url}:{port}"

    def create_user(self):
        r = requests.post(f"{self.url}/users", json={
            'name': 'test',
            'email': 'testuser@test.net',
        })
        print(r.json())
        return r.json()['user_id']

    def update_records(self, user_id: str):
        for i in range(10000):
            r = requests.put(f"{self.url}/users/{i}", json={
                'user_id': user_id,
                'name': f"test{i}",
                'email': f"testuser{i}@test.net",
            })
            if r.status_code != 200:
                print(r.json())


if __name__ == '__main__':
    args = parse_args()

    stresser = Stress(args.host, args.port)
    user_id = stresser.create_user()
    stresser.update_records(user_id)
