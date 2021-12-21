# 小型 C 语言编译器

## 简介

1921 编译原理课程大作业。

大作业的任务是手写一个小型编译器，可以编译`miniSysY`语言，该语言完整文法与各实验子任务详见[实验指导书](https://buaa-se-compiling.github.io/miniSysY-tutorial/)。这个语言来自毕昇杯编译大赛，经过了助教的简化，可以简单认为是**C 语言的一个子集**。概括的说，这个编译器支持输入输出，变量声明，for，if，函数定义，多维数组，短路求值等功能。

本项目主要借助于 Python 的第三方库 Ply 实现，词法分析部分使用了`ply.lex`，语法分析则借助了`ply.yacc`。由于评测环境无法使用`pip`，故本项目直接使用了这个库的源文件。

本项目主要结构如下所示：

```txt
Compile
├─ .gitignore
├─ Dockerfile
├─ README.md
├─ a.sh
├─ judge.toml
├─ libsysy.c
├─ libsysy.h
├─ run.sh
└─ src
 	├─ a.c
 	├─ lexical
 	│	├─ laxer.py
 	│	└─ lex.py
 	├─ main.py
 	├─ syntactic
 	│	├─ analyze.py
 	│	├─ ast.py
 	│	├─ node.py
 	│	├─ table.py
 	│	└─ yacc.py
 	├─ values.py
 	└─ yacctest.py
```

整个项目主要分为两大部分：词法分析和语法分析，以及一些测试用的文件。

词法分析相关代码位于`lexical`目录下，`lex.py`是 Ply 库的源文件，`laxer.py`是词法分析所必须的配置文件。

语法分析相关代码位于`syntactic`目录下，`yacc.py`同样是 Ply 库的源文件，`analyze.py`里定义了文法和抽象语法树的生成规则，`node.py`里定义了语法树的结构，`ast.py`中是项目的核心文件，负责遍历抽象语法树并输出中间代码。

## 运行项目

### 环境配置

要运行本项目，首先要有 Python 环境，并安装 Ply 库:

```shell
pip install ply
```

推荐在 Ubuntu 环境上执行，并安装 llvm 工具链。Ubuntu 20.04 的安装命令如下：

```shell
$ sudo apt-get install llvm
$ sudo apt-get install clang
```

安装完成后可以通过以下命令进行测试：

```shell
$ clang -v 		# 查看版本，若出现版本信息则说明安装成功
$ lli --version # 查看版本，若出现版本信息则说明安装成功
```

对于 Ubuntu 18.04，官方源中的 LLVM 版本仍然停留在 6.0，因此需要在安装时额外指定版本号：

```shell
$ sudo apt-get install llvm-10
$ sudo apt-get install clang-10
```

相应的，使用时也需要在末尾额外加上 `-10` 用来指定版本，如 `clang-10` 或 `lli-10`。

完成安装后可以通过以下命令进行测试：

```shell
$ clang-10 -v	 	# 查看版本，若出现版本信息则说明安装成功
$ lli-10 --version 	# 查看版本，若出现版本信息则说明安装成功
```

### 修改文件并运行

完成环境配置后，首先将`value.py`中的`LOCAL`直接置为 True，表示在本地环境而不是评测环境运行。然后在`src`目录下创建`a.c`文件，在其中放入想要编译的代码文件，执行命令`python main.py`，即可在`src/test.ll`中看到输出。

`run.sh`是执行`test.ll`文件的脚本，可以使用`sh run.sh`来观察生成结果的正确性。

# 其他

这个项目只是一个课程大作业，里面的Bug可能很多，功能方面也不是十分完善（比如缺少很多错误检查），之后不打算进行任何维护。如果您对本项目感兴趣或者有什么疑问，欢迎邮件联系。您可以在我的个人主页中找到我的联系方式。

# 附录
## 实验完成时间线

手写 Token 识别。

-   10.15 pass Lab 1

代码重构，引入 ply.lex 处理 Token，并手写递归下降。

-   10.22 pass Lab 2
-   10.28 重构，引入 ply.yacc 处理文法，引入 AST
-   10.29 pass Lab 3
-   11.4 pass Lab 4
-   11.18 pass Lab 5
-   11.18 pass Lab 6 
-   11.22 pass Lab 7
-	11.24 pass Lab 8
-	11.28 pass Challenge Lab-短路求值
-	11.28 pass Challenge Lab-多维数组

## 主要参考资料

[Ply 官方文档](https://ply.readthedocs.io/en/latest/)

[LLVM 推荐指令集](https://llvm.org/docs/LangRef.html)
