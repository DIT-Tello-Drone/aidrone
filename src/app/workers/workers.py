import time
import cv2
import threading
import zmq
import logging
import asyncio
from qdi import IContainer
from services.tfmodels import ITFModel, TFModel
from services.ws import WebSocketManager

class IWorker:
    def work(self) -> None: ...
    def send(self, message: str) -> None: ...

class BaseWorker(IWorker):
    def __init__(self):
        self.sender_context = zmq.Context.instance()
        self.sender = self.sender_context.socket(zmq.PAIR)
        self.sender.connect(self.url)

        self.receiver_context = zmq.Context.instance()
        self.receiver = self.receiver_context.socket(zmq.PAIR)
        self.receiver.bind(self.url)

    async def handle(self, receiver) -> None: ...

    def send(self, message: str):
        self.sender.send(message.encode('utf-8'))

    def work(self) -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.handle(self.receiver))
        loop.close()


    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.sender_context.term()
        self.receiver_context.term()
        self._close(manual_close=False)


class TFModelWorker(BaseWorker):
    def __init__(self, container: IContainer, socket_manager: WebSocketManager):
        self.url="inproc://worker"
        super().__init__()
        self.container = container
        self.socket_manager=socket_manager

    async def handle(self, receiver) -> None:
        while True:
            msg  = receiver.recv()
            logging.info("Loading model: [ %s ]" % (msg))

            await self.socket_manager.send("Model loaded")
            #model = SSD_TFModel("/app/trt_graph.pb")
            #image = cv2.imread('/app/18.jpg')
            #res=model.predict(image)
            #self.container.register_instance(ITFModel,model)
            logging.info("Model loaded: [ %s ]" % (msg))
            time.sleep(1)


