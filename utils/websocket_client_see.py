# client.py
import asyncio
import base64
import json

import websockets
import cv2
import numpy as np

async def send_video():
    # uri = "ws://localhost:8765"
    group = 0
    # uri = f"ws://localhost:8000/ws/{group}0/"
    uri = f"ws://113.44.87.161/ws/{group}0/"
    # uri = f"ws://localhost:8000/ws/system/"
    # uri = f"ws://113.44.87.161/ws/system/"
    async with websockets.connect(uri, open_timeout=10) as websocket:
        # await websocket.send(json.dumps({
        #     "headers": {
        #         "type": "system",
        #         "message": "finish_send",  # finish_send require_sendd require_send
        #         "author": "0",
        #         "receiver": "0",
        #     },
        #     "body": {
        #
        #     }
        # }))
        while True:
            data = await websocket.recv()
            # print(data)
            json_data = json.loads(data)
            image_message = base64.b64decode(json_data["body"]["content"].encode("utf-8"))
            nparr = np.frombuffer(image_message, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # 用cv2展示图像
            cv2.imshow("Received Video", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # print(data)
        # cap = cv2.VideoCapture(0)  # 打开摄像头或提供视频文件路径
        #
        # while cap.isOpened():
        #     ret, frame = cap.read()
        #     if not ret:
        #         print("Failed to grab frame")
        #         break
        #
        #     # 编码图像为JPEG格式
        #     _, buffer = cv2.imencode('.jpg', frame)
        #     img_as_text = buffer.tobytes()
        #
        #     # 发送图像数据
        #     await websocket.send(img_as_text)
        #
        #     # 增加适当的延迟可以避免摄像头过载
        #     await asyncio.sleep(0.01)
        #
        # cap.release()

asyncio.get_event_loop().run_until_complete(send_video())
