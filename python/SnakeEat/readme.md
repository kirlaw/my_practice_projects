使用base64格式把图片保存在py文件再读出，方便程序打包


打包
pyinstaller -F -w main.py -p PoseModule.py --add-data="E:\ComputerVersion\venv\Lib\site-packages\mediapipe\modules;mediapipe/modules"
