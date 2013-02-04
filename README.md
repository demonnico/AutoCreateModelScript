#How To Use
------
*	如果你想要添加一个新的类，在Model.plist的根节点中添加一个新的Dictionary.

*	成员变量名即新增后Dictionary的key
*	成员变量value属性格式为'变量类型'+' '+'相应服务端返回的key'(***注意中间的空格***)

```
cd  ~
git clone https://github.com/demon1105/AutoCreateModelScript.git
cd AutoCreateModelScript
python automodel.py Model.plist MyModelFileName w

```
最后的参w为python文件写入的参数(w：覆盖写入。也可以是a：添加模式)

