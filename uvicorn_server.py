import uvicorn


if __name__ == '__main__':
    uvicorn.run('app7:app', port=5000, reload=True)

