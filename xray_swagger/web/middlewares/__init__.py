from fastapi import FastAPI

from .process_time import register_process_time_middleware

__all__ = ("register_middlewares",)


def register_middlewares(app: FastAPI):
    # 미들웨어의 추가 순서도 중요하다. 스택 프레임 구성에 의해 아래에서부터 처리해오게 됨.
    register_process_time_middleware(app)
