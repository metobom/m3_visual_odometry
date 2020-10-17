# m3_visual_odometry
Henüz odometry değil. Okul, iş ve günlük yaşam sorumluluklarından zaman kaldıkça güncellenecek.

# Yapılacaklar
- Frame güncellemesi yok. Sadece her frame'deki noktalar ve kameranın konumu aynı aralıktaki kordinatlarda oluşuyor. Noktların konumu sürekli hale gelecek. 
(-> frame ve frame - 1 arası R matrisi ve t vektörü bulunup hareket yönü belirlenecek. !!!Shi-Tomasi ve Essential Matrix decomposition kötü sonuç verdi.)

- Image plane'de tespit edilen nesne 3D'ye aktarılacak. (!!!Matchlerin oranına göre triangulate etme kötü sonuç verdi.)

# Açıklamalar
- GET_POSE: "Yapılacaklar" da bahsettiğim hareket olayını gerçekleştirmesi gereken class.
- GET_IMG_PTS: Stereo frame'lerden feature extract edip matchleyen class. 

- GET_OBJ_PTS: Triangulation yapan class.

- param.py: Kullanılan parametreleri tutuyor.

- vis_odom.py: Main.

# Kullanım
Kullandığım kameralar Logitech C310. Kalibrasyon parametreleri cam_params içinde. Kullanmak için kendi kameralarınızı kalibre edip cam_params'a atmalısınız. Kalibrasyon için: https://github.com/metobom/camera_calibration_tool

Kalibrasyondan sonra vis_odom.py'ı çalıştırmak yeterli. 

# Testler
![1](https://user-images.githubusercontent.com/46991761/96351237-d51bc980-10c2-11eb-81c8-647198e6c252.png)

![2](https://user-images.githubusercontent.com/46991761/96351248-e238b880-10c2-11eb-8027-f49d35a1a2f6.png)

![3](https://user-images.githubusercontent.com/46991761/96351257-ea90f380-10c2-11eb-851e-59b52b555d06.png)

![4](https://user-images.githubusercontent.com/46991761/96351263-f086d480-10c2-11eb-9614-fc1c087e64cb.png)

![5](https://user-images.githubusercontent.com/46991761/96351275-f8467900-10c2-11eb-929f-53206d8205d8.png)

![6](https://user-images.githubusercontent.com/46991761/96351283-ff6d8700-10c2-11eb-9c40-0cd00921bec3.png)


# KAYNAKLAR

[0] https://www.youtube.com/watch?v=bn4KHa_zWuQ&list=PLjMXczUzEYcHvw5YYSU92WrY8IwhTuq7p&index=6&ab_channel=JosephRedmon
 
[1] https://www.youtube.com/watch?v=taty6lPVcmA&list=PLjMXczUzEYcHvw5YYSU92WrY8IwhTuq7p&index=7

[2] https://www.youtube.com/watch?v=a-v5_8VGV0A&list=PLjMXczUzEYcHvw5YYSU92WrY8IwhTuq7p&index=8&t=939s

[3] https://www.youtube.com/watch?v=AA8FEwutsVk&list=PLjMXczUzEYcHvw5YYSU92WrY8IwhTuq7p&index=9

[4] https://www.learnopencv.com/camera-calibration-using-opencv/

[5] https://www.cambridge.org/core/books/multiple-view-geometry-in-computer-vision/0B6F289C78B2B23F596CAA76D3D43F7A

[6] http://www.cs.toronto.edu/~urtasun/courses/CSC2541/03_odometry.pdf

[7] https://stackoverflow.com/questions/64260851/cv2-triangulatepoints-always-returns-same-z-value

[8] https://docs.opencv.org/master/dc/dbb/tutorial_py_calibration.html

[9] https://docs.opencv.org/master/d9/db7/tutorial_py_table_of_contents_calib3d.html

[10] https://cvgl.stanford.edu/teaching/cs231a_winter1415/prev/projects/CS231a-FinalReport-sgmccann.pdf

[11] https://stackoverflow.com/questions/9026567/3d-reconstruction-from-2-images-without-info-about-the-camera

