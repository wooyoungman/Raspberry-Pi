# Mnist_pi

* export DISPLAY="localhost:10.0” 로 mobaxterm 환경에서 GUI 이미지를 표시하기위해 입력해준다.

* 파이카메라 사용을 위한 각종 명령어들 
[https://neosarchizo.gitbooks.io/raspberrypiforsejonguniv/content/chapter4.html](https://neosarchizo.gitbooks.io/raspberrypiforsejonguniv/content/chapter4.html)

* 파이카메라 Mnist 구현을 위해 따라한 영상
[https://webnautes.tistory.com/1384](https://webnautes.tistory.com/1384)
---

* 01.py : MNIST 데이터셋을 사용하여 손글씨 숫자 이미지를 인식하는 머신러닝 모델을 학습시킨다.
* 02.py : OpenCV 라이브러리를 사용하여 웹캠에서 영상을 캡처하고, 해당 영상에서 관심 영역을 추출한 뒤, 해당 영역에 대해 이미지 전처리를 수행하고, 미리 훈련된 MNIST 모델을 사용하여 추출한 관심 영역의 손글씨 숫자를 인식

![image](https://user-images.githubusercontent.com/101693311/195550625-9ad8e82b-487b-45b6-8274-8d5ea8c75912.png)
