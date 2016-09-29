class GameMain:
    Units={}#单位dict
    HQs=[]#主基地
    Buildings=[]#中立建筑
    turn_flag=0#谁的回合
    turn_num=0#回合数
    phase_num=0#回合阶段指示
    Buffs0=[]#选手0的buffs
    Buffs1=[]#选手1的buffs
    def __init__(self):
        pass
    def WinDeterminePhase(self):
        #胜利判定
        pass
    def CleanUpPhase(self, ai_id):
        #单位死亡判定
        """

        :type ai_id: int
        """
        pass
    def SkillPhase(selfself, ai_id):
        #技能结算
        """

        :type ai_id: int
        """
        pass
    def MovePhase(self, ai_id):
        #移动指令结算
        """

        :type ai_id: int
        """
        pass
    def ProducePhase(self,ai_id):
        #兵种获取指令结算
        """

        :type ai_id: int
        """
        pass
    def CapturePhase(self,ai_id):
        #占领建筑阶段
        """

        :type ai_id: int
        """
    def NextTick(self):
        #进入下一回合前通信等任务
    def toString(self):
        #将当前状态信息返回，用String,Json什么都行，你们自己起名字吧
