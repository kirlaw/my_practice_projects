using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using LitJson;
using System.IO;

public class Landmark
{
    public double x { get; set; }
    public double y { get; set; }
    public double z { get; set; }
    public double visibility { get; set; }
}

public class LandmarksData
{
    public List<Landmark> landmarks { get; set; }
}




public class NormalGesture : MonoBehaviour {

	private static NormalGesture instance = null;

	private UDPRecive recive;
	string data;
	Landmark Nose;
	Landmark LeftWrist;
	Landmark RightWrist;
	Landmark LeftHip;
	Landmark RightHip;
	double MHip;
	double MHip_before;


	public static NormalGesture Instance           //引用
	{
		get
		{
			return instance;
		}
	}

	// Use this for initialization
	void Start () {
		recive = GetComponent<UDPRecive>();
		
		MHip_before = 0;
	}


	
	// Update is called once per frame
	void Update () {
		data = recive.data;
		//Debug.Log(data);
		LandmarksData poses = JsonMapper.ToObject<LandmarksData>(data);
		Nose = poses.landmarks[0];
		LeftWrist = poses.landmarks[15];
		RightWrist = poses.landmarks[16];
		LeftHip = poses.landmarks[23];//23
		RightHip = poses.landmarks[24];//24
		MHip = (LeftHip.y + RightHip.y) / 2;

	}


	public bool IsJumpOneHit()
	{
		Debug.Log(MHip_before);
		if (MHip_before == 0){
			MHip_before = MHip;
        }

		if (MHip-MHip_before>0.1f)
		{
			Debug.Log("Jump");
			return true;
			
		}

		return false;
	}
	void Awake()
	{
		instance = this;
	}

}
