using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.IO;
using System.Net.Sockets;
using System.Text;

public class Receive : MonoBehaviour
{
    public Button screenshotButton;

    public string IP = "127.0.0.1";  // Python服务器的IP地址
    public int Port = 9999;  // Python服务器的端口号

    string imagePath= "Assets/lego/test_path/image.jpg"; // 图像文件的路径
    public Image image; // 显示图像的Image组件

   

    // Start is called before the first frame update
    void Start()
    {

        //点击按钮拍照，监听按钮是否按下
        screenshotButton.onClick.AddListener(SendMessageToPython);

    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void SendMessageToPython()
    {
        // 创建一个TcpClient连接到Python服务器
        TcpClient client = new TcpClient(IP, Port);

        // 将消息转换为字节数组并发送
        byte[] data = Encoding.ASCII.GetBytes("1");
        NetworkStream stream = client.GetStream();
        stream.Write(data, 0, data.Length);

        byte[] buffer = new byte[1024];
        int length = stream.Read(buffer, 0, buffer.Length); //接收数据
        string receivedMessage = Encoding.UTF8.GetString(buffer, 0, length); //将接收到的数据转换成字符串
        //Debug.Log("Received message from Python: " + receivedMessage); //输出接收到的消息

        if (receivedMessage!="")
        {
            ShowImage();
        }

        // 关闭连接
        stream.Close();
        client.Close();
    }


    public void ShowImage()
    {
        // 从文件中读取图像字节数组
        Debug.Log(imagePath);
        byte[] imageBytes = File.ReadAllBytes(imagePath);

        // 创建新的Texture2D对象
        Texture2D texture = new Texture2D(2, 2);
        texture.LoadImage(imageBytes); // 将字节数组转换为纹理数据

        // 创建Sprite对象并设置纹理
        Sprite sprite = Sprite.Create(texture, new Rect(0, 0, texture.width, texture.height), Vector2.zero);
        image.sprite = sprite; // 设置Image组件的Sprite
    }
}
