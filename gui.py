import wx


class Banker():

    def __init__(self,parent):
        self.Max = [[7, 5, 3],
                    [3, 2, 2],
                    [9, 0, 2],
                    [2, 2, 2],
                    [4, 3, 3]]

        self.Allocation = [[0, 1, 0],
                           [2, 0, 0],
                           [3, 0, 2],
                           [2, 1, 1],
                           [0, 0, 2]]

        self.Need = [[7, 4, 3],
                     [1, 2, 2],
                     [6, 0, 0],
                     [0, 1, 1],
                     [4, 3, 1]]

        self.Available = [3, 3, 2]
        self.parent = parent

    # compare request to it's need
    # 任意一项请求的资源不能超过事先规定的大小
    def re2nd(self, re: list, i: int):
        ND = self.Need[i]
        for j in range(len(re)):
            if re[j] <= ND[j]:
                continue
            else:
                print('请求失败，所需资源超过所宣布最大值')
                return False
        return True

    # compare request to available
    # 任意一项请求的资源不能超过当前可用的资源
    def re2av(self, re: list):
        for j in range(len(re)):
            if re[j] <= self.Available[j]:
                continue
            else:
                print('请求失败，当前可用资源不足，请等待')
                return False
        return True

    # 进行预分配并执行安全性算法
    # 如果安全则通过，如果不安全则回退操作到分配前
    def PreAllocate(self, re: list,index:int):
        i = index
        for j in range(len(re)):
            self.Allocation[i][j] += re[j]
            self.Need[i][j] -= re[j]
            self.Available[j] -= re[j]
        if self.SecurityDetect():
            print('请求成功，已分配')
            return True
        else:
            for j in range(len(re)):
                self.Allocation[i][j] -= re[j]
                self.Need[i][j] += re[j]
                self.Available[j] += re[j]
            print('预分配失败，不安全状态')
            return False

    def SecurityDetect(self):
        # step 1
        work = list(self.Available)     # 获得值，而不是引用
        print(work)
        finish = [False] * len(self.Need)
        finish_change_flag = True

        # step 2
        while (finish_change_flag):
            miniflag = 0
            finish_change_flag = False
            for i in range(len(self.Need)):
                if finish[i] == False:
                    for j in range(len(work)):
                        if self.Need[i][j] <= work[j]:
                            miniflag += 1
                        else:
                            miniflag = 0
                            break
                    if miniflag == len(work):
                        # step 3
                        for j in range(len(work)):
                            work[j] += self.Allocation[i][j]
                            finish[i] = True
                            finish_change_flag = True

        if self.judgeAllTrue(finish):
            return True
        else:
            return False

    def judgeAllTrue(self,l:list):
        for i in l:
            if i == True:
                continue
            else:
                return False
        return True

    def request(self, re: list, index: int):
        if self.re2nd(re, index):
            if self.re2av(re):
                if self.PreAllocate(re,index):
                    self.parent.output_Text.AppendText('\n请求成功，已分配')
                else:
                    self.parent.output_Text.AppendText('\n预分配失败，不安全状态')
            else:
                self.parent.output_Text.AppendText('\n请求失败，当前可用资源不足，请等待')
        else:
            self.parent.output_Text.AppendText('\n请求失败，所需资源超过所宣布最大值')


class MyFrame(wx.Frame):
    def __init__(self):
        # 算法与实现
        self.banker = Banker(self)

        # 界面渲染
        wx.Frame.__init__(self, None, -1, '银行家算法', size=(600, 600))
        panel = wx.Panel(self, -1)


        Allocation_Text = wx.StaticText(panel,-1,'Allocation',pos=(100,50),style=wx.ST_NO_AUTORESIZE)
        Need_Text = wx.StaticText(panel,-1,'Needd',pos=(350,50),style=wx.ST_NO_AUTORESIZE|wx.ALIGN_LEFT)
        Available_Text = wx.StaticText(panel,-1,'Available',pos=(100,330),style=wx.ALIGN_LEFT)
        input_Text1 = wx.StaticText(panel,-1,'input:Request',pos=(100,380))
        input_Text2 = wx.StaticText(panel, -1, 'input:index', pos=(250, 380))
        output_Text = wx.StaticText(panel, -1, 'output', pos=(100, 430))


        # 文本框初始化
        self.output_Allocation = wx.TextCtrl(panel, -1, '', pos = (100, 70),
                                             size = (150,200),style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.output_Need = wx.TextCtrl(panel, -1, '', pos = (350, 70),
                                             size = (150,200),style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.output_Available = wx.TextCtrl(panel, -1, '', pos = (100,350),
                                             style=wx.TE_READONLY)
        self.input_Request = wx.TextCtrl(panel, -1, '', pos=(100, 400))
        self.input_index = wx.TextCtrl(panel, -1, '', pos=(250, 400))

        self.output_Text = wx.TextCtrl(panel,-1,'',pos = (100, 450),
                                             size = (400,100),style=wx.TE_MULTILINE|wx.TE_READONLY)

        # 提交按钮初始化
        btn = wx.Button(panel,-1,'提交',pos=(400,400))
        self.Bind(wx.EVT_BUTTON, self.OnClick, btn)

        btn_reset = wx.Button(panel,-1,'Reset',pos=(400,300))
        self.Bind(wx.EVT_BUTTON,self.ResetOnClick,btn_reset)

        self.ChangeText()

    def ChangeText(self):
        self.output_Allocation.Clear()
        self.output_Need.Clear()
        self.output_Available.Clear()

        for i in range(len(self.banker.Allocation)):
            string = str(self.banker.Allocation[i])
            self.output_Allocation.AppendText(str(i)+'\t'+string+'\n')
        for i in range(len(self.banker.Need)):
            string = str(self.banker.Need[i])
            self.output_Need.AppendText(str(i) +'\t'+ string+'\n')

        self.output_Available.AppendText(str(self.banker.Available))

    def OnClick(self,event):
        if self.input_index.GetLineText(0)=='' or self.input_Request.GetLineText(0)=='':
            wx.MessageBox('请按要求输入请求内容和进程序号，逗号分割，不能为空！')
        else:
            Request = []
            strlist = self.input_Request.GetLineText(0).split(',')
            for s in strlist:
                Request.append(int(s))
            self.output_Text.AppendText('\nRequest:'+'\t'+str(Request))

            index = int(self.input_index.GetLineText(0))
            self.banker.request(Request, index)

            self.ChangeText()

    def ResetOnClick(self,event):
        self.banker = Banker(self)
        self.output_Text.Clear()
        self.ChangeText()





class myApp(wx.App):
    def OnInit(self):
        frame = MyFrame()
        frame.Show()
        return True



if __name__ == '__main__':
    app = myApp()
    app.MainLoop()

    # Request:	[1, 0, 2] 1
    # 请求成功，已分配
    # Request:	[3, 3, 0] 4
    # 请求失败，当前可用资源不足，请等待
    # Request:	[0, 2, 0] 0
    # 预分配失败，不安全状态
    # Request:	[0, 1, 0] 0
    # 请求成功，已分配
