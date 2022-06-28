# 2022 IRC 暑期学校机器人组项目指导书

## 一、项目介绍

本专题旨在为学员介绍机器人路径规划问题，引导学员在提供的代码框架中实现经典的 RRT 算法系列算法，完成在 2D 地图中的路径规划问题。

教程分为环境配置篇，背景介绍篇，开发篇以及资料篇共

环境配置篇，我们将使用引导学员完成项目的基础环境配置。项目使用 Conda 进行环境管理并通使用 VSCode 作为开发工具

背景介绍篇，我们将简要介绍机器人路径规划以及本项目的主要目标 RRT 系列算法

开发篇，我们将具体介绍项目任务，引导学院完成 2D 路径规划算法实现并进行实验评价实现算法优劣。除最终效果外，我们更看重学员在完成项目过程中的表现，例如发现问题，思考并提出解决方案的能力，欢迎同学们尽可能多得完成布置任务并进行开放题的思考

资料篇，我们罗列了与项目相关的一些参考文献，如其它知名 2D 机器人路径规划算法。
鼓励大家在项目基础上实现其它 RRT 算法或非 RRT 路径规划算法，并与项目中所涉及的算法进行比较，提出自己的思考

项目以 Python 进行实现，其语法简单，极易上手。没有经验的同学可通过以下链接进行学习

- Python3 官方文档 https://docs.python.org/zh-cn/3/tutorial/index.html

- Python 入门 from CS231N https://cs231n.github.io/python-numpy-tutorial/

- Python 入门 from CS224N https://web.stanford.edu/class/cs224n/readings/cs224n-python-review.pdf

## 二、环境配置

本章节，我们将安装配置 Python 开发环境，IDE 及框架所需依赖、

我们以 conda 进行 Python 环境管理，并以 vscode 为例进行 IDE 配置

### Conda

Conda 是一个开源跨系统的环境管理软件，其支持 *Python, R, Ruby, Lua, Scala, Java, JavaScript, C/ C++,* 等多种语言。

我们将以 Conda 管理 Python 环境

#### 下载 Conda

通过以下链接登录 Conda 官网，并根据自己所使用系统安装对应版本 Conda 进行下载

https://docs.conda.io/en/latest/miniconda.html#system-requirements

- Windows: 选择 Miniconda3 Windows 64-bit
- macOS: 根据自己处理器选择 Miniconda3 macOS Intel x86 64-bit bash 或 Miniconda3 macOS Apple M1 64-bit bash
- Linux: 选择 Miniconda3 Linux 64-bit

<img src="assets/image-20220628215459188.png" alt="image-20220628215459188" style="zoom:40%;" />

#### 安装 Conda

##### Windows

双击下载的 Miniconda3 Windows 64-bit.exe, 执行安装程序，全程除安装路径可自定义外，其余选项全部保持默认即可

一直点击下一步，直到完成安装

##### Linux/Mac

打开终端 (Terminal)，执行下载好的 .sh 文件并执行

```bash
bash Miniconda3-latest-xxxxx.sh
```

在下述页面时输入回车

<img src="assets/image-20220628215624023.png" alt="image-20220628215624023" style="zoom:50%;" />


之后不断空格进行翻页 (Vim 语法)，直到出现下述页面，输入 yes 表示接受条款并回车

<img src="assets/image-20220628215643502.png" alt="image-20220628215643502" style="zoom:50%;" />

输入安装路径并回车（也可保持默认路径直接回车）, 等待安装完成

<img src="assets/image-20220628215909057.png" alt="image-20220628215909057" style="zoom:50%;" />

到最后一步，直接回车，完成 Conda 初始化结束安装
<center><img src="assets/image-20220628215944785.png" alt="image-20220628215944785" style="zoom:40%;" /></center>

###  VSCode

进入 VSCode 官网下载编辑器并完成安装

https://code.visualstudio.com/

<img src="assets/image-20220628215814039.png" alt="image-20220628215814039" style="zoom:32%;" />

安装完成后，打开 VSCode，点击左侧由多个 Cube 组成的图标进行插件下载

<img src="assets/image-20220628215744234.png" alt="image-20220628215744234" style="zoom:30%;" />

输入搜索 python, 安装如图所示的插件包完成 VSCode 配置

<img src="assets/image-20220628215715712.png" alt="image-20220628215715712" style="zoom:25%;" />

#### 使用 VSCode 运行项目 Demo

打开安装的 VSCode, 选择文件(File) -->打开文件夹(Open Folder)，浏览文件选择项目

#### 安装项目所需环境

从官方群中下载项目基础代码，并解压缩，进入项目路径 (使用 cd 命令进行目录切换. Windows 用户从开始菜单选择 Anaconda Prompt(Conda), Linux/Mac 用户直接使用终端)

<img src="assets/image-20220628220055489.png" alt="image-20220628220055489" style="zoom:25%;" />

<img src="assets/image-20220628220132006.png" alt="image-20220628220132006" style="zoom:30%;" />



创建项目环境 

```bash
conda env create --file env.yml 
```

接下来，从左侧选择要运行的文件 (这里我们运行 baseline_rrt.py)，在右下角点击选择解释器，在弹出的选择框中选择刚刚安装的 IRC_DIY 环境

<img src="assets/image-20220628220224362.png" alt="image-20220628220224362" style="zoom:30%;" />

<img src="assets/image-20220628220253979.png" alt="image-20220628220253979" style="zoom:30%;" />

之后，点击右上角的 “播放键” 运行代码，基础代码开始进行规划并完成绘图

<img src="assets/image-20220628220414183.png" alt="image-20220628220414183" style="zoom:30%;" />

<img src="assets/image-20220628220348661.png" alt="image-20220628220348661" style="zoom:32%;" />

到此，环境配置完成

## 三、背景介绍

## 四、开发篇

该项目结构如下，其中 tool 文件夹内不需要改动，专注完成任务 1，任务 2，任务 3 所涉及到的 3 个文件即可

<img src="assets/image-20220628221353182.png" alt="image-20220628221353182" style="zoom:50%;" />

### 测试场景

我们准备了 3 个不同的场景方便同学们进行算法测试，其中蓝色点为起点，绿色点为目标终点

<img src="assets/image-20220628221711966.png" alt="image-20220628221711966" style="zoom:50%;" />

<img src="assets/image-20220628221809527.png" alt="image-20220628221809527" style="zoom:50%;" />

<img src="assets/image-20220628222039165.png" alt="image-20220628222039165" style="zoom:50%;" />

通过启动不同的函数，在不同环境中进行测试

- 其中当参数 eval_time == 1 时，会进行绘制命令并打印花费时间，迭代次数
  - 建议同学们首先使用该配置进行算法调试
- 当参数 eval_time > 1 时，代码会统计多次规划的平均花费时间，平均迭代次数
  - 最终同学们需要报告不同算法，不同参数在不同环境下运行 5 次的平均结果
  - 通过注释开启，关闭不同场景

<img src="assets/image-20220628222119653.png" alt="image-20220628222119653" style="zoom:50%;" />

### 任务 1：RRT 算法

#### 任务 1.1 根据环境配置步骤，成功运行 RRT 算法，并在三个环境中完成规划

请保存不同场景下的规划结果

#### 任务 1.2 调整 RRT 算法参数（步长，随机采样拒绝率，最大迭代次数），在三个环境中获得比默认参数更少的时间，更少的迭代次数

由于不同机器配置问题，这里只提供 baseline 的迭代次数作为参考

请同学们充分理解算法，调整算法参数，获得比 baseline 更少的迭代次数， 并报告相应参数及结果（设置 eval_time=5 获取平均时间，迭代次数）

- Baseline
  - 环境 1:
    - 迭代次数 1449
  - 环境 2:
    - 迭代次数 8285
  - 环境 3:
    - 迭代次数 5728