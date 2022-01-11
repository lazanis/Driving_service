import uvicorn
from datetime import datetime
from fast_api_methods import app

if __name__ == '__main__':
    key_path = "certificates/example.key"
    cert_path = "certificates/example.crt"

    print(f'Service started at {datetime.now()}')
    try:
        uvicorn.run(app, host='localhost', port=7777, ssl_keyfile=key_path, ssl_certfile=cert_path)
    except Exception as e:
        print(f'Service stopped at {datetime.now()} for reason: {e}')
