













# 绘图系统使用说明书

姓名：王梓博

学号：181860106

邮箱：[181860106@smail.nju.edu.cn]()













## 目录

[TOC]



## 总体布局

![1607565296573](picture/1607565296573.png)

如上图所示，我的绘图系统分为菜单栏、图像编辑框、图元列表、及状态栏四个部分，其各自配合以完成系统实现的各种操作。

在菜单栏，选中菜单并点击，可以显示出二级菜单，其中列出了本系统能够进行的各种操作，如：



### 文件菜单

文件菜单中有设置画笔、重置画布、退出等，而将鼠标放在设置画笔处，又能弹出三级菜单，进行设置画笔颜色和设置画笔粗细操作；

![1607565369916](picture/1607565369916.png)



#### 设置画笔颜色

当点击设置画笔颜色时，会弹出颜色选择框，选中任意颜色之后点击 OK，即可完成画笔颜色的设置。

![1607565637635](picture/1607565637635.png)



#### 设置画笔粗细

当选择设置画笔粗细时，会弹出输入框以供输入代表画笔粗细的数字，该数字的初始值为当前画笔粗细，由键盘输入数字或点击上下三角形均可调整画笔的粗细。

![1607565655638](picture/1607565655638.png)





### 绘制菜单

绘制菜单中能够选择绘制图元的类型，而每个二级菜单又包含能够选择绘图算法的三级菜单。



#### 绘制线段

![1607566892853](picture/1607566892853.png)

将鼠标停止在线段处，会显示出二级菜单，其中包括绘制线段的各种算法，选择想要使用的算法之后，状态栏会出现提示信息如下：

![1607567009449](picture/1607567009449.png)

以 DDA 算法绘制线段为例，根据提示信息进行操作，绘制出图元，图元的编号会显示在右侧图元列表一栏中，为后续进行的编辑操作做准备。

![1607568737234](picture/1607568737234.png)



#### 绘制多边形

![1607567649532](picture/1607567649532.png)

将鼠标停止在多边形处，会显示出二级菜单，其中包括绘制多边形时能够使用的两种算法，选择想要使用的算法之后，状态栏会出现提示信息如下：

![1607567715865](picture/1607567715865.png)

以 DDA 算法绘制多边形为例，根据提示信息进行操作，绘制出图元，图元的编号会显示在右侧图元列表一栏中，为后续进行的编辑操作做准备。

![1607568802091](picture/1607568802091.png)



#### 绘制椭圆

![1607568091457](picture/1607568091457.png)

由于本系统只实现了中点圆生成算法绘制椭圆，因此绘制椭圆选项无三级菜单，只需选择绘制椭圆，状态栏会出现提示信息如下：

![1607568152483](picture/1607568152483.png)

根据提示信息进行操作，绘制出图元，图元的编号会显示在右侧图元列表一栏中，为后续进行的编辑操作做准备。

![1607568860855](picture/1607568860855.png)



#### 绘制曲线

![1607569002750](picture/1607569002750.png)

将鼠标停止在曲线处，会显示出二级菜单，其中包括绘制曲线的各种算法。在此处，我分别使用绘制曲线的两种算法进行曲线的绘制。



##### Bezier算法绘制曲线

![b1607569053675](picture/1607569053675.png)

选择 Bezier 算法之后，状态栏会出现提示信息，根据提示信息进行操作，绘制出图元，图元的编号会显示在右侧图元列表一栏中，为后续进行的编辑操作做准备。

![1607569339988](picture/1607569339988.png)



##### B-spline 算法绘制曲线

![1607569402914](picture/1607569402914.png)

选择 B-spline 算法之后，状态栏会出现提示信息，根据提示信息进行操作，绘制出图元，图元的编号会显示在右侧图元列表一栏中，为后续进行的编辑操作做准备。

![1607569600018](picture/1607569600018.png)

需要注意的是，由于本系统中实现的是四阶三次 B 样条曲线，因此在设置前 3 个控制点时，曲线并不会被绘制，只有当设置第四个控制点的时候，曲线才会被绘制。



### 编辑菜单

在界面右侧的图元列表中用鼠标点击数字，可以选中相应 id 的图元，而被选中的图元会出现红色的方框；编辑菜单中的各种操作能够对被选中的图元进行相应的操作。

#### 平移图元

![1607569782953](picture/1607569782953.png)

在右侧图元列表中选择图元，并选择编辑菜单中的平移操作，在画布上对图元进行拖动，即可实现图元的平移。

![1607570046273](picture/1607570046273.png)

状态栏会出现如上提示，根据提示进行操作。

![1607570503342](picture/1607570503342.png)



#### 旋转图元

![1607570608863](picture/1607570608863.png)

在右侧图元列表中选择图元，并选择编辑菜单中的旋转操作，在画布上绕图元中心点拖动鼠标，即可实现图元的旋转。

![1607571193600](picture/1607571193600.png)

状态栏会出现如上提示，根据提示进行操作。

![1607571268751](picture/1607571268751.png)



#### 缩放图元

![1607571300136](picture/1607571300136.png)

在右侧图元列表中选择图元，并选择编辑菜单中的缩放操作，在画布上绕图元中心点拖动鼠标，即可实现图元的缩放。

![1607571193600](picture/1607571193600.png)

![1607572185085](picture/1607572185085.png)



#### 裁剪线段

![1607572206967](picture/1607572206967.png)

在右侧图元列表中选择图元，并选择编辑菜单中的裁剪，在三级菜单中选择裁剪算法。

![1607576947782](picture/1607576947782.png)

状态栏出现如上提示，根据提示进行操作，对图中的线段进行修剪，得到最终的图像如下：

![1607572185085](picture/1607572185085.png)

