import cv2

def list_cameras(max_cameras=10):
    available_cameras = []#储存所有可用摄像头的信息的列表
    
    print("正在检测摄像头...")
    for i in range(max_cameras):
        cap = cv2.VideoCapture(i)
        
        if cap.isOpened():
            ret, frame = cap.read()#尝试抓取一帧以确认摄像头是否真正可用，ret为bool值，frame为抓取的图像（数组）
            if ret:
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))#获取摄像头图像的宽度
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))#获取摄像头图像的高度
                fps = cap.get(cv2.CAP_PROP_FPS)#获取摄像头帧率

                print(f"摄像头 {i}: 可用")
                print(f"  - 分辨率: {width}x{height}")
                print(f"  - FPS: {fps}")#FPS，1s多少张图片
                
                #往列表添加字典元素，包含摄像头编号、分辨率和帧率
                available_cameras.append({
                    'id': i,
                    'resolution': (width, height),
                    'fps': fps
                })
            else:
                print(f"摄像头 {i}: 打开但无法读取帧")
            
            cap.release()#有开有关，释放硬件资源
        else:
            print(f"摄像头 {i}: 不可用")
    
    return available_cameras

if __name__ == "__main__":
    # 执行检测
    cameras = list_cameras()
    print(f"\n总共找到 {len(cameras)} 个可用摄像头")
    for cam in cameras:
        print(f"编号 {cam['id']}, 分辨率:{cam['resolution'][0]}x{cam['resolution'][1]},帧率：{cam['fps']}")