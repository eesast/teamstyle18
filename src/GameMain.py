class game_main:
    units={}#单位dict
    hqs=[]#主基地
    buildings=[]#中立建筑
    turn_flag=0#谁的回合
    turn_num=0#回合数
    phase_num=0#回合阶段指示
    buffs0=[]#选手0的buffs
    buffs1=[]#选手1的buffs
    def __init__(self):
        pass
    def windetermine_phase(self):
        #胜利判定
        pass
    def cleanup_phase(self, ai_id):
        #单位死亡判定
        """

        :type ai_id: int
        """
        pass
    def skill_phase(selfself, ai_id):
        #技能结算
        """

        :type ai_id: int
        """
        pass
    def move_phase(self, ai_id):
        #移动指令结算
        """

        :type ai_id: int
        """
        pass
    def produce_phase(self,ai_id):
        #兵种获取指令结算
        """

        :type ai_id: int
        """
        pass
    def capture_phase(self,ai_id):
        #占领建筑阶段
        """

        :type ai_id: int
        """
    def next_tick(self):
        #进入下一回合前通信等任务
    def to_string(self):
        #将当前状态信息返回，用String,Json什么都行，你们自己起名字吧
