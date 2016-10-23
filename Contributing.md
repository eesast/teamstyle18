为了提高大家开发的效率及代码质量，在工作流程以及代码规范上@wangqr给大家提了一些建议：（参照：https://github.com/eesast/teamstyle17/blob/master/CONTRIBUTING.md）
# 工作方式

请大家将此仓库fork到自己的账户下，在自己的仓库中进行修改并通过发起pull request来提交代码。具体要求如下：

* *禁止直接在网页上编辑、删除任何文件！*
* 不要使用自己的master或任何经常编辑的分支来发起pull request
* 发起pull request前请执行`git pull --rebase upstream master`，其中upstream是指EESAST/teamstyle18，尽量使得GitHub能够自动merge
* Pycharm Professional中有Github版本控制功能，从不同的remote pull changes以及pull request等操作非常方便
* 发起之后请到GitHub上的Commits和Files changed页查看自己的变更，检查是否有误
* 每个人都有仓库的写权限，一般情况下请找另一个人来merge，在修改很小或时间较紧，且找不到另一个人时也可自行merge，一般不要直接push。如果看到有他人发起的pull request请协助检查，无误后请merge
* 发现问题且短期内不能解决的，请发至GitHub的issues处。如果pull request解决了一个或多个issue，请在pull request的标题的注明“resolve #xxx”

# 代码
### 规范

如变量命名等，尽量遵循PEP8标准，如#9

（个人）推荐大家在方法下注明返回类型，在PyCharm中选中参数alt+enter

### 编码

如果提交的代码中包含中文，且使用了GB2312编码，会导致GitHub显示不正常。推荐使用utf-8 without BOM，这意味着需要在文本编辑器中进行相关的设置。记事本不支持此编码，请换用其他文本编辑器，如[notepad++](https://notepad-plus-plus.org/)。

如果提交的Python代码中包含中文，请在文件开头注明编码字符集。也就是说，utf-8编码的.py文件前两行应该是这样的：
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
```

msysgit可能不能正确处理commit message中的汉字，出现问题请自行google或使用cygwin中的git，或使用英语。

### 换行符

建议使用LF作为文本文件的换行符，许多编辑器都可以设置。也可以通过执行下面的命令来使git自动处理换行。
```sh
git config --global core.autocrlf true
```

### 缩进

Python中的缩进是有意义的，而且Python3已经明确禁止混用Tab和空格。Python代码请一律使用4空格缩进。许多文本编辑器都可以自动地将Tab转为空格。

# commit

请在commit message中写明此次commit所实现的功能或解决的问题，如果一个commit包含多个小修改，请先在标题中简要概括，如有需要请先空一行再分条列举所做的修改。

单次commit应该解决、实现一个较为独立的部分，不要在一个commit中实现多个功能。提交commit前尽量确保程序能够正常工作。

# Pull Requests

> 一个 PR 的命运，当然要看代码的质量，但是也要考虑历史的行程。

为避免 Pull Requests 被长期放置，请在发出 Pull Request 的同时 @ 同组进行相关工作的同学来 review 并 merge 代码。如果 Pull Request 的改动足够简单，可以自行 merge。

一个 Pull Request 不要 open 超过 2 天。
