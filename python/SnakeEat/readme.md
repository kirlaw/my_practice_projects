使用base64格式把图片保存在py文件再读出，方便程序打包


打包
pyinstaller -F -w snake_eat.py -p memory_pic.py --add-data="E:\ComputerVersion\venv\Lib\site-packages\mediapipe\modules;mediapipe/modules"


![image](https://user-images.githubusercontent.com/35916301/216256232-a2a24988-f1b4-4afd-8829-e7445544fedc.png)


### 用pygame实现

snake_eat_pygame.py

随机生成食物，手指控制移动
